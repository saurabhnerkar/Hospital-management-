from .config import LLM_PROVIDER, LLM_MODEL, GOOGLE_API_KEY

def get_llm():
    """
    Initializes and returns the Large Language Model (LLM).
    This acts as the 'brain' of the chatbot that reads the retrieved documents 
    and formulates a human-like answer.
    """
    
    if LLM_PROVIDER.lower() == "gemini":
        # Import inside the function to avoid errors if the library isn't installed
        from langchain_google_genai import ChatGoogleGenerativeAI
        
        if not GOOGLE_API_KEY:
            raise ValueError("GOOGLE_API_KEY is not set in your .env file.")
            
        # We initialize the Gemini model
        return ChatGoogleGenerativeAI(
            model=LLM_MODEL,
            google_api_key=GOOGLE_API_KEY,
            # temperature controls creativity: 0.0 is very strict/factual, 1.0 is very creative. 
            # We use 0.3 because for a hospital, we want factual and professional answers, not made-up stories.
            temperature=0.3, 
        )
        
    elif LLM_PROVIDER.lower() == "openai":
        from langchain_openai import ChatOpenAI
        
        return ChatOpenAI(
            model=LLM_MODEL,
            temperature=0.3,
        )
        
    else:
        raise ValueError(f"Unsupported LLM_PROVIDER in config: {LLM_PROVIDER}")
