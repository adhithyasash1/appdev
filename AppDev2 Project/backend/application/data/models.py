from application.data.database import db
from flask_security import UserMixin, RoleMixin, SQLAlchemyUserDatastore


Roles_Users = db.Table('Roles_Users',
                       db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
                       db.Column('role_id', db.Integer(), db.ForeignKey('role.id')))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer(), nullable=False, unique=True, autoincrement=True, primary_key=True)
    username = db.Column(db.String())
    email = db.Column(db.String(), unique=True)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean())
    fs_uniquifier = db.Column(db.String(255), unique=True, nullable=False)
    roles = db.relationship('Role', secondary='Roles_Users', backref=db.backref('users', lazy='dynamic'))
    lists = db.relationship("List", back_populates="user")

    def get_security_payload(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
        }

    def __repr__(self):
        return "<User(username = '%s', email = '%s')>" % (self.username, self.email)


class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))


class List(db.Model):
    list_id = db.Column(db.Integer(), autoincrement=True, primary_key=True, nullable=False, unique=True)
    list_name = db.Column(db.String(), nullable=False)
    list_description = db.Column(db.String())
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id', ondelete="CASCADE"), nullable=False)
    user = db.relationship("User")
    cards = db.relationship("Card", backref="list", lazy=True, cascade="all, delete")

    def __repr__(self):
        return "<List(list_name='%s', list_description='%s')>" % (self.list_name, self.list_description)


class Card(db.Model):
    card_id = db.Column(db.Integer(), autoincrement=True, primary_key=True, nullable=False, unique=True)
    card_title = db.Column(db.String(), nullable=False)
    card_content = db.Column(db.String(), nullable=False)
    card_creation_date = db.Column(db.String(), nullable=False)
    card_updation_date = db.Column(db.String(), nullable=True)
    card_deadline = db.Column(db.String(), nullable=False)
    card_status = db.Column(db.String(), nullable=False)
    card_list_id = db.Column(db.Integer(), db.ForeignKey('list.list_id', ondelete="CASCADE"), nullable=False)

    def __repr__(self):
        return "<Card(card_title='%s', card_content='%s', card_deadline='%s', card_status='%s')>" % (
            self.card_title, self.card_content, self.card_deadline, self.card_status)


user_datastore = SQLAlchemyUserDatastore(db, User, Role)
