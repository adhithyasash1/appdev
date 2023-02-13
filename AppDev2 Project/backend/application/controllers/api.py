# Imports
from application.utils.functions import *
from application.utils.validation import *
from application.data.access import *
from flask import request
from flask_restful import Resource, reqparse, fields, marshal_with
from flask_security import auth_required, current_user, utils
from application.data.cache import *
from application.data.models import user_datastore
from application.jobs import tasks


# IdentificationAPI
class IdentificationAPI(Resource):
    @staticmethod
    def get():
        """ User Identification :rtype: string """
        try:
            if current_user.is_authenticated:
                if current_user.username is not None:
                    return {'authenticated': True, 'username': current_user.username, 'email': current_user.email,
                            'id': current_user.id}, 200
                else:
                    return {'authenticated': True, 'email': current_user.email, 'id': current_user.id}, 200
            else:
                return {'authenticated': False}, 200
        except Exception as e:
            print(e)
            return {'message': 'Internal Server Error'}, 200


# USER API
user_response_fields = {
    "username": fields.String,
    "email": fields.String,
}

user_request_parse = reqparse.RequestParser()
user_request_parse.add_argument("username", type=str, required=True, help="Username is required")
user_request_parse.add_argument("email", type=str, required=True, help="Email is required")
user_request_parse.add_argument("password", type=str, required=True, help="Password is required")

class UserAPI(Resource):
    @auth_required('token')
    @marshal_with(user_response_fields)
    # @cache.cached(timeout=60)
    def get(self):
        """ Get user details :rtype: string """
        try:
            user_id = request.headers.get('user_id', None)
            if current_user.is_authenticated and int(current_user.id) == int(user_id):
                user = getUser(user_id)
                if user is None:
                    raise NotFoundError(status_code=404, error_code='USER404', error_message='User not found!')
                else:
                    return user, 200
            else:
                raise BusinessValidationError(
                    status_code=400, error_code='USER000',
                    error_message="Invalid token!")
        except Exception as e:
            print(e)
            raise BusinessValidationError(
                status_code=400, error_code='USER000',
                error_message="Internal Server Error!")

    @staticmethod
    def post():
        """ Create user :rtype: string """
        try:
            args = user_request_parse.parse_args()
            username = args.get('username', None)
            email = args.get('email', None)
            password = args.get('password', None)
            print("New user: " + username + "\nEmail : " + email + "\nPassword : " + password)

            if username is None or email is None or password is None:
                raise BusinessValidationError(
                    status_code=400, error_code='USER000',
                    error_message="Username, email and password are required!")

            if User.query.filter_by(email=email).first() is not None:
                raise BusinessValidationError(
                    status_code=400, error_code='USER000',
                    error_message="Email already exists!")

            else:
                try:
                    print("Creating user...")
                    user_datastore.create_user(username=username, email=email, password=utils.hash_password(password))
                    db.session.flush()
                    db.session.commit()
                    tasks.welcomeUser.delay(email, password)
                    return {'message': 'User created successfully!'}, 200
                except Exception as e:
                    print(e)
                    raise BusinessValidationError(
                        status_code=400, error_code='USER005',
                        error_message="Error creating user!")
        except Exception as e:
            print(e)
            raise BusinessValidationError(
                status_code=400, error_code='USER000',
                error_message="Internal Server Error!")


# LIST API
list_request_parse = reqparse.RequestParser()
list_request_parse.add_argument('list_name')
list_request_parse.add_argument('list_description')

update_request_parse = reqparse.RequestParser()
update_request_parse.add_argument('list_name')
update_request_parse.add_argument('list_description')

list_response_fields = {
    "list_id": fields.Integer,
    "list_name": fields.String,
    "list_description": fields.String,
    "user_id": fields.Integer,
}

