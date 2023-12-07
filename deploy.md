Настройка и запуск Django-приложения с использованием следующих компонентов: uWSGI, Nginx и systemd. Давайте разберем каждый шаг подробно:

1. **uWSGI команда:**
   ```bash
   uwsgi --http :8000 --home /home/33-3/venv/ --chdir /home/33-3/ -w main.wsgi
   ```
   Эта команда запускает uWSGI как HTTP-сервер на порту 8000. Он указывает путь к виртуальному окружению (`--home`), рабочий каталог (`--chdir`) и точку входа для приложения (`-w`).

2. **Создание файла конфигурации для uWSGI (`news.ini`):**
    ```bash
    sudo nano /etc/uwsgi/sites/news.ini
    ```
   Содержание файла:
   ```ini
   [uwsgi]
   chdir = /home/33-3
   home = /home/33-3/venv
   module = /home/33-3/main.wsgi:application

   master = true
   processes = 5

   socket = /run/uwsgi/news.sock
   chown-socket = root:www-data
   chmod-socket = 660
   vacuum = true
   ```
   Этот файл содержит конфигурацию uWSGI для приложения, включая рабочий каталог, виртуальное окружение, точку входа, количество процессов и настройки сокета.

3. **Настройка службы systemd для uWSGI (`uwsgi.service`):**
    ```
    sudo nano /etc/systemd/system/uwsgi.service
    ```
   Содержание файла:
   ```ini
   [Unit]
   Description=uWSGI Emperor service

   [Service]
   ExecStartPre=/bin/bash -c 'mkdir -p /run/uwsgi; chown root:www-data /run/uwsgi'
   ExecStart=/usr/local/bin/uwsgi --emperor /etc/uwsgi/sites
   Restart=always
   KillSignal=SIGQUIT
   Type=notify
   NotifyAccess=all

   [Install]
   WantedBy=multi-user.target
   ```
   Этот файл настраивает службу systemd для управления uWSGI. Он создает директорию для сокета перед запуском и указывает uWSGI на каталог с конфигурационными файлами.

4. **Конфигурация Nginx (`news`):**
    ```
   sudo nano /etc/nginx/sites-available/news
   ```
    Содержание файла:
   ```nginx
   server {
       listen 8000;
       server_name firstsite.com www.firstsite.com;

       location /static/ {
           root /home/33-3/;
       }

       location / {
           include         uwsgi_params;
           uwsgi_pass      unix:/run/uwsgi/news.sock;
       }
   }
   ```
   Этот конфигурационный файл Nginx настраивает сервер для прослушивания порта 8000, обрабатывает статические файлы и перенаправляет запросы к uWSGI через сокет.

5. **Создание символической ссылки для конфигурации Nginx:**
   ```bash
   sudo ln -s /etc/nginx/sites-available/news /etc/nginx/sites-enabled
   ```
   Это создает символическую ссылку на файл конфигурации Nginx, чтобы его можно было легко включить или отключить.

6. **Проверка конфигурации Nginx:**
   ```bash
   sudo nginx -t
   ```
   Эта команда проверяет, не содержит ли файл конфигурации Nginx ошибок.

7. **Перезапуск Nginx:**
   ```bash
   sudo systemctl restart nginx
   ```
   Это перезапускает Nginx для применения новой конфигурации.

8. **Запуск uWSGI:**
   ```bash
   sudo systemctl start uwsgi
   ```
   Эта команда запускает службу uWSGI.

9. **Удаление правила ufw для порта 8000:**
   ```bash
   sudo ufw delete allow 8000
   ```
   Эта команда удаляет правило брандмауэра для порта 8000, так как теперь Nginx проксирует запросы через этот порт.

10. **Добавление правила ufw для Nginx:**
    ```bash
    sudo ufw allow 'Nginx Full'
    ```
    Это добавляет правило брандмауэра для полного доступа Nginx.

11. **Включение автозапуска Nginx:**
    ```bash
    sudo systemctl enable nginx
    ```
    Эта команда настраивает автозапуск Nginx при загрузке системы.

12. **Включение автозапуска uWSGI:**
    ```bash
    sudo systemctl enable uwsgi
    ```
    Эта команда настраивает автозапуск службы uWSGI при загрузке системы.

Общий результат этих шагов - развертывание Django-приложения с использованием uWSGI, Nginx и systemd.