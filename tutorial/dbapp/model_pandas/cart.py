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

# 주문내역 전체조회
def getCartList() : 
    conn = getConnection()
    cursor = getCursor(conn)
    
    sql = ''' select*from cart '''
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

# 주문내역 상세 조회 - 1건조회
def getCart(no, prod) :
    conn = getConnection()
    cursor = getCursor(conn)
    
    sql = """ select*from cart
    where cart_no = :cart_no 
    and cart_prod = :cart_prod """
    
    cursor.execute(sql, cart_no = no, cart_prod = prod)
    
    row = cursor.fetchone()
    
    colname = cursor.description
    col = []
    for i in colname :
        col.append(i[0])
        
    dict_row = getDict_fetchone(col, row)
    
    dbClose(cursor, conn)
    
    return dict_row


# 주문내역 입력
def setCartInsert(id, prod, qty) :
    conn = getConnection()
    cursor = getCursor(conn)
    
    # 주문번호 생성
    sql = """ select decode(substr(max(cart_no),1,8), 
    to_char(sysdate,'yyyymmdd'), max(cart_no)+1, 
    to_char(sysdate,'yyyymmdd') || '00001') as max_no
    from cart """
    cursor.execute(sql)
    
    # 한건조회
    max_no = cursor.fetchone()
    no = max_no[0]
    
    # 주문내역 입력
    sql = """ INSERT INTO cart(cart_member,cart_no,cart_prod,cart_qty)
                values(:cart_member,:cart_no,:cart_prod,:cart_qty) """
    cursor.execute(sql,
                   cart_member = id,
                   cart_no = no,
                   cart_prod = prod,
                   cart_qty = qty)
    
    conn.commit()
    
    dbClose(cursor, conn)
    
    return "Y"


# 주문내역 삭제
def setCartDelete(no, prod) :
    conn = getConnection()
    cursor = getCursor(conn)
    
    # 주문내역 입력
    sql = """ delete from cart
                where cart_no = :cart_no and
                cart_prod = :cart_prod """
    cursor.execute(sql,cart_no = no,cart_prod = prod)
    
    conn.commit()
    
    dbClose(cursor, conn)
    
    return 'Y'

# 주문수량 수정
def setCartUpdate(no, prod, qty) :
    conn = getConnection()
    cursor = getCursor(conn)
    
    # 주문내역 입력
    sql = """ update cart
                set cart_qty = :cart_qty
                where cart_no = :cart_no and
                cart_prod = :cart_prod """
    cursor.execute(sql,
                    cart_qty=qty,
                    cart_no = no,cart_prod = prod)
    
    conn.commit()
    
    dbClose(cursor, conn)
    
    return 'Y'