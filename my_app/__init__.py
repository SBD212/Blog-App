from flask import Flask
from flask_moment import Moment
import os
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_manager

app = Flask(__name__)

app.config["SECRET_KEY"] = '9eaead86f0682ed25b8b86f29871dcf9d44d8d53ef86a981sssssssss33333333334343443'

basedir=os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'my_database.db')

#connecting to databse
#username = "c21100637"
#password = "passW0rddd"
#db_name = "flask_coursework"

#pp_config_sql_db_uri = f"mysql+pymysql://{username}:{password}@csmysql.cs.cf.ac.uk:3306/{username}_{db_name}"

#app.config["SQLALCHEMY_DATABASE_URI"] = app_config_sql_db_uri


db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)
moment = Moment(app)

from my_app import routes