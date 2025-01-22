#Import Necessary Libraries for EduAssistant
#streamlit for its ability to make web-based applications without HTML or Java
import streamlit as st
#Interacts with operating system
import os
os.system("pip install openai")
#Allows us to interact with the ChatGPT OpenAI's API
import openai

# Initialize OpenAI client, use os to retrieve API key
#Using an environmentala variable rather than hardcoding into script
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

# Function to create a lesson plan using AI
#This function takes in a prompt and returns lesson plan using 5 input parameters
#The string will describe the prompt for OpenAI in an f string
def create_lesson_plan(time, grade, environment, confidence, topic):
    prompt = f"""
    Create a lesson plan with these details:
    - Time Available: {time}
    - Grade Level: {grade}
    - Learning Environment: {environment}
    - Teacher's confidence in hands-on projects: {confidence}
    - Topic of teacher's lesson plans: {topic}

    Include:
    1. Learning Objectives
    2. Materials Needed
    3. Step-by-Step Activities
    4. Closure Activity

    Make it one to two pages and easy to follow.
    """
#Defining try-except for exception handling while communicating with OpenAI API
    #Define parameters of model and how the systerm and user will interact
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            #Define whose speaking and instructions for the assistant
            messages=[
                {"role": "system", "content": "You are a helpful teacher education assistant who creates clear, practical lesson plans."},
                {"role": "user", "content": prompt}
            ]
        )
    #Return the response from OpenAI API
        return response.choices[0].message.content
    except Exception as e:
        return f"Sorry, there was an error: {str(e)}"
    

# Function to create an assessment using AI
#This function will be very similar to the one we used for the lesson plan, however they have different parameters
#These parameters will be used as arguments and fed as a prompt to OpenAI
def create_assessment(grade, lesson_plan, topic):
    prompt = f"""
    Create a simple assessment for:
    Grade Level: {grade}

    Based on this lesson plan:
    {lesson_plan}

    Based on this topic:
    {topic}

    Include:
    1. 2-3 multiple choice questions
    2. 1-2 short answer questions
    3. A simple rubric for grading

    Make it student-friendly and aligned with the lesson objectives.
    """

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful teacher education assistant who creates clear, effective assessments."},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Sorry, there was an error: {str(e)}"


#Here is where streamlit steps in, setting up the page configuration

# Set up page configuration
st.set_page_config(page_title="Educator Interview Assistant", layout="wide")

# Main Page and Intro
st.title('Educator Interview Assistant')
st.write('Welcome! Please answer these questions to generate your custom lesson plan.')

#Looking for our environment variable
# Check for API key, create error message if none there
if not os.getenv('OPENAI_API_KEY'):
    st.error('Please add your OpenAI API key to Replit secrets!')
    st.stop()

# Create the AI assisted questionaire using .form also allows us to add cool and interactive widgets within the form
with st.form("teacher_form"):
    # Questions
    time = st.text_input("How much time do you have for this activity?", 
                        placeholder="e.g., 45 minutes")

    grade = st.text_input("What grade(s) or age group(s) are your learners?",
                         placeholder="e.g., 5th grade")

    environment = st.text_input("What is the learning environment?",
                              placeholder="e.g., classroom, library, after-school")
#The slider is one of the most useful widgets in streamlit, it allows us to create a slider that allows us to select a value between defined options
    confidence = st.select_slider(
        "How confident are you in using hands-on projects?",
        options=["Not confident", "Somewhat confident", "Very confident"]
    )
    topic = st.text_input("What is the topic of your lesson plan?",
                          placeholder="e.g., math, science, history")

    want_assessment = st.checkbox("Do you want to include an assessment?")

    # Submit button used in streamlit to show when user is done with the form, also can be labeled. Triggers our lesson plan and assesment generation
    submitted = st.form_submit_button("Create My Lesson Plan")

# Handling form submission
if submitted:
    # Create columns for better layout of our responses
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Your Responses")
        st.write(f"**Time Available:** {time}")
        st.write(f"**Grade Level:** {grade}")
        st.write(f"**Learning Environment:** {environment}")
        st.write(f"**Confidence Level:** {confidence}")
        st.write(f"**Topic:** {topic}")

    # Create lesson plan
    with st.spinner('Generating your custom lesson plan...'):
        lesson_plan = create_lesson_plan(time, grade, environment, confidence, topic)
        st.subheader("Your Lesson Plan")
        st.write(lesson_plan)

    # Create assessment if requested
    if want_assessment:
        with st.spinner('Creating your assessment...'):
            assessment = create_assessment(grade, lesson_plan, topic)
            st.subheader("Your Assessment")
         
