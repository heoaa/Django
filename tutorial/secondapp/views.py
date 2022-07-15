from django.shortcuts import render

from django.http import HttpResponse

from secondapp.model_pandas.lprod import getLprod, getLprodList

from .models import Course

# Create your views here.
def main(request) :
    return HttpResponse("<u>Main</u>")

def insert(request) :
    msg = ''
    Course.objects.create(name = '데이터 분석', cnt = 30)
    msg += '데이터 분석 입력 성공</br>'
    Course(name = '데이터 수집', cnt = 20).save()
    msg += '데이터 수집 입력 성공</br>'
    Course(name = '웹개발', cnt = 25).save()
    msg += '웹개발 입력 성공</br>'
    Course(name = '인공지능 데이터', cnt = 20).save()
    msg += '인공지능 데이터 입력 성공</br>'
    return HttpResponse(msg)

def oneshow(request) :
    data = Course.objects.get(pk = 1)
    return HttpResponse(data.name)

def show2(request) :
    data = Course.objects.all()
    return render(
        request, 
        # templates 폴더 내 경로만 작성
        "secondapp/show2.html",
        {'data' : data}
    )

    
    
def view_Lprod_List(request):
    #return HttpResponse('test')
    df_list = getLprodList()
    context = {'context' : df_list}
    return render(
        request,
        'secondapp/lprod_list.html',
        context
    )

def view_Lprod(request):
    lprod_gu = request.GET['lprod_gu']
    # return HttpResponse(lprod_gu)
    
    context = getLprod(lprod_gu)
    return render(
        request,
        'secondapp/lprod.html',
        context
    )