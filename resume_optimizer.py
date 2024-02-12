import os
import google.generativeai as genai


def llm_response(prompt_template, key):
    genai.configure(api_key=key)
    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content(prompt_template)
    return response.text


def llm_result(job_description, resume, prompt, key):
    prompt_template = f"""You are applying to a job. For given resume and job description,
    {prompt}. List the keywords you added and what other changes you made and why. \n resume =
    {resume} , \n job description = {job_description}. Return a well formatted and organised resume with proper segmentation."""
    return llm_response(prompt_template, key)


def linkedin_jobs(resume, key):
    prompt_template = f"""Based on the experience from my resume, which job roles should I apply to on LinkedIn? 
    \n resume = {resume}
    Give a list of top 5 job roles like [Software Engineer,Mechanical Engineer] 
    and locations to apply with evidence supporting the results. 
    Give the LinkedIn job urls for the same."""
    return llm_response(prompt_template, key)


def cold_outreach(purpose, person, key):
    prompt_template = f"""I'm reaching out to a {person}. Write a cold outreach message for this purpose: {purpose} """
    return llm_response(prompt_template, key)


def suggestions(text, person, key):
    prompt_template = f"""I'm reaching out to a {person}. Here's my message to them:{text} .
    Suggest me ways I can improve my writing skills and make the cold outreach message more refined.
    Explain with example. If you were that person, would you engage back? """
    return llm_response(prompt_template, key)


def sample_resume(job_description, key):
    prompt_template = f"""For the given job description: {job_description}, 
    write a sample resume for an ideal candidate for this position. 
    Include quantitative impact examples of experience and projects with most important keywords."""
    return llm_response(prompt_template, key)


def project_suggestions_job(job_description, key):
    prompt_template = f"""For the given job description: {job_description}, 
    give practical project suggestions to showcase my abilities to perform well in the job."""
    return llm_response(prompt_template, key)


def project_suggestions_skill(skills, domain, key):
    prompt_template = f"""For the given job skills: {skills}, 
    give practical project suggestions to showcase my abilities to use those skills in the domain : {domain} , if given."""
    return llm_response(prompt_template, key)


def roadmap(skill, key):
    prompt_template = f"""You are an instructor. For the given skill: {skill}, 
    design a roadmap to learn the skills with links to resources and practical examples."""
    return llm_response(prompt_template, key)


def interview(job_desc, key):
    prompt_template = f"""For the given job description: {job_desc}, 
    help me prepare for the interview by asking relevant questions as an employer."""
    return llm_response(prompt_template, key)
