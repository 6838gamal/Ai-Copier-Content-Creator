from fastapi import APIRouter
from app.services.retriever import retrieve_relevant_texts
from app.services.prompt_builder import build_prompt
from app.services.gemini_service import generate_text

router = APIRouter()

memory = []

@router.post("/generate")
def generate(data: dict):
    user_input = data.get("prompt")

    texts = retrieve_relevant_texts(user_input)

    prompt = build_prompt(user_input, texts)

    result = generate_text(prompt)

    memory.append({"input": user_input, "output": result})
    if len(memory) > 3:
        memory.pop(0)

    return {"result": result}
