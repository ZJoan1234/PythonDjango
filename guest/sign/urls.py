from django.urls import path
from sign import views_if
urlpatterns = [
    #添加发布会路径
    path('add_event/', views_if.add_event, name='add_event'),
    #查询发布会路径
    path('get_event_list/', views_if.get_event_list, name='get_event_list'),
    #添加嘉宾接口
    path('add_guest/', views_if.add_guest, name='add_guest'),
    #查询嘉宾接口
    path('get_guest_list/', views_if.get_guest_list, name='get_guest_list'),
    #嘉宾签到接口
    path('user_sign/', views_if.user_sign, name='user_sign'),
]

