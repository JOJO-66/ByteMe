
from django.urls import path
from django.views.generic import RedirectView

from . import views,admin   # 从当前的views导入该函数

urlpatterns=[
    path('first_page/', views.first_page, name="first_page"),
    path('second_page/',views.second_page,name='second_page'),
    path('third_page/',views.third_page,name='third_page'),
    path('intro_page/',views.intro_page,name="intro_page"),
    path('handle_excel_upload/',views.handle_excel_upload),
    path('handle_excel_download/',views.handle_excel_download),
   # path('favicon.ico', RedirectView.as_view(url='/static/favicon.ico', permanent=True)),
]