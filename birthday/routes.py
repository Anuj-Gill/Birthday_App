from birthday.models import User, Post
from flask import render_template, url_for,flash, redirect, request, abort
from birthday.forms import RegistrationForm,LoginForm, PostForm
from birthday import bcrypt,app,db
from flask_login import login_user, current_user, logout_user, login_required



@app.route("/")
@app.route("/about")
def about():
  return render_template("about.html",title='About')

@app.route("/home",methods=['POST','GET'])
@login_required
def home():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(name=form.name.data, day=form.day.data,month=form.month.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash("Birthday added successfully!","success")
        return redirect(url_for('home'))
    post = Post.query.filter_by( user_id=current_user.id)
    return render_template("home.html",form = form,title = "Home Feed",post = post)

@app.route("/register", methods=['GET','POST']) #methods is used to specify that this specific route can accept these methods
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data,email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Account created for {form.username.data}! Please login now','success')
        return redirect(url_for('login'))
    # else:
    #     flash
    return render_template('register.html',form=form,title='Register')

@app.route("/login",methods=['POST','GET'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password,form.password.data):
          login_user(user,remember=form.remember.data)
          next_page = request.args.get('next')
          flash('Loged In!','success')
          return redirect(next_page) if next_page else  redirect(url_for('home'))
        else:
             flash('Login Unseccessful. Please check email and password','danger')
    return render_template('login.html',form=form,title='Login')

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route("/delete",methods=['POST'])
@login_required
def delete_post():
    id = int(request.args.get('id'))
    post = Post.query.get_or_404(id)
    db.session.delete(post)
    db.session.commit()
    flash('Birthday has been deleted!','success')
    return redirect(url_for('home'))
