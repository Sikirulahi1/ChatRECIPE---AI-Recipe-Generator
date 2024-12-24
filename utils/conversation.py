from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
import os 
from dotenv import load_dotenv
import os 
from dotenv import load_dotenv

def get_ai_response(input_text: str) -> str:
    """
    Get AI response using LangChain and OpenAI.
    
    Args:
        input_text (str): User input text/question
        
    Returns:
        str: AI generated response
    """
    load_dotenv()

    os.environ['OPENAI_API_KEY'] = os.getenv('OPENAI_API_KEY')
    os.environ['LANGCHAIN_API_KEY'] = os.getenv('LANGCHAIN_API_KEY')

    # Prompt Template
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", "You are a friendly and intelligent assistant. You can provide helpful answers, engage in casual conversation, and be thoughtful and patient with your responses. Feel free to ask follow-up questions if needed."),
            ("user", "I need assistance with: {question}")
        ]
    )

    llm = ChatOpenAI(model='gpt-3.5-turbo')
    output_parser = StrOutputParser()
    chain = prompt|llm|output_parser

    if input_text:
        result = chain.invoke({"question": input_text})
        return result
    return ""
