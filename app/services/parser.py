# app/services/parser.py

from flask import request, Blueprint, url_for, redirect, render_template
from flask_login import login_required, current_user
from ..models import student, course, time, classes
from app import db

bp=Blueprint('parser', __name__)

@bp.route('/parser', methods=['GET','POST'])
@login_required
def parser():
    return render_template('parser.html')

#__________________________________________________________________________

# db inserts need to be done in try except blocks

@bp.route('/parser_check', methods=['POST'])
@login_required
def parser_check():
    
    if request.method=='POST':
        user_id=current_user.get_id()
        theory={}
        lab={}
        theory_timing=[]
        lab_timing=[]
        #--------------------------------------------------------
        # Just clearing out the variables
        theory_start, theory_end = None, None
        lab_start, lab_end = None, None
        day = None
        #--------------------------------------------------------
        raw_text=request.form.get('table')
        rows=raw_text.splitlines()
        for row in rows:
            part=row.split('\t')
            if part[0]=='THEORY' and part[1]=='Start':
                 # ['08:00', '09:00', '10:00', '11:00', '12:00', '-', 'Lunch', '14:00', '15:00', '16:00', '17:00', '18:00', '18:51', '19:01']
                 theory_start=part[2:]

            elif part[0]=='End' and not theory_end:
                 # ['08:50', '09:50', '10:50', '11:50', '12:50', '-', 'Lunch', '14:50', '15:50', '16:50', '17:50', '18:50', '19:00', '19:50']
                 theory_end=part[1:]

            elif part[0]=='LAB' and part[1]=='Start':
                 # ['Start', '08:00', '08:51', '09:51', '10:41', '11:40', '12:31', 'Lunch', '14:00', '14:51', '15:51', '16:41', '17:40', '18:31', '-']
                 lab_start=part[2:]

            elif part[0]=='End' and not lab_end:
                 # ['08:50', '09:40', '10:40', '11:30', '12:30', '13:20', 'Lunch', '14:50', '15:40', '16:40', '17:30', '18:30', '19:20', '-']
                 lab_end=part[1:]

            elif part[0] in ['MON','TUE','WED','THU','FRI','SAT','SUN']:
                 day=part[0]
                 theory[day] = [item for item in part[2:] if item != 'Lunch']
                 # ['A1', 'F1', 'D1', 'TB1', 'TG1', '-', 'Lunch', 'A2-BAEEE101-ETH-PRP105-ALL03', 'F2', 'D2-BACSE103-ETH-PRP105-ALL03', 'TB2-BAMAT101-ETH-PRP105-ALL03', 'TG2-BACHY105-ETH-PRP105-ALL03', '-', 'V3']
                 # ['B1', 'G1', 'E1', 'TC1', 'TAA1', '-', 'Lunch', 'B2-BAMAT101-ETH-PRP105-ALL03', 'G2-BACHY105-ETH-PRP105-ALL03', 'E2', 'TC2', 'TAA2', '-', 'V4']
                 # ['C1', 'A1', 'F1', 'V1', 'V2', '-', 'Lunch', 'C2', 'A2-BAEEE101-ETH-PRP105-ALL03', 'F2', 'TD2-BACSE103-ETH-PRP105-ALL03', 'TBB2', '-', 'V5']
                 # ['D1', 'B1', 'G1', 'TE1', 'TCC1', '-', 'Lunch', 'D2-BACSE103-ETH-PRP105-ALL03', 'B2-BAMAT101-ETH-PRP105-ALL03', 'G2-BACHY105-ETH-PRP105-ALL03', 'TE2', 'TCC2', '-', 'V6']
                 # ['E1', 'C1', 'TA1', 'TF1', 'TD1', '-', 'Lunch', 'E2', 'C2', 'TA2-BAEEE101-ETH-PRP105-ALL03', 'TF2', 'TDD2', '-', 'V7']      
                 # ['V8', 'X11', 'X12', 'Y11', 'Y12', '-', 'Lunch', 'X21', 'Z21', 'Y21', 'W21', 'W22', '-', 'V9']
                 # ['V10', 'Y11', 'Y12', 'X11', 'X12', '-', 'Lunch', 'Y21', 'Z21', 'X21', 'W21', 'W22', '-', 'V11']
                

            elif part[0]=='LAB' and day:
                lab[day] = [item for item in part[1:] if item != 'Lunch']
                 # ['L1', 'L2', 'L3-BAMAT101-ELA-PRP445-ALL03', 'L4-BAMAT101-ELA-PRP445-ALL03', 'L5', 'L6', 'Lunch', 'L31', 'L32', 'L33', 'L34', 'L35', 'L36', '-']
                 # ['L7-BACSE101-LO-PRP117a-ALL03', 'L8-BACSE101-LO-PRP117a-ALL03', 'L9', 'L10', 'L11', 'L12', 'Lunch', 'L37', 'L38', 'L39', 'L40', 'L41', 'L42', '-']
                 # ['L13-BACHY105-ELA-PRPG07-ALL03', 'L14-BACHY105-ELA-PRPG07-ALL03', 'L15-BACSE103-ELA-PRP356-ALL03', 'L16-BACSE103-ELA-PRP356-ALL03', 'L17', 'L18', 'Lunch', 'L43', 'L44', 'L45', 'L46', 'L47', 'L48', '-']
                 # ['L25-BAEEE101-ELA-PRP355-ALL03', 'L26-BAEEE101-ELA-PRP355-ALL03', 'L27-BACSE101-LO-PRP117a-ALL03', 'L28-BACSE101-LO-PRP117a-ALL03', 'L29', 'L30', 'Lunch', 'L55', 'L56', 'L57', 'L58', 'L59', 'L60', '-']
                 # ['L25-BAEEE101-ELA-PRP355-ALL03', 'L26-BAEEE101-ELA-PRP355-ALL03', 'L27-BACSE101-LO-PRP117a-ALL03', 'L28-BACSE101-LO-PRP117a-ALL03', 'L29', 'L30', 'Lunch', 'L55', 'L56', 'L57', 'L58', 'L59', 'L60', '-']
                 # ['L71', 'L72', 'L73', 'L74', 'L75', 'L76', 'Lunch', 'L77', 'L78', 'L79', 'L80', 'L81', 'L82', '-']
                 # ['L83', 'L84', 'L85', 'L86', 'L87', 'L88', 'Lunch', 'L89', 'L90', 'L91', 'L92', 'L93', 'L94', '-']

                 

        time.query.delete()  
        classes.query.delete()
        #
        #
        # Right now all the time and course tables are getting dropped
        # but in the future that would be changed and checks would be placed for
        # edit functionality
        #
        db.session.commit()
        db.session.commit()


        for start, end in zip(theory_start, theory_end): 
          if start not in ['Lunch','-'] and end not in ['Lunch','-']:
              theory_timing.append({'start':start,'end':end})

        for start, end in zip(lab_start, lab_end): 
          if start not in ['Lunch','-'] and end not in ['Lunch','-']:
               lab_timing.append({'start':start,'end':end})

        column_id=0
        for slot in theory_timing:
          db.session.add(time(user_id, column_id, slot['start'], slot['end'], 'ETH'))
          column_id+=1
        db.session.commit()

        column_id=0
        for slot in lab_timing:
          db.session.add(time(user_id, column_id, slot['start'], slot['end'], 'ELA'))
          column_id+=1
        db.session.commit()

#-------------------------------------------------------------------------------------

        for day in theory:
          column_id=0
          for part in theory[day]:
               if part.count('-')>1:
                    parts=part.split('-')
                    db.session.add(classes(user_id, parts[1], parts[2], day, column_id))
               column_id+=1
        db.session.commit()

        for day in lab:
          column_id=0
          for part in lab[day]:
               if part.count('-')>1:  
                    parts=part.split('-')
                    if parts[2]=='LO':
                         db.session.add(classes(user_id, parts[1],'ELA', day, column_id))
                    else:
                         db.session.add(classes(user_id, parts[1], parts[2], day, column_id))
               column_id+=1
        db.session.commit()



        return render_template('redirect_to_schedule.html')

    return redirect(url_for('auth.signin'))