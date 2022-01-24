from my_app import db
from my_app.models import User, Post

db.drop_all()
db.create_all()