class ListAPI(Resource):
    @auth_required('token')
    @marshal_with(list_response_fields)
    # @cache.cached(timeout=60)
    def get(self):
        """ Get a List :rtype: string """
        try:
            user_id = request.headers.get('user_id', None)
            if current_user.is_authenticated and int(current_user.id) == int(user_id):
                list_details = getListsDefault(user_id)
                if list_details:
                    return list_details, 200
                else:
                    raise NotFoundError(
                        status_code=404, error_code='LIST004',
                        error_message="List not found!")
            else:
                raise BusinessValidationError(
                    status_code=400, error_code='NAME000',
                    error_message="Invalid token!")
        except Exception as e:
            print(e)
            raise BusinessValidationError(
                status_code=400, error_code='LIST000',
                error_message="Error in getting the list!")

    @auth_required('token')
    def delete(self):
        """ Delete a list :rtype: string """
        try:
            user_id = request.headers.get('user_id', None)
            list_id = request.headers.get('list_id', None)
            if current_user.is_authenticated and int(current_user.id) == int(user_id):
                list_details = getList(list_id)
                if list_details:
                    db.session.delete(list_details)
                    db.session.flush()
                    db.session.commit()

                    cache.delete_memoized(getListsDefault)
                    cache.delete_memoized(getLists)
                    cache.delete_memoized(getList)

                    return {"message": "List Deleted!"}, 200
                else:
                    raise NotFoundError(
                        status_code=404, error_code='LIST004',
                        error_message="List not found!")
            else:
                raise BusinessValidationError(
                    status_code=400, error_code='LIST000',
                    error_message="Invalid token!")
        except Exception as e:
            print(e)
            raise BusinessValidationError(
                status_code=400, error_code='LIST005',
                error_message="Error deleting list!")

    @auth_required('token')
    @marshal_with(list_response_fields)
    def put(self):
        """ Update a list :rtype: string """
        try:
            user_id = request.headers.get('user_id', None)
            list_id = request.headers.get('list_id', None)
            if current_user.is_authenticated and int(current_user.id) == int(user_id):
                args = update_request_parse.parse_args()
                list_name = args.get('list_name', None)
                list_description = args.get('list_description', None)

                if list_name is None:
                    raise SchemaValidationError(
                        status_code=400, error_code='LIST005',
                        error_message='List Name is required and should be a String!')

                if list_description is None:
                    raise SchemaValidationError(
                        status_code=400, error_code='LIST006',
                        error_message='List Description should be a String!')

                list_exists = getList(list_id)

                if list_exists is None:
                    raise NotFoundError(
                        status_code=404, error_code='LIST004',
                        error_message="List not found!")
                else:
                    db.session.query(List).filter(List.list_id == list_id).update(
                        {'list_name': list_name, 'list_description': list_description})
                    db.session.flush()
                    db.session.commit()

                    cache.delete_memoized(getListsDefault)
                    cache.delete_memoized(getLists)
                    cache.delete_memoized(getList)

                    return {"message": "List updated successfully!"}, 200
            else:
                raise BusinessValidationError(
                    status_code=400, error_code='LIST000',
                    error_message="Invalid token!")
        except Exception as e:
            print(e)
            raise BusinessValidationError(
                status_code=400, error_code='LIST007',
                error_message="Error updating list!")

    @auth_required('token')
    @marshal_with(list_response_fields)
    def post(self):
        """ Create a list :rtype: string """
        try:
            user_id = request.headers.get('user_id', None)
            if current_user.is_authenticated and int(current_user.id) == int(user_id):
                args = list_request_parse.parse_args()
                list_name = args.get('list_name', None)
                list_description = args.get('list_description', None)

                if list_name is None:
                    raise SchemaValidationError(
                        status_code=400, error_code='LIST005',
                        error_message='List Name is required and should be a String!')

                if list_description is None:
                    raise SchemaValidationError(
                        status_code=400, error_code='LIST006',
                        error_message='List Description should be a String!')

                else:
                    new_list = List(list_name=list_name, list_description=list_description, user_id=user_id)
                    db.session.add(new_list)
                    db.session.flush()
                    db.session.commit()

                    cache.delete_memoized(getList)
                    cache.delete_memoized(getLists)
                    cache.delete_memoized(getListsDefault)

                    return {"message": "List created successfully!"}, 200
            else:
                raise BusinessValidationError(
                    status_code=400, error_code='LIST000',
                    error_message="Invalid token!")
        except Exception as e:
            print(e)
            raise BusinessValidationError(
                status_code=400, error_code='LIST007',
                error_message="Error creating list!")


# CARD API
card_request_parse = reqparse.RequestParser()
card_request_parse.add_argument('card_title')
card_request_parse.add_argument('card_content')
card_request_parse.add_argument('card_deadline')
card_request_parse.add_argument('card_status')

cardUpdate_request_parse = reqparse.RequestParser()
cardUpdate_request_parse.add_argument('card_title')
cardUpdate_request_parse.add_argument('card_content')
cardUpdate_request_parse.add_argument('card_deadline')
cardUpdate_request_parse.add_argument('card_status')
cardUpdate_request_parse.add_argument('card_list_id')

card_response_fields = {
    "card_id": fields.Integer,
    "card_title": fields.String,
    "card_content": fields.String,
    "card_deadline": fields.String,
    "card_status": fields.String,
    "card_list_id": fields.Integer,
}

