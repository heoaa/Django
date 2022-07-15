from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse

# <u> 밑줄 그을 텍스트 </u>
def index1(request) :
    return HttpResponse("<u>Hello...</u>")

# <p>문단</p>
def index2(request) :
    return HttpResponse("<p>index2 함수 호출</>")

# <b> 볼드체 </b>
def home(request) :
    return HttpResponse("<b>Home</b>")

def main(request) :
    return HttpResponse("<u>Main</u>")

# 데이터 입력
from .models import Curriculum

def insert(request) :
    msg = ""
    # 1) linux 입력
    Curriculum.objects.create(name='linux')
    msg += '1) linux 입력 성공 <br>'
    # 2) python 입력
    c = Curriculum(name='python')
    c.save()
    msg += '2) python 입력 성공 <br>'
    # 3) html/css/js 입력
    Curriculum(name='html/css/js').save()
    msg += '3) html/css/js 입력 성공 <br>'
    # 4) django 입력
    Curriculum(name='django')
    msg += '4) django 입력 성공 <br>'
    return HttpResponse(msg)

# 전체 데이터 조회
def show(request) : 
    data = Curriculum.objects.all()
    
    msg = ''
    for dt in data :
        msg += dt.name + '<br>'
        
    return HttpResponse(msg)

# 한건 조회
def oneshow(request) :
    onedata = Curriculum.objects.get(pk=4)
    return HttpResponse(onedata.name)

def show2(request) :
    return render(
        request, 
        # templates 폴더 내 경로만 작성
        "firstapp/show2.html",
        {}
    )
    
def show3(request) :
    data = Curriculum.objects.all()
    
    return render(
        request, 
        # templates 폴더 내 경로만 작성
        "firstapp/show3.html",
        {'data' : data}
    )
    
def show4(request) :
    data = Curriculum.objects.all()
    
    return render(
        request, 
        # templates 폴더 내 경로만 작성
        "firstapp/show4.html",
        {'data' : data}
    )    
    
# 수정하기
def update(request) :
    data = Curriculum.objects.get(pk=1)
    data.name = 'linux_update'
    data.save()
    return HttpResponse('수정 성공')

# 삭제하기
def delete(request) :
    data1 = Curriculum.objects.get(pk=1)
    data1.delete()
    data2 = Curriculum.objects.get(pk=2)
    data2.delete()
    return HttpResponse('삭제 성공')
    