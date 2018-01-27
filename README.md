基于Django的简易发布签签系统（基于Dango2.0）。

Python的版本与依赖库：

python 3：https：//www.python.org/
Django 2.0：https：//www.djangoproject.com/
PyMySQL 0.8.0：https：//github.com/PyMySQL/PyMySQL
django-bootstrap3 9.1.0：https：//github.com/dyve/django-bootstrap3
提供接口

接口	        网址	                                      请求方式
添加发布会接口	http://127.0.0.1:8000/api/add_event/	        POST
查询发布会接口	http://127.0.0.1:8000/api/get_event_list/	get
添加嘉宾接口	http://127.0.0.1:8000/api/add_guest/	        POST
查询嘉宾接口	http://127.0.0.1:8000/api/get_guest_list/	get
嘉宾签到接口	http://127.0.0.1:8000/api/user_sign/	        get
