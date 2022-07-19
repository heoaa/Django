from django.http import HttpResponse
import pandas as pd
import cx_Oracle as ora

def getConnection() :
    dsn = ora.makedsn('localhost', 1521, 'orcl')
    conn = ora.connect('busan_06', 'dbdb', dsn)
    return conn

def getCursor(conn) :
    cursor = conn.cursor()
    return cursor

def dbClose(cursor, conn) :
    cursor.close()
    conn.close()
    
# -----------------------------------------------------------


## survey 테이블 생성하기
def createTableSurvey() :
    conn = getConnection()
    cursor = getCursor(conn)
    
    sql = '''
            Create Table survey(
                rnum number(15) not null,
                gender varchar2(20) not null,
                age number(15) not null,
                co_survey varchar2(50) not null,
                Constraint pk_rnum Primary key (rnum)
            )'''
            
    cursor.execute(sql)
    dbClose(cursor, conn)
    
    
## 설문 입력하기
def setSurveyInsert(pgender, page, pco_survey):
    conn = getConnection()
    cursor = getCursor(conn)
    
    # rnum 자동 생성
    sql = '''
            select nvl(max(rnum)+1, 1) as max_no
            from survey
            '''
            
    cursor.execute(sql)
    rs_max_no = cursor.fetchone()
    no = rs_max_no[0]
    
    # 저장하기
    sql = '''
            Insert Into survey (
                rnum, gender, age, co_survey
            ) values (
                :rnum, :gender, :age, :co_survey
            )
            '''
    cursor.execute(sql,
                    rnum = no,
                    gender = pgender,
                    age = page,
                    co_survey = pco_survey)
    conn.commit()
    
    dbClose(cursor, conn)
    return '성공'


def getSurveyList() :
    conn = getConnection()
    cursor = getCursor(conn)
    
    sql = ''' select*from survey '''
    cursor.execute(sql)
    
    row = cursor.fetchall()
    
    colname = cursor.description
    col = []
    for i in colname :
        col.append(i[0].lower())
        
    dbClose(cursor, conn)
    
    # 데이터프레임에 조회 결과 넣기
    df = pd.DataFrame(row, columns=col)
    return df