class CardAPI(Resource):
    @auth_required('token')
    @marshal_with(card_response_fields)
    # @cache.cached(timeout=60)
    def get(self):
        """ Get a card :rtype: string """
        try:
            user_id = request.headers.get('user_id', None)
            list_id = request.headers.get('list_id', None)
            if current_user.is_authenticated and int(current_user.id) == int(user_id):
                card_details = getCards(list_id)
                if card_details:
                    return card_details, 200
                else:
                    raise NotFoundError(
                        status_code=404, error_code='CARD004',
                        error_message="Cards not found!")
            else:
                raise BusinessValidationError(
                    status_code=400, error_code='CARD000',
                    error_message="Invalid token!")
        except Exception as e:
            print(e)
            raise BusinessValidationError(
                status_code=400, error_code='CARD008',
                error_message="Error in getting the card!")

    @auth_required('token')
    def delete(self):
        """ Delete a card :rtype: string """
        try:
            user_id = request.headers.get('user_id', None)
            card_id = request.headers.get('card_id', None)
            if current_user.is_authenticated and int(current_user.id) == int(user_id):
                card_exists = getCard(card_id)

                if card_exists:
                    db.session.delete(card_exists)
                    db.session.flush()
                    db.session.commit()

                    cache.delete_memoized(getCardsDefault)
                    cache.delete_memoized(getCards)
                    cache.delete_memoized(getCard)

                    return {"message": "Card deleted successfully!"}, 200

                else:
                    raise NotFoundError(
                        status_code=404, error_code='CARD004',
                        error_message="Card not found for deletion!")
            else:
                raise BusinessValidationError(
                    status_code=400, error_code='CARD000',
                    error_message="Invalid token!")
        except Exception as e:
            print(e)
            raise BusinessValidationError(
                status_code=400, error_code='CARD007',
                error_message="Error in deleting card!")

    @auth_required('token')
    @marshal_with(card_response_fields)
    def put(self):
        """ Update a card :rtype: string """
        try:
            user_id = request.headers.get('user_id', None)
            card_id = request.headers.get('card_id', None)
            if current_user.is_authenticated and int(current_user.id) == int(user_id):
                args = cardUpdate_request_parse.parse_args()
                card_title = args.get('card_title', None)
                card_content = args.get('card_content', None)
                card_deadline_raw = args.get('card_deadline', None)
                card_status = args.get('card_status', None)
                new_card_list_id = args.get('card_list_id', None)

                if card_title is None:
                    raise SchemaValidationError(
                        status_code=400, error_code='CARD005',
                        error_message='Card Name is required and should be a String!')

                if card_content is None:
                    raise SchemaValidationError(
                        status_code=400, error_code='CARD006',
                        error_message='Card Content is required and should be a String!')

                if card_deadline_raw is None:
                    raise SchemaValidationError(
                        status_code=400, error_code='CARD007',
                        error_message='Card Deadline is required!')

                if card_status is None:
                    raise SchemaValidationError(
                        status_code=400, error_code='CARD008',
                        error_message='Card Status is required and should be a String!')

                f = datetime.datetime.now()
                x = f.strftime("%Y-%m-%d %H:%M:%S")
                card_deadline = getdate(card_deadline_raw)

                card_exists = getCard(card_id)

                if card_exists is None:
                    raise NotFoundError(
                        status_code=404, error_code='CARD004',
                        error_message="Card not found for updation!")

                else:
                    if card_status == 'Completed':
                        db.session.query(Card).filter(Card.card_id == card_id).update(
                            {'card_title': card_title, 'card_content': card_content, 'card_updation_date': x,
                             'card_deadline': card_deadline, 'card_status': card_status, 'card_list_id': new_card_list_id})

                        db.session.flush()
                        db.session.commit()

                        cache.delete_memoized(getCardsDefault)
                        cache.delete_memoized(getCards)
                        cache.delete_memoized(getCard)

                        return card_exists, 200

                    else:
                        db.session.query(Card).filter(Card.card_id == card_id).update(
                            {'card_title': card_title, 'card_content': card_content, 'card_deadline': card_deadline,
                             'card_status': card_status, 'card_list_id': new_card_list_id})
                        db.session.flush()
                        db.session.commit()

                        cache.delete_memoized(getCardsDefault)
                        cache.delete_memoized(getCards)
                        cache.delete_memoized(getCard)

                        return card_exists, 200

            else:
                raise BusinessValidationError(
                    status_code=400, error_code='CARD000',
                    error_message="Invalid token!")
        except Exception as e:
            print(e)
            raise BusinessValidationError(
                status_code=400, error_code='CARD000',
                error_message="Error in updating card!")

    @auth_required('token')
    @marshal_with(card_response_fields)
    def post(self):
        """ Create a card :rtype: string """
        try:
            user_id = request.headers.get('user_id', None)
            list_id = request.headers.get('list_id', None)
            if current_user.is_authenticated and int(current_user.id) == int(user_id):
                args = card_request_parse.parse_args()
                card_title = args.get('card_title', None)
                card_content = args.get('card_content', None)
                card_deadline_raw = args.get('card_deadline', None)
                card_status = args.get('card_status', None)

                if card_title is None:
                    raise SchemaValidationError(
                        status_code=400, error_code='CARD005',
                        error_message='Card Name is required and should be a String!')

                if card_content is None:
                    raise SchemaValidationError(
                        status_code=400, error_code='CARD006',
                        error_message='Card Content is required and should be a String!')

                if card_deadline_raw is None:
                    raise SchemaValidationError(
                        status_code=400, error_code='CARD007',
                        error_message='Card Deadline is required!')

                if card_status is None:
                    raise SchemaValidationError(
                        status_code=400, error_code='CARD008',
                        error_message='Card Status is required and should be a String!')

                else:
                    f = datetime.datetime.now()
                    x = f.strftime("%Y-%m-%d %H:%M:%S")
                    card_deadline = getdate(card_deadline_raw)

                    new_card = Card(card_title=card_title, card_content=card_content, card_creation_date=x,
                                    card_deadline=card_deadline, card_status=card_status, card_list_id=list_id)
                    db.session.add(new_card)
                    db.session.flush()
                    db.session.commit()

                    cache.delete_memoized(getCardsDefault)
                    cache.delete_memoized(getCards)
                    cache.delete_memoized(getCard)

                    return new_card, 200
            else:
                raise BusinessValidationError(
                    status_code=400, error_code='CARD000',
                    error_message="Invalid token!")
        except Exception as e:
            print(e)
            raise BusinessValidationError(
                status_code=400, error_code='CARD001',
                error_message="Error while creating card!")


