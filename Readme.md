1) Запуск проекта: fastapi dev app.py
2) Обновить все таблицы в БД (postgres): раскомментировать строки внутри функции lifespan


Для докера (image):
1) docker build . -t fastapi_app:latest 
2) docker run -d -p 7329:8000 fastapi_app

Для докера (compose):
1) docker compose build
2) docker compose up   

**Билд для выкладки в cloud:**

0) Нужно лишь раз для залогина:

*docker login dnd-helper.cr.cloud.ru -u 946fc3614818fc753a24b8e252eb942e -p d50f543f58786e1dcc93b1e88fa5943c*

1) docker build --tag dnd-helper.cr.cloud.ru/fastapi_app . --platform linux/amd64
2) docker push dnd-helper.cr.cloud.ru/fastapi_app 
