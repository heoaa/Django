from email.utils import make_msgid
from urllib import request
from django.http import HttpResponse
from django.shortcuts import render
from .model_pandas import cart
from .model_pandas import login
from django.core.paginator import Paginator    # 페이지처리 라이브러리

# Create your views here.

# 주문내역 전체 조회 - 페이지 처리(django만 적용 가능 코드)    
def view_Cart_List_Page(request):
    
    # 페이지 처리 1) ------------------------
    # 문법적오류가 아닌
    # 물리적오류가 발생하는 경우에는 예외처리
    try :
        now_page = request.GET.get('page')
        now_page = int(now_page)
    except :
        now_page = 1
    # ---------------------------------------
    
    # 모델 조회
    df_list = cart.getCartList()
    
    # 페이지 처리 2) ------------------------
    p = Paginator(df_list, 10)    #(모델 조회한 데이터, 한 페이지에 보여줄 행 개수)
    
    info = p.get_page(now_page)   # 사용할 데이터 추출
    
    start_page = (now_page - 1) // 10 * 10 + 1    # 시작페이지 번호
    end_page = start_page + 9                     # 마지막페이지 번호
    
    # end_page : 계산에 의한 페이지 수(10단위 계산)
    # p.num_pages : 전체페이지 수
    # 전체페이지 수보다 크다면,
    # 전체페이지 수로 변경
    if end_page > p.num_pages :
        end_page = p.num_pages
    
    is_prev = False    # 이전 페이지 가기
    is_next = False    # 다음 페이지 가기
    
    # 이전/다음 체크하기
    if start_page > 1 :
        is_prev = True
        
    if end_page < p.num_pages :
        is_next = True
    # ---------------------------------------
    
    #context = {'df_list':df_list}
    context = {'info'       :info,
                'page_range':range(start_page, end_page + 1),
                'is_prev'   :is_prev,
                'is_next'   :is_next,
                'start_page':start_page,
                'end_page'  :end_page}
    
    # page_control/cart_list_page.html
    # return HttpResponse('test')
    return render(
        request,
        'dbapp/page_control/cart_list_page.html',
        context
    )


# 주문내역 전체 조회
def view_Cart_List(request) :
    df = cart.getCartList()
    
    context = {'df': df}
    
    return render(
        request,
        'dbapp/cart_list.html',
        context
    )
    

# 주문내역 한건 조회
def view_Cart(request) :
    pcart_no = request.GET['pcart_no']
    pcart_prod = request.GET['pcart_prod']
    
    dict = cart.getCart(pcart_no, pcart_prod)

    #return HttpResponse(cart)
    return render(
        request,
        'dbapp/cart.html',
        dict,
    )
    
# 입력폼(form)
def view_Cart_Insert(request) :
    pcart_member = 'e001'
    pcart_prod = 'P102000001'
    
    return render(
        request,
        'dbapp/cart_insert_form.html',
        {"pcart_member": pcart_member,
         "pcart_prod":pcart_prod},
    )

# 입력처리
def set_Cart_Insert(request) :
    pcart_member = request.POST["pcart_member"]
    pcart_prod = request.POST["pcart_prod"]
    cart_qty = request.POST["cart_qty"]
    
    msg = cart.setCartInsert(pcart_member, pcart_prod, cart_qty)
    
    pageControl = ""
    
    if msg == "Y" :
        pageControl = """
        <script>
            alert('입력 되었습니다!')
            location.href='/db/cart_list_dict/'
        </script>
        """
    else :
        pageControl = """
        <script>
            alert('입력 실패!')
            history.go(-1)
        </script>
        """
    return HttpResponse(pageControl)

#def testDict(request) :
#    context = {'dt':[{"no1":1,"no2":2,"no3":3},
#                     {"no1":4,"no2":5,"no3":6}]}
#    return render(
#        request,
#        'dbapp/testdict.html',
#        context
#    )
    
# 주문내역 전체 조회 : 리스트-딕셔너리
def view_Cart_List_dict(request) :
    df_list = cart.getCartList()
    context = {'df_list':df_list}
    return render(
        request,
        'dbapp/cart_list_dict.html',
        context
    )
    
    