# User Summary Data API
summary_response_fields = {
    "list_id": fields.Integer,
    "list_name": fields.String,
    "list_description": fields.String,
    "TotalCards": fields.Integer,
    "Completed": fields.Integer,
    "InProgress": fields.Integer,
    "PastDeadline": fields.Integer,
}

class UserSummaryAPI(Resource):
    @auth_required('token')
    @marshal_with(summary_response_fields)
    # @cache.cached(timeout=50)
    def get(self):
        """ Get User Summary Data :rtype: string """
        try:
            user_id = request.headers.get('user_id', None)
            if current_user.is_authenticated and int(current_user.id) == int(user_id):
                lists = db.engine.execute(
                    'select l.list_id, l.list_name, l.list_description from List as l, User as u where u.id = l.user_id and u.id = ?',
                    user_id).fetchall()
                cards = db.engine.execute(
                    'select c.card_id, c.card_updation_date, c.card_status, c.card_list_id from Card as c, List as l, User as u where c.card_list_id = l.list_id and l.user_id = u.id and u.id = ?',
                    user_id).fetchall()
                chart = chartjsData(lists, cards)
                return chart, 200
            else:
                raise BusinessValidationError(
                    status_code=400, error_code='SUMMARY000',
                    error_message="Invalid token!")
        except Exception as e:
            print(e)
            raise InternalServerError(
                status_code=500, error_code='SUMMARY001',
                error_message="Internal Server Error!")


# Transfer Cards API

class TransferCardsAPI(Resource):
    @auth_required('token')
    def put(self):
        """ Transfer Cards :rtype: string """
        try:
            user_id = request.headers.get('user_id', None)
            list_id = request.headers.get('list_id', None)
            new_list_id = request.headers.get('new_list_id', None)
            if current_user.is_authenticated and int(current_user.id) == int(user_id):
                db.session.query(Card).filter(Card.card_list_id == list_id).update({'card_list_id': new_list_id})
                db.session.flush()
                list = List.query.get(list_id)
                db.session.delete(list)
                db.session.flush()
                db.session.commit()
                cache.delete_memoized(getCardsDefault)
                cache.delete_memoized(getCards)
                cache.delete_memoized(getCard)
                cache.delete_memoized(getListsDefault)
                cache.delete_memoized(getLists)
                cache.delete_memoized(getList)
                return {"message": "Cards Transferred Successfully before deletion!"}, 200
            else:
                raise BusinessValidationError(
                    status_code=400, error_code='TRANSFER000',
                    error_message="Invalid token!")
        except Exception as e:
            print(e)
            raise BusinessValidationError(
                status_code=400, error_code='TRANSFER001',
                error_message="Error in transferring cards!")


