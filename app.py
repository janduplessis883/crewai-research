import streamlit as st
import pandas as pd
import os
from crewai import Agent, Task, Crew
from langchain_groq import ChatGroq


def main():
    st.set_page_config(page_title="CrewAI Research Assistant")
    # Set up the customization options
    st.sidebar.title('Customization')
    model = st.sidebar.selectbox(
        'Choose a model',
        ['mixtral-8x7b-32768', 'llama2-70b-4096']
    )

    llm = ChatGroq(
            temperature=0, 
            groq_api_key = st.secrets["GROQ_API_KEY"], 
            model_name=model
        )

    # Streamlit UI
    html = """
        <style>
        .gradient-text {
            background: linear-gradient(45deg, #ae4f4d, #ad5831, #f3aa49);
            -webkit-background-clip: text;
            background-clip: text;
            color: transparent;
            font-size: 3em;
            font-weight: bold;
        }
        </style>
        <div class="gradient-text">CrewAI Research Assistant</div>
    """
    st.markdown(html, unsafe_allow_html=True)
    
    multiline_text = """
    Introducing **CrewAI Research Assistant:** Your Personal Navigator in the Vast Ocean of **Web Research**. Whether you're delving into new academic territories, exploring cutting-edge technological advancements, or simply satisfying your curiosity on a diverse array of topics, CrewAI Research Assistant is here to streamline your journey.

    At the heart of CrewAI Research Assistant lies a synergistic team of AI agents, each specialized in distinct facets of web research. These agents collaborate seamlessly to offer you a comprehensive and nuanced exploration of any subject matter. Here's how CrewAI Research Assistant empowers your research:
    """
    col1, col2 = st.columns([5,1])
    with col1:
        pass
    
    with col2:
        st.image('logo.png')
        
        
    st.markdown(multiline_text, unsafe_allow_html=True)
    agent_list = ['Manager_Agent', 'YouTube_Research_Agent', 'Web_Research_Agent', 'Research_Summarizer_Agent', 'Writer_Agent']
    st.multiselect(label="Select your Agents:", options=agent_list)
    
    task_list = ['ResearchNewsTask', 'ResearchYoutubeTask', 'ArticleWriterTask', 'HistoricalEventsResearchTask']
    st.multiselect(label="Pick Tasks:", options=task_list)




    Manager_Agent = Agent(
        role='Web_Research_Manager',
        goal="""Manage and coordinate the web research process to gather high-quality, relevant information for the project.
        This includes:
        Identifying key research topics and questions based on the project requirements.
        Assigning research tasks to appropriate agents or team members.
        Monitoring progress and ensuring research tasks are completed efficiently and effectively.
        Reviewing and synthesizing research findings to provide comprehensive and actionable insights.""",
        backstory="""You are a highly skilled and experienced manager in overseeing web research projects.
        Your expertise lies in breaking down complex research requirements, delegating tasks to the right people,
        and ensuring the research process runs smoothly and delivers valuable insights. You have a keen eye for detail
        and are adept at identifying the most relevant and reliable sources of information on the web. Your goal is to
        lead the research team to success by providing clear guidance, effective coordination, and strategic decision-making.""",
        verbose=True,
        allow_delegation=True,
        llm=llm,
        )

    YouTube_Research_Agent = Agent(
        role='YouTube_Research_Agent',
        goal="""conduct research on YouTube to find relevant videos, channels, and playlists related to the given topic.
        Assess the quality and relevance of the content, and provide a curated list of the most informative and engaging resources.
        Suggest ways to extract valuable insights and data from the identified YouTube content.""",
        backstory="""You are a YouTube research specialist with a keen eye for discovering high-quality content.
        Your expertise lies in navigating the vast landscape of YouTube videos, channels, and playlists to find the most relevant
        and informative resources for a given topic. You excel at assessing the credibility and value of YouTube content,
        and you can provide guidance on how to extract meaningful data and insights from the identified videos.""",
        verbose=True,
        allow_delegation=False,
        llm=llm,
        )

    Web_Research_Agent = Agent(
        role='Web_Research_Agent',
        goal="""conduct thorough web research to gather relevant, reliable, and up-to-date information on the given topic.
        Identify key sources, assess the credibility of the information, and synthesize the findings to provide comprehensive
        and actionable insights. Suggest strategies for further research and analysis to deepen understanding of the topic.""",
        backstory="""As a skilled web researcher, you have a talent for navigating the vast expanse of online information to find
        the most relevant and trustworthy sources. Your expertise lies in identifying key websites, databases, and publications
        that provide valuable insights on a given topic. You excel at assessing the credibility and reliability of the information
        you find, and you can synthesize complex data into clear, actionable insights. Your goal is to provide the user with
        a comprehensive understanding of the topic, backed by the most current and reliable information available on the web.""",
        verbose=True,
        allow_delegation=True,
        llm=llm,
        )


    Research_Summarizer_Agent = Agent(
        role='Research_Summarizer_Agent',
        goal="""synthesize the findings from various research agents, such as the Web_Research_Agent and YouTube_Research_Agent,
        to create a comprehensive and coherent summary of the gathered information. Identify key insights, trends, and conclusions,
        and present them in a clear and concise manner. Highlight any gaps in the research and suggest areas for further investigation.""",
        backstory="""As an expert in research synthesis, you have a keen ability to analyze and consolidate information from various sources.
        Your expertise lies in identifying the most important insights and conclusions from a wide range of research findings and presenting
        them in a clear, organized manner. You excel at connecting the dots between different pieces of information and identifying overarching
        themes and trends. Your goal is to provide the user with a comprehensive and easily digestible summary of the research, enabling them
        to make informed decisions and take action based on the insights gathered.""",
        verbose=True,
        allow_delegation=False,
        llm=llm,
        )

    Writer_Agent = Agent(
        role='Writer_Agent',
        goal="""compose a well-structured, engaging, and informative article of 5 paragraphs based on the comprehensive research summary
        provided by the Research_Summarizer_Agent. Ensure that the article effectively communicates the key insights, trends, and conclusions
        from the research, while maintaining a clear and coherent narrative flow. Use appropriate language, tone, and style to appeal to the
        target audience and optimize readability.""",
        backstory="""As a talented writer with a background in journalism and content creation, you have a gift for crafting compelling stories
        and articles that capture the essence of complex topics. Your expertise lies in distilling research findings and insights into
        well-structured, engaging, and informative pieces of writing that resonate with the target audience. You excel at finding the right
        balance between depth and clarity, ensuring that your articles are both comprehensive and easily understandable. Your goal is to create
        a 5-paragraph article that effectively communicates the key takeaways from the research summary, leaving the reader informed,
        enlightened, and eager to learn more.""",
        verbose=True,
        allow_delegation=False,
        llm=llm,
        )
    # Summarization_Agent = Agent(
    #     role='Starter_Code_Generator_Agent',
    #     goal="""Summarize findings from each of the previous steps of the ML discovery process.
    #         Include all findings from the problem definitions, data assessment and model recommendation 
    #         and all code provided from the starter code generator.
    #         """,
    #     backstory="""You are a seasoned data scientist, able to break down machine learning problems for
    #         less experienced practitioners, provide valuable insight into the problem and why certain ML models
    #         are appropriate, and write good, simple code to help get started on solving the problem.
    #         """,
    #     verbose=True,
    #     allow_delegation=False,
    #     llm=llm,
    # )

    user_question = st.text_input("What do you want to research:")
    data_upload = False
    uploaded_file = st.file_uploader("Upload a sample .csv of your data (optional)")
    if uploaded_file is not None:
        try:
            # Attempt to read the uploaded file as a DataFrame
            df = pd.read_csv(uploaded_file).head(5)
            
            # If successful, set 'data_upload' to True
            data_upload = True
            
            # Display the DataFrame in the app
            st.write("Data successfully uploaded and read as DataFrame:")
            st.dataframe(df)
        except Exception as e:
            st.error(f"Error reading the file: {e}")

    if user_question:

        task_define_problem = Task(
        description="""Clarify and define the machine learning problem, 
            including identifying the problem type and specific requirements.
            
            Here is the user's problem:

            {ml_problem}
            """.format(ml_problem=user_question),
        agent=Problem_Definition_Agent,
        expected_output="A clear and concise definition of the machine learning problem."
        )

        if data_upload:
            task_assess_data = Task(
                description="""Evaluate the user's data for quality and suitability, 
                suggesting preprocessing or augmentation steps if needed.
                
                Here is a sample of the user's data:

                {df}

                The file name is called {uploaded_file}
                
                """.format(df=df.head(),uploaded_file=uploaded_file),
                agent=Data_Assessment_Agent,
                expected_output="An assessment of the data's quality and suitability, with suggestions for preprocessing or augmentation if necessary."
            )
        else:
            task_assess_data = Task(
                description="""The user has not uploaded any specific data for this problem,
                but please go ahead and consider a hypothetical dataset that might be useful
                for their machine learning problem. 
                """,
                agent=Data_Assessment_Agent,
                expected_output="A hypothetical dataset that might be useful for the user's machine learning problem, along with any necessary preprocessing steps."
            )

        task_recommend_model = Task(
        description="""Suggest suitable machine learning models for the defined problem 
            and assessed data, providing rationale for each suggestion.""",
        agent=Model_Recommendation_Agent,
        expected_output="A list of suitable machine learning models for the defined problem and assessed data, along with the rationale for each suggestion."
        )


        task_generate_code = Task(
        description="""Generate starter Python code tailored to the user's project using the model recommendation agent's recommendation(s), 
            including snippets for package import, data handling, model definition, and training
            """,
        agent=Starter_Code_Generator_Agent,
        expected_output="Python code snippets for package import, data handling, model definition, and training, tailored to the user's project, plus a brief summary of the problem and model recommendations."
        )

        # task_summarize = Task(
        #     description="""
        #     Summarize the results of the problem definition, data assessment, model recommendation and starter code generator.
        #     Keep the summarization brief and don't forget to share the entirety of the starter code!
        #     """,
        #     agent=Summarization_Agent
        # )


        crew = Crew(
            agents=[Problem_Definition_Agent, Data_Assessment_Agent, Model_Recommendation_Agent,  Starter_Code_Generator_Agent], #, Summarization_Agent],
            tasks=[task_define_problem, task_assess_data, task_recommend_model,  task_generate_code], #, task_summarize],
            verbose=2
        )

        result = crew.kickoff()

        st.write(result)


if __name__ == "__main__":
    main()

