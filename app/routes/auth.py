from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, current_user
from werkzeug.security import generate_password_hash as hash, check_password_hash as hash_check
from ..models import student
from .. import db

bp = Blueprint('auth', __name__)


#___________________________________________________________________________________________

@bp.route("/", methods=["GET", "POST"])
def signup():
    if request.method=='POST':
        email=request.form.get('email').strip().lower()
        password=request.form.get('password')
        hash_password=hash(password)
        user=student.query.filter_by(email=email).first()
        if user:  #----------------------------------- checks for existing email in db
            if user.password is None: #--------------- checks for existing email in db with no password
                user.password=hash_password
                db.session.commit()
                login_user(user)
                return redirect(url_for('dashboard'))
            else:
                return '<h1>Acc already exists<h1>'
        else:
            return '<h1>No acc<h1>'

    return render_template('auth/signup.html')



@bp.route("/signup_check", methods=["GET", "POST"])
def signup_check():
        if request.method=='POST':
            email=request.form.get('email').strip().lower()
            password=request.form.get('password')
            hash_password=hash(password)
            user=student.query.filter_by(email=email).first()
            if user:  #----------------------------------- checks for existing email in db with no password
                if user.password is None: #--------------- checks if account has been initialized
                    user.password=hash_password
                    db.session.commit()
                    login_user(user)
                    return redirect(url_for('services.parser'))
                else:
                    return '<h1>Acc already exists<h1>'
            else:
              return '<h1>No acc<h1>'
        else:
              return redirect(url_for('index'))

#__________________________________________________________________________________________

@bp.route('/signin',methods=['POST','GET'])          
def signin():
        return render_template('auth/signin.html')



@bp.route('/signin_check',methods=['POST'])          
def signin_check():
    if request.method=='POST':
        if current_user.is_authenticated:
             return redirect(url_for('services.parser'))
        email=request.form.get('email').strip().lower()
        password=request.form.get('password')
        user=student.query.filter_by(email=email).first()
        if user and hash_check(user.password,password):
            login_user(user)
            return redirect(url_for('services.parser'))
        else:
            return redirect(url_for('auth.signin'))
    else:
        return redirect(url_for('auth.signin'))