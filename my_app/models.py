from datetime import datetime
from email.policy import default
from enum import unique
from sqlalchemy import ForeignKey

from sqlalchemy.orm import backref
from my_app import db, login_manager
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class Post(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
  title = db.Column(db.Text, nullable=False)
  content = db.Column(db.Text, nullable=False)
  avg_rating = db.Column(db.Integer)
  comments = db.Column(db.Integer,default=0)
  author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

  def __repr__(self):
    return f"Post('{self.date}', '{self.title}', '{self.content}','{self.rating}','{self.comments}')"
  
  #calculate average rating of a post
  def get_avg_rating(self):
    ratings = Rating.query.filter_by(post_id=self.id).all()
    rating_count = 0
    rating_sum = 0
    for rating in ratings:
      rating_sum = int(rating.score) + rating_sum
      rating_count = rating_count + 1
    if rating_count > 0:
      avg_post_rating = rating_sum/ rating_count
      avg_post_rating = round(avg_post_rating,1)
    else:
      avg_post_rating = None
    self.avg_rating = avg_post_rating

class User(UserMixin,db.Model):
  id = db.Column(db.Integer, primary_key=True)
  first_name = db.Column(db.String(80), unique=False, nullable=False)
  email = db.Column(db.String(120), unique=True, nullable=False)
  username = db.Column(db.String(80), unique=True, nullable=False)
  image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
  hashed_password=db.Column(db.String(128))
  post = db.relationship('Post', backref='author', lazy=True)

  def __repr__(self):
    return f"User('{self.first_name}','{self.email}',{self.username}','{self.image_file}')"
  
  #check if current user has rated the post or not
  def has_rated_post(self, post):
    return Rating.query.filter(Rating.user_id == self.id, Rating.post_id == post.id).count() > 0
  
  #get rating score if user has already rated the post
  def get_user_rating_for_post(self, post):
    return Rating.query.filter_by(score = Rating.score, user_id = self.id, post_id = post.id).first()

#adated from Grinberg(2014, 2018)
  @property
  def password(self):
    raise AttributeError('Password is not readable.')

  @password.setter
  def password(self,password):
    self.hashed_password=generate_password_hash(password)

  def verify_password(self,password):
    return check_password_hash(self.hashed_password,password)


class Post_Comments(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  body = db.Column(db.Text, nullable=False)
  timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
  author = db.Column(db.Text, nullable=False)
  post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)

  def __repr__(self):
    return f"Post_Comments('{self.body}','{self.timestamp}')"

class Rating(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  score = db.Column(db.Integer)
  user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
  post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)
  
  def __repr__(self):
    return f"Rating('{self.score}')"
  

@login_manager.user_loader
def load_user(user_id):
  return User.query.get(int(user_id))
