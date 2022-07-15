from django.db import models

# Create your models(=Table) here.

# sqlite에서만 가능
# class name == table name
# 테이블 생성 시 반드시 한개 이상 컬럼 생성이 필요
class Curriculum(models.Model) :
    # 변수 이름 == 컬럼 이름
    name = models.CharField(max_length=255)