# Export Board API

class ExportBoardAPI(Resource):
    @auth_required('token')
    def get(self):
        """ Export Board :rtype: string """
        try:
            user_id = request.headers.get('user_id', None)
            if current_user.is_authenticated and int(current_user.id) == int(user_id):
                try:
                    tasks.exportBoard.delay(user_id)
                    return {"message": "Board Exported Successfully and sent as attachment to your email."}, 200
                except Exception as e:
                    print(e)
                    raise BusinessValidationError(
                        status_code=400, error_code='EXPORT000',
                        error_message="Board Export Failed!")
            else:
                raise BusinessValidationError(
                    status_code=400, error_code='EXPORT003',
                    error_message="Invalid token!")
        except Exception as e:
            print(e)
            raise BusinessValidationError(
                status_code=400, error_code='EXPORT001',
                error_message="Error while exporting board!")


# Export List API

class ExportListAPI(Resource):
    @auth_required('token')
    def get(self):
        """ Export List :rtype: string """
        try:
            user_id = request.headers.get('user_id', None)
            list_id = request.headers.get('list_id', None)
            if current_user.is_authenticated and int(current_user.id) == int(user_id):
                try:
                    tasks.exportList.delay(user_id, list_id)
                    return {"message": "List Exported Successfully and sent as attachment to your email."}, 200
                except Exception as e:
                    print(e)
                    raise BusinessValidationError(
                        status_code=400, error_code='EXPORT002',
                        error_message="Export List Failed!")
            else:
                raise BusinessValidationError(
                    status_code=400, error_code='EXPORT003',
                    error_message="Invalid token!")
        except Exception as e:
            print(e)
            raise BusinessValidationError(
                status_code=400, error_code='EXPORT001',
                error_message="Error in exporting list!")


# Import Lists API

class ImportListsAPI(Resource):
    @auth_required('token')
    def post(self):
        """ Import List :rtype: string """
        try:
            user_id = request.headers.get('user_id', None)
            file = request.files['file']
            with open('importList.csv', 'wb') as f:
                f.write(file.read())
            if current_user.is_authenticated and int(current_user.id) == int(user_id):
                try:
                    tasks.importLists.delay(user_id, 'importList.csv')
                    return 200
                except Exception as e:
                    print(e)
                    raise BusinessValidationError(
                            status_code=400, error_code='IMPORT002',
                            error_message="Import List Failed!")
            else:
                raise BusinessValidationError(
                        status_code=400, error_code='IMPORT003',
                        error_message="Invalid token!")
        except Exception as e:
            print(e)
            raise BusinessValidationError(
                    status_code=400, error_code='IMPORT001',
                    error_message="Error in importing list!")

# Import Cards API

class ImportCardsAPI(Resource):
    @auth_required('token')
    def post(self):
        """ Import Cards :rtype: string """
        try:
            user_id = request.headers.get('user_id', None)
            list_id = request.headers.get('list_id', None)
            file = request.files['file']
            with open('importCard.csv', 'wb') as f:
                f.write(file.read())
            if current_user.is_authenticated and int(current_user.id) == int(user_id):
                try:
                    tasks.importCards.delay(list_id, 'importCard.csv')
                    tasks.updateDashboard.delay()
                    return 200
                except Exception as e:
                    print(e)
                    raise BusinessValidationError(
                        status_code=400, error_code='IMPORT002',
                        error_message="Import Cards Failed!")
            else:
                raise BusinessValidationError(
                    status_code=400, error_code='IMPORT003',
                    error_message="Invalid token!")
        except Exception as e:
            print(e)
            raise BusinessValidationError(
                status_code=400, error_code='IMPORT004',
                error_message="Error in importing cards!")


# Test API
test_api_response_fields = {
    'message': fields.String,
}

class TestAPI(Resource):
    @auth_required("token")
    @marshal_with(test_api_response_fields)
    def get(self):
        """ Test API :rtype: string """
        try:
            if current_user.is_authenticated:
                return {"message": "Hello, %s!" % current_user.username + "," + "your id is" % current_user.id}, 200
            else:
                raise BusinessValidationError(status_code=401, error_code='TEST400', error_message='Unauthorized Access!')
        except Exception as e:
            print(e)