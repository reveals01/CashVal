from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import distinct
from flask_login import LoginManager
#from .parameters.models import Parameter



app = Flask(__name__)
app.config.from_object("project.config.Config")
db = SQLAlchemy(app)
from .users.models import User

login_manager = LoginManager()
login_manager.login_view = 'users.login'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    # since the user_id is just the primary key of our user table, use it in the query for the user
    return User.query.get(int(user_id))



#from .positions.positions import positions_bp as positions_blueprint
#app.register_blueprint(positions_blueprint)

from .parameters.parameters import parameters_bp as parameters_blueprint
app.register_blueprint(parameters_blueprint)

from .accounts.accounts import accounts_bp as accounts_blueprint
app.register_blueprint(accounts_blueprint)

from .api.apis import apis_bp as apis_blueprint
app.register_blueprint(apis_blueprint)

from .users.users import users_bp as users_blueprint
app.register_blueprint(users_blueprint)

from .clients.clients import clients_bp as clients_blueprint
app.register_blueprint(clients_blueprint)

from .movements.movements import movements_bp as movements_blueprint
app.register_blueprint(movements_blueprint)


# blueprint for non-auth parts of app
from .main import main as main_blueprint
app.register_blueprint(main_blueprint)



#@app.context_processor
#def load_paramType():
#    distinct_labels = db.session.query(distinct(Parameter.typeLabel)).all()
#    distinct_labels_list = [label[0] for label in distinct_labels]
#    return dict(distinct_labels_list=distinct_labels_list)

