#for creating forms we need many different validation checks, some reg-ex for valid email, check password etc. For this is an extension wtforms which makes all these things easy.We will be writing python classes representing forms, they will be converted to html forms in templates
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField,SubmitField,BooleanField, TextAreaField
from wtforms.validators import DataRequired,Length,Email,EqualTo, ValidationError
from birthday.models import User,Post

class RegistrationForm(FlaskForm): # use of inheritance, RegistratonForm(child class) inheriting from FlaskForm(parent class)  
  username = StringField('Username',validators=[DataRequired(),Length(min = 2,max = 20)]) #first argument is the name of the field and it will also be used as a label in out html. 
  email = StringField('Email', validators=[DataRequired(),Email()])
  password = PasswordField("Password",validators=[DataRequired()])
  confirm_password = PasswordField("Password",validators=[DataRequired(),EqualTo('password')])
  submit = SubmitField('Sign Up') #Sign up is the label

  #template for our validation check
  # def validate_field(self,field):
  #   if True:
  #     raise ValidationError('Validation Message')

  #validation for the username to be unique
  def validate_username(self,username):
    user = User.query.filter_by(username=username.data).first()
    if user:
      raise ValidationError('Username already taken! Please choose a different username')
  #for email
  def validate_email(self,email):
    user = User.query.filter_by(username=email.data).first()
    if user:
      raise ValidationError('Email already used! Please enter a different email')
    


class LoginForm(FlaskForm):
  email = StringField('Email', validators=[DataRequired(),Email()])
  password = PasswordField("Password",validators=[DataRequired()])
  remember = BooleanField('Remember Me')
  submit = SubmitField('Log In')

class PostForm(FlaskForm):
  name =  StringField('Name',validators=[DataRequired()])
  day = StringField('Day',validators=[DataRequired()])
  month = StringField('Month',validators=[DataRequired()])
  submit = SubmitField('Post')

  # def validate_name(self,name):
  #   check_name = Post.query.filter_by(name=name.data).first()
  #   if check_name :
  #     raise ValidationError(f'Already added a person named {check_name.name}. Please use another name!  ')