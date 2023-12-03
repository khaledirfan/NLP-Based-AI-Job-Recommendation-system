import streamlit as st
import fitz  # PyMuPDF
import string
from io import BytesIO
import pickle
with open('le.pkl' , 'rb') as f:
    le = pickle.load(f)
with open('ML_model.pkl' , 'rb') as f:
    ml_model = pickle.load(f)
with open('scaler.pkl' , 'rb') as f:
    scaler = pickle.load(f)
from collections import Counter

# Load your skills list
skills = ["artificial intelligence", "python", "sql", "aws", "data analysis", "communication", "financial analysis",
          # ... (your other skills)
          "fitness", "health and wellness", "flexibility training"]

# Function to extract text from PDF and create a binary array for each skill
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

    # Create binary array for each skill
    binary_array = []

    # Check presence of each skill in the CV text
    for skill in skills:
        skill_present = 1 if skill in cv_text else 0
        binary_array.append(skill_present)

    return binary_array

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
if work_type == "Onsite":
  work_type = 1
elif work_type == "Remote":
  work_type = 2
else:
  work_type = 0
work_type = 1 if work_type in cv_text else 0

# Prediction Button
predict_button = st.button("Display Skill Counts and Predict Job Type")

# Display result when button is clicked
if uploaded_file is not None and work_type and predict_button:
    # Get the binary array indicating presence of each skill in the CV
    binary_array = process_cv(uploaded_file, skills)

    # Display binary array
    st.subheader("Binary Array for Skill Presence:")
    for skill, is_present in zip(skills, binary_array):
        st.write(f"{skill}: {is_present}")

    # Generate predictions based on the binary array (you can customize this part based on your model)
    predicted_job_type = "Software Developer"  # Replace with your actual prediction logic

    # Display the predicted job type
    st.subheader("Predicted Job Type:")

    input1 = []
    input1.append(work_type)
    input1.extend(binary_array)
    input_data = [input1]

    normalized_data = scaler.transform(input_data)

    # Make predictions using the normalized data
    prediction = ml_model.predict(normalized_data)


    st.write(prediction)
