import sqlite3

# Занесение 1-го типа мошенничества
def search_fraud_1_type(conn):
	cursor = conn.cursor()
	
	cursor.execute('''
	insert into REP_FRAUD
	(event_dt, passport, fio, phone, event_type, report_dt)
	select
	distinct
		TRANS.trans_date
		,CLIENT.passport_num
		,CLIENT.last_name || ' ' || CLIENT.first_name 
		,CLIENT.phone
		,'Совершение операции при просроченном или заблокированном паспорте.'
		,current_timestamp
	from V_TRANSACTIONS TRANS
		left join cards							on TRANS.card_num = cards.card_num
		left join accounts ACC					on cards.account = ACC.account
		left join clients client				on ACC.client = CLIENT.client_id
		left join V_PASSPORT_BLACKLIST as PB	on CLIENT.passport_num = PB.passport_num
	where 
		(
			(
				PB.entry_dt not NULL 
				and PB.entry_dt <= TRANS.trans_date
			)
			or 
			(
				CLIENT.passport_valid_to <= TRANS.trans_date 
				and CLIENT.passport_valid_to not NULL
			)
		)
		and (TRANS.trans_date || CLIENT.passport_num) not in (select event_dt || passport from REP_FRAUD)
		order by CLIENT.last_name || ' ' || CLIENT.first_name
	''')
	conn.commit()

# Занесение 2-го типа мошенничества
def search_fraud_2_type(conn):
	cursor = conn.cursor()
	cursor.execute('''
	insert into REP_FRAUD
	(event_dt, passport, fio, phone, event_type, report_dt)
	select
	distinct
		TRANS.trans_date
		,CLIENT.passport_num
		,CLIENT.last_name || ' ' || CLIENT.first_name 
		,CLIENT.phone
		,'Совершение операции при недействующем договоре.'
		,current_timestamp
	from V_TRANSACTIONS TRANS
		left join cards							on TRANS.card_num = cards.card_num
		left join accounts ACC					on cards.account = ACC.account
		left join clients client				on ACC.client = CLIENT.client_id
		left join V_PASSPORT_BLACKLIST as PB	on CLIENT.passport_num = PB.passport_num
	where
		ACC.valid_to is not NULL
		and ACC.valid_to <= TRANS.trans_date
		and (TRANS.trans_date || CLIENT.passport_num) not in (select event_dt || passport from REP_FRAUD)
	order by CLIENT.last_name || ' ' || CLIENT.first_name
	''')
	conn.commit()


# Занесение 3-го типа мошенничества
def search_fraud_3_type(conn):
	cursor = conn.cursor()
	
	cursor.executescript('''
		drop table if exists test_03;

		create table test_03 as
		select
		distinct
			TRANS.trans_date
			,CLIENT.passport_num
			,CLIENT.last_name || ' ' || CLIENT.first_name as name
			,CLIENT.phone
			,term.terminal_city
		from V_TRANSACTIONS TRANS
		left join V_TERMINALS as term on TRANS.terminal = term.terminal_id
		left join cards on TRANS.card_num = cards.card_num
		left join accounts ACC on cards.account = ACC.account
		left join clients client on ACC.client = CLIENT.client_id
		group by CLIENT.passport_num;

		insert into REP_FRAUD
		(event_dt, passport, fio, phone, event_type, report_dt)
		select
			t1.trans_date
			,t1.passport_num
			,t1.name
			,t1.phone
			,'Совершение операций в разных городах в течение одного часа.'
			,current_timestamp
		from test_03 t1
		inner join test_03 t2
		on (t1.name = t2.name and t1.terminal_city != t2.terminal_city)
		where
			abs((julianday(t1.trans_date) - julianday(t2.trans_date)) * 24 * 60) <= 60
			and (t1.trans_date || t1.passport_num) not in (select event_dt || passport from REP_FRAUD);
		
		drop table if exists test_03;
	''')

	conn.commit()

# Занесение 4-го типа мошенничества
def search_fraud_4_type(conn):
	cursor = conn.cursor()

	cursor.executescript('''
	insert into REP_FRAUD
	(event_dt, passport, fio, phone, event_type, report_dt)
	select
		trans_date
		,passport_num
		,name
		,phone
		,'Попытка подбора суммы. В течение 20 минут проходит более 3х операций.'
		,current_timestamp
	FROM 
	(
	select
	distinct
		TRANS.trans_date
		,lag(trans_date, 1, '2999-12-31 23:59:59')
			over (partition by passport_num
			order by trans_date) as data_min_one
		,lag(trans_date, 2, '2999-12-31 23:59:59')
			over (partition by passport_num
			order by trans_date) as data_min_two
		,CLIENT.passport_num
		,CLIENT.last_name || ' ' || CLIENT.first_name as name
		,CLIENT.phone
		,TRANS.amt
		,lag(amt, 1, amt)
			over (partition by passport_num
			order by trans_date) as amt_min_one
		,lag(amt, 2, amt)
			over (partition by passport_num
			order by trans_date) as amt_min_two
		,TRANS.oper_result
		,lag(oper_result, 1, 'SUCCESS')
			over (partition by passport_num
			order by trans_date) as res_min_one
		,lag(oper_result, 2, 'SUCCESS')
			over (partition by passport_num
			order by trans_date) as res_min_two
 	from V_TRANSACTIONS TRANS
 	left join V_TERMINALS as term on TRANS.terminal = term.terminal_id
 	left join cards on TRANS.card_num = cards.card_num
 	left join accounts ACC on cards.account = ACC.account
 	left join clients client on ACC.client = CLIENT.client_id
)
	where
		amt - amt_min_one < 0
		and amt_min_one - amt_min_two < 0
		and oper_result = 'SUCCESS'
		and res_min_one = 'REJECT'
		and res_min_two = 'REJECT'
		and (abs(julianday(trans_date) - julianday(data_min_two)) * 24 * 60 < 20)
		and (trans_date || passport_num) not in (select event_dt || passport from REP_FRAUD)
	order by name, trans_date;
''')

	conn.commit()


# Занесение всех 4-х типов мошенничества
# Будут добавлены только те операции
# Которых еще нет в отчете
def fraud_all(conn):
	cursor = conn.cursor()

	search_fraud_1_type(conn)
	search_fraud_2_type(conn)
	search_fraud_3_type(conn)
	search_fraud_4_type(conn)
	conn.commit()