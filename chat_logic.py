chat_history = []

async def get_chatbot_response(user_query, patient_id):
    global chat_history
    
    # 1. جلب بيانات المريض من الـ API
    history_data = requests.get(f"http://127.0.0.1:8000/patient/{patient_id}/history").json()
    
    # 2. إعداد السياق للـ LLM (Mistral)
    context = f"بيانات المريض الحالية: {history_data['vision_logs'][-1]}"
    
    # 3. منطق التلخيص كل 10 رسائل
    if len(chat_history) >= 10:
        summary = "تم تلخيص آخر 10 رسائل لضمان دقة النظام..." # هنا يتم استدعاء LLM للتلخيص
        chat_history = [summary]
    
    chat_history.append(user_query)
    # استدعاء Ollama هنا لإعطاء الرد النهائي
    return f"الرد بناءً على البيانات: المريض مستقر وحالته {history_data['vision_logs'][-1]['posture']}"