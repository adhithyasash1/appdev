import os
import datetime
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import matplotlib.pyplot as plt
# from sqlalchemy import text, delete, insert, update

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'database/database.db')
db = SQLAlchemy(app)
DB_PATH = 'database/database.db'


# Models

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer(), nullable = False, unique = True, autoincrement = True, primary_key = True)
    username = db.Column(db.String(), nullable = False)
    email = db.Column(db.String(), nullable = False)
    lists = db.relationship("List")

    def __repr__(self):
        return "<User(username = '%s')>" % self.username

class List(db.Model):
    __tablename__ = 'list'
    list_id = db.Column(db.Integer(), autoincrement = True, primary_key = True, nullable = False, unique = True)
    list_name = db.Column(db.String(), nullable = False)
    list_description = db.Column(db.String())
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id',  ondelete="CASCADE"), nullable = False)
    user = db.relationship("User")
    cards = db.relationship("Card", cascade="all, delete")

    def __repr__(self):
        return "<List(list_name='%s', list_description='%s')>" % (self.list_name, self.list_description)

class Card(db.Model):
    __tablename__ = 'card'
    card_id = db.Column(db.Integer(), autoincrement = True, primary_key = True, nullable = False, unique = True)
    card_title = db.Column(db.String(), nullable = False)
    card_content = db.Column(db.String(), nullable = False)
    card_creation_date = db.Column(db.String(), nullable = False)
    card_updation_date = db.Column(db.String(), nullable = True)
    card_deadline = db.Column(db.String(), nullable = False)
    card_status = db.Column(db.String(), nullable = False)
    card_list_id = db.Column(db.Integer(), db.ForeignKey('list.list_id',  ondelete="CASCADE"), nullable = False)

    def __repr__(self):
        return "<Card(card_title='%s', card_content='%s', card_deadline='%s', card_status='%s')>" % (self.card_title, self.card_content, self.card_deadline, self.card_status)

# Helper Functions

def getdate(date_in):
    date_out = datetime.datetime(*[int(v) for v in date_in.replace('T', '-').replace(':', '-').split('-')])
    return str(date_out)

def month(cr_date):
    cr_date = datetime.datetime.strptime(cr_date, '%Y-%m-%d %H:%M:%S')
    cr_date = cr_date.strftime("%d/%B/%Y")
    return cr_date

def details(lists, cards):
    d = { }
    for list in lists:
        d[list.list_id] = [ ]
        total_cards_value = 0
        completed_value, in_progress_value, past_deadline_value = 0, 0, 0
        for card in cards:
            if card.card_list_id == list.list_id:
                if card.card_status == 'In Progress':
                    in_progress_value += 1
                    total_cards_value += 1
                if card.card_status == 'Completed':
                    completed_value += 1
                    total_cards_value += 1
                if card.card_status == 'Past Deadline':
                    past_deadline_value += 1
                    total_cards_value += 1
        d[list.list_id].append(total_cards_value)
        d[list.list_id].append(completed_value)
        d[list.list_id].append(in_progress_value)
        d[list.list_id].append(past_deadline_value)
    return d

def data_generation(lists, cards):
    d = { }
    for list in lists:
        d[list.list_id] = { }
        for card in cards:
            if card.card_list_id == list.list_id:
                if card.card_status == 'Completed':
                    if card.card_updation_date is not None:
                        x = month(card.card_updation_date)
                        if x not in d[list.list_id].keys():
                            d[list.list_id][x] = 1
                        else:
                            d[list.list_id][x] += 1
    return d


def graph_generation(d):
    for key in d.keys():
        x, y = [], []
        f = datetime.datetime.now()
        z = f.strftime("%d/%B/%Y")

        if d[key] == {}:
            x.append(z)
            y.append(0)
        else:
            for i in d[key].keys():
                if d[key]:
                    x.append(i)
                    y.append(d[key][i])

        plt.scatter(x, y, edgecolor='yellow', color=['saddlebrown'])
        plt.title('Number of Cards VS Completion Dates')
        plt.xlabel('Dates', fontsize=15)
        plt.ylabel('Cards', fontsize=15)
        plt.savefig(f'static/{str(key)}.png')
        plt.close()

