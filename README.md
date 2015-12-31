# PKUCourier

## 项目目录
对于不同模块，只给出了deal子文件夹中各文件的说明，task、user、will与之类似

	.
    |-- .gitignore
    |-- README.md
    |-- LICENSE
    |-- manage.py
    |-- pkucourier	# 项目设置
    	|-- __init__.py
    	|-- settings.py
    	|-- urls.py
    	|-- segi.py
    |-- deal	# deal模块
    	|-- __init__.py
    	|-- admin.py
    	|-- apps.py 
    	|-- models.py	# deal model的定义（数据库定义） 
    	|-- urls.py		# deal相关接口的定义
    	|-- views.py	# deal相关接口的实现
    |-- task
    	|-- __init__.py
    	|-- admin.py
    	|-- apps.py
    	|-- models.py
    	|-- urls.py
    	|-- views.py
    |-- user
    	|-- __init__.py
    	|-- admin.py
    	|-- apps.py
    	|-- models.py
    	|-- urls.py
    	|-- views.py
    |-- will
    	|-- __init__.py
    	|-- admin.py
    	|-- apps.py
    	|-- models.py
    	|-- urls.py
    	|-- views.py
## 代码运行
执行以下指令：

	python3 manage.py makemigrations
	python3 manage.py migrate
	python3 manage.py runserver

之后访问localhost:8000即可
