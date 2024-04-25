import os
import sys
from flask import Blueprint ,request, jsonify
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from DB import Attendance

attendance = Blueprint('attendance', __name__)

@attendance.route('/take')
def take():
    data=request.json
    conditions=("div" in data and "period" in data and "subject" in data and "present" in data and "absent" in data and "user_id" in data)
    if(conditions):
        attendance=Attendance(div=data['div'],period=data['period'],subject=data['subject'],present=data["present"],absent=data["absent"],user_id=data["user_id"])
        attendance.save()
        return jsonify({"success":True,"message": "attendance take successfully"})
    else:
        return jsonify({"success":False,"message":"Incompolete Data"})

