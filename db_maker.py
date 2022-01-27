from my_app import db
from my_app.models import User, Post

db.drop_all()
db.create_all()

#user1 = User(first_name = 'Junaid', email = 'junaidawan17@gmail.com', username = 'juniada2', password = '!234%_l@l')
test_user = User(first_name = 'test_user', email = 'user1@test.ac.uk',  username = 'test_user', password = 'passuser1')

db.session.add_all([test_user])
db.session.commit()

