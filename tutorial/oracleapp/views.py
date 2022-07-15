from django.http import HttpResponse
from django.shortcuts import render
from .model_pandas import member as mem

from oracleapp.model_pandas.member import getMemberList

from django.core.paginator import Paginator    # 페이지처리 라이브러리

# Create your views here.
# 회원목록 전체 조회 - 페이지 처리(django만 적용 가능 코드)    
def view_Member_List_Page(request):
    
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
    df_list = getMemberList()
    
    # 페이지 처리 2) ------------------------
    p = Paginator(df_list, 3)    #(모델 조회한 데이터, 한 페이지에 보여줄 행 개수)
    
    info = p.get_page(now_page)   # 사용할 데이터 추출
    
    start_page = (now_page - 1) // 3 * 3 + 1    # 시작페이지 번호
    end_page = start_page + 2                     # 마지막페이지 번호
    
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
        'oracleapp/page_control/member_list_page.html',
        context
    )
    




# templates
def test(request) :
    return render(
        request,
        'oracleapp/test.html',
        {}
    )

# 회원 전체 조회(member)
def view_Member_List(request) :
    
    df = mem.getMemberList()
    # return HttpResponse(df)
    
    context = {"df" : df}
    
    return render(
        request,
        "oracleapp/member_list.html",
        context
    )

# 회원 상세 조회
def  view_Member(request) :
    
    df_dict = mem.getMember('a001')
    
    # context = {"df" : df}
    
    # return HttpResponse(df_dict)
    return render(
        request,
        'oracleapp/member.html',
        df_dict,
    )