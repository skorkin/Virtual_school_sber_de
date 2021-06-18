import sqlite3
import json
conn = sqlite3.connect('sber.db')

def createTableClient(conn):
	cursor = conn.cursor()
	try:
		cursor.execute("""
		CREATE TABLE client(
		name varchar (128),
		lastname varchar (128),
		age int default 0
		)
	""")
	except sqlite3.OperationalError as e:
		print ('Таблица уже существует')

	conn.commit()

def addClient(conn, name, lastname, age):
	cursor = conn.cursor()
	cursor.execute("""
	INSERT INTO client(name, lastname, age)
	VALUES (?, ?, ?);
	""", [name, lastname, age])

	conn.commit()

def addClients(conn,users):
	cursor = conn.cursor()
	cursor.executemany("""
	INSERT INTO client(name, lastname, age)
	VALUES (?, ?, ?);
	""", users)

	conn.commit()

def getData(conn, tableName):
	cursor = conn.cursor()
	cursor.execute(f"select * from {tableName};")
	result = cursor.fetchall()
	print('_-'*20)
	print(tableName)
	print('_-'*20)
	for row in result:
		print (row)

def addUniqineClient(conn, name, lastname, age):
	cursor = conn.cursor()
	cursor.execute(f"""
		select
			*
		from client
		where name = ?
		and lastname = ?;""", [name, lastname])

	if len(cursor.fetchall()) == 0:
		cursor.execute("""
		INSERT INTO client (name, lastname, age)
				VALUES (?, ?, ?);
		""", [name, lastname, age])
		
		conn.commit()

def	clearTable(conn, tableName):
	cursor = conn.cursor()
	cursor.execute(f"""
	DELETE FROM {tableName};
	""")

	conn.commit()

def addClientFromFile(conn, path):
	cursor = conn.cursor()
	with open(path, 'r') as f:
		data = json.loads(f.read())

		for row in data:
			addUniqineClient(conn, row['name'], row['lastname'], row['age'])

def avgClientsAge(conn, tableName):
	cursor = conn.cursor()
	cursor.execute(f"""
	SELECT avg(age) FROM {tableName};
	""")
	res = cursor.fetchall()
	return (res)