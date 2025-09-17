from transformers import pipeline
classifier = pipeline(
    "zero-shot-classification",model="facebook/bart-large-mnli" 
)

COMPLAINT_CATEGORIES=["Water Issue","Electricity Issue","Public Health","Sanitation","Road and Traffic","Environmental issues","Civic issues"]

def classify_and_assign(complaint_text):
    result=classifier(
        complaint_text,
        candidate_labels=COMPLAINT_CATEGORIES,
        multi_label=False
    )
    category=result['labels'][0]
    department_map = {
        "Water Issue":"Jal Board",
        "Electricity Issue":"State Electricity Board",
        "Public Health":"Public Health Department",
        "Sanitation":"Sanitation Department",
        "Road and Traffic":"Public Works Department",
        "Environmental issues":"Municipal Green Cell",
        "Civic issues":"General Municipal Department"
    }
    department=department_map.get(category,"General Municipal Department")
    return category,department
