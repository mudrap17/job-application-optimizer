import pandas as pd
import numpy as np
import streamlit as st
from streamlit_option_menu import option_menu
from PyPDF2 import PdfReader
from resume_optimizer import (
    llm_result,
    linkedin_jobs,
    cold_outreach,
    suggestions,
    sample_resume,
    project_suggestions_job,
    project_suggestions_skill,
    roadmap,
    interview,
)

# Sidebar section
with st.sidebar:
    st.subheader("Enter the information to proceed")
    key = st.text_input(label="Your Gemini API key", type="password")
    st.subheader("Choose your task:")
    option = option_menu(
        menu_title="",
        options=[
            "Resume Optimizer",
            "Sample resume",
            "Cover letter",
            "Job Industry Analysis",
            "LinkedIn Jobs",
            "Cold outreach Assist",
            "Project Suggestions",
            "Roadmap to skills",
            "Interview prep",
        ],
        icons=[
            "house-fill",
            "file-text-fill",
            "pencil-square",
            "bar-chart-fill",
            "linkedin",
            "chat-right-text-fill",
            "rocket",
            "map-fill",
            "person-check",
        ],
    )

if option == "Resume Optimizer" or option == "Cover letter":
    if option == "Resume Optimizer":
        prompt = """optimize the resume to include keywords from the job description,Using practical language, 
        write three to five resume achievements based on my work experience. 
        Add details about quantitative results and impact instead of listing responsibilities to support the relevant experience
        and evidence to show you the perfect fit for the job."""
        st.title("AI powered Resume optimization")
        st.write(
            "Use this tool to optimize your resume according to the job description"
        )
    else:
        prompt = """Using practical language, write a conversational, persuasive cover letter 
        to include relevant keywords from the job descriptions 
        and highlight the appropriate experience from the resume with required details to make you the perfect fit for the job. 
        The cover letter should highlight skills beyond those mentioned in the resume."""
        st.title("AI powered Cover Letter optimization")
        st.write(
            "Use this tool to optimize your cover letter according to the job description"
        )

    job_desc = st.text_input(label="Enter the job description:")

    # file upload
    pdf = st.file_uploader(label="Upload your resume:", type="pdf")
    resume_optimize = ""
    cover_letter = ""
    if option == "Resume Optimizer":
        resume_optimize = st.button(label="Optimize my resume")
    else:
        cover_letter = st.button(label="Write an amazing cover letter")
    if key is None:
        st.info("Enter your Gemini API key on your left please")
    try:
        if pdf is not None:
            pdf_reader = PdfReader(pdf)

            # extract text from each page separately
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text()
            if resume_optimize is not None or cover_letter is not None:
                if key is None:
                    st.info("Enter your Gemini API key on your left please")
                else:
                    with st.spinner("Wait for it..."):
                        result = llm_result(job_desc, text, prompt, key)
                    st.write(result)

    except Exception as e:
        st.warning(e)

if option == "Sample resume":
    st.title("Give a sample resume that is ideal for the given job description")
    job_desc = st.text_input(label="Enter the job description:")
    if key is None:
        st.info("Enter your Gemini API key on your left please")
    else:
        resume = sample_resume(job_desc, key)
        st.write(resume)


if option == "Job Industry Analysis":
    st.title("Job Industry Analysis")
    st.subheader(
        "Explore the industry and prominent states according to 2023 H1B approvals"
    )
    with st.spinner("Wait for it..."):
        df = pd.read_excel("EmployerInformation.xlsx", engine="openpyxl")
    df = df[
        [
            "Employer (Petitioner) Name",
            "Industry (NAICS) Code",
            "Initial Approval",
            "Petitioner State",
        ]
    ]
    option = st.selectbox(
        "Select an industry",
        df["Industry (NAICS) Code"].unique(),
        index=None,
        placeholder="Select your industry",
    )

    if option:
        cf = df[(df["Industry (NAICS) Code"] == option) & (df["Initial Approval"] > 0)]
        st.info(
            "Hover over this table to download, search or expand. Find the top 5 states data below the table.",
            icon="ℹ️",
        )
        st.write(
            cf[
                [
                    "Employer (Petitioner) Name",
                    "Initial Approval",
                    "Petitioner State",
                ]
            ]
        )
        df1 = (
            cf["Petitioner State"]
            .value_counts()
            .rename_axis("States")
            .reset_index(name="Approval counts")
        )
        st.write("Top 5 states by approvals in this Industry")
        st.bar_chart(df1[:5], x="States", y="Approval counts", color="#00ff11")


if option == "LinkedIn Jobs":
    st.title("LinkedIn jobs based on your resume")
    if key is None:
        st.info("Enter your Gemini API key on your left please")
    pdf = st.file_uploader(label="Upload your resume:", type="pdf")
    search_jobs = st.button("Search for jobs")

    try:
        if pdf is not None and key is not None:
            pdf_reader = PdfReader(pdf)

            # extract text from each page separately
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text()
            if search_jobs:
                result = linkedin_jobs(text, key)
                st.write(result)

    except Exception as e:
        st.warning(e)

if option == "Cold outreach Assist":
    st.title("Cold Outreach Assist")
    st.write("Use AI to help you write better cold outreach messages")
    person = st.text_input(label="Whom are you reaching out to?")
    purpose = st.text_input(label="What would you like to talk about?")
    tab1, tab2 = st.tabs(["Draft first message", "Get suggestions"])
    if key is None:
        st.info("Enter your Gemini API key on your left please")
    else:
        with tab1:
            st.title("Write a cold outreach message")
            cm = st.button("Sample cold message")
            if cm:
                result = cold_outreach(purpose, person, key)
                st.write(result)

        with tab2:
            st.title("Give suggestions to improve")
            text = st.text_input("What did you have in mind?")
            sug = st.button("Rewrite mine")
            if sug:
                result = suggestions(text, person, key)
                st.write(result)

if option == "Project Suggestions":
    st.title("Project Suggestions")
    st.write(
        "Get suggestions for projects including the requested skills and/or domain"
    )
    tab1, tab2 = st.tabs(
        ["Related to given job description", "According to skills/domain "]
    )
    if key is None:
        st.info("Enter your Gemini API key on your left please")
    else:
        with tab1:
            job_desc = st.text_input(label="Give job description")
            project = project_suggestions_job(job_desc, key)
            st.write(project)
        with tab2:
            skills = st.text_input(label="Give list of skills")
            domain = st.text_input(label="Give the domain name(sustainability,finance)")
            project = project_suggestions_skill(skills, domain, key)
            st.write(project)

if option == "Roadmap to skills":
    st.title("Roadmap to a skill of your choice")
    skill = st.text_input("Give the skill name:")
    if key is None:
        st.info("Enter your Gemini API key on your left please")
    else:
        roadmap_skill = roadmap(skill, key)
        st.write(roadmap_skill)

if option == "Networking events search":
    st.title("Networking event")
    st.write("Get a list of networking events for given domain and dates")

if option == "Interview prep":
    st.title("Interview prep")
    job_desc = st.text_input("Give the job description you're preparing for:")
    if key is None:
        st.info("Enter your Gemini API key on your left please")
    else:
        questions = interview(job_desc, key)
        st.write(questions)
