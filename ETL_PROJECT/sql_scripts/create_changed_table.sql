/*
passport_blacklist
*/
CREATE TABLE IF NOT EXISTS	DWH_PASSPORT_BLACKLIST(
	date					date
	,passport				varchar(128)
	,effective_from			datetime DEFAULT current_timestamp
	,effective_to			datetime DEFAULT (datetime('2999-12-31 23:59:59'))
	,deleted_flg			integer DEFAULT 0
);

/*
terminals
*/
CREATE TABLE IF NOT EXISTS	DWH_TERMINALS(
	terminal_id 			varchar(128)
	,terminal_type			varchar(128)
	,terminal_city			varchar(128)
	,terminal_address		varchar(128)
	,effective_from			datetime DEFAULT current_timestamp
	,effective_to			datetime DEFAULT (datetime('2999-12-31 23:59:59'))
	,deleted_flg			integer DEFAULT 0
);

/*
transaction
*/
CREATE TABLE IF NOT EXISTS	DWH_TRANSACTIONS(
	transaction_id			varchar(128)
	,transaction_date		date
	,amount					decimal(10,2)
	,card_num				varchar(128)
	,oper_type				varchar(128)
	,oper_result			varchar(128)
	,terminal				varchar(128)
	,effective_from			datetime DEFAULT current_timestamp
	,effective_to			datetime DEFAULT (datetime('2999-12-31 23:59:59'))
	,deleted_flg			integer DEFAULT 0
);

/*
REP_FRAUD
*/
CREATE TABLE IF NOT EXISTS REP_FRAUD(
	event_dt 	date default current_timestamp
	,passport	varchar(128)
	,fio		varhcar(128)
	,phone		varchar(128)
	,event_type	integer
	,report_dt	date default current_timestamp
);
	