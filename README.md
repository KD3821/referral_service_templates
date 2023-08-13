# referral_service_templates

<h1 align="center">Referral service with Django Templates <br>(Django REST framework)</h1>
<p align="center">

<img src="https://img.shields.io/badge/madeBy-KD3821-lightyellow" >

<p align="center">Реферальная система (Django, DRF)</b><br>

<b>Описание работы сервиса</b><br>
<ul>
<li>
Зарегистрироваться в системе по номеру телефона.</li>
<li>
Верифицировать номер телефона вводом 4-х значного кода.</li>
<li>
В личном кабинете сохранить инвайт-код пригласившего Вас Пользователя.(Необязательно)</li>
<li>
Для приглашения в сервис другого пользователя необходимо передать ему Ваш инвайт-код, и он должен сохранить его в ЛК.</li>
<li>
В дальнейшем для входа в систему использовать номер телефона, указанный при регистрации.</li>
<li>
Просматривать список приглашенных Вами пользователей в таблице "Ваши рефералы"</li>
<li>
Ознакомиться с документацией по работе API во вкладках "Swagger", "ReDoc".</li></ul><br>
<b>Демонстрация работы сервиса (Django Templates + Bootstrap 5 ): <a href="https://mytest78.ru/" target="_blank">Я участвую!🚀</a></b>
<br><br>

![Alt text](https://github.com/KD3821/referral_service/assets/80853241/db7f3499-2c28-495f-b491-34b74d47cb5d)
![Alt text](https://github.com/KD3821/referral_service/assets/80853241/0f1bbdb5-f36e-4a6c-a138-ca78e7109c60)
![Alt text](https://github.com/KD3821/referral_service/assets/80853241/3ea4e842-f8d8-42b3-95c2-eda67e70cbfe)
![Alt text](https://github.com/KD3821/referral_service/assets/80853241/a000db7f-9558-455d-a073-b932dd84052e)
![Alt text](https://github.com/KD3821/referral_service/assets/80853241/4398c9f1-7b72-419f-bc37-eccfe8738331)
![Alt text](https://github.com/KD3821/referral_service/assets/80853241/4c2340dc-f8ef-427b-888f-9c29479108ad)
![Alt text](https://github.com/KD3821/referral_service/assets/80853241/b49fd0c1-3932-49b9-b06e-bc440df9de56)
<br><br>
<b>[<a href="https://github.com/KD3821/referral_service" target="_blank">Код версии приложения без шаблонов (API с Swagger UI & ReDoc)</a>]</b>
<br>

<b>Краткая инструкция по запуску и настройке сервиса</b><br><br>
Стэк:
<ul>
  <li>Django и Django REST framework.</li>
  <li>PostgreSQL</li>
  <li>Docker и Docker-compose</li>
</ul><br>
Сущности проекта:
<ul>
  <li>TemporaryUser - модель для сохранения данных неподтвержденных Пользователей</li>
  <li>User - модель подтвержденного пользователя</li>
</ul><br>

<b>Таблица ендпоинтов</b>
<table>
<thead>
<tr>
  <th>HTTP Verb</th>
  <th>Scope</th>
  <th>Semantics</th>
  <th>URL</th>
</tr>
</thead>
<tbody>
<tr>
  <td>POST</td>
  <td>Login</td>
  <td>Enter Phone - get Code</td>
  <td>http://127.0.0.1:8000/api/accounts/code</td>
</tr>
<tr>
  <td>POST</td>
  <td>Verification</td>
  <td>Enter Phone and Code - get Tokens</td>
  <td>http://127.0.0.1:8000/api/accounts/verify</td>
</tr>
<tr>
  <td>GET</td>
  <td>Profile</td>
  <td>View Profile</td>
  <td>http://127.0.0.1:8000/api/service/profile</td>
</tr>
<tr>
  <td>PUT/PATCH</td>
  <td>InviteCode</td>
  <td>Provide Invite Code</td>
  <td>http://127.0.0.1:8000/api/service/profile</td>
</tr>
</tbody>
</table>
<br>
Авторизация:
<ul>
  <li>После верификации 4-х значного кода для Пользователя создаются JWT токены (по стандарту: Access и Refresh)</li>
  <li>Токен необходимо передавать в заголовке 'Authorization': 'Bearer TOKEN'</li>
  <li>Данная версия API не предусматривает получения нового Access токена по истечении срока действия - т.е. необходимо пройти повторную авторизацию с помощью номера телефона и 4-х значного кода верификации</li>
</ul><br>
Запуск проекта на локальной машине:
<ul>
  <li>Создать папку для проекта</li>
  <li>Создать в папке виртуальное окужение для Python 3.10 и активировать его</li>
  <li>Клонировать репозитории в папку и установить зависимости из файла requirements.txt</li>
  <li>Создать .env файл с данными для переменных окружения по образцу из env.example</li>
  <li>Внести необходимые Вам изменения в settings.py</li>
  <li>Собрать статику в неоходимую вам папку: python3 manage.py collectstatic</li>
  <li>Запустить контейнер с PostgreSQL с помощью файла docker-compose.yml</li>
  <li>Произвести миграции с помощью команд: python3 manage.py makemigrations и python3 manage.py migrate</li>
  <li>Создать Супер Пользователя -python3 manage.py createsuperuser - ввести данные для полей: Phone, Passcode(любой код), Password(ограничения Django)</li>
  <li>Запустить сервер: python3 manage.py runserver</li>
</ul><br>
