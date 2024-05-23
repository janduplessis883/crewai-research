import os
import requests
from pydantic import BaseModel, EmailStr, ValidationError, Field

# Warning control
import warnings
warnings.filterwarnings('ignore')

from crewai import Agent, Task, Crew



from crewai_tools import BaseTool

import contiguity

contiguity_crewai_token = os.getenv("CONTIGUITY_CREWAI_TOKEN")
client = contiguity.login(contiguity_crewai_token) # Delete True to exit debug mode.

class SendEmailTool(BaseTool):
    name: str ="Send Email Tool"
    description: str = ("Use this tool whenever you need to send an email to someone. You will need to create the email body in 'html' format as a string. Write an engaging email subject: {subject} and email body html: [text]")

    def _run(self, text: str, subject: str) -> str:
        # Plain text email (To send as HTML change "text" to "html")
        email_object = {
                "to": inputs['email_address'],
                "from": "CrewAI Email Agent - Contiguity",
                "subject": subject,
                "html": text
            }
        return client.send.email(email_object)
    
send_email_tool = SendEmailTool() 

single_agent = Agent(
    role="Email Agent",
    goal="You are an expert in email communication. You will send any report to our client via email in 'html' format.",
    backstory=(
        "You work in a large compnay as a personal assistant to the executive team, you manage the whole teams eamil correspondance, you are a detailed oriented person. and signs all emails with: Kind Regards, Orson, the email agent."
    ),
    allow_delegation=False,
    tools=[send_email_tool],
    verbose=True
)

# Define a task for sending the email
email_task = Task(
    description='Send an report on AI Today by email to: {email_address}',
    expected_output='Email sent confirmation, response from API in json format',
    agent=single_agent,
    tools=[send_email_tool]

)

crew = Crew(
    agents=[single_agent],
    tasks=[email_task],
    verbose=2,
	memory=True
)

# Define your inputs
inputs = {
    "email_address": "breda886@aol.com",
}

result = crew.kickoff(inputs=inputs)
print(100*'=')
print("🧔🏻‍♂️ Final Result: 🧡")
print(100*'=')
print(result)