# 주문내역 삭제
def set_Cart_Delete(request) :
    pcart_no = request.GET['pcart_no']
    pcart_prod = request.GET['pcart_prod']

    msg = cart.setCartDelete(pcart_no, pcart_prod)

    pageControl = ""
    
    if msg == "Y" :
        # 자바스크립트 링크 처리 location.href=""
        pageControl = """
        <script>
            alert('삭제 되었습니다!')
            location.href='/db/cart_list_dict/'
        </script>
        """
    else :
        # history.go(-1) : 이전 페이지로 // -2 : 이전이전 페이지
        pageControl = """
        <script>
            alert('삭제 실패!')
            history.go(-1)
        </script>
        """
    return HttpResponse(pageControl)
    # return render(
    #     request,
    #     'dbapp/cart_delete.html',
    #     {'msg' : msg}
    # )
    
    
# 수정 화면
def view_Cart_Update(request) :
    pcart_no = request.GET['pcart_no']
    pcart_prod = request.GET['pcart_prod']

    df_dict = cart.getCart(pcart_no, pcart_prod)
    
    # context = {"pcart_no":pcart_no,
    #            "pcart_prod":pcart_prod}

    df_dict["pcart_no"] = pcart_no
    df_dict["pcart_prod"] = pcart_prod

    return render(
        request,
        'dbapp/cart_update_form.html',
        df_dict
    )
    
    
# 수정처리
def set_Cart_Update(request) :
    pcart_no = request.POST['pcart_no']
    pcart_prod = request.POST['pcart_prod']
    cart_qty = request.POST['cart_qty']

    # setCartUpdate return값이 Y
    msg = cart.setCartUpdate(pcart_no, pcart_prod, cart_qty)
    
    pageControl = ""
    
    if msg == "Y" :
        pageControl = """
        <script>
            alert('수정 되었습니다!')
            location.href='/db/cart_list_dict/'
        </script>
        """
    else :
        pageControl = """
        <script>
            alert('수정 실패!')
            history.go(-1)
        </script>
        """
    return HttpResponse(pageControl)
#    return render(
#        request,
#        'dbapp/cart_update.html',
#        {"msg":msg}
#    )/


# 로그인 화면
def login_form(request) :
    return render(
       request,
       'dbapp/login/login_form.html',
       {}
   )
    
        
# 로그인 함수
def getLogin(request) :
    try :
        pmem_id = request.POST['mem_id']
        pmem_pass = request.POST['mem_pass']
    except :
        context = """<script>
                        alert('직접 접근하시면 안됩니다. 로그인 페이지로 이동')
                        location.href = '/db/login_form/'
                    </script>"""
                    
        return HttpResponse(context)
    
    # 아이디, 패스워드 확인 모델 호출(한건조회)
    df_dict = login.getLogin(pmem_id, pmem_pass)
    
    # 로그인 실패시 처리
    if df_dict['rs'] == 'no' :
        context = """<script>
                        alert('아이디 또는 패스워드를 확인하여 주세요.');
                        history.go(-1)
                    </script>"""
        return HttpResponse(context)
    
    # session 처리 (회원 정보를 서버에 저장해 놓고 있는 상태)
    #  - 로그아웃 하기 전까지 회원 정보는 어느 페이지를 가든 살아 있습니다.
    #  - session에 저장되는 값들은 딕셔너리 형태로 저장됨
    #  - request.session[]
    
    # 세션 등록
    request.session['sMem_id'] = pmem_id
    request.session['sMem_name'] = df_dict['mem_name']
    
    # 세션에 저장된 값 불러오기
    if request.session.get('sMem_id') :
        # 세션에 값이 있는 경우
        df_dict['sMem_id'] = request.session['sMem_id']
        df_dict['sMem_name'] = request.session['sMem_name']
    else :
        # 세션에 값이 없는 경우
        df_dict['sMem_id'] = None
    
    df_dict["pmem_id"] = pmem_id
    df_dict["pmem_pass"] = pmem_pass
    
    return render(
       request,
       #'dbapp/login/login.html',
       'dbapp/login/login_form.html',
       df_dict
   )
    
    
# 로그아웃
def set_Logout(request) :
    
    # 세션 정보 확인
    if request.session.get('sMem_id') :
        # 세션정보 삭제
        request.session.flush()
        
        context = """<script>
                        alert('로그아웃 되었습니다.');
                        location.href = '/db/login_form/'
                    </script>"""
                    
        return HttpResponse(context)
    
    else:
        context = """<script>
                        alert('직접 접근하시면 안됩니다. 로그인 페이지로 이동')
                        location.href = '/db/login_form/'
                    </script>"""
                    
        return HttpResponse(context)
    
    
