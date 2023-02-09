import os
import csv
<<<<<<< HEAD

from flask import Flask, session, render_template, request, redirect, url_for
from flask_session import Session
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Email, Length
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
=======
>>>>>>> master

from flask import Flask, session, render_template, request, redirect, url_for
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Email, Length
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

bootstrap = Bootstrap()
db = SQLAlchemy()

<<<<<<< HEAD
=======

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[
                           InputRequired(), Length(min=4, max=15)])
    password = PasswordField('Password', validators=[
                             InputRequired(), Length(min=8, max=80)])
    remember = BooleanField('Remember me')


class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[
                           InputRequired(), Length(min=4, max=15)])
    password = PasswordField('Password', validators=[
                             InputRequired(), Length(min=8, max=80)])


class Users(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True)
    password = db.Column(db.String(255))


>>>>>>> master
class Books(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    isbn = db.Column(db.String, nullable=False)
    name = db.Column(db.String, nullable=False)
    author = db.Column(db.String, nullable=False)
    year = db.Column(db.String, nullable=False)

<<<<<<< HEAD
class Users(UserMixin, db.Model):
    _tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[
                           InputRequired(), Length(min=4, max=15)])
    password = PasswordField('Password', validators=[
                             InputRequired(), Length(min=8, max=80)])
    remember = BooleanField('Remember me')
    


class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[
                           InputRequired(), Length(min=4, max=15)])
    password = PasswordField('Password', validators=[
                             InputRequired(), Length(min=8, max=80)])
    error_message = "User already exists"
=======

class BookForm(FlaskForm):
    id = IntegerField("ID", validators=[InputRequired()])
    isbn = StringField('ISBN', validators=[InputRequired()])
    name = StringField('Book Name', validators=[
                       InputRequired()])
    author = StringField('Author Name', validators=[InputRequired()])
    year = StringField('Year Published', validators=[InputRequired()])
>>>>>>> master
