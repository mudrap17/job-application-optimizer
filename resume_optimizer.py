import os
import google.generativeai as genai


def llm_response(prompt_template,key):
    genai.configure(api_key = key)
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(prompt_template)
    return response.text

def llm_result(job_description,resume,prompt,key):
    prompt_template = f"""You are applying to a job. For given resume and job description,
    {prompt}. Explain which keywords you added and what changes you made and why. \n resume =
    {resume} , \n job description = {job_description}. Return a well formatted resume.""" 
    return llm_response(prompt_template,key)

def linkedin_jobs(resume,key):
    prompt_template = f"""Based on the experience from my resume, which job roles should I apply to on LinkedIn? 
    \n resume = {resume}
    Give a list of top 5 job roles like [Software Engineer,Mechanical Engineer] 
    and locations to apply with evidence supporting the results. 
    Give the LinkedIn job urls for the same."""
    return llm_response(prompt_template,key)

def cold_outreach(purpose, person, key):
    prompt_template = f"""I'm reaching out to a {person}. Write a cold outreach message for this purpose: {purpose} """
    return llm_response(prompt_template , key)

def suggestions(text, person, key):
    prompt_template = """I'm reaching out to a {person}. Here's my message to them:{text} .
    Suggest me ways I can improve my writing skills and make the cold outreach message more refined.
    Explain with example. If you were that person, would you engage back? """ 
    return llm_response(prompt_template, key)









