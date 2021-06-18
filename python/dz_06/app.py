import sqlite3
from database import addUser, createTableUser, showTable, deleteUser, save2csv, clearTable

conn = sqlite3.connect('sber.db')


createTableUser(conn)
addUser(conn, 'Jo', 'Taro')
addUser(conn, 'Le', 'Ipanio', 2, 112323)
# deleteUser(conn, 'Гайк', 'Инанц')
# deleteUser(conn, 'Гайк2', 'Инанц')

showTable(conn, 'v_user')
save2csv(conn, 'v_user')
clearTable(conn, 'user')
print('----------------')
showTable(conn, 'v_user')