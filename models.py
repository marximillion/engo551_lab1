import os
import csv

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

db = SQLAlchemy()

class Books(db.Model):
    _tablename__ = "books"
    id = db.Column(db.Integer, primary_key=True)
    isbn = db.Column(db.String, nullable=False)
    name = db.Column(db.String, nullable=False)
    author = db.Column(db.String, nullable=False)
    year = db.Column(db.String, nullable=False)

class Users(UserMixin, db.Model):
    _tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False)
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