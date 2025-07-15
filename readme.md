# 📝 Продвинутый To-Do дашборд / Advanced To-Do Dashboard 📝

## 🎨 Описание / 🇬🇧 Description

🇷🇺 Полнофункциональное веб-приложение для управления задачами, созданное на Python (Flask) и SQLAlchemy. Приложение поддерживает индивидуальные аккаунты пользователей, позволяет детально настраивать задачи (приоритеты, теги, дедлайны), прикреплять файлы, а также анализировать свою продуктивность с помощью встроенной аналитики.

🇬🇧 A full-featured web application for task management, built with Python (Flask) and SQLAlchemy. The application supports individual user accounts, allows for detailed task customization (priorities, tags, deadlines), file attachments, and provides tools to analyze your productivity with built-in analytics.

-----

## ✨ Возможности / ✨ Features

* **👤 Система пользователей:** Регистрация и вход в систему. Каждый пользователь видит только свои задачи.
* **👤 User System:** Registration and login. Each user sees only their own tasks.

* **🗂️ Детализация задач:** Устанавливайте **приоритеты** (высокий, средний, низкий), добавляйте **теги** и назначайте **дедлайны**.
* **🗂️ Task Detailing:** Set **priorities** (high, medium, low), add **tags**, and assign **deadlines**.

* **📎 Прикрепление файлов:** К каждой задаче можно прикрепить один файл для контекста.
* **📎 File Attachments:** Attach one file to any task for context.

* **↔️ Drag & Drop сортировка:** Меняйте порядок задач простым перетаскиванием мыши.
* **↔️ Drag & Drop Sorting:** Change task order with a simple drag-and-drop.

* **🔍 Поиск и фильтры:** Мощная система фильтрации по статусу, тегам и поиску по названию.
* **🔍 Search & Filters:** A powerful filtering system by status, tags, and text search.

* **🗄️ Архив:** Выполненные задачи можно архивировать, чтобы они не мешали, с возможностью восстановления.
* **🗄️ Archive:** Completed tasks can be archived to keep the main list clean, with an option to restore them.

* **📊 Аналитика:** Отдельная страница с графиком продуктивности за последние 30 дней и сводкой за неделю/месяц.
* **📊 Analytics:** A dedicated page with a productivity chart for the last 30 days and a weekly/monthly summary.

-----

## 🛠️ Установка и запуск / 🛠️ Installation and Launch

1.  **🇷🇺 Клонируйте или скачайте репозиторий / 🇬🇧 Clone or download the repository:**
    * `git clone https://github.com/avielienna/todo-dashboard.git`
    * (🇷🇺 или скачайте ZIP-архив и распакуйте его / 🇬🇧 or download the ZIP and extract it)

2.  **🇷🇺 Перейдите в папку проекта и создайте папку `uploads` / 🇬🇧 Navigate to the project folder and create an `uploads` folder:**
    * `cd todo-dashboard`
    * `mkdir uploads`

3.  **🇷🇺 Установите зависимости / 🇬🇧 Install dependencies:**
    * `pip install Flask Flask-SQLAlchemy Flask-Login Flask-Bcrypt`

4.  **🇷🇺 Запустите приложение / 🇬🇧 Run the application:**
    * `python app.py`
    * (🇷🇺 При первом запуске будет создан файл базы данных `todo.db` / 🇬🇧 A `todo.db` database file will be created on the first run)

5.  **🇷🇺 Откройте в браузере / 🇬🇧 Open in your browser:**
    * ➡️ **[http://127.0.0.1:5001](http://127.0.0.1:5001)**
    * (🇷🇺 Первым делом нужно будет зарегистрировать нового пользователя / 🇬🇧 You will need to register a new user first)

-----

## ⚙️ Как пользоваться / ⚙️ How to Use

* **🇷🇺 Регистрация:** Создайте свой аккаунт, чтобы начать работу.
* **🇬🇧 Registration:** Create your account to get started.

* **🇷🇺 Создание задачи:** Заполните форму: укажите название, выберите приоритет, добавьте теги через запятую, установите дедлайн и прикрепите файл, если нужно.
* **🇬🇧 Creating a Task:** Fill out the form: enter a description, select a priority, add tags separated by commas, set a deadline, and attach a file if needed.

* **🇷🇺 Фильтрация:** Используйте панель фильтров для поиска задач по тексту, статусу (активные/выполненные) или по конкретному тегу.
* **🇬🇧 Filtering:** Use the filter bar to search for tasks by text, status (active/completed), or by a specific tag.

* **🇷🇺 Управление:** Нажимайте ✔️ для выполнения задачи. После этого появится иконка 🗄️ для отправки в архив.
* **🇬🇧 Management:** Click ✔️ to complete a task. An archive icon 🗄️ will then appear to move it to the archive.