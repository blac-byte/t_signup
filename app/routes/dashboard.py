# routes/dashboard.py

from flask import render_template, Blueprint, session
from flask_login import login_required

bp=Blueprint('dashboard', __name__)

@bp.route('/dashboard', methods=['GET','POST'])
@login_required
def dashboard():
    schedule = session.get('schedule')
    return render_template('dashboard.html', schedule)