def get_images(lists):
    x = { }
    for list in lists:
        x[list.list_id] = str(list.list_id)+'.png'
    return x

# Controllers

@app.route("/", methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username, email = request.form['username'], request.form['email']
        if db.session.query(User).filter(User.username == username, User.email == email).first() is None:
            user = User(username=username, email=email)
            db.session.add(user)
            db.session.commit()
            user = db.session.query(User).filter(User.username == username, User.email == email).first()
            return render_template('NewHome.html', user=user)
        else:
            user = db.session.query(User).filter(User.username == username, User.email == email).first()
            id = user.id
            return redirect(url_for('Home', id=id))
    return render_template('Login.html')

@app.route("/Home/user/<int:id>", methods=('GET', 'POST'))
def Home(id):
    lists = db.engine.execute('select l.list_name, l.list_description from list as l, user as u where u.id = l.user_id and u.id = ?', id).fetchall()
    if not lists:
        user = db.session.query(User).filter(User.id == id).first()
        return render_template('NewHome.html', user=user)
    else:
        f = datetime.datetime.now()
        x = f.strftime("%Y-%m-%d %H:%M:%S")
        lists = db.engine.execute('select l.list_id, l.list_name, l.list_description from list as l, user as u where u.id = l.user_id and u.id = ?', id).fetchall()
        cards = db.engine.execute('select c.card_id, c.card_title, c.card_content, c.card_creation_date, c.card_updation_date, c.card_deadline, c.card_status, c.card_list_id from list as l, card as c, user as u where u.id = l.user_id and l.list_id = c.card_list_id and u.id = ?', id).fetchall()
        user = db.session.query(User).filter(User.id == id).first()
        for card in cards:
            if card.card_deadline < x:
                y = card.card_id
                status = 'Completed'
                db.session.query(Card).filter(Card.card_id == y).update({'card_status' : status, 'card_updation_date' : x})
                db.session.commit()
        return render_template('Home.html', lists=lists, cards=cards, user=user)

@app.route('/user/<int:id>/newlist', methods=["GET", "POST"])
def newlist(id):
    user = db.session.query(User).filter(User.id == id).first() # User.query.get(id)
    if request.method == 'POST':
        list_name, list_description = request.form['list_name'], request.form['list_description']
        list = List(list_name=list_name, list_description=list_description, user_id = id)
        db.session.add(list)
        db.session.commit()
        return redirect(url_for('Home', id=id))
    return render_template('NewList.html', user = user)

@app.route('/user/<int:id>/newcard', methods=["GET", "POST"])
def newcard(id):
    lists = db.engine.execute('select l.list_id, l.list_name, l.list_description from list as l, user as u where u.id = l.user_id and u.id = ?', id).fetchall()
    user = db.session.query(User).filter(User.id == id).first()
    if request.method == 'POST':
        f = datetime.datetime.now()
        x = f.strftime("%Y-%m-%d %H:%M:%S")
        card_list_id = request.form['card_list_id']
        card_title, card_content = request.form['card_title'], request.form['card_content']
        string = request.form['card_deadline']
        card_deadline = getdate(string)
        card_status = request.form['card_status']
        if card_status == 'Completed':
            card = Card(card_title=card_title, card_content=card_content, card_creation_date = x, card_updation_date = x, card_deadline=card_deadline, card_status=card_status, card_list_id=card_list_id)
            db.session.add(card)
        else:
            card = Card(card_title=card_title, card_content=card_content, card_creation_date = x, card_deadline=card_deadline, card_status=card_status, card_list_id=card_list_id)
            db.session.add(card)
        db.session.commit()
        return redirect(url_for('Home', id=id))
    return render_template('NewCard.html', lists=lists, user=user)

@app.route('/user/<int:id>/list/<int:list_id>/update', methods=["GET", "POST"])
def updatelist(id, list_id):
    list = db.session.query(List).filter(List.list_id == list_id).first()
    user = db.session.query(User).filter(User.id == id).first()
    if request.method == 'POST':
        list_name = request.form['list_name']
        list_description = request.form['list_description']
        db.session.query(List).filter(List.list_id == list_id).update({'list_name': list_name, 'list_description' : list_description})
        db.session.commit()
        return redirect(url_for('Home', id=id))
    return render_template('UpdateList.html', user=user, list=list)

@app.route('/user/<int:id>/card/<int:card_id>/update', methods=["GET", "POST"])
def updatecard(id, card_id):
    lists = db.engine.execute('select l.list_id, l.list_name, l.list_description from list as l, user as u where u.id = l.user_id and u.id = ?', id).fetchall()
    user = db.session.query(User).filter(User.id == id).first()
    card = db.session.query(Card).filter(Card.card_id == card_id).first()
    if request.method == 'POST':
        f = datetime.datetime.now()
        x = f.strftime("%Y-%m-%d %H:%M:%S")
        card_list_id = request.form['card_list_id']
        card_title, card_content = request.form['card_title'], request.form['card_content']
        string = request.form['card_deadline']
        card_deadline = getdate(string)
        card_status =request.form['card_status']
        if card_status == 'Completed':
            db.session.query(Card).filter(Card.card_id == card_id).update({'card_title': card_title, 'card_content' : card_content, 'card_updation_date' : x, 'card_deadline' : card_deadline, 'card_status' : card_status, 'card_list_id' : card_list_id})
        else:
            db.session.query(Card).filter(Card.card_id == card_id).update({'card_title': card_title, 'card_content' : card_content, 'card_updation_date' : x, 'card_deadline' : card_deadline, 'card_status' : card_status, 'card_list_id' : card_list_id})
        db.session.commit()
        return redirect(url_for('Home', id=id))
    return render_template('UpdateCard.html', lists=lists, user=user, card=card)

@app.route('/user/<int:id>/list/<int:list_id>/delete', methods=["GET", "POST"])
def deletelist(id, list_id):
    list =  db.session.query(List).filter(List.list_id == list_id).first()
    user = db.session.query(User).filter(User.id == id).first()
    lists = db.engine.execute('select l.list_id, l.list_name, l.list_description from list as l, user as u where u.id = l.user_id and u.id = ?', id).fetchall()
    cards =  db.engine.execute('select * from card where card_list_id = ?', list.list_id).fetchall()
    if len(cards) >= 1:
        if request.method == 'GET':
            return render_template('Transfer.html', lists=lists, user=user, list=list)
        if request.method == 'POST':
            if request.form['sup'] == 'Transfer':
                cards_list_id = request.form['cards_list_id']
                db.session.query(Card).filter(Card.card_list_id == list_id).update({'card_list_id' : cards_list_id})
                list = List.query.get(list_id)
                db.session.delete(list)
                db.session.commit()
                return redirect(url_for('Home', id=id))
            if request.form['sup'] == 'Delete':
                list = List.query.get(list_id)
                db.session.delete(list)
                db.session.commit()
                return redirect(url_for('Home', id=id))
    else:
        if request.method == 'GET':
            list = List.query.get(list_id)
            db.session.delete(list)
            db.session.commit()
            return redirect(url_for('Home', id=id))

@app.route('/user/<int:id>/card/<int:card_id>/delete', methods=["GET", "POST"])
def deletecard(id, card_id):
    if request.method == 'GET':
        card = Card.query.get(card_id)
        db.session.delete(card)
        db.session.commit()
        return redirect(url_for('Home', id=id))

@app.route('/user/<int:id>/summary', methods=["GET", "POST"])
def summary(id):
    user = db.session.query(User).filter(User.id == id).first()
    lists = db.engine.execute('select l.list_id, l.list_name, l.list_description from list as l, user as u where u.id = l.user_id and u.id = ?', id).fetchall()
    cards = db.engine.execute('select c.card_id, c.card_updation_date, c.card_status, c.card_list_id from card as c, list as l, user as u where c.card_list_id = l.list_id and l.user_id = u.id and u.id = ?', id).fetchall()
    if request.method == 'GET':
        value = details(lists, cards)
        d = data_generation(lists, cards)
        graph_generation(d)
        images = get_images(lists)
        return render_template('Summary.html', user=user, lists=lists, value=value, images=images)

# Executor

if __name__ == '__main__':
    app.run(host = "0.0.0.0", port = 8080)

