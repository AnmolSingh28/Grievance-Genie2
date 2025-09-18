from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from notify import Notify
from preprocess import Cleaning_complaint_text
import pandas as pd
import random
from classify_assign import classify_and_assign
from anony_util import anonymize_data_of_complaint
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///grievance_genie.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)
import os
from dotenv import load_dotenv
load_dotenv()

TWILIO_ACCOUNT_SID=os.getenv("TWILIO_SID")
TWILIO_AUTH_TOKEN=os.getenv("TWILIO_TOKEN")
TWILIO_FROM_NUMBER=os.getenv("TWILIO_NUMBER")

notifier = Notify(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_FROM_NUMBER)
class Complaints(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    complainer_name=db.Column(db.String(40))
    placeofissue=db.Column(db.String(30))
    complainer_phonenum=db.Column(db.String(12))
    category=db.Column(db.String(30))
    complaint_detail=db.Column(db.String(100))
    department=db.Column(db.String(25))
    status=db.Column(db.String(30),default="Issue Submitted Successfully")
    priority=db.Column(db.String(20))
with app.app_context():
    db.create_all()
    
@app.route("/", methods=["GET", "POST"])
def submit_complaint():
    message=None
    real_complaints=Complaints.query.order_by(Complaints.id.desc()).all()
    complaints=[]
    for rc in real_complaints:
        anon = anonymize_data_of_complaint(rc)
        complaints.append({
            "id": rc.id,
            "complainer_name":anon["complainer_name"],
            "placeofissue":anon["placeofissue"],
            "complainer_phonenum":anon["complainer_phonenum"],
            "category":rc.category,
            "complaint_detail":rc.complaint_detail,
            "department":rc.department,
            "status":rc.status,
            "priority":rc.priority
        })
    if request.method=="POST":
        complainer_name=request.form.get("complainer_name")
        placeofissue=request.form.get("placeofissue"," ")
        complainer_phonenum=request.form.get("complainer_phonenum")
        raw_complaint_text=request.form.get("complaint_detail")

        if not complainer_name or not complainer_phonenum or not raw_complaint_text:
            message="Please fill all the important fields for good issue solving"
            return render_template("index.html",message=message,complaints=complaints)
        cleaned_text=Cleaning_complaint_text(raw_complaint_text)
        if not cleaned_text:
            message="Please enter a complaint which is correct"
            return render_template("index.html",message=message,complaints=complaints)

        category,department=classify_and_assign(cleaned_text)
        priority="Low"
        complaint=Complaints(
            complainer_name=complainer_name,
            placeofissue=placeofissue,
            complainer_phonenum=complainer_phonenum,
            department=department,
            complaint_detail=cleaned_text,
            category=category,
            priority=priority,
            status="Registered",
        )
    
        db.session.add(complaint)
        db.session.commit()
        real_complaints = Complaints.query.order_by(Complaints.id.desc()).all()
        complaints = []
        for rc in real_complaints:
            anon=anonymize_data_of_complaint(rc)
            complaints.append({
                "id":rc.id,
                "complainer_name": anon["complainer_name"],
                "placeofissue": anon["placeofissue"],
                "complainer_phonenum": anon["complainer_phonenum"],
                "category":rc.category,
                "complaint_detail":rc.complaint_detail,
                "department":rc.department,
                "status":rc.status,
                "priority":rc.priority
            })
        def format_phone_number(number):
            number = number.strip()
            if not number.startswith("+"):
                number = "+91" + number.lstrip("0")
            return number

        to_number = format_phone_number(complainer_phonenum)
        sms_message = (
            f"Dear {complainer_name}, your complaint ('{category}') has successfully been registered on Grievance Genie."
            f"The {department} department will update you regarding the issue that you filled. Thank you!"
        )
        notify_result=notifier.send_sms(to_number,sms_message)
        #print(f"Twilio Notify:{notify_result}")
        message=f"Complaint registered successfully! Category: {category}, Department: {department}"

    return render_template("index.html",complaints=complaints,message=message)

@app.route("/export_anonymized")
def export_anonymized():
    complaints=Complaints.query.all()
    anonymized=[anonymize_data_of_complaint(c) for c in complaints]
    df=pd.DataFrame(anonymized)
    df.to_csv("anonymized_complaints.csv",index=False)
if __name__ == "__main__":
    app.run(debug=True)
