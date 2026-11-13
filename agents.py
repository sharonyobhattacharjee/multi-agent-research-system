
import os
from dotenv import load_dotenv

from langchain.agents import create_agent
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

from tool import web_search, scrape_url


# Load environment variables
load_dotenv()


# Initialize Gemini LLM
llm = ChatGoogleGenerativeAI(
    model="gemini-3.5-flash-lite",
    temperature=0,
    google_api_key=os.getenv("GEMINI_API_KEY"),
    timeout=60,
    max_retries=2
)


# --------------------------------------------------
# SEARCH AGENT
# --------------------------------------------------

def build_search_agent():
    return create_agent(
        model=llm,
        tools=[web_search]
    )


# --------------------------------------------------
# READER AGENT
# --------------------------------------------------

def build_reader_agent():
    return create_agent(
        model=llm,
        tools=[scrape_url]
    )


# --------------------------------------------------
# WRITER AGENT
# --------------------------------------------------

writer_prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        "You are an expert research writer. "
        "Write clear, structured, factual and insightful research reports."
    ),
    (
        "human",
        """Write a detailed research report on the topic below.

Topic: {topic}

Research Gathered:
{research}

Structure the report as:

1. Introduction

2. Key Findings
   - Include a minimum of 3 well-explained points.
   - Support important claims using the research provided.

3. Conclusion

4. Sources
   - List all URLs found in the research.

Be detailed, factual, objective, and professional."""
    ),
])

writer_chain = writer_prompt | llm | StrOutputParser()


# --------------------------------------------------
# CRITIC AGENT
# --------------------------------------------------

critic_prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        "You are a sharp and constructive research critic. "
        "Be honest and specific."
    ),
    (
        "human",
        """Review the research report below and evaluate it strictly.

Report:
{report}

Respond in this exact format:

Score:
X/10

Strengths:
- Point 1
- Point 2
- Point 3

Areas to Improve:
- Point 1
- Point 2
- Point 3

One Line Verdict:
[Write one concise sentence evaluating the overall quality of the report.]
"""
    ),
])

critic_chain = critic_prompt | llm | StrOutputParser()
