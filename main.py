from typing import Union
from fastapi import FastAPI
from pydantic import BaseModel
from sllm2 import getAiSales
from ai_chatbot import getChatbotAnswer
import json
app = FastAPI()

# 요청 모델 정의
class Question(BaseModel):
    pd_name : str
    detail: str

# 응답 모델 정의
class Answer(BaseModel):
    salestitle: str
    detail: str

    # 응답 모델 정의
class ChatBotAnswer(BaseModel):
    answer : str

@app.post("/askaisales", response_model=Answer)
async def ask_question(question: Question):
    try:
        response = json.loads(getAiSales("아래 내용을 바탕으로 판매글을 작성해줘.\n" + "제목 : " + question.pd_name + "\n" + question.detail))
        
        # response를 파싱하여 적절한 형식으로 변환
        # response_data = json.load(response)  # JSON 문자열을 파이썬 딕셔너리로 변환
        # response_data = {"salestitle": "a", "detail": "d"}  # 예시 데이터
        
        answer = Answer(**response)
        return answer

    except Exception as e:
        print(e)
        return {"error": str(e)}
    

@app.get("/askaichatbot", response_model=ChatBotAnswer)
async def ask_question(message: str = "질문을 다시 해주세요라고 답변해줘"):
    try:
        response = json.loads(getChatbotAnswer(message))
        
        answer = ChatBotAnswer(**response)
        return answer

    except Exception as e:
        print(e)
        return {"error": str(e)}
    

# FastAPI 애플리케이션 실행 (uvicorn 사용)
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8003)
