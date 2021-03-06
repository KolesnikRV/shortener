### Лучший сокращатель ссылок | ShortyURL (По мнению [KolesnikRV](https://github.com/KolesnikRV))
-----------------
### Описание
-------------
- Web-приложение - аналог bit.ly и подобных систем, для длинных урлов создает их короткие аналоги &lt;domain>/&lt;subpart>.
- Состоит из двух приложений url и api;
- Разделение пользователей - по session cookies (при первом обращении к приложению ключ сессии сохраняется в базе);
- Функции формирования коротких url и сохранения сессий расположены в functions/functions.py;
- Важные настройки django, redis, mysql прописаны в файле .env (файл предоставлен в качестве примера, не желательно использовать).
- Остальные настройки, такие как автомачитеское удаление старых записей из таблицы, пагинация, настройки логирования и т.д расположены в файле ./shortener/settings.py.
- По умолчанию работает в DEBUG=True (до появления веб сервера nginx).

Использованные технологии:
- python 3.8.10
- django 3.2.9
- djangorestframework 3.12.4
- mysql 8.0.27
- redis 6.2.6
- docker
- celery

### Приложение url
-------------------
- описывает модель хранения сокращённых ссылок (Url)
- позволяет пользователю указать свой <subpart> (http:/127.0.0.1:8000/subpart)
- представления:
  - index (эндпоинт '/') - возвращает шаблон содержащий форму для ввода длинной ссылки и возможного варианта короткой, также возвращает список сокращенных ссылок текущего пользователя с пагинацией. Поддерживает запросы GET и POST.
пример: GET: http:/127.0.0.1/
  - url_redirect (эндпоинт '/^[a-zA-Z0-9_,/.:;&@]*$') - при переходе по короткому url перенаправлят на длинный url.
пример: http:/127.0.0.1:8000/A12H4Ttm, http:/127.0.0.1:8000/Hamster
внимание: http:/127.0.0.1:8000/Hamster и http:/127.0.0.1:8000/hamster - это разные короткие ссылки.

### Приложение api
-------------------
- апи приложения
- содержит только один эндпоинт: '/' и поддерживает запросы GET и POST.
- при запросе GET(если указан sessionid в Headers cookies) возвращает данные о всех сокращенных ссылках пользователя.
Возможно отсутствие данных если:
- завершилась сессия;
- данные устарели (автоматическое удаления старых данных настраивается параметром CLEAR_DATA_MINUTES в файле ./shortener/settings.py)
- при запросе POST пользователь передаёт на сервер форму с полями full_url=длинный url и short_url=<пусто или subpart>, где subpart - желаемый пользователем в (http:/127.0.0.1:8000/subpart)

### Установка и использование
------------------------------
Для установки и запуска достаточно выполнить следующие действия:
  - $ git clone https://github.com/KolesnikRV/shortener.git
  - $ cd shortener
  - $ sudo docker-compose up --build
  - Затем переходим по ссылке http://127.0.0.1:8000 или http://127.0.0.1:8000/api

### Планируемые улучшения
  - В качестве веб сервера использовать nginx
  - Переработать веб интерфейс (React)
  - Логирование запросов к бд и время их выполнения
  - Статистика переходов по сокращенным ссылкам
  - Оптимизировать процедуры создания сокращенной ссылки (алгоритм формирования subpart)

### Автор
  - [KolesnikRV](https://github.com/KolesnikRV)
