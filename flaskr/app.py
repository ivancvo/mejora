from flaskr import create_app
from flask_migrate import Migrate
from flaskr.modelos.modelos import db
from flask_restful import Api

from flask_cors import CORS

app = create_app('default')
app_context = app.app_context()
app_context.push()
CORS(app)
db.init_app(app)
db.create_all()

api = Api(app)



migrate = Migrate()
migrate.init_app(app, db)