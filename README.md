Grievance Genie 

Grievance Genie is a smart municipal complaint management system that helps citizens easily raise complaints about civic issues and automatically routes them to the correct department using AI.

--->Features<---

1) Citizens can register complaints online using a simple form.

2) AI-powered text classification automatically assigns complaint categories.

3) Complaints are routed to the correct department (Water, Electricity, Sanitation, etc.).

4) Transparent tracking with a list of all registered complaints.

5) Clean and simple UI with a green civic-themed design.

--->Tech Stack<---

1) Backend: Python, Flask

2) AI/ML: Hugging Face Transformers (zero-shot classification using facebook/bart-large-mnli)

3) Database: SQLite

4) Frontend: HTML, CSS

5) Version Control: Git + GitHub

--->Fallback Note<---

Originally, the project was supposed to integrate with IBM Watson Orchestrate for workflow automation. But due to some issues (unauthorized errors for backend integration), we implemented a local ML pipeline with Hugging Face to ensure the project runs smoothly during the hackathon.

--->Project Structure<---
Grievance-Genie/
│-- src/                 Flask backend and ML pipeline
│-- templates/           HTML frontend files
│-- static/              CSS and other assets
│-- notebooks/           Testing notebooks for ML pipeline
│-- secrets.env          Environment variables (NOT pushed to GitHub)
│-- requirements.txt     Python dependencies
│-- README.md            Project documentation

--->Installation and Setup<---

1) Clone the repository

git clone https://github.com/your-username/Grievance-Genie.git
cd Grievance-Genie


2) Create a virtual environment

python -m venv venv
source venv/bin/activate   # For Linux/Mac
venv\Scripts\activate      # For Windows

3) Install dependencies

pip install -r requirements.txt

4) Run the Flask app

flask run

5) Visit http://127.0.0.1:5000/ in your browser.

--->Usage<---

1) Open the app in your browser.

2) Fill in your name, phone, locality, and complaint details.

3) Submit the complaint — AI will classify the issue and assign it to the right department.

4) Scroll down to view all Registered Complaints in a table format.

--->License<---

This project is developed for hackathon purposes and is open for educational use.
   
