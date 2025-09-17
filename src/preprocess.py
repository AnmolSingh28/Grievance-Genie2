def Cleaning_complaint_text(text):
    if not text or not text.strip():
        return "No complaint is provided for now"
    cleaned_text=text.strip()
    cleaned_text=cleaned_text.lower()
    cleaned_text=' '.join(cleaned_text.split())
    replacements={
        'light gone':'electricity issue',
        'light not coming':'electricity issue',
        'no light':'electricity issue',
        'line gone':'electricity issue',
        'chamber issue':'sewage issue',
    }
    for new,old in replacements.items():
        cleaned_text=cleaned_text.replace(new,old)
    return cleaned_text