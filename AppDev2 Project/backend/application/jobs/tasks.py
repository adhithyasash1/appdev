import csv
from datetime import datetime
from application.data.models import *
from application.data.cache import *
from application.utils.reporter import *
from application.utils.postmaster import *
from application.data.access import *
from application.utils.functions import *
from application.data.database import *
from application.jobs.workers import celery
from celery.schedules import crontab


@celery.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    # tester
    # sender.add_periodic_task(10.0, updateDashboard.s(), name='testing beat scheduler')

    # Pushes updateDashboard() into the message queue every day for workers to execute
    sender.add_periodic_task(86400.0, updateDashboard.s(), name='checks for cards that are overdue and updates their status!')

    # Pushes dailyReminder() into message queue every day morning for the workers to execute; Executes every Monday morning at 6:00 a.m.
    sender.add_periodic_task(crontab(hour=6, minute=00, day_of_week=1), dailyReminder.s())

    # Pushes monthlyReport() into message queue every month for workers to execute
    sender.add_periodic_task(crontab(0, 0, day_of_month='1'), monthlyReport.s(), name='sends monthly reminders to users regarding their goals!')


@celery.task
def welcomeUser(mail, passwerd):
    try:
        user = User.query.filter_by(email = mail).first()
        data = {'username': user.username, 'email': user.email, 'password': passwerd}
        pdf_formatter('Welcome.html', data, 'Welcome')
        basic_email(user.email, 'Getting Started!', 'Welcome to Minimal Kanban!', attachment_file='Welcome.pdf')
    except Exception as e:
        print(e)


@celery.task
def importLists(user_id, file):
    try:
        with open(file, 'r') as f:
            reader = csv.reader(f, skipinitialspace=True, delimiter=',')
            header = next(reader)
            if header == ['list_name', 'list_description']:
                for row in reader:
                    list = List(list_name=row[0], list_description=row[1], user_id=user_id)
                    db.session.add(list)
                    db.session.flush()
                    db.session.commit()
            else:
                return False
        cache.delete_memoized(getList)
        cache.delete_memoized(getLists)
        cache.delete_memoized(getListsDefault)
        return True
    except Exception as e:
        print(e)
        return False


@celery.task
def importCards(list_id, file):
    f = datetime.datetime.now()
    x = f.strftime("%Y-%m-%d %H:%M:%S")
    try:
        with open(file, 'r') as f:
            reader = csv.reader(f, skipinitialspace=True, delimiter=',')
            header = next(reader)
            if header == ['card_title', 'card_content', 'card_deadline', 'card_status']:
                for row in reader:
                    card = Card(card_title=row[0], card_content=row[1], card_deadline=row[2], card_status=row[3], card_creation_date=x, card_list_id=list_id)
                    db.session.add(card)
                    db.session.flush()
                    db.session.commit()
            else:
                return False
        cache.delete_memoized(getCard)
        cache.delete_memoized(getCards)
        cache.delete_memoized(getCardsDefault)
        return True
    except Exception as e:
        print(e)
        return False


@celery.task()
def exportList(user_id, list_id):
    user = User.query.filter_by(id=user_id).first()
    cards = getCards(list_id)
    try:
        if cards:
            data = ['card_id', 'card_title', 'card_content', 'card_deadline', 'card_status']
            rows = []
            for card in cards:
                card_id = card.card_id
                card_title = card.card_title
                card_content = card.card_content
                card_deadline = card.card_deadline
                card_status = card.card_status
                row = [card_id, card_title, card_content, card_deadline, card_status]
                rows.append(row)
            with open('exportList.csv', 'w') as csvfile:
                csvwriter = csv.writer(csvfile)
                csvwriter.writerow(data)
                csvwriter.writerows(rows)
        basic_email(user.email, 'Exported List Data', 'This is the details of the list you requested to export as CSV file.', attachment_file='exportList.csv')
    except Exception as e:
        print(e)


@celery.task()
def exportBoard(user_id):
    lists = getLists(user_id)
    user = User.query.filter_by(id=user_id).first()
    try:
        if lists:
            data = ['list_id', 'list_name', 'list_description', 'total_cards']
            rows = []
            for list in lists:
                cards = getCards(list.list_id)
                x = len(cards)
                list_id = list.list_id
                list_name = list.list_name
                list_description = list.list_description
                total_cards = x
                row = [list_id, list_name, list_description, total_cards]
                rows.append(row)
            with open('exportBoard.csv', 'w') as csvfile:
                csvwriter = csv.writer(csvfile)
                csvwriter.writerow(data)
                csvwriter.writerows(rows)
        basic_email(user.email, 'Exported Board Data', 'This is your kanban board exported as a CSV file.', attachment_file='exportBoard.csv')
    except Exception as e:
        print(e)


@celery.task()
def updateDashboard():
    f = datetime.datetime.now()
    x = f.strftime("%Y-%m-%d %H:%M:%S")
    try:
        users = db.session.query(User).all()
        for user in users:
            lists = getLists(user.id)
            for list in lists:
                cards = getCards(list.list_id)
                for card in cards:
                    if card.card_deadline < x and card.card_status != 'Completed':
                        y = card.card_id
                        status = 'Past Deadline'
                        db.session.query(Card).filter(Card.card_id == y).update(
                            {'card_status': status, 'card_updation_date': x})
                        db.session.flush()
                        db.session.commit()
        cache.delete_memoized(getCardsDefault)
        cache.delete_memoized(getCards)
        cache.delete_memoized(getCard)
    except Exception as e:
        db.session.rollback()
        return str(e), 500


@celery.task()
def dailyReminder():
    users = db.session.query(User).all()
    try:
        for user in users:
            data = {'username': user.username}
            lists = getLists(user.id)
            data['pending'] = []
            data['total'] = 0
            data['earliest'] = None
            data['earliest_value'] = None
            for list in lists:
                cards = getCards(list.list_id)
                for card in cards:
                    if card.card_status == 'In Progress':
                        if data["earliest_value"] is None:
                            data['earliest'], data['earliest_value'] = card.card_title, card.card_deadline
                        else:
                            if card.card_deadline < data["earliest_value"]:
                                data['earliest'], data['earliest_value'] = card.card_title, card.card_deadline
                        data['pending'].append(card.card_title)
                        data['total'] += 1
            pdf_formatter('DailyReminder.html', data, 'Daily Reminder')
            basic_email(user.email, 'Daily Reminder', 'This is your daily reminder for minimal kanban application', attachment_file='Daily Reminder.pdf')
    except Exception as e:
        print(e)


@celery.task()
def monthlyReport():
    users = db.session.query(User).all()
    try:
        for user in users:
            data = {'username': user.username}
            lists = getLists(user.id)
            data['list_names'], data['completed'], data['overdue'] = [], [], []
            for list in lists:
                data['list_names'].append(list.list_name)
                cards = getCards(list.list_id)
                for card in cards:
                    if card.card_status == 'Completed':
                        data['completed'].append(card.card_title)
                    if card.card_status == 'Past Deadline':
                        data['overdue'].append(card.card_title)
            pdf_formatter('MonthlyReport.html', data, 'Monthly Report')
            basic_email(user.email, 'Monthly Report', 'This is your Monthly Report for minimal kanban application',
                        attachment_file='Monthly Report.pdf')
    except Exception as e:
        print(e)