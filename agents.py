from langchain.agents import create_agent
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from tools import web_search,web_scrape
from dotenv import load_dotenv
load_dotenv()

llm = ChatGroq(model="openai/gpt-oss-120b",temperature=0.2)

#1st agent for web search 
def build_search_agent():
    return create_agent(
        model=llm,
        tools=[web_search]
    )

#2nd agent for web scraping
def build_scrape_agent():
    return create_agent(
        model=llm,
        tools=[web_scrape]
    )

writer_prompt=ChatPromptTemplate.from_messages([
    ("system",
        """You are an AI research analyst.

Your task is to analyze the provided research and create a clear,
well-structured research report.

Use only the information provided in the research.
Do not invent facts or information.

Structure the report as follows:

1.Introduction
2. Key Findings (Minimum of 3 key findings)
3. Conclusion
4. Sources (list all urls used in the research)

Keep the report factual, concise, and easy to understand."""
    ),
    (
        "human",
        """Research Topic:
{topic}

Research:
{research}

Create a structured research report based on the information above."""
    )
])

writer_chain=writer_prompt | llm | StrOutputParser()

critic_prompt = ChatPromptTemplate.from_messages([
    ( "system", """You are an expert research critic. 
    Evaluate the research report for accuracy, relevance, depth, clarity, completeness, organization, and source quality. 
    Provide a structured critique containing: 
    - Overall Score (out of 10) 
    - Category Scores (out of 10) 
    - Strengths 
    - Weaknesses 
    - Missing Information 
    - Areas for Improvement 
    - Critical Issues 
    - Final Assessment 

    Be objective, specific, and concise. Do not rewrite the report.""" ), 
    ( "human", """Review the following research report: {report}""" ) 
])

critic_chain = critic_prompt | llm | StrOutputParser()