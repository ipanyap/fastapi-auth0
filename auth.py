from fastapi import APIRouter, Header, Depends, HTTPException

from typing import List, Optional

from jose import jwt
from six.moves.urllib.request import urlopen

import json
import ssl

from pydantic import BaseModel

config_file = open("auth_config.json")
config = json.load(config_file);
config_file.close()

class AccessToken(BaseModel):
	credentials: dict
	scopes: List[str] = []
	
	def hasScope(self, checkedToken):
		if checkedToken in self.scopes:
			return True
		else:
			raise HTTPException(
				status = 403,
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
		jsonurl = urlopen("https://" + config["domain"] + "/.well-known/jwks.json", context = ssl._create_unverified_context())
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
		payload = jwt.decode(authorization, rsa_key, algorithms = ["RS256"], audience = config["audience"], issuer = "https://" + config["domain"] + "/")
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

