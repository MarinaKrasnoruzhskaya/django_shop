# Проект интернет-магазина

- Для приложения ```catalog``` созданы два шаблона: ```home.html``` для домашней страницы и ```contacts.html``` страницы
  с контактной информацией; реализованы контроллеры, которые отвечают за отображение домашней страницы и страницы с
  контактной информацией; реализована обработка сбора обратной связи от пользователя с выводом в консоль;
- Реализована работа с ORM: созданы модели ```Category```,  ```Product``` и ```Contact```; перенесены отображения
  моделей в базу данных с помощью инструмента миграций; настроены отображения в административной панели; сформированы
  фикстуры для заполнения базы данных; создана кастомная команда, которая умеет заполнять данные в базу данных,
  предварительно ее зачищая от старых данных.
- Шаблонизация: выделен базовый шаблон ```base.html```, подшаблон с главным меню ```inc_menu.html```; в шаблон для
  главной страницы выведен список всех товаров; создан контроллер и шаблон для отображения отдельной страницы с товаром.
- FBV и CBV: имеющиеся контроллеры переведены с FBV на CBV; создано новое приложение ```Blog```, в нем создана
  модель ```BlogPost``` и для нее неё реалозован механизм CRUD на основе CBV; реализован счетчик просмотров записей
  блока (когда статья достигает 100 просмотров, отправляется на почту пользователю (или себе) поздравление с
  достижением), вывод записей блога только с положительным признаком публикации, динамическое формирование slug name для
  заголовка записи статьи, перенаправление пользователя на просмотр статьи после её редактирования.
- Формы: реализована валидация названия и описания продукта (нельзя создать продукты с запрещенными словами); добавлена
  модель ```Версия``` и реализован вывод в список продуктов информации об активной версии; реализована возможностью на
  странице продукта добавлять его версии с проверкой, что активных версий только одна.
- Аутентификация: создано приложение ```Users``` для работы с пользователем; реализован функционал аутентификации  (
  регистрация пользователя по почте и паролю, верификация почты пользователя через отправленное письмо, авторизация
  пользователя, восстановление пароля зарегистрированного пользователя на автоматически сгенерированный пароль);
  контроллеры, отвечающие за работу с продуктами, закрыты для анонимных пользователей, а создаваемые продукты
  автоматически привязываются к авторизованному пользователю.
- Права доступа: создана группа для роли модератора с правами доступа: может отменять публикацию продукта, может менять
  описание и категорию любого продукта; в контроллерах и шаблонах внедрена проверка возможности редактирования продукта,
  отображения списка опубликованных или всех продуктов; для приложения ```Blog``` создана группа контент-менеджер,
  который может управлять публикациями в блоге.
- Кэширование: установлен брокер для кеширования Redis, настроено кеширование всего контроллера отображения данных
  относительно одного продукта, добавлено низкоуровневое кеширование для списка категорий и списка продуктов.

Инструкции по установке
------------

1. Клонировать репозиторий
   ```sh
   git clone https://github.com/MarinaKrasnoruzhskaya/django_shop
   ```
2. Перейти в директорию django_shop
   ```sh
   cd django_shop
   ```
3. Установить виртуальное окружение
   ```sh
   python -m venv env
   ```
4. Активировать виртуальное окружение
   ```sh
   env\Scripts\activate
   ```
5. Установить зависимости
   ```sh
   pip install -r requirements.tx
   ```
6. Заполнить файл ```.env.sample``` и переименовать его, дав имя ```.env```
7. Создать БД ```bowshop```
   ```
   psql -U postgres
   create database bowshop;  
   \q
   ```
8. Применить миграции
    ```sh
   python manage.py migrate
    ```
9. Заполнить БД
    ```sh
   python manage.py fill
   ```

Руководство по использованию
---------------

1. Для запуска проекта в терминале IDE выполните команду:
  ```sh
   python manage.py runserver
   ```
2. После запуска сервера перейти по ссылке http://127.0.0.1:8000/ и будет отображена домашняя страница проекта. На
   домашней странице представлен список категорий продуктов.
3. С помощью кнопки ```Каталог ``` переходим на страницу, где представлен список продуктов.
4. С помощью кнопки ```Контакты ```  или одноименной ссылки можно перейти на страницу с контактной информацией. Здесь же
   можно заполнить и отправить данные с помощью формы ```Свяжитесь с нами```.
5. С помощью кнопки ```Блог ``` можно перейти на страницу ```Блог "Бантики для первых хвостиков и косичек"``` , где
   представлены записи блога.

Пользователи проекта
---------------

1. Пользователи-владельцы:
   mitenkovamarina@yandex.ru (пароль: vsnrupw1f8),
   krasnoruzhskayamarina@yandex.ru (пароль: 5BDsZhB6O1)
2. Модератор
   moderator@sky.pro (пароль: admin123)
3. Контент-менеджер
   content_manager@sky.pro (пароль: admin123)
4. Суперпользователь
   admin@sky.pro (пароль: admin123)

Построен с:
---------------

1. Python 3.12
2. env
3. Django 5.0.6
4. UIkit Bootstrap 5.3
5. Python-dotenv 1.0.1
6. Psycopg2-bynary 2.9.9
7. Pillow 10.4.0
8. ipython 8.26.0
9. pytils 0.4.1
10. docutils 0.21.2
11. phonenumberslite 8.13.42
12. redis 5.0.8

Контакты
---------------
Марина Красноружская - krasnoruzhskayamarina@yandex.ru

Ссылка на
проект: [https://github.com/MarinaKrasnoruzhskaya/django_shop](https://github.com/MarinaKrasnoruzhskaya/django_shop)

<p align="right">(<a href="#readme-top">Наверх</a>)</p>

