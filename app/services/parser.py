# app/services/parser.py

from flask import request, Blueprint, url_for, redirect, render_template
from flask_login import login_required
from ..models import student, course, time
from app import db

bp=Blueprint('services', __name__)

@bp.route('/parser', methods=['GET','POST'])
@login_required
def parser():
    return render_template('parser.html')

#__________________________________________________________________________

@bp.route('/parser_check', methods=['POST'])
@login_required
def parser_check():
    if request.method=='POST':
        theory={}
        lab={}
        theory_timing=[]
        lab_timing=[]
        theory_start, theory_end = None, None
        lab_start, lab_end = None, None
        day = None
        raw_text=request.form.get('table')
        rows=raw_text.splitlines()
        for row in rows:
            part=row.split('\t')
            if part[0]=='THEORY' and part[1]=='Start':
                 theory_start=part[2:]
            elif part[0]=='End' and not theory_end:
                 theory_end=part[1:]
            elif part[0]=='LAB' and part[1]=='Start':
                 lab_start=part[2:]
            elif part[0]=='End' and not lab_end:
                 lab_end=part[1:]
            elif part[0] in ['MON','TUE','WED','THU','FRI','SAT','SUN']:
                 day=part[0]
                 theory[day]=part[2:]
            elif part[0]=='LAB' and day:
                 lab[day]=part[1:]

        time.query.delete()  
        course.query.delete()
        #
        #
        # Right now all the tables are just for one person.
        # In the future it would be that each user has their own set of tables for slots, courses, days
        #
        #
        db.session.commit()
        db.session.commit()


        for start, end in zip(theory_start, theory_end): 
             if start not in ['Lunch','-'] and end not in ['Lunch','-']:
                  theory_timing.append({'start':start,'end':end})

        for start, end in zip(lab_start, lab_end): 
             if start not in ['Lunch','-'] and end not in ['Lunch','-']:
                  lab_timing.append({'start':start,'end':end})

        for slot in theory_timing:
            db.session.add(time(slot['start'], slot['end'], 'Theory'))
        db.session.commit()

        for slot in lab_timing:
            db.session.add(time(slot['start'], slot['end'], 'Lab'))
        db.session.commit()

        for day in theory:
            for part in theory[day]:
                if part.count('-')>1:
                     parts=part.split('-')
                     db.session.add(course(parts[0],parts[1],parts[2],parts[3],parts[4]))
        db.session.commit()

        for day in lab:
            for part in lab[day]:
                if part.count('-')>1:
                     parts=part.split('-')
                     db.session.add(course(parts[0],parts[1],parts[2],parts[3],parts[4]))
        db.session.commit()



        return redirect(url_for('services.parser'))

    return redirect(url_for('auth.signin'))