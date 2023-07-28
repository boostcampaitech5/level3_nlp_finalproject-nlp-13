from distutils.log import INFO
from hashlib import new
import pymongo
import re
from datetime import datetime, timedelta
import yaml
import os.path
from os import path

with open('api.yaml') as f:
    db_key = yaml.load(f, Loader=yaml.FullLoader)

client = pymongo.MongoClient(db_key['mongo_client'])
db = client.boostcamp
collection = db.users
print("got client")

def check(id_info):
    """
    id_info : email and name
    Check if the email is in the database, and if it is a new user, save the info in the database
    """
    user = collection.find_one({'email': id_info['email']})
    #print(user)

    if not user:
        user_data = {
            'email': id_info['email'],
            'name': id_info['name'],
        }
        collection.insert_one(user_data)
    #print("compelte check")

def attendance(target_email):
    new_date=datetime.now().date() #today's date
    #print(new_date)

    #Check whether the email is in the database
    existing_data = collection.find_one({'email': target_email})
    new_date = new_date.strftime("%Y-%m-%d") #datetime to string
    
    if existing_data:
        if 'date' in existing_data:
            #If it is the first visit of the day, add new date
            if collection.find_one({'email': target_email,"date":new_date})==None:
                existing_data['date'].append(new_date)
        else:
            #Create a date field
            existing_data['date'] = [new_date]

        #update the document
        collection.update_one({'email': target_email}, {'$set': existing_data})
    #print("attendance complete")
    return heatmap(target_email)

def heatmap(target_email):
    today = datetime.now().date() #todays's date
    days=99 #99
    start = today + timedelta(days = -days)
    new = []

    #today ~ days ago
    for i in range(0,days+1):
        tmp_date = start + timedelta(days = i)
        tmp_date = tmp_date.strftime("%Y-%m-%d")
        if collection.find_one({'email': target_email,"date":tmp_date}):
            new.append(True)
        else:
             new.append(False)

    #print("heatmap days complete")
    return new

if __name__ == '__main__':
    info={'email':'email','name':'hi'}
    check(info)
    attendance(info['email'])
    print(heatmap(info['email']))