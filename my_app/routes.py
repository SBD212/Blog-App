from flask import render_template, url_for, redirect, request, flash, abort
from flask_login.utils import confirm_login, login_required
from flask_wtf import form
from my_app import app, db
from my_app.forms import RegistrationForm, LoginForm, PostForm, CommentForm, RatingForm, SortPostsForm
from my_app.models import User, Post, Post_Comments, Rating
from flask_login import login_user, logout_user, current_user

@app.route('/', methods = ['GET', 'POST'])
def home():
  posts = Post.query.order_by(Post.date.desc()).all()
  form = SortPostsForm()
  if form.validate_on_submit():
    if form.sorted.data == 'date_asc':
      posts = Post.query.order_by(Post.date.asc()).all()
    elif form.sorted.data == 'date_desc':
      posts = Post.query.order_by(Post.date.desc()).all()
  return render_template('home.html', posts = posts, form = form)

@app.route('/register', methods=['GET','POST'])
def register():
    form = RegistrationForm()
    user = User.query.filter_by(email = form.email.data).first()

    if user:
      flash('An account with that email already exists.', 'error')
      return redirect(url_for('login'))

    if form.validate_on_submit():
      user = User(first_name = form.first_name.data,email=form.email.data, username=form.username.data, password=form.password.data)
      db.session.add(user)
      db.session.commit()
      login_user(user)
      flash('Registration successful, logging you in!')
      return redirect(url_for('registered'))
    return render_template('register.html', form=form)

@app.route('/register_success')
def registered():
    return render_template('home.html')

@app.route("/login",methods=['GET','POST'])
def login():
  form = LoginForm()
  if form.validate_on_submit():
    user = User.query.filter_by(username=form.username.data).first()
    if user is not None and user.verify_password(form.password.data):
      login_user(user)
      flash('You\'ve successfully logged in,'+' '+ current_user.username +'!','message')
      return redirect(url_for('home'))
  return render_template('login.html', form=form)


@app.route('/post/new', methods = ['GET', 'POST'])
@login_required
def new_post():
  form = PostForm()
  if form.validate_on_submit():
    post = Post(title=form.title.data, content=form.content.data, author = current_user)
    db.session.add(post)
    db.session.commit()
    flash('Your post has been created!','message')
    return redirect(url_for('home'))
  return render_template('create_post.html', title='New Post', form=form, legend='New Post')

@app.route('/post/<int:post_id>', methods=["GET", "POST"])
def post(post_id):
  post = Post.query.get_or_404(post_id)
  comments = Post_Comments.query.filter_by(post_id=post.id ).all()

  form_rating = RatingForm()
  if form_rating.validate_on_submit():
    form_rating = Rating(score=form_rating.rate.data, user_id=current_user.id, post_id=post.id)
    if current_user.has_rated_post(post):
      previous_rating = current_user.get_user_rating_for_post(post)
      db.session.delete(previous_rating)
      db.session.commit()

    db.session.add(form_rating)
    post.get_avg_rating()
    db.session.commit()
    flash('Your rating has been created!','message')
    return redirect(request.referrer)

  form_comment = CommentForm()
  if form_comment.validate_on_submit():
    form_comment = Post_Comments(body=form_comment.body.data, author = form_comment.author.data, post_id=post.id)
    db.session.add(form_comment)
    post.comments = post.comments + 1
    db.session.commit()
    flash('Your comment has been created!','message')
    return redirect(request.referrer)
  
  if current_user.is_authenticated:
    return render_template('post.html', title=post.title, post=post, form_comment = form_comment, form_rating = form_rating, comments=comments, has_rated = current_user.has_rated_post(post), 
    previous_rating = current_user.get_user_rating_for_post(post))
  
  else:
    return render_template('post.html', title=post.title, post=post, form_comment = form_comment, form_rating = form_rating, comments=comments, previous_rating = 0)


@app.route('/post/<int:post_id>/update', methods = ['GET', 'POST'])
@login_required
def update_post(post_id):
  post = Post.query.get_or_404(post_id)
  if post.author !=current_user:
    abort(403)
  
  form = PostForm()
  if form.validate_on_submit():
    post.title = form.title.data
    post.content = form.content.data
    db.session.commit()
    flash('Your post has been updated!', 'message')
    return redirect(url_for('post', post_id=post.id))
  
  elif request.method == 'GET':
    form.title.data = post.title
    form.content.data = post.content
  return render_template('create_post.html', title='Update Post', form=form, legend='Update Post')

@app.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'message')
    return redirect(url_for('home'))


@app.route('/logout')
def logout():
  if current_user:
    flash('You\'ve successfully logged out,'+' '+ current_user.username +'!','message')
  logout_user()
  return redirect(url_for('home'))
