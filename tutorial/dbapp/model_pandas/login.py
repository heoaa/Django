import pandas
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
    
    
# <실제 사용 함수>------------------------------------------


# 한건 행 딕셔너리 만드는 함수
def getDict_fetchone(colname, rowone) :
    dict_row = {}
    for i in range(len(rowone)) :
        dict_row[colname[i].lower()] = rowone[i]
    return dict_row

# 주문내역 상세 조회 - 1건조회
def getLogin(id, pw) :
    conn = getConnection()
    cursor = getCursor(conn)
    
    sql = """ select mem_id, mem_pass, mem_name from member
                where mem_id = :mem_id 
                and mem_pass = :mem_pass """
    
    cursor.execute(sql, 
                    mem_id = id, 
                    mem_pass = pw)
    
    row = cursor.fetchone()
    
    # row 값이 없는 경우 : 조회 결과가 없는 경우
    # 아이디 또는 패스워드가 틀린 경우 조회 결과 없음
    # 조회결과 없으면 오류 발생
    if row == None : 
        dbClose(cursor, conn)
        return {'rs':'no'}
    
    # 컬럼명 조회
    colname = cursor.description
    col = []
    for i in colname :
        col.append(i[0])
        
    dict_row = getDict_fetchone(col, row)
    dict_row['rs'] = 'yes'
    
    dbClose(cursor, conn)
    
    return dict_row