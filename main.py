from typing import Optional

from fastapi import FastAPI, Depends, HTTPException

import auth

app = FastAPI()

@app.get("/")
def read_root():
	return {"message": "Hello World"}

@app.get("/signup/")
def sign_up(token:auth.accessToken = Depends(auth.accessToken)):
	return {"message": "You are signing up", "token": token}

@app.get("/login/")
def sign_up(token:auth.accessToken = Depends(auth.accessToken)):
	return {"message": "You are logging in", "token": token}

@app.get("/logout/")
def sign_up(token:auth.accessToken = Depends(auth.accessToken)):
	return {"message": "You are logging out", "token": token}

@app.get("/logstatus/")
def sign_up(token:auth.accessToken = Depends(auth.accessToken)):
	return {"message": "You are checking login status", "token": token}