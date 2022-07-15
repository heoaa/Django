"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import include, path
# import 이름이 같아서 에러 발생 > 별칭 지정 필요
from firstapp import views as fv
from secondapp import views as sv

urlpatterns = [
    path('admin/', admin.site.urls),
    path('index1/', fv.index1),
    path('index2/', fv.index2),
    path('first/', include('firstapp.urls')),
    path('second/', include('secondapp.urls')),
    path('oracle/', include('oracleapp.urls')),
    path('db/', include('dbapp.urls')),
    path('frontend/', include('frontendapp.urls')),
    # path('home/', views.home)
]
