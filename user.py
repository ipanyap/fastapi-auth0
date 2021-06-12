from typing import List

from pydantic import BaseModel

import json
import psycopg2

import datetime

config_file = open("config.json")
config = json.load(config_file);
config_file.close()

class UserHandle(BaseModel):
	provider: str
	user_id: str
	name: str
	connection: str

class User(BaseModel):
	id: str
	name: str
	username: str
	email: str
	photo: str
	create_date: datetime.datetime = None
	status: int = 1
	identities: List[UserHandle] = []


def connect():
	return psycopg2.connect(
		host = config["db"]["host"],
		database = config["db"]["database"],
		port = config["db"]["port"],
		user = config["db"]["user"],
		password = config["db"]["password"]
	)


def find(id: str):
	conn = connect()
	cur = conn.cursor()
	cur.execute(
		"SELECT name, username, email, photo, create_date, status FROM Users WHERE id = %s",(id,)
	)
	row = cur.fetchone()
	
	if row is None:
		return None
	
	data = User(id = id, name = row[0], username = row[1], email = row[2], photo = row[3], create_date = row[4], status = row[5])
	cur.execute(
		"SELECT handle_provider, handle_user_id, handle_name, handle_connection FROM UserHandle WHERE user_id = %s", (id,)
	)
	rows = cur.fetchall()
	
	cur.close()
	conn.close()
	
	for row in rows:
		data.identities.append(UserHandle(provider = row[0], user_id = row[1], name = row[2], connection = row[3]))
	
	return data

	
def add(user: User):
	conn = connect()
	cur = conn.cursor()
	cur.execute(
		"INSERT INTO Users (id, name, username, email, photo, create_date, status) VALUES (%s, %s, %s, %s, %s, CURRENT_TIMESTAMP, 1);",
		(user.id, user.name, user.username, user.email, user.photo)
	)
	
	for handle in user.identities:
		cur.execute(
			"INSERT INTO UserHandle (user_id, handle_provider, handle_user_id, handle_name, handle_connection) VALUES (%s, %s, %s, %s, %s);",
			(user.id, handle.provider, handle.user_id, handle.name, handle.connection)
		)
	
	conn.commit()
	cur.close()
	conn.close()

