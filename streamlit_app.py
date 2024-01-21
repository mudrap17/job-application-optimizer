import pandas as pd
import numpy as np
import streamlit as st
from streamlit_option_menu import option_menu
from PyPDF2 import PdfReader
import seaborn as sns
from resume_optimizer import llm_result,linkedin_jobs,cold_outreach,suggestions

# Sidebar section
with st.sidebar:
  st.subheader('Choose your task:')
  option = option_menu(menu_title='', options=['Resume Optimizer', 'Cover letter', 'Job Industry Analysis', 'LinkedIn Jobs', 'Cold outreach Assist'],
                         icons=['house-fill', 'file-text-fill', 'bar-chart-fill', 'linkedin','chat-right-text-fill'])

if option == 'Resume Optimizer' or option == 'Cover letter':
    if option == 'Resume Optimizer':
        prompt = "optimize the resume to include keywords from the job description, add quantitative results to support the relevant experience and show yourself as the perfect fit for the job."
        st.title('AI powered Resume optimization')
        st.write('Use this tool to optimize your resume according to the job description')
    else:
        prompt = "write a cover letter  for the given job description and inlcude relevant experience from the resume and add details to make you the perfect fit for the job."
        st.title('AI powered Cover Letter optimization')
        st.write('Use this tool to optimize your cover letter according to the job description')
    
    key = st.text_input(label='Enter your Gemini API key:',type='password')
    job_desc = st.text_input(label='Enter the job description:')

    # file upload
    pdf = st.file_uploader(label='Upload your resume:', type='pdf')
    resume_optimize=''
    cover_letter =''
    if option == 'Resume Optimizer':
        resume_optimize = st.button(label='Optimize my resume')
    else:
        cover_letter = st.button(label='Write an amazing cover letter')


    try:
        if pdf is not None:
           pdf_reader = PdfReader(pdf)

           # extract text from each page separately
           text = ""
           for page in pdf_reader.pages:
                text += page.extract_text()
           if resume_optimize is not None or cover_letter is not None:
               result = llm_result(job_desc, text ,prompt, key)
               st.write(result)
               

    except Exception as e:
       st.warning(e)

if option == 'Job Industry Analysis':
    st.title('Job Industry Analysis')
    st.subheader('Explore the industry and prominent states according to 2023 H1B approvals')
    with st.spinner('Wait for it...'):
      df = pd.read_excel('EmployerInformation.xlsx')
    df = df[['Employer (Petitioner) Name','Industry (NAICS) Code','Initial Approval','Petitioner State']]
    option = st.selectbox("Select an industry", df['Industry (NAICS) Code'].unique(),index=None,placeholder="Select your industry")
    if option:
        cf = df[(df['Industry (NAICS) Code'] == option) & (df['Initial Approval'] > 0)]
        st.info('Hover over this table to download, search or expand. Find the top 5 states data below the table.', icon="ℹ️")
        st.write(cf[['Employer (Petitioner) Name','Initial Approval','Petitioner State']])
        df1 = cf['Petitioner State'].value_counts().rename_axis('States').reset_index(name='Approval counts')
        st.write('Top 5 states by approvals in this Industry')
        st.bar_chart(df1[:5], x='States' , y= 'Approval counts',color = '#00ff11')

    

if option == 'LinkedIn Jobs':
    st.title('LinkedIn jobs based on your resume')
    key = st.text_input(label='Enter your Gemini API key:',type='password')
    # file upload
    pdf = st.file_uploader(label='Upload your resume:', type='pdf')
    search_jobs = st.button('Search for jobs')

    try:
        if pdf is not None and key is not None:
           pdf_reader = PdfReader(pdf)

           # extract text from each page separately
           text = ""
           for page in pdf_reader.pages:
                text += page.extract_text()
           if search_jobs:
               result = linkedin_jobs(text,key)
               st.write(result)
    
    except Exception as e:
       st.warning(e)

if option == 'Cold outreach Assist':
    st.title('Cold Outreach Assist')
    st.write('Use AI to help you write better cold outreach messages')
    key = st.text_input(label='Enter your Gemini API key:',type='password')
    person = st.text_input(label='Whom are you reaching out to?')
    purpose = st.text_input(label= 'What would you like to talk about?')
    tab1,tab2 = st.tabs(['Draft first message','Get suggestions'])
    with tab1:
        st.title('Write a cold outreach message')
        cm =st.button('Sample cold message')
        if cm:
            result = cold_outreach(purpose, person ,key)
            st.write(result)
    
    with tab2:
        st.title('Give suggestions to improve')
        text = st.text_input('What did you have in mind?')
        sug =st.button('Rewrite mine')
        if sug:
            result = suggestions(text, person ,key)
            st.write(result)