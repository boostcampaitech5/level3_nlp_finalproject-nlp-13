from distutils.log import INFO
from hashlib import new
import pymongo
import re
from datetime import datetime

db_api=""
client = pymongo.MongoClient(db_api)
db = client.boostcamp
collection = db.users
    
def check(id_info):
    """
    DB에 해당 유저가 있는지 확인하는 함수
    user가 없다면 새로 저장하기
    id_info : google token
    """
    user = collection.find_one({'email': id_info['email']})

    if not user:
        # 새 user 저장
        user_data = {
            'email': id_info['email'],
            'name': id_info['name'],
        }
        collection.insert_one(user_data)

def attendance(target_email):
    new_date=datetime.today() 
    existing_data = collection.find_one({'email': target_email})
    # 이미 해당 id에 대한 document가 존재하는 경우
    if existing_data:
        # 'date' 필드가 이미 존재하는지 확인합니다.
        if 'date' in existing_data:
            # 'date' 필드에 새로운 날짜를 추가합니다.
            existing_data['date'].append(new_date)
        else:
            # 'date' 필드가 존재하지 않으면 새로 생성합니다.
            existing_data['date'] = [new_date]

        # 업데이트된 document를 저장합니다.
        collection.update_one({'email': target_email}, {'$set': existing_data})