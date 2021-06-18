import sqlite3
from database import addUniqineClient, getData, addClient, addClients, addClientFromFile, clearTable, createTableClient, avgClientsAge

conn = sqlite3.connect('sber.db')
cursor = conn.cursor()

#Создание таблицы
createTableClient(conn)

#Добавление уникальных клиентов
addUniqineClient(conn, 'name', 'lastname', 20)

#Добавление уникальных пользователей из json
addClientFromFile(conn, 'client.json')
getData(conn, 'client')

#Средний возраст
res = avgClientsAge(conn, 'client')
print(res)