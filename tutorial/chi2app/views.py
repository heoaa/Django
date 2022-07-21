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

## 설문 분석결과 보기
def survey_Analysis(request) :
    
    ## 설문 데이터 조회하기
    df = survey.getSurveyList()
    
    ## 설문 분석하기(함수로 처리)
    # rs_df : 분석에 사용된 컬럼 추가된 최종본
    # rs_ct : 교차표(crossTable) 데이터
    # rs_msg : 해석 결과
    rs_df, rs_ct, rs_msg = get_Analysis(df)
    
    # 시각화 및 저장하기 (함수로 처리)
    view_Visualization(rs_df)
    
    context = {
        # 교차표를 html로 전환하여 키 생성
        'crossTab' : rs_ct.to_html(),
        # 해석내용
        'results' : rs_msg
    }
    
    return render(
        request,
        'chi2app/analysis.html',
        context
    )
    
# 분석 및 시각화 함수 v ------------------------------
import pandas as pd
import scipy.stats as stats
import seaborn as sns
import matplotlib.pyplot as plt

## 분석하기
def get_Analysis(df) :
    # 성별을 숫자로
    df['genNum'] = df['gender'].apply(lambda g:1 if g=='남' else 2)
    
    # 커피숍 이름을 숫자로
    df['coNum'] = df['co_survey'].apply(lambda c:1 if c=='스타벅스'\
                                                    else 2 if c=='커피빈'\
                                                    else 3 if c=='이디야'\
                                                    else 4)
    # 교차표(빈도표) 생성
    crossTab = pd.crosstab(index = df['gender'], columns=df['co_survey'])
    
    # 검증하기
    chi, pv, _, _ = stats.chi2_contingency(crossTab)
    
    # 검증결과
    results = ''
    
    if pv > 0.05 :
        results = 'p-value(유의확률) 값이 <b>{:.3f} > 0.05</b>이므로, '\
                    '유의수준보다 크게 나타나 귀무가설을 기각할 수 없다. '\
                    '<br> 따라서, 성별에 따라 선호하는 커피브랜드에는'\
                    '<b> 차이가 없다고 할 수 있다.(귀무가설 채택)</b>'.format(pv)
                    
    else :
        results = 'p-value(유의확률) 값이 <b>{:.3f} < 0.05</b>이므로, '\
                    '유의수준보다 작게 나타나 귀무가설을 기각할 수 있다. '\
                    '<br> 따라서, 성별에 따라 선호하는 커피브랜드에는'\
                    '<b> 차이가 있다고 할 수 있다.(대립가설 채택)</b>'.format(pv)
                    
    return df, crossTab, results
    
# 시각화 및 저장하기
def view_Visualization(df) :
    # 한글처리
    plt.rc('font', family='Malgun Gothic')
    # 그래프 사이즈
    plt.figure(figsize=(18,18))
    # fig 객체 얻기 : gcf는  figure와 같음
    fig = plt.gcf()
    # 그룹화
    gen_group = df['co_survey'].groupby(df['coNum']).count()
    # 그룹에 인덱스 이름 정의하기 (인덱스 번호를 한글 이름으로)
    gen_group.index = ['스타벅스', '커피빈', '이디야', '탐앤탐스']
    # 막대그래프 그리기(width = 막대너비)
    gen_group.plot.bar(color=['red', 'green', 'blue', 'orange'],
                        width=0.3)
    # 제목 정의
    plt.title('커피숍별 선호도', fontsize = 40)
    plt.xlabel('커피숍', fontsize = 40)
    plt.ylabel('선호도 건수', fontsize = 40)
    # 축별 값들에 대한 폰트 사이즈 조정
    plt.xticks(fontsize = 30, rotation = 0)
    plt.yticks(fontsize = 30)
    # 그래프 저장
    fig.savefig('chi2app/static/chi2app/images/chi2.png') 
    
# ---------------------------------------------------