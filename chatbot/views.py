import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .ai.rag import ask_chatbot

@csrf_exempt
def chat_api(request):
    """
    This view receives the user's message from the frontend (home.html)
    via AJAX, sends it to the AI, and returns the AI's answer.
    """
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            user_msg = data.get("message", "").strip()
            
            if not user_msg:
                return JsonResponse({"error": "Empty message"}, status=400)
                
            # We call the RAG pipeline we just built!
            # We'll use the 'patients' collection by default for general queries.
            ai_reply = ask_chatbot(collection_name="patients", user_question=user_msg)
            
            return JsonResponse({"reply": ai_reply})
            
        except Exception as e:
            print("Chatbot Error:", str(e))
            return JsonResponse({"error": "Something went wrong processing your request."}, status=500)
            
    return JsonResponse({"error": "Invalid request method"}, status=400)
