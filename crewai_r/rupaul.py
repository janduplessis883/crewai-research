import os
from crewai import Agent, Task, Crew, Process
from crewai_tools import SerperDevTool, WebsiteSearchTool, YoutubeVideoSearchTool, WebsiteSearchTool, ScrapeWebsiteTool
from langchain_community.llms import Ollama
import streamlit as st
from datetime import datetime
import agentops
agentops.init()

now = datetime.now()

llm = Ollama(model="openhermes")
search_tool = SerperDevTool()
web_search_tool = WebsiteSearchTool()
youtube_search = YoutubeVideoSearchTool(youtube_vidoe_url='https://youtu.be/F-FL2f9rRxQ?si=T57kAz8ImRf4YGBH')
website_search_tool = WebsiteSearchTool()
website_scrape_tool = ScrapeWebsiteTool()

# Manager Agent

manager = Agent(
    llm=llm,
    role="Manager",
    goal="Oversee, manages and initialize new requests, making a detailed plan of execution ofr other agents before they set off.",
    backstory="Experienced project manager with a background in overseeing AI news research and content creation.",
    allow_delegation=True,
    tools=[search_tool, website_scrape_tool, youtube_search, web_search_tool],
    verbose=True,
)

# Senior Researcher Agent

researcher = Agent(
    llm=llm,
    role="Senior Researcher",
    goal="Research credible sources for the latest AI news published on {datetime_today}, check with Manager Agent if search results are comprehesive enough.",
    backstory="Experienced AI news Researcher",
    allow_delegation=False,
    tools=[search_tool, website_scrape_tool, youtube_search, web_search_tool],
    verbose=True,
)


task1 = Task(
    description="Search the internet and YouTube and blog posts for the latest AI and Python news.",
    expected_output="Formatted results with title, date, and summary.",
    agent=researcher,
    output_file="task1_output.txt",
)

# Writer Agent

writer = Agent(
    llm=llm,
    role="Writer",
    goal="Craft a compelling, well-researched summary of the latest news about AI and Python",
    backstory="The Writer is a well-known AI and Python journalist experienced in writing about Tech.",
    allow_delegation=False,
    verbose=True,
)

task2 = Task(
    description="Summarize the findings from the research conducted online about the latest AI and Python news",
    expected_output="""AI and Python News: in the format of a blog post in markdown
    Here is a template:
    title: The Rise of AI Agents in Modern Business
author: AI Agent 
date: 2023-05-15
tags: [AI, Automation, Business]
---

# The Rise of AI Agents in Modern Business

## Introduction

In the ever-evolving landscape of modern business, the emergence of AI agents has transformed the way organizations operate and thrive. As an AI agent, I'm excited to share my insights on the profound impact these cutting-edge technologies are having on the corporate world.

## The Advantages of AI Agents

AI agents offer a multitude of advantages that are revolutionizing the way businesses approach their challenges. Some of the key benefits include:

1. **Increased Efficiency**: AI agents can automate repetitive tasks, streamline workflows, and make data-driven decisions with lightning speed, freeing up valuable human resources for more strategic and creative endeavors.

2. **Enhanced Decision-Making**: By leveraging advanced analytics and machine learning algorithms, AI agents can provide businesses with deeper insights, helping them make more informed and strategic decisions.

3. **Improved Customer Experience**: AI-powered chatbots and virtual assistants can offer personalized, 24/7 support, enhancing customer satisfaction and loyalty.

4. **Cost Savings**: The implementation of AI agents can lead to significant cost savings by reducing the need for manual labor, optimizing resource allocation, and minimizing errors.

## Case Studies: AI Agents in Action

To illustrate the real-world impact of AI agents, let's explore a few case studies:
    
    """,
    agent=writer,
    output_file="task2_output.txt",
)

# Update Crew Configuration with Manager
crew = Crew(agents=[manager, researcher, writer], tasks=[task1, task2], 
            process=Process.hierarchical,
            manager_llm=Ollama(model="llama3"),
            memmory=True,
            verbose=2)
print(f"{now}=*100")
inputs = {'datetime_today': now}
task_output = crew.kickoff()
print(task_output)
agentops.end_session('Success')