import requests
import ollama

def ask_icu_chatbot(patient_id, user_question):
    # 1. جلب البيانات الحقيقية من السيرفر
    response = requests.get(f"http://127.0.0.1:8000/patient/{patient_id}/history")
    data = response.json()
    
    last_log = data['vision_logs'][-1] if data['vision_logs'] else "No data"
    
    # 2. بناء السياق للذكاء الاصطناعي
    prompt = f"""
    You are a medical assistant. Patient Status: 
    Eyes: {last_log.get('eye_state')}, 
    Posture: {last_log.get('posture')}, 
    Person in room: {last_log.get('person_type')}.
    Question: {user_question}
    Answer briefly:
    """
    
    res = ollama.chat(model='llama3', messages=[{'role': 'user', 'content': prompt}])
    return res['message']['content']

# تجربة
# print(ask_icu_chatbot(1, "هل المريض مستيقظ؟"))