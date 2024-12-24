import os
from langchain_community.document_loaders import WebBaseLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains import LLMChain
from langchain_community.llms import Cohere
from langchain.prompts import PromptTemplate
import re

def clean_document_text(text):
    """
    Cleans the input text by removing excess whitespace and irrelevant characters.
    
    Args:
        text (str): The raw text content of the document.
        
    Returns:
        str: The cleaned text.
    """
    # Remove excessive line breaks, tabs, and spaces
    text = re.sub(r'\s+', ' ', text).strip()
    
    # Optionally, further filtering can be done here (e.g., remove ads or footers if patterns are known)
    
    return text

def get_recipe_details(url):
    """
    Retrieves and analyzes recipe details from a given URL using LangChain and Cohere.
    
    Args:
        url (str): URL of the recipe webpage to analyze.
        
    Returns:
        str: HTML formatted response containing ingredients and preparation steps.
    """
    # Ensure API key is available
    cohere_api_key = os.getenv('COHERE_API_KEY')
    if not cohere_api_key:
        raise EnvironmentError("COHERE_API_KEY environment variable is not set.")
    os.environ['COHERE_API_KEY'] = cohere_api_key

    # Load the webpage content
    loader = WebBaseLoader(url)
    docs = loader.load()

    # Clean the content of each document
    cleaned_docs = [clean_document_text(doc.page_content) for doc in docs]

    # Combine all cleaned content into a single string
    combined_text = " ".join(cleaned_docs)

    # Split the combined text into manageable chunks
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    documents = text_splitter.split_text(combined_text)

    # Initialize Cohere LLM
    llm = Cohere(
        temperature=0.7,
        max_tokens=4000  # Adjust as per your needs
    )

    # Define the prompt template
    prompt = PromptTemplate(
        input_variables=["context", "input_ingredients", "input_steps"],
        template="""
        You are a highly intelligent and helpful assistant specialized in providing precise and insightful answers based on the given context. Always base your response strictly on the provided information and include step-by-step reasoning to ensure clarity and accuracy. Avoid assumptions and external knowledge unless explicitly asked for.

        Here is the context for your response:
        {context}

        Now, answer the following question in HTML format:

        <html>
        <body>
            <h2>Ingredients</h2>
            <ul>
                {input_ingredients}
            </ul>

            <h2>Preparation Steps</h2>
            <ol>
                {input_steps}
            </ol>
        </body>
        </html>
        """
    )

    # Initialize LLM chain
    chain = LLMChain(llm=llm, prompt=prompt)

    # Define maximum token allowance for context
    max_tokens = 4081
    prompt_token_length = len(prompt.template.split())  # Approximate token count for the prompt

    # Process the combined document chunks

    # Calculate available tokens for the context
    available_tokens = max_tokens - prompt_token_length
    truncated_content = [docs for docs in documents][:available_tokens]

    # Generate response for the current document chunk
    response = chain.run({
        "context": truncated_content,
        "input_ingredients": "Ingredients List Placeholder",
        "input_steps": "Preparation Steps Placeholder"
    })

    return response
