import os
import requests
import urllib.parse

from flask import redirect, render_template, request, session
from functools import wraps
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField
from wtforms.validators import DataRequired, Length
  
  
def lookup(post_code):
    try:
        
        url = f"https://findthatpostcode.uk/postcodes/{post_code}"
        response = requests.get(url)
        response.raise_for_status()

    except requests.RequestException:
        return "1st try"
  
    try:
        data = response.json()
        y = data['data']['attributes']['long']
        x = data['data']['attributes']['lat']
        return x, y
    except (KeyError, TypeError, ValueError):
        return "2nd try"




class emailForm(FlaskForm):
    name = StringField('name', validators=[DataRequired(), Length(max=50)])
    number = StringField('phone number', validators=[DataRequired(), Length(max=13)])
    email = StringField('email', validators=[DataRequired(), Length(max=50)])
    message = TextAreaField('message', validators=[DataRequired()])

