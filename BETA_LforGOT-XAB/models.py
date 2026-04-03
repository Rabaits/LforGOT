import os
from ollama import chat

os.environ["OLLAMA_API_KEY"] = "05d4fe56b0ca49d1938f29e01a812d42.-FmDAW-Gwg-vgHryhu1XqnP1"

MODEL_NAME = "rugemma3"

def AI_return(request_user: str) -> str:
    """Быстрый ответ на запрос"""
    try:
        # Проверяем, что запрос не пустой
        if not request_user or not request_user.strip():
            return "Пожалуйста, задайте вопрос."
        
        response = chat(
            model=MODEL_NAME,
            messages=[
                {
                    "role": "system", 
                    "content": "Ты полезный ассистент. Отвечай кратко и по делу."
                },
                {
                    "role": "user", 
                    "content": request_user
                }
            ],
            options={
                "num_predict": 150,  # Увеличил для более полных ответов
                "temperature": 0.7,   # Немного увеличил для разнообразия
                "top_p": 0.9,
                "stop": ["\n\n"]      # Останавливаем генерацию при двойном переносе строки
            }
        )
        
        # Проверяем, есть ли ответ
        if response and response.message and response.message.content:
            return response.message.content.strip()
        else:
            return "Не удалось получить ответ от модели."
        
    except Exception as e:
        return f"Ошибка: {e}"

# Для тестирования
if __name__ == "__main__":
    test_question = "Привет, как дела?"
    result = AI_return(test_question)
    print(f"Вопрос: {test_question}")
    print(f"Ответ: {result}")