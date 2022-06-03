## Запуск проекта  
### Инициализация репозитория
```python
pip install git  

git clone https://github.com/drive-knight/ansol-test  

cd ansol-test/  

pip3 install -r requirenments.txt
```  
### Настройка базы данных  
1. Я использую PostgreSQL database которую скачать и установить можно по этому адресу https://www.postgresql.org/.
2. В процессе установки нужно будет создать superuser и записать введенные данные, которые понадобятся в следующем шаге. 
3. В файле `config.py` в переменной `SQLALCHEMY_DATABASE_URI` указать свои данные типа `postgresql://<user>:<password>@<url>/<db name>`.  
4. Я создал базу данных в pgAdmin. Вы можете воспользоваться `psql` или же моим способом.  
5. Создание таблицы происходит с помощью alembic и sqlalchemy.  
 
Выполните данный код:
```python  
flask db init  

flask db migrate  

flask db upgrade
```  
Таблица имеет данный вид:  
| id | rubrics | text | created_date |
|:---------|:----------------|:----------------|:----------------|
| [PK] integer | character varying&#91;&#93;(255)  | character varying | character varying(255) |
| целое число | массив&#91;текст&#93; | текст |  текст |   

### Настройка Elasticsearch  
1. На сайте https://www.elastic.co/guide/en/elasticsearch/reference/current/install-elasticsearch.html выбрать подходящий способ установки и следовать инструкциям.
2. В файле `settings.py` нужно изменить переменную DIRECTORY на свой абсолютный путь к папке установленного Elasticsearh
и COMMAND на подходящую для вашей ОС команду запуска. Если у вас ОС Windows то COMMAND изменять не требуется.
### Заполнение таблицы  
1. Заполнение выполняется в скрипте `run.py` по выданному массиву данных `posts.csv`, который находится в репозитории.  
2. Я использовал библиотеку psycopg2 для выполнения sql запросов. В подключении нужно будет снова ввести свои данные.
Нужно изменить соответствующие этим переменным константы DB, USER, PASSWORD, HOST, PORT в файле `settings.py`.  

Функция подключения:  
```python
conn = psycopg2.connect(database=<db name>,
                        user=<user>, password=<password>,
                        host=<host>, port=<port>
                        )
```  

### Запуск flask приложения  
1. Создание индекса и добавление документов происходит также в скрипте `run.py`. На момент исполнения скрипта все инструкции, приведенные выше, должны быть выполнены.
2. Запуск приложения также происходит в данном скрипте.  
4. Выполните данный код:  
```python
python run.py
```

                          
