from application.data.models import *
from application.data.cache import *
from application.data.database import *


@cache.cached(timeout=30, key_prefix='getUsers')
def getUsers():
    users = User.query.all()
    return users


@cache.memoize(50)
def getUser(user_id):
    user = User.query.filter_by(id=user_id)
    return user


@cache.memoize(50)
def getLists(user_id):
    lists = List.query.filter_by(user_id=user_id).all()
    return lists


@cache.memoize(50)
def getListsDefault(user_id):
    lists = db.engine.execute('select l.list_id, l.list_name, l.list_description from List as l, User as u where u.id = l.user_id and u.id = ?', user_id).fetchall()
    return lists


@cache.memoize(50)
def getList(list_id):
    list = List.query.filter_by(list_id=list_id).first()
    return list


@cache.memoize(50)
def getCards(list_id):
    cards = Card.query.filter_by(card_list_id=list_id).all()
    return cards


@cache.memoize(50)
def getCardsDefault(list_id):
    cards = db.engine.execute('select c.card_id, c.card_name, c.card_description, c.card_deadline, c.card_status, c.card_creation_date, c.card_updation_date, c.card_list_id from Card as c, List as l where c.card_list_id = l.list_id and l.list_id = ?', list_id).fetchall()
    return cards


@cache.memoize(50)
def getCard(card_id):
    card = Card.query.filter_by(card_id=card_id).first()
    return card
