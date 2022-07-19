from django.shortcuts import render
from django.http import HttpResponse
from .model_pandas import survey
from django.core.paginator import Paginator    # 페이지처리 라이브러리

# Create your views here.
def test(request) :
        return render(
        request,
        'chi2app/test.html',
        {'msg': 'test'}
    )
        
## survey 테이블 생성
def createTable(request) : 
    survey.createTableSurvey()
    
    return HttpResponse('성공')


## 설문 데이터 입력 - 테스트
def set_Survey_Insert_test(request):
    pgender = '여'
    page = 20
    pco_survey = '스타벅스'
    
    survey.setSurveyInsert(pgender, page, pco_survey)
    
    return HttpResponse('Insert OK')

## 설문 전체 조회하기
def view_Survey_List(request) :
    df = survey.getSurveyList()
    context = {'df':df.to_html()}
    
    #return HttpResponse(df.to_html())
    return render(
        request,
        'chi2app/list.html',
        context
    )
    
## 설문 참여하기 페이지
def view_Survey(request) :
    return render(
        request,
        'chi2app/survey.html',
        {}
    )
    
## 설문 데이터 입력
def set_Survey_Insert(request):
    # html form태그를 확인하면 method가 post
    pgender    = request.POST.get('gender')
    page       = request.POST.get('age')
    pco_survey = request.POST.get('co_survey')
    
    survey.setSurveyInsert(pgender, page, pco_survey)
        
    context = """<script>
                        alert('Insert 성공');
                        location.href = '/chi2/list'
                    </script>"""
                    
    return HttpResponse(context)
