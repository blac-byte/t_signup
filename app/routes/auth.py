# app/routes/auth.py

from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, current_user
from werkzeug.security import generate_password_hash as hash, check_password_hash as hash_check
from ..models import student
from .. import db
import re


bp = Blueprint('auth', __name__)


#___________________________________________________________________________________________

@bp.route("/", methods=["GET", "POST"])
def signup():


##### Maybe add a token system where upon the click of the proceed button
##### an email is sent to the user to verify the user is the owner of the account






    # Checks if the user data is cached or not
    if current_user.is_authenticated:
        return redirect(url_for('parser.parser'))
    
    # only triggers this if after cllicking the PROCEED button
    if request.method=='POST':
        email=request.form.get('email').strip().lower()
        password=request.form.get('password')
        
        # Here we are using re module to check the password format
        # to verify the email is valid
        pattern = r'^[a-zA-Z]+\.[a-zA-Z]+\d{4}@vitstudent\.ac\.in$'
        if re.match(pattern, email):

            # checks for existing email, if not triggers else clause
            if student.query.filter_by(email=email).first():
                return 'already acc'
            else:  
                hash_password=hash(password, method='pbkdf2:sha256')
                user=student(email=email,password=hash_password)
                db.session.add(user)
                db.session.commit()
                login_user(user)
                return redirect(url_for('parser.parser'))
        else:
            return 'Not a valid email'#---------------add flash here
    return render_template('auth/signup.html')


#__________________________________________________________________________________________

@bp.route('/signin',methods=['POST','GET'])          
def signin():
    
    if request.method=='POST':

        # If the user data is cached in the browser auto logs the user in
        if current_user.is_authenticated:
             return redirect(url_for('parser.parser'))
        
        # If not cached
        email=request.form.get('email').strip().lower()
        password=request.form.get('password')
        user=student.query.filter_by(email=email).first()

        # Authentication of user happens here with user and hashed password
        if user and hash_check(user.password,password):
            login_user(user)
            return redirect(url_for('parser.parser'))
        
        # If invalid gets redirected to the same page
        else:
            return redirect(url_for('auth.signin'))#---------------add flash here 
        
    # returns to sign page if you try to access this route in not POST method
    return render_template('auth/signin.html')






