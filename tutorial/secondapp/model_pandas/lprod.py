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

# 여러건에 대한 리스트 + 딕셔너리 만드는 함수
def getDictType_Fetchall(col_name, row) :
    list_row = []
    for tup in row :
        dict_row = {}
        for p in range(len(tup)) :
            dict_row[col_name[p].lower()] = tup[p]
        list_row.append(dict_row)
    
    return list_row

# 상품분류정보 전체조회
def getLprodList() : 
    conn = getConnection()
    cursor = getCursor(conn)
    
    sql = ''' select*from lprod '''
    cursor.execute(sql)
    
    row = cursor.fetchall()
    
    colname = cursor.description
    col = []
    for i in colname :
        col.append(i[0])
        
    row_list = getDictType_Fetchall(col, row)
    
    dbClose(cursor, conn)
    
    return row_list



# 한건 행 딕셔너리 만드는 함수
def getDict_fetchone(colname, rowone) :
    dict_row = {}
    for i in range(len(rowone)) :
        dict_row[colname[i].lower()] = rowone[i]
    return dict_row

# 상품분류정보 상세 조회 - 1건조회
def getLprod(gu) :
    conn = getConnection()
    cursor = getCursor(conn)
    
    sql = """ select*from lprod
    where lprod_gu = :lprod_gu """
    
    cursor.execute(sql, lprod_gu = gu)
    
    row = cursor.fetchone()
    
    colname = cursor.description
    col = []
    for i in colname :
        col.append(i[0])
        
    dict_row = getDict_fetchone(col, row)
    
    dbClose(cursor, conn)
    
    return dict_row