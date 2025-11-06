import json, re
from typing import List, Dict, Any
from config import Config

try:
    import google.generativeai as genai
    genai_available = True
except Exception:
    genai_available = False

# ✅ Best model from list you provided
MODEL_NAME = "gemini-2.0-flash"


# --------------------------------------------------------
# INTERNAL HELPER
# --------------------------------------------------------
def _ensure_client():
    """Ensure Gemini is configured and returns a model client."""
    if not genai_available:
        raise RuntimeError("❌ Gemini SDK not installed")
    if not Config.GEMINI_API_KEY:
        raise RuntimeError("❌ GEMINI_API_KEY missing")
    genai.configure(api_key=Config.GEMINI_API_KEY)
    return genai.GenerativeModel(MODEL_NAME)


def _extract_json(text: str):
    """Extract JSON payload from messy LLM responses."""
    try:
        match = re.search(r"\{.*\}|\[.*\]", text, re.S)
        if match:
            return json.loads(match.group(0))
        return json.loads(text)
    except:
        return None


# --------------------------------------------------------
# GEMINI BASIC TEXT CALL
# --------------------------------------------------------
def call_gemini_text(prompt: str) -> str:
    model = _ensure_client()

    resp = model.generate_content(prompt)

    # Standard .text extraction
    text = getattr(resp, "text", "").strip()

    # In case .text is empty → inspect candidates
    if not text and hasattr(resp, "candidates"):
        try:
            text = resp.candidates[0].content.parts[0].text
        except:
            text = ""

    return text.strip()


# --------------------------------------------------------
# AUDIO TRANSCRIPTION
# --------------------------------------------------------
def transcribe_audio_wav(audio_bytes: bytes) -> str:
    """Send raw wav audio bytes → plain English transcription."""
    model = _ensure_client()

    parts = [
        "Transcribe the following audio. Output plain text only.",
        {"mime_type": "audio/wav", "data": audio_bytes},
    ]

    resp = model.generate_content(parts)
    text = getattr(resp, "text", "").strip()
    if not text and hasattr(resp, "candidates"):
        try:
            text = resp.candidates[0].content.parts[0].text
        except:
            text = ""

    return text.strip()


# --------------------------------------------------------
# GENERATE FIRST 20 QUESTIONS
# --------------------------------------------------------
def generate_questions_for_role(role: str, experience: str) -> List[Dict[str, str]]:
    prompt = f"""
You are an interview question generator.
Return ONLY valid JSON list with 4 objects:

[
  {{ "category": "Behavioral", "questions": ["...5 questions..."] }},
  {{ "category": "Technical", "questions": ["...5 questions..."] }},
  {{ "category": "Decision-Making", "questions": ["...5 questions..."] }},
  {{ "category": "Problem-Solving", "questions": ["...5 questions..."] }}
]

Role: {role}
Experience: {experience}
"""

    try:
        raw = call_gemini_text(prompt)
        data = _extract_json(raw)

        out = []
        if data:
            for obj in data:
                cat = obj.get("category", "General")
                for q in obj.get("questions", []):
                    out.append({"category": cat, "question": q})

        # Ensure 20 questions
        if len(out) < 20:
            out = out * (20 // len(out) + 1)
        return out[:20]

    except Exception as e:
        # ✅ fallback
        cats = ["Behavioral", "Technical", "Decision-Making", "Problem-Solving"]
        fallback = []
        for cat in cats:
            for i in range(5):
                fallback.append({"category": cat, "question": f"{cat} question {i+1} for {role}"})
        return fallback


# --------------------------------------------------------
# ADAPTIVE FOLLOW-UP
# --------------------------------------------------------
def generate_adaptive_question(prev_q: str, prev_a: str, category: str, role: str, experience: str) -> str:
    prompt = f"""
You are an adaptive interviewer.
Return JSON:
{{"next_question": "..."}}

QUESTION: {prev_q}
ANSWER: {prev_a}
CATEGORY: {category}
ROLE: {role}
EXPERIENCE: {experience}
"""

    try:
        raw = call_gemini_text(prompt)
        data = _extract_json(raw)
        if data:
            return data.get("next_question", "").strip()
    except:
        pass
    return ""


# --------------------------------------------------------
# EVALUATE ANSWER
# --------------------------------------------------------
def evaluate_answer_ai(question: str, answer: str, category: str, role: str, experience: str) -> Dict[str, Any]:
    prompt = f"""
You are an expert interview evaluator.

Return JSON:
{{"score": <0-100>, "feedback": "one concise sentence"}}

QUESTION: {question}
ANSWER: {answer}
CATEGORY: {category}
ROLE: {role}
EXPERIENCE: {experience}
"""

    try:
        raw = call_gemini_text(prompt)
        data = _extract_json(raw)

        if data:
            score = data.get("score", 0)
            try:
                score = int(score)
            except:
                score = 0
            score = max(0, min(100, score))
            return {
                "score": score,
                "feedback": data.get("feedback", "").strip()
            }

    except Exception:
        pass

    # ✅ fallback scoring
    score = min(95, max(35, len(answer) // 3))
    return {"score": score, "feedback": "Fallback evaluation."}
