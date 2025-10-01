# app/services/schedule.py

from app import db
from flask import Blueprint, redirect, session
from flask_login import current_user, login_required
from ..models import student, classes, time
from sqlalchemy.orm import aliased
from sqlalchemy import and_
from datetime import date



bp=Blueprint('schedule', __name__)

@bp.route('/schedule', methods=['POST'])
@login_required
def schedule():
    user_id=current_user.get_id()
    today = date.today()
    abbreviated_day_name = today.strftime("%a").upper()


    time_alias = aliased(time)

    # queries the db using the system date, probably change to a more accurate system later
    results = (
        db.session.query(time_alias.start, time_alias.end, classes.course_id)
        .select_from(student)
        .join(classes, student.reg_id == classes.reg_id)
        .join(time_alias, and_(
            time_alias.column_id == classes.column_id,
            time_alias.course_type == classes.course_type
        ))
        .filter(
            classes.day == abbreviated_day_name,
            student.reg_id == int(user_id)
        )
        .all()
    )

    # storing the query in session
    session['schedule']=results

    return redirect('dashboard.dashboard')