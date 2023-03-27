# Code to demonstrate Synchronous REST Api - with the data stored in JSON file
# Demonstrated for GET, GET ID, POST, PUT AND DELETE HTTP Methods
# URL to run -> http://localhost:8000/docs which opens the Swagger API documentation
# Run Uvicorn - uvicorn main:app --reload

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
import json

app = FastAPI()

class User(BaseModel):
    id: Optional[int] = None
    name: str
    email: str
    address:str
    mobile:int


import os

here = os.path.dirname(os.path.abspath(__file__))
filename = os.path.join(here, 'user.json')

with open(filename,'r') as f:
    user = json.load(f)['user']
    

@app.get('/')
def getAllUsers():
    return user


@app.get('/users/{u_id}', status_code=200)
def get_user(u_id: int):
    userObj = [u for u in user if u['id'] == u_id]
    return userObj[0] if len(userObj) > 0 else {}


@app.post('/users', status_code=201)
def new_user(userObj: User):
    u_id = int(max([u['id'] for u in user])) + 1
    #u_id = 5
    new_user = {
        "id" : u_id,
        "name" : userObj.name,
        "email" : userObj.email,
        "address" : userObj.address,
        "mobile" : userObj.mobile
    }
    user.append(new_user)

    with open(filename,'w') as f:
        json.dump(user,f)

    return new_user

@app.delete('/users/{u_id}',status_code=202)
def delete_user(u_id: int):
    try:
        userList = [u for u in user if u['id'] == u_id]
        if len(userList) > 0:
            user.remove(userList[0])
            with open(filename,'w') as f:
                json.dump(user,f)
        else:
            raise HTTPException(status_code=404, detail=f"There is no User with id as {u_id}")
    except:
        print('Exception occurred')

@app.put('/users', status_code=204)
def change_user(userObj: User):
    new_user = {
        "id" : userObj.id,
        "name" : userObj.name,
        "email" : userObj.email,
        "address" : userObj.address,
        "mobile" : userObj.mobile
    }

    user_list = [u for u in user if u['id'] == userObj.id]
    if(len(user_list) > 0):
        user.remove(user_list[0])
        user.append(new_user)
        with open(filename,'w') as f:
            json.dump(user,f)
        return new_user
    else:
        return HTTPException(status_code=404, detail=f"User with id {userObj.id} does not exist")
