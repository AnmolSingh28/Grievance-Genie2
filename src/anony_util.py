import random
def anonymize_data_of_complaint(complaint):
    dummy_phone_numbers=["0000000010","1010101110"]
    dummy_names=["Complainer1","Complainer2","Complainer3","Complainer4"]
    dummy_areas=["Area1","Area2","Area3","Area4","Area5","Area6"]
    return{
        "complainer_name":random.choice(dummy_names),
        "placeofissue":random.choice(dummy_areas),
        "complainer_phonenum":random.choice(dummy_phone_numbers),
        "category":complaint.category,
        "complaint_detail":complaint.complaint_detail,
        "department":complaint.department,
        "status":complaint.status,
        "priority":complaint.priority
    }