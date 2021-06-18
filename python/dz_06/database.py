import sqlite3
import csv

conn = sqlite3.connect('sber.db')
	
def createTableUser(conn):
	cursor = conn.cursor()
	cursor.execute('''
	CREATE TABLE if not exists user(
		id integer primary key autoincrement,
		name varchar(128),
		lastname varchar(128),
		age integer,
		salary integer,
		start_dttm datetime default current_timestamp,
		end_dttm datetime default (datetime('2999-12-31 23:59:59')),
		deleted_flg default 0
	)
	''')
	cursor.execute('''
	CREATE VIEW if not exists
	v_user as
	select id, name, lastname, age, salary, start_dttm, end_dttm from user
	where deleted_flg = 0;
	''')

def clearTable(conn, tableName):
	cursor = conn.cursor()
	cursor.execute(f"""
	DELETE FROM {tableName};
	""")

	conn.commit()

#Добавляет пользователя
def addUser(conn, name='забыл имя', lastname='забыл фамилию', age='забыл возраст', salary='забыл зп'):
	cursor = conn.cursor()
	cursor.execute('''
		UPDATE user
		set end_dttm = datetime('now', '-1 second')
		where name = ? 
		  and lastname = ?
		  and age = ?
		  and salary = ?
		  and end_dttm = datetime('2999-12-31 23:59:59')
		''', [name, lastname, age, salary])

	cursor.execute('''
	INSERT INTO user (name, lastname, age, salary)
	VALUES(?, ?, ?, ?)''', [name, lastname, age, salary])
	conn.commit()

#Удаляет пользователя по имени и фамилии
def deleteUser(conn, name,  lastname):
	cursor = conn.cursor()
	cursor.execute('''
	UPDATE user
	SET deleted_flg = 1
	WHERE 
		name = ?
		AND
		lastname = ?
	''', [name, lastname])
	conn.commit()

#Показывает данные определенной таблицы
def showTable(conn, tableName):
	cursor = conn.cursor()
	cursor.execute(f'''
		select * from {tableName}
		''')

	for row in cursor.fetchall():
		print(row)


#Возвращает удаленного пользователя
def returnUser(conn, name, lastname):
	cursor = conn.cursor()
	cursor.execute('''
	UPDATE user
	set deleted_flg = 0
	WHERE
		name = ?
		lastname = ?
	''', [name, lastname])
	conn.commit()


#Записывает данные о пользователях на указанную дату
def save2csv(conn, tableName, data='current_timestamp'):
	cursor = conn.cursor()
	with open('result.csv', 'a', newline='') as file:
		cursor.execute(f'''
		select * from {tableName}
		WHERE start_dttm = {data}
		''')
		for row in cursor.fetchall():
			file.write(str(row))
			file.write('\n')
