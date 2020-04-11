create database pytest;
use pytest;
#drop table ti_test;

create table ti_test;

insert into ti_test values(5,'Test5',curdate(),'This is a test data');
commit;
select * from ti_test;

create database loans;
use loans;

drop table cust_loans;
drop table customers;
drop table loan_table_lookup;



create table loan_table_lookup(
	loan_mdm_lookup_id	int
,CreditScoreMin			int
,CreditScoreMax			int
,LoanAmountMin			int
,LoanAmountMax			int
,InterestRatePct		decimal(4,2)
,DurationMonths			int
,eff_from_date			date
,eff_to_date			date
);

alter table loan_table_lookup add constraint loan_table_lookup_pk primary key(loan_mdm_lookup_id);

create table customers(
	cust_id				int
    ,cust_name			varchar(20)
    ,cust_address 		varchar(20)
    ,cust_contact		varchar(20)
    ,cust_credit_score	int
); 

alter table customers add constraint customers_pk primary key(cust_id);

create table cust_loans(
	cust_loan_id			int
    ,loan_mdm_lookup_id		int
    ,cust_id 				int
    ,req_date				date
    ,req_loan_amount		decimal(8,2)
    ,req_DurationMonths		int
    ,approved_loan_amount	decimal(8,2)
    ,approved_DurationMonths	int
    ,application_status		varchar(20)
    ,application_notes		text
); 
alter table cust_loans add constraint cust_loan_pk primary key(cust_loan_id);
alter table cust_loans add constraint FK_loan_mdm foreign key(loan_mdm_lookup_id) references loan_table_lookup(loan_mdm_lookup_id);
alter table cust_loans add constraint FK_cust foreign key(cust_id) references customers(cust_id);


select * from loan_table_lookup;










