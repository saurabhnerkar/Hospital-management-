from langchain_core.prompts import ChatPromptTemplate

# This is the system prompt. It tells the AI who it is and how to behave.
# It acts as the "rules of the game" for the LLM.
SYSTEM_PROMPT = """You are a highly intelligent, professional, and helpful AI assistant for a Hospital Management System.

Your job is to answer the user's questions based ONLY on the provided context.
The context will contain information retrieved from the hospital's database (like patient records, bills, or doctor schedules).

Follow these rules strictly:
1. If the answer is not in the provided context, say "I don't have enough information to answer that based on the current records." Do not make up an answer (hallucinate).
2. Keep your answers clear, concise, and professional.
3. If the user asks for medical advice, remind them that you are an AI assistant and they should consult a doctor.

Context provided from database:
{context}
"""

def get_rag_prompt() -> ChatPromptTemplate:
    """
    Returns the ChatPromptTemplate used for the RAG pipeline.
    It combines the system prompt (rules + context) with the user's actual question.
    """
    
    # We construct a prompt with two messages:
    # 1. A "system" message setting up the rules and providing the retrieved {context}.
    # 2. A "human" message containing the user's {input} (their actual question).
    prompt = ChatPromptTemplate.from_messages([
        ("system", SYSTEM_PROMPT),
        ("human", "{input}"),
    ])
    
    return prompt
