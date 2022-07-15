import pandas
# django 가상환경에서 cx_Oracle 설치
import cx_Oracle as ora

# 1) 오라클 연결 및 접속
# 웹은 함수기반으로 움직이므로 함수화 필요
def getConnection() :
    # 오라클 연결
    dsn = ora.makedsn('localhost', 1521, service_name='orcl')
    # 오라클 접속
    conn = ora.connect('busan_06', 'dbdb', dsn)
    return conn

# 2) 커서 받기
def getCursor(conn) :
    cursor = conn.cursor()
    return cursor

# 3) 접속 정보 및 커서 반납
def dbClose(cursor, conn) :
    # 커서 먼저 반납해야 함
    cursor.close()
    # 다음으로 접속정보 반납
    conn.close()
    
    
################ < 실제 사용하는 함수 > #####################

# 회원 전체 리스트 조회(member)
def getMemberList() :
    conn = getConnection()
    cursor = getCursor(conn)
    
    sql = """ select*from member """
    cursor.execute(sql)
    
    row = cursor.fetchall()
    
    dbClose(cursor, conn)
    
    return row

# 딕셔너리 변환
def getDicType_FetchOne(col_name, row_one) :
    dict_row = {}

    for i in range(len(row_one)) :
        dict_row[col_name[i].lower()] = row_one[i]
    
    return dict_row


# 회원 상세 조회 - 1건 조회
def getMember(id) :
    conn = getConnection()
    cursor = getCursor(conn)
    
    sql = """ select * from member
    where mem_id = :mem_id """
    cursor.execute(sql, mem_id = id)
    
    row = cursor.fetchone()
    
    # 컬럼명 조회
    colname = cursor.description
    col = []
    for i in colname :
        col.append(i[0])
    
    dict_row = getDicType_FetchOne(col, row)
    
    dbClose(cursor, conn)
    
    return dict_row