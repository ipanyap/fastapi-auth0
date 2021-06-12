from typing import Optional

from fastapi import Body, FastAPI, Depends, HTTPException

from starlette.responses import Response
from pydantic import BaseModel

import auth
import user

class ResponseMessage(BaseModel):
	status: bool = True
	message: str

app = FastAPI()

@app.get("/", response_model = ResponseMessage)
def read_root():
	return ResponseMessage(message = "Hello World")


@app.post("/signup/", response_model = ResponseMessage)
def sign_up(body: user.User = Body(...), token: auth.accessToken = Depends(auth.accessToken)):
	user.add(body)
	
	return ResponseMessage(message = "New user successfully signed up")


@app.post("/login/", response_model = ResponseMessage)
def log_in(response: Response, id: str = Body(..., embed = True), token: auth.accessToken = Depends(auth.accessToken)):
	if not id:
		raise HTTPException(
			status_code = 400,
			detail = "Bad request"
		)
	
	data = user.find(id)
	if data is None:
		raise HTTPException(
			status_code = 403,
			detail = "Invalid user"
		)
	
	auth.createSession(response, id)
	
	return ResponseMessage(message = "You are successfully logged in as " + data.username)


@app.post("/logout/", response_model = ResponseMessage)
def log_out(response: Response, token: auth.accessToken = Depends(auth.accessToken)):
	auth.destroySession(response)
	
	return ResponseMessage(message = "You are successfully logged out")


@app.get("/logstatus/", response_model = ResponseMessage)
def log_status(user: user.User = Depends(auth.currentUser), token: auth.accessToken = Depends(auth.accessToken)):
	if user is None:
		return ResponseMessage(message = "You are not logged in", status = False)
	
	return ResponseMessage(message = "You are logged in as " + user.username, status = True)
