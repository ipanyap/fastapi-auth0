from fastapi import Header, Depends, HTTPException
from fastapi.security import APIKeyCookie

from typing import List

from jose import jwt
from six.moves.urllib.request import urlopen

import json
import ssl

from starlette.responses import Response
from pydantic import BaseModel

import user

config_file = open("config.json")
config = json.load(config_file);
config_file.close()

cookie_sec = APIKeyCookie(name="session")

class AccessToken(BaseModel):
	credentials: dict
	scopes: List[str] = []
	
	def hasScope(self, checkedToken):
		if checkedToken in self.scopes:
			return True
		else:
			raise HTTPException(
				status_code = 403,
				detail = "Not authorized to perform this action"
			)


def accessToken(authorization: str = Header(None)):
	if not authorization:
		raise HTTPException(
			status_code = 403,
			detail = "Access Denied"
		)

	try:
	
		#1. Get jwks
		jsonurl = urlopen("https://" + config["auth0"]["domain"] + "/.well-known/jwks.json", context = ssl._create_unverified_context())
		unverified_header = jwt.get_unverified_header(authorization)
		unverified_claims = jwt.get_unverified_claims(authorization)
		jwks = json.loads(jsonurl.read())
		rsa_key = {}
		for key in jwks["keys"]:
			if key["kid"] == unverified_header["kid"]:
				rsa_key = {
					"kty": key["kty"],
					"kid": key["kid"],
					"use": key["use"],
					"n": key["n"],
					"e": key["e"]
				}
			
		#3. Decode token
		payload = jwt.decode(authorization, rsa_key, algorithms = ["RS256"], audience = config["auth0"]["audience"], issuer = "https://" + config["auth0"]["domain"] + "/")
		returnedToken = AccessToken(credentials = payload, scopes = unverified_claims["scope"].split(" "))
		return returnedToken
		
	except jwt.ExpiredSignatureError:
		raise HTTPException(
			status_code = 401,
			detail = "Token is expired"
		)
		
	except jwt.JWTError:
		raise HTTPException(
			status_code = 401,
			detail = "Wrong credentials"
		)


def currentUser(session: str = Depends(cookie_sec)):
	if not session:
		raise HTTPException(
			status_code = 403,
			detail = "No valid session found"
		)
	
	try:
		payload = jwt.decode(session, config["session"]["secret"])
		user_id = payload["sub"]
		
		return user.find(user_id)
	except Exception:
		raise HTTPException(
			status_code = 403,
			detail = "Invalid authentication"
		)


def createSession(response: Response, user_id: str):
	token = jwt.encode({"sub": user_id}, config["session"]["secret"])
	response.set_cookie("session", token)

	
def destroySession(response: Response):
	response.delete_cookie("session")


