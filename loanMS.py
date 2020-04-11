import csv
import pymysql as sql


def getDBConnCursor():
    conn=sql.connect(host='localhost',port=3306,user='root',password='Dirtydula1$', db='loans')
    cursor=conn.cursor()
    return cursor,conn

def LoadLoanMDdata():
    cursor,conn=getDBConnCursor()
    sql_script='INSERT INTO loan_table_lookup( loan_mdm_lookup_id, CreditScoreMin, CreditScoreMax, LoanAmountMin, LoanAmountMax, InterestRatePct, DurationMonths) VALUES'
    with open('D:\PythonLoanManagmentProjectMaster\loanmdm.csv') as csv_file:
        csv_reader=csv.reader(csv_file,delimiter=',')
        print("######### ADDING FIELDS INTO THE MYSQL DATABASE FROM CSV USING PYTHON")
        for row in csv_reader:
            print(row)
            print(sql_script+'('+row[0]+','+row[1]+','+row[2]+','+row[3]+','+row[4]+','+row[5]+','+row[6]+');')
            cursor.execute(sql_script+'('+row[0]+','+row[1]+','+row[2]+','+row[3]+','+row[4]+','+row[5]+','+row[6]+');')
        print("#########PRINT ALL THE FIELDS FROM THE DATABSE USING SELECT * IN PYTHON#############")
        cursor.execute('select * from loan_table_lookup')
        res=cursor.fetchall()
        print(res)
        return res
    conn.commit()
    cursor.close()
    conn.close()
LoadLoanMDdata()
def ChangeLoanMDdata():
    previous_result=LoadLoanMDdata()
    master_data=[]
    for row in previous_result:
        student = {"ID": row[0], "MinCredit": row[1], "MaxCredit": row[2],"MinLoan":row[3],"MaxLoan":row[4]}
        master_data.append(student)
    master=tuple(master_data)
    print("########## CONVERTING THE DATABASE FIELD ENTRY INTO A DICTIONARY INSIDE A TUPLE###########")
    print(master)
    return master

ChangeLoanMDdata()

def LoanProcessingMachine(p_input):
    start_data=ChangeLoanMDdata()
    print("####### ENTERING CUSTOMER INFORMATION AND RETRIEVING THE DATA ##########")
    for l_data in start_data:
        if p_input["CustomerCreditScore"] >= l_data["MinCredit"] and p_input["CustomerCreditScore"] <= l_data["MaxCredit"]:
            if p_input["RequestedLoanAmount"] >= l_data["MinLoan"] and p_input["RequestedLoanAmount"] <= l_data["MaxLoan"]:
                print("ID:", l_data["ID"], "\n", "Credit score Minimum:", l_data["MinCredit"], "\n","Credit score Maximum:", l_data["MaxCredit"], "\n", "Customer Credit score:",p_input["CustomerCreditScore"])
                print("Congrats on the transaction", p_input["Custname"], ".\n")
        elif p_input["CustomerCreditScore"] < 100:
            print("Loan has been rejected")

input_1 = {"Custname": "AAA", "CustomerCreditScore": 332, "RequestedLoanAmount": 15000}
LoanProcessingMachine(p_input=input_1)

def UpdateLoadData(loan_mdm_lookup_id,st_date,ed_date):
    cursor, conn = getDBConnCursor()
    b=""
    if isinstance(loan_mdm_lookup_id,list):
        for c in loan_mdm_lookup_id:
            b=b+str(c)+","
        b=b.rstrip(",")
    else:
        b=str(loan_mdm_lookup_id)
    print(b)
    l_update=""
    try:
        l_update="""update  loan_table_lookup
                    set     eff_from_date = str_to_date('"""+st_date+"""','%Y%m%d')
                           ,eff_to_date = str_to_date('"""+ed_date+"""','%Y%m%d')
                    where   loan_mdm_lookup_id in ( """ + b + ');'
    except:
        print("No updates")
    print(l_update)

    cursor.execute(l_update)
    conn.commit()
    cursor.close()
    conn.close()
next_set=list(range(6,17))
UpdateLoadData(1,"20200101","30000101")
UpdateLoadData([1,2,3,4,5],"20200101","30000101")
UpdateLoadData(next_set,"20200101","30000101")
UpdateLoadData([5,6],"30200101","40000101")

def GetAllLoanMD(i_creditScore,i_loanAmt):
    cursor, conn = getDBConnCursor()
    l_sql = """select loan_mdm_lookup_id,CreditScoreMin,CreditScoreMax
                       ,LoanAmountMin,LoanAmountMax,InterestRatePct,DurationMonths
                from   loan_table_lookup
                where curdate() between eff_from_date and eff_to_date 
                and   """ + str(i_creditScore) + """ between CreditScoreMin and CreditScoreMax 
                and   """ + str(i_loanAmt) + """ between LoanAmountMin and LoanAmountMax;"""

    cursor.execute(l_sql)
    print("Requested Loan Amount:", str(i_loanAmt), "  CreditScore:", str(i_creditScore))
    print("Availabe Options")
    print("loan_mdm_lookup_id".ljust(20, ' ') + "CreditScoreMin".ljust(20, ' ') + "CreditScoreMax".ljust(20,' ') + "LoanAmountMin".ljust(20, ' ') + "LoanAmountMax".ljust(20, ' ') + "IntrestRatePct".ljust(20, ' ') + "DurationMonths".ljust(20, ' '))
    for loan_mdm_lookup_id, CreditScoreMin, CreditScoreMax, LoanAmountMin, LoanAmountMax, IntrestRatePct, DurationMonths in cursor.fetchall():
        print(str(loan_mdm_lookup_id).ljust(20, ' ')
              , str(CreditScoreMin).ljust(20, ' ')
              , str(CreditScoreMax).ljust(20, ' ')
              , str(LoanAmountMin).ljust(20, ' ')
              , str(LoanAmountMax).ljust(20, ' ')
              , str(IntrestRatePct).ljust(20, ' ')
              , str(DurationMonths).ljust(20, ' '))

    cursor.close()
    conn.close()

GetAllLoanMD(300,18000)