import streamlit as st
import fitz  # PyMuPDF
import string
from io import BytesIO
from collections import Counter

# Load your skills list
skills = ["artificial intelligence","javascript","python", "sql", "aws", "data analysis", "communication", "financial analysis", "recruiting",
    "training", "performance management", "advertising", "tableau", "marketing", "excel",
    "sales", "digital marketing", "css", "project management", "html", "writing",
    "content creation", "sem", "social media", "javascript", "erp", "critical thinking",
    "analytics", "crm", "research", "seo", "design", "artificial intelligence",
    "machine learning", "compliance", "accounting", "forecasting", "leadership",
    "audit", "risk management", "legal", "budgeting", "databases", "teamwork", "java",
    "linux", "windows", "network security", "agile", "scrum", "spring", "hibernate",
    "supply chain", "logistics", "operations management", "negotiation", "cisco",
    "quality assurance", "human resources", "business development", "c++", "git",
    "data science", "big data", "deep learning", "r", "hadoop", "spark", "etl",
    "data warehousing", "mysql", "sql server", "docker", "kubernetes", "ci/cd",
    "jenkins", "electrical engineering", "autocad", "matlab", "power systems", "circuit design",
    "organizational skills", "administrative skills", "microsoft office", "react", "angular",
    "web development", "ux/ui design", "safety", "compliance", "auditing", "environmental health",
    "process improvement", "lean manufacturing", "six sigma", "interior design", "3d modeling",
    "photoshop", "financial analysis", "investment strategies", "economics", "troubleshooting",
    "itil", "hardware support", "laboratory skills", "quality control", "chemistry", "biology",
    "instrumentation", "legal research", "transportation management", "planning", "pharmaceutical industry",
    "medical knowledge", "patient care", "healthcare", "time management", "organization",
    "legal documentation", "prototyping", "product development", "creativity", "technical documentation",
    "graphic design", "user research", "fabrication", "metalworking", "blueprint reading",
    "mig/tig welding", "yoga teaching", "fitness", "health and wellness", "flexibility training"
]


# Function to extract text from PDF and count occurrences of each skill
def process_cv(pdf_file, skills):
    # Read the content of the PDF
    def extract_text_from_pdf(pdf_file):
        pdf_bytes = pdf_file.read()
        pdf_stream = BytesIO(pdf_bytes)
        doc = fitz.open(stream=pdf_stream, filetype="pdf")
        text = ""
        for page_num in range(doc.page_count):
            page = doc[page_num]
            text += page.get_text()
        return text

    cv_text = extract_text_from_pdf(pdf_file)

    # Preprocess the text (convert to lowercase)
    cv_text = cv_text.lower().translate(str.maketrans('', '', string.punctuation))

    # Create Counter for skills occurrences
    skills_counter = Counter()

    # Count occurrences of each skill in the CV text
    for skill in skills:
        skill_occurrences = cv_text.count(skill)
        skills_counter[skill] = skill_occurrences

    return skills_counter

# Set Streamlit app title and page layout
st.set_page_config(
    page_title="Job Recommendation System",
    page_icon=":chart_with_upwards_trend:",
    layout="wide"
)

# Set Streamlit app theme
st.markdown(
    """
    <style>
    body {
        background: linear-gradient(to right, #232526, #414345);
        color: #F8F9FA;
    }
    .stApp {
        text-align: center;
        margin-top: 50px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Main title and description
st.title("Job Recommendation System")
st.markdown("Welcome to the Job Recommendation System! Upload your CV and select work type to get job recommendations.")

# File Upload
uploaded_file = st.file_uploader("Upload PDF CV:", type=['pdf'])

# Work Type Dropdown
work_type = st.selectbox("Select Work Type:", ["Onsite", "Remote", "Hybrid"])

# Prediction Button
predict_button = st.button("Display Skill Counts and Predict Job Type")

# Display result when button is clicked
if uploaded_file is not None and work_type and predict_button:
    # Count occurrences of each skill in the CV
    skill_counts = process_cv(uploaded_file, skills)

    # Display skill counts greater than or equal to one
    st.subheader("Skill Counts in CV:")
    for skill, count in skill_counts.items():
        if count >= 1:
            st.write(f"{skill}: {count}")

    # Generate predictions based on skill counts (you can customize this part based on your model)
    predicted_job_type = "Software Developer"  # Replace with your actual prediction logic

    # Display the predicted job type
    st.subheader("Predicted Job Type:")
    st.write(predicted_job_type)