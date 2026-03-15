# ─── httpx compatibility patch ──────────────────────────────────────────────
# groq SDK passes `proxies` to httpx.Client, which was removed in httpx 0.28+.
# This patch strips the argument before __init__ runs, making it version-safe.
import httpx as _httpx
_orig_client_init = _httpx.Client.__init__
def _patched_client_init(self, *args, **kwargs):
    kwargs.pop('proxies', None)
    _orig_client_init(self, *args, **kwargs)
_httpx.Client.__init__ = _patched_client_init

_orig_async_init = _httpx.AsyncClient.__init__
def _patched_async_init(self, *args, **kwargs):
    kwargs.pop('proxies', None)
    _orig_async_init(self, *args, **kwargs)
_httpx.AsyncClient.__init__ = _patched_async_init
# ─────────────────────────────────────────────────────────────────────────────

from groq import Groq
from config import Config
from services.rag_engine import retrieve_context

_client = None

def get_groq_client():
    global _client
    if _client is None:
        _client = Groq(api_key=Config.GROQ_API_KEY)
    return _client

SYSTEM_PROMPT = """You are RAGnosis, an intelligent and empathetic AI medical assistant. 
Your role is to help patients understand their medical reports in simple, clear language.

Guidelines:
- Always explain medical terms in simple language that a patient can understand.
- Be empathetic, supportive, and non-alarming.
- Use the provided report context and medical knowledge to answer accurately.
- Always recommend consulting a doctor for diagnosis and treatment.
- Present numbers and values with their normal ranges for comparison.
- Format responses clearly with bullet points where helpful.
- If you don't know something, say so honestly rather than guessing.

⚠️ IMPORTANT: You are an educational assistant, NOT a substitute for professional medical advice."""

def get_chatbot_response(user_message: str, report_text: str = "", chat_history: list = []) -> str:
    """Get AI response using Groq with RAG context."""
    # Retrieve relevant knowledge
    rag_context = retrieve_context(user_message, report_text)

    # Build context message
    context_parts = []
    if report_text:
        context_parts.append(f"PATIENT'S REPORT (excerpt):\n{report_text[:1500]}")
    if rag_context:
        context_parts.append(f"MEDICAL KNOWLEDGE:\n{rag_context}")

    context_msg = "\n\n".join(context_parts)

    # Build messages
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]

    if context_msg:
        messages.append({
            "role": "user",
            "content": f"Context for this conversation:\n{context_msg}"
        })
        messages.append({
            "role": "assistant",
            "content": "I've reviewed your report and the relevant medical information. I'm ready to answer your questions!"
        })

    # Add chat history (last 6 messages)
    for msg in chat_history[-6:]:
        messages.append({"role": msg["role"], "content": msg["content"]})

    # Add current question
    messages.append({"role": "user", "content": user_message})

    try:
        client = get_groq_client()
        response = client.chat.completions.create(
            model=Config.GROQ_MODEL,
            messages=messages,
            max_tokens=1024,
            temperature=0.3,
        )
        return response.choices[0].message.content
    except Exception as e:
        error_msg = str(e)
        if "api_key" in error_msg.lower() or "authentication" in error_msg.lower():
            return "⚠️ Groq API key not configured. Please add your GROQ_API_KEY to the backend/.env file. Get a free key at console.groq.com"
        return f"I'm having trouble connecting to the AI service right now. Please try again in a moment. (Error: {error_msg[:100]})"
