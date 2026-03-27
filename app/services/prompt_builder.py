def build_prompt(user_input, retrieved_texts):
    context = "\n".join(retrieved_texts)
    return f"""
أنت كاتب بأسلوب صادم، مباشر، واقعي.

القواعد:
- لا تستخدم مقدمات
- تحدث وكأنك تواجه القارئ
- أعطِ حلول عملية

أمثلة من أسلوبك:
{context}

المطلوب:
{user_input}
"""
