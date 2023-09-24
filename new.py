# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker
# from sqlalchemy.ext.declarative import declarative_base
# from test import ai_model_class
# # app 모듈에서 필요한 클래스와 함수만 가져오기
# from db_model import URLInfo,save_url
# # 데이터베이스에서 URL 확인 함수
# def check_url_in_db(url,return_queue):
#     DATABASE_URL = "mysql+mysqlconnector://root:1q2w3e4r!@localhost/tigerdb"
#     engine = create_engine(DATABASE_URL)
#     Base = declarative_base()

#     Base.metadata.create_all(bind=engine)

#     SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
#     db = SessionLocal()

#     malicious = False
#     url_type = "Null"

#     # 데이터베이스에서 URL 검색
#     #db_url = db.query(URLInfo).filter(URLInfo.url == url or URLInfo.url == url.lstrip("www.")).first()
#     # save_url = db.query(ai_model_class.saved_url).filter(ai_model_class.saved_url.ai_output == 0 and (ai_model_class.saved_url.url == url or ai_model_class.saved_url.url == url.lstrip("www."))).first()

#     results = db.query(URLInfo).all()
#     for result in results:
#         if (result.url == url or result.url == url.lstrip("www.")):
#             malicious = False
#             url_type = "benign"
#             break

#     results = db.query(save_url).all()
#     for result in results:
#         if (result.url == url or result.url == url.lstrip("www.")):
#             malicious = result.ai_output
#             url_type = result.url_type
#             print(malicious,url_type)
#             break
#     # # URL이 데이터베이스에 있는 경우 "benign"으로 표시
#     # if db_url:
#     #     malicious = False
#     #     url_type = "benign"

#     # 세션 닫기
#     db.close()
#     return (malicious,url_type)

# def ai_predict(input_string, return_queue):
#     ai_model = ai_model_class()
#     ai_result = ai_model.predict_results(input_string)[0]
#     malicious = ''
#     if ai_result != "benign":
#         malicious = True
#     else:
#         malicious = False
#     return (malicious,ai_result)
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from test import ai_model_class
from db_model import URLInfo, save_url

def check_url_and_ai(url):
    DATABASE_URL = "mysql+mysqlconnector://root:1q2w3e4r!@localhost/tigerdb"
    engine = create_engine(DATABASE_URL)
    Base = declarative_base()

    Base.metadata.create_all(bind=engine)

    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()

    ai_model = ai_model_class()
    ai_result = ai_model.predict_results(url)[0]
    malicious = ''
    url_type = ''

    # 데이터베이스에서 URL 검색
    results = db.query(URLInfo).all()
    for result in results:
        if (result.url == url or result.url == url.lstrip("www.")):
            malicious = False
            url_type = "benign"
            break

    results = db.query(save_url).all()
    for result in results:
        if (result.url == url or result.url == url.lstrip("www.")):
            malicious = result.ai_output
            url_type = result.url_type
            break

    return malicious,url_type
    # 세션 닫기


# 사용 예시:

