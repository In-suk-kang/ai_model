from fastapi import FastAPI
from model import Model
from test import model_process_example,ai_model_class
import uvicorn
app = FastAPI()
ai_model = ai_model_class()

@app.post("/predict")
def predict(data: Model):
    input_url = data.url

    # URL을 벡터로 변환하는 작업 (비동기 함수)
    predict_result = ai_model.predict_results(input_url)
    return {"predict_result": predict_result[0], "input_url": input_url}

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)
