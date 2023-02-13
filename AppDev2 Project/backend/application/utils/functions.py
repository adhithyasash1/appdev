# Helper Functions
import datetime


def getdate(date_in):
    try:
        if type(date_in) is str:
            date_out = datetime.datetime(*[int(v) for v in date_in.replace('T', '-').replace(':', '-').split('-')])
            return date_out
        else:
            date_out = datetime.datetime(*[int(v) for v in date_in.replace('T', '-').replace(':', '-').split('-')])
            return str(date_out)
    except Exception as e:
        print(e)


def month(cr_date):
    try:
        cr_date = datetime.datetime.strptime(cr_date, '%Y-%m-%d %H:%M:%S')
        cr_date = cr_date.strftime("%d/%B/%Y")
        return cr_date
    except Exception as e:
        print(e)


def chartjsData(lists, cards):
    data = []
    try:
        for list in lists:
            d = {"list_id": list.list_id, "list_name": list.list_name, "list_description": list.list_description, "TotalCards": 0,
                 "Completed": 0, "InProgress": 0, "PastDeadline": 0}
            for card in cards:
                if card.card_list_id == d["list_id"]:
                    if card.card_status == 'Completed':
                        d['Completed'] += 1
                        d['TotalCards'] += 1
                    if card.card_status == 'In Progress':
                        d['InProgress'] += 1
                        d['TotalCards'] += 1
                    if card.card_status == 'Past Deadline':
                        d['PastDeadline'] += 1
                        d['TotalCards'] += 1
            data.append(d)
        return data
    except Exception as e:
        print(e)
