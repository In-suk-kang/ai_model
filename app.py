from fastapi import FastAPI
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from model import Model
#from multi import multi_processing
import uvicorn
from db_model import save_url
from new import check_url_and_ai
# 데이터베이스 연결 설정
DATABASE_URL = "mysql+mysqlconnector://root:1q2w3e4r!@localhost/tigerdb"
engine = create_engine(DATABASE_URL)
Base = declarative_base()

# SQLAlchemy 세션 생성
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
db = SessionLocal()

# FastAPI 애플리케이션 생성
app = FastAPI()

# URL 예측 엔드포인트
@app.post("/predict")
async def predict(data: Model):
    input_url = data.url
    AI_output, url_type = check_url_and_ai(input_url)
    print(AI_output,url_type)
    db_data = save_url(ai_output=AI_output, url_type=url_type, url=input_url)
    db.add(db_data)
    db.commit()
    db.close()
    
    return {"predict_result": AI_output, "url_type": url_type, "input_url": input_url}

if __name__ == '__main__':
    # FastAPI 서버 실행
    uvicorn.run(app, host='0.0.0.0', port=8000)

