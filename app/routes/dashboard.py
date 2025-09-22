# routes/dashboard.py

from flask import render_template, Blueprint
from flask_login import login_required

bp=Blueprint('dashboard', __name__)

@bp.route('/dashboard', methods=['GET','POST'])
@login_required
def dashboard():
    return render_template('dashboard.html')