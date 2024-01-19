import streamlit as st
import numpy as np
import fitz  # PyMuPDF
import string
from io import BytesIO
import pickle
with open('skills.txt', 'r') as file:
    skills_text = file.read()
with open('le.pkl' , 'rb') as f:
    le = pickle.load(f)
with open('ML_model.pkl' , 'rb') as f:
    ml_model = pickle.load(f)
from collections import Counter

# Load skills list
skills = skills_text.split('\n')
skills.pop()

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
# st.write(skills)
# File Upload
uploaded_file = st.file_uploader("Upload PDF CV:", type=['pdf'])

# Work Type Dropdown
work_type = st.selectbox("Select Work Type:", ["On-site", "Remote", "Hybrid"])

# Prediction Button
predict_button = st.button("Predict Job Type")

# Display result when button is clicked
if uploaded_file is not None and work_type and predict_button:
    # Get the binary array indicating presence of each skill in the CV
    binary_array = process_cv(uploaded_file, skills)

    # Display binary array
    #st.subheader("Binary Array for Skill Presence:")
    #for skill, is_present in zip(skills, binary_array):
    #    st.write(f"{skill}: {is_present}")

    # Display the predicted job type
    st.subheader("Predicted Job Types:")

    input1 = []
    work_type_arr = [work_type]
    work_type_arr = le.transform(work_type_arr)
    work_type_val = work_type_arr[0]

    input1.append(work_type_val)
    input1.extend(binary_array)
    input_data = [input1]

    predictions = ml_model.predict_proba(input_data)

    # Get the indices of the top three classes for each prediction
    top_three_classes = np.argsort(predictions)[:, -3:][0][::-1]
    top_three_probabilities = np.sort(predictions)[:, -3:][0][::-1]
    # st.write(top_three_classes)

    # Get the actual class labels
    class_labels = ml_model.classes_
    # st.write(class_labels)

    predicted_classes = class_labels[top_three_classes]

    # Display the three most probable classes for each prediction
    for i, prediction in enumerate(predicted_classes):
        st.markdown(f"Prediction {i + 1}: {prediction}, Probability: {top_three_probabilities[i]:.4f}")
        # st.markdown(f"Prediction {i + 1}: {prediction}")