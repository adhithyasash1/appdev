from application.jobs import workers
from application.config import LocalDevelopmentConfig
from application.data.database import *
from application.data.models import *
from flask import Flask, render_template
from flask_caching import Cache
from flask_restful import Api
from flask_security import Security, SQLAlchemyUserDatastore
from flask_cors import CORS
import logging

logging.basicConfig(filename='logs/debug.log', level=logging.DEBUG, format=f'%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')


def create_app():
    app = Flask(__name__, template_folder="templates")
    CORS(app)

    app.logger.info("Starting Local Development.")
    app.config.from_object(LocalDevelopmentConfig)
    print("App running at http://localhost:8080")

    db.init_app(app)
    app.app_context().push()
    app.logger.info("App tools complete")
    user_datastore = SQLAlchemyUserDatastore(db, User, Role)
    security = Security(app, user_datastore)
    api = Api(app)
    app.app_context().push()

    celery = workers.celery
    celery.conf.update(broker_url=app.config['CELERY_BROKER_URL'], result_backend=app.config['CELERY_RESULT_BACKEND'], enable_utc=False, timezone='Asia/Kolkata')
    celery.Task = workers.ContextTask
    app.app_context().push()

    cache = Cache(app)
    app.app_context().push()

    return app, api, celery, cache


app, api, celery, cache = create_app()

from application.controllers.api import *
from application.controllers.controllers import *

api.add_resource(IdentificationAPI, '/api/identification')
api.add_resource(UserAPI, '/api/user')
api.add_resource(ListAPI, '/api/user/list')
api.add_resource(CardAPI, '/api/user/list/card')
api.add_resource(TestAPI, '/api/test')
api.add_resource(UserSummaryAPI, '/api/user/summary')
api.add_resource(TransferCardsAPI, '/api/user/list/cards/transfer')
api.add_resource(ExportListAPI, '/api/user/list/export')
api.add_resource(ExportBoardAPI, '/api/user/board/export')
api.add_resource(ImportListsAPI, '/api/user/lists/import')
api.add_resource(ImportCardsAPI, '/api/user/list/cards/import')


@app.errorhandler(404)
def page_not_found(e):
    print(e)
    return render_template('Error/404.html'), 404

@app.errorhandler(403)
def not_authorized(e):
    print(e)
    return render_template('Error/403.html'), 403


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
