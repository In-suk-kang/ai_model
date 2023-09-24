# from multiprocessing import Pool, Manager
# from test import ai_model_class
# from new import check_url_in_db, ai_predict

# def multi_processing(input_string):
#     print("multi_process in!")

#     # AI 모델 인스턴스화 (한 번만 인스턴스화)
#     ai_model = ai_model_class()

#     # Manager를 사용하여 공유 큐 생성
#     manager = Manager()
#     return_queue_ai = manager.Queue()
#     return_queue_db = manager.Queue()

#     # 멀티 프로세스 풀 생성
#     with Pool(processes=2) as pool:
#         # check_url_in_db 함수를 멀티 프로세스로 실행하고 결과를 큐에 넣음
#         db_process = pool.apply_async(check_url_in_db, (input_string, return_queue_db))
#         # ai_predict 함수를 멀티 프로세스로 실행하고 결과를 큐에 넣음
#         ai_process = pool.apply_async(ai_predict, (input_string, return_queue_ai))

#         # 결과를 가져옵니다.
#         result_DB = db_process.get()
#         result_AI = ai_process.get()

#     # 반환된 값이 None인 경우를 처리합니다.
#     if result_DB is None:
#         result_DB = (False, "Null")
#     if result_AI is None:
#         result_AI = (False, "Null")

#     print(result_DB, result_AI)

#     if result_DB[1] != "benign":  # db에 해당 url 정보가 존재한다면
#         return result_AI[0], result_AI[1]
#     else:
#         return result_DB[0], result_DB[1]

from multiprocessing import Pool, Manager
from test import ai_model_class
from new import check_url_in_db, ai_predict

def multi_processing(input_string):
    print("multi_process in!")

    # AI 모델 인스턴스화 (한 번만 인스턴스화)
    ai_model = ai_model_class()

    # Manager를 사용하여 공유 큐 생성
    manager = Manager()
    return_queue_ai = manager.Queue()
    return_queue_db = manager.Queue()

    # 멀티 프로세스 풀 생성
    with Pool(processes=2) as pool:
        # check_url_in_db 함수를 멀티 프로세스로 실행하고 결과를 큐에 넣음
        db_process = pool.apply_async(check_url_in_db, (input_string, return_queue_db))
        # ai_predict 함수를 멀티 프로세스로 실행하고 결과를 큐에 넣음
        ai_process = pool.apply_async(ai_predict, (input_string, return_queue_ai))

        # 결과를 가져옵니다.
        result_DB = db_process.get()

        # db_process의 결과가 "benign"인 경우 ai_process를 종료
        if result_DB[1] == "benign":
            pool.terminate()
            pool.join()
            return result_DB[0], result_DB[1]

        result_AI = ai_process.get()

    # 반환된 값이 None인 경우를 처리합니다.
    if result_DB is None:
        result_DB = (False, "Null")
    if result_AI is None:
        result_AI = (False, "Null")

    print(result_DB, result_AI)

    return result_AI[0], result_AI[1]
