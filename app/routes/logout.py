from flask import flash, redirect, url_for, Blueprint
from flask_login import login_required, logout_user

bp=Blueprint('logout', __name__)


@bp.route('/logout', methods=['GET','POST'])
@login_required
def logout():
        logout_user()
        flash("You have been logged out successfully!", "info")
        return redirect(url_for('signin'))