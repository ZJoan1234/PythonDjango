from django.urls import path
from sign import views_if
app_name="sign"
urlpatterns = [
    path('add_event/', views_if.add_event, name='add_event'),

]