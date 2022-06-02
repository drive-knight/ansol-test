import os
import time
import subprocess

import csv
import psycopg2
from elastic_transport import ConnectionTimeout

from app import create_app
from app import es
import settings


app = create_app()


def main():
    conn = psycopg2.connect(database=settings.DB,
                            user=settings.USER, password=settings.PASSWORD,
                            host=settings.HOST, port=settings.PORT
                            )
    conn.autocommit = True
    cursor = conn.cursor()

    cursor.execute('SELECT EXISTS(SELECT 1 FROM documents)')
    if not cursor.fetchone()[0]:
        with open('posts.csv', 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            id = 1
            for row in reader:
                cursor.execute('INSERT INTO documents VALUES (%s, %s, %s, %s)',
                               (id, row['rubrics'].replace('[', '{').replace(']', '}'), row['text'],
                                row['created_date']))
                conn.commit()
                print(f'Запись {id} добавлена')
                id += 1

    if not es.indices.exists(index='text'):
        try:
            cursor.execute('SELECT id, text FROM documents ORDER BY id')
            a = cursor.fetchall()
            n = 1
            for i in a:
                es.index(index='text', document={'text': i[1], 'id': i[0]})
                print(f'Документ {n} добавлен')
                n += 1
        except ConnectionTimeout:
            print('Время соединения истекло \n'
                  'Повторите запуск')

    conn.close()
    time.sleep(10)
    app.run()


if __name__ == '__main__':
    subprocess.Popen('{}'.format(os.path.join(settings.DIRECTORY, settings.COMMAND)), shell=True)
    time.sleep(60)
    main()


