import sqlite3
import sys
import os
import zipfile
from py_scripts import create_view
from py_scripts import incr_terminals
from py_scripts import incr_transactions
from py_scripts import incr_passport_blacklist
from py_scripts import fraud_check
from py_scripts import utils

sys.path.append("py_scripts/") 
conn = sqlite3.connect("sber.db")
cursor = conn.cursor()



def get_day(conn, file_path_passp, file_path_term, file_path_trans):
	# Выполняет загрузку
	incr_terminals.incr(conn, file_path_term)
	incr_transactions.incr(conn, file_path_trans)
	incr_passport_blacklist.incr(conn, file_path_passp)
	# Делает отчет
	fraud_check.fraud_all(conn)
	# Переименовывает
	os.rename(file_path_term, file_path_term [:-5] +  '.backup')
	os.rename(file_path_trans, file_path_trans [:-4] + '.backup')
	os.rename(file_path_passp, file_path_passp [:-5] + '.backup')


# Парсит .zip Архив
# Раскидывает файлы по спискам
# В цикле закидывает пути до файлов в функцию get_date
def get_3_days_from_data_archive(conn):
	passport_list = []
	transactions_list = []
	terminals_list = []

	file_list  = os.listdir('data')
	for i in file_list:
		if (i.find('passport') + 1) and (i.find('.xlsx') + 1):
			passport_list.append('data/' + i)
		if (i.find('transactions') + 1) and (i.find('.txt') + 1):
			transactions_list.append('data/' + i)
		if (i.find('terminals') + 1) and (i.find('.xlsx') + 1):
			terminals_list.append('data/' + i)
	for i in range(0,3):
		get_day(conn, passport_list[i], terminals_list[i], transactions_list[i])


create_view.create_all_view(conn)
cursor.executescript(' drop table if exists DWH_TRANSACTIONS')


utils.use_sql_script(conn, 'sql_scripts/create_changed_table.sql')
utils.use_sql_script(conn, 'sql_scripts/ddl_dml.sql')

#Проверка на архив в папке data
if (os.listdir('data')[1].find('.zip') + 1):
	z = zipfile.ZipFile('data/' + os.listdir('data')[1], 'r')
	z.extractall('data/')
	z.close()
	
	get_3_days_from_data_archive(conn)
#иначе проверка базовых файлов
else :
	get_day(conn, 'data/passport_blacklist_01032021.xlsx', 'data/terminals_01032021.xlsx', 'data/transactions_01032021.txt')
	get_day(conn, 'data/passport_blacklist_02032021.xlsx', 'data/terminals_02032021.xlsx', 'data/transactions_02032021.txt')
	get_day(conn, 'data/passport_blacklist_03032021.xlsx', 'data/terminals_03032021.xlsx', 'data/transactions_03032021.txt')
