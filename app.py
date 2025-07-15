import os
from datetime import datetime, date, timedelta
from flask import Flask, render_template, request, redirect, url_for, jsonify, send_from_directory, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from flask_bcrypt import Bcrypt
from werkzeug.utils import secure_filename

basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'todo.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'a-very-hard-to-guess-secret-key'
app.config['UPLOAD_FOLDER'] = os.path.join(basedir, 'uploads')
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Пожалуйста, войдите, чтобы получить доступ к этой странице.'

TRANSLATIONS = {
    "ru": {
        "title": "Менеджер задач",
        "header_tasks": "Мои задачи",
        "header_archive": "Архив задач",
        "header_analytics": "Аналитика",
        "auth_login_title": "Вход",
        "auth_register_title": "Регистрация",
        "username": "Имя пользователя",
        "password": "Пароль",
        "login_btn": "Войти",
        "register_btn": "Зарегистрироваться",
        "no_account": "Нет аккаунта?",
        "have_account": "Уже есть аккаунт?",
        "placeholder_desc": "Описание задачи",
        "label_priority": "Приоритет:",
        "priority_high": "Высокий",
        "priority_medium": "Средний",
        "priority_low": "Низкий",
        "label_tags": "Теги (через запятую):",
        "placeholder_tags": "работа, учеба",
        "label_deadline": "Дедлайн:",
        "label_attachment": "Прикрепить файл:",
        "add_task_btn": "Добавить задачу",
        "filter_search_placeholder": "Поиск по задачам...",
        "filter_all_statuses": "Все статусы",
        "filter_active": "Активные",
        "filter_completed": "Выполненные",
        "filter_all_tags": "Все теги",
        "filter_search_btn": "🔍",
        "filter_reset_btn": "Сбросить",
        "attachment_link": "📎 Файл",
        "deadline_overdue": "Просрочено",
        "deadline_today": "Сегодня",
        "deadline_days_left": "Осталось",
        "days_unit": "дн.",
        "user_controls_analytics": "Аналитика",
        "user_controls_archive": "Архив",
        "user_controls_logout": "Выйти",
        "archive_restore_btn": "Восстановить",
        "archive_delete_forever_btn": "Удалить навсегда",
        "archive_back_link": "К задачам ↩️",
        "stats_this_week": "задач выполнено на этой неделе",
        "stats_this_month": "задач выполнено в этом месяце",
        "stats_header": "Активность за последние 30 дней",
        "chart_label": "Выполненные задачи"
    },
    "en": {
        "title": "Task Manager",
        "header_tasks": "My Tasks",
        "header_archive": "Task Archive",
        "header_analytics": "Analytics",
        "auth_login_title": "Login",
        "auth_register_title": "Register",
        "username": "Username",
        "password": "Password",
        "login_btn": "Login",
        "register_btn": "Register",
        "no_account": "No account?",
        "have_account": "Already have an account?",
        "placeholder_desc": "Task description",
        "label_priority": "Priority:",
        "priority_high": "High",
        "priority_medium": "Medium",
        "priority_low": "Low",
        "label_tags": "Tags (comma-separated):",
        "placeholder_tags": "work, study",
        "label_deadline": "Deadline:",
        "label_attachment": "Attach file:",
        "add_task_btn": "Add Task",
        "filter_search_placeholder": "Search tasks...",
        "filter_all_statuses": "All statuses",
        "filter_active": "Active",
        "filter_completed": "Completed",
        "filter_all_tags": "All tags",
        "filter_search_btn": "🔍",
        "filter_reset_btn": "Reset",
        "attachment_link": "📎 File",
        "deadline_overdue": "Overdue by",
        "deadline_today": "Today",
        "deadline_days_left": "days left",
        "days_unit": "d.",
        "user_controls_analytics": "Analytics",
        "user_controls_archive": "Archive",
        "user_controls_logout": "Logout",
        "archive_restore_btn": "Restore",
        "archive_delete_forever_btn": "Delete permanently",
        "archive_back_link": "To tasks ↩️",
        "stats_this_week": "tasks completed this week",
        "stats_this_month": "tasks completed this month",
        "stats_header": "Activity in the last 30 days",
        "chart_label": "Completed tasks"
    }
}

def get_text(lang, key):
    return TRANSLATIONS.get(lang, TRANSLATIONS['ru']).get(key, key)

@app.context_processor
def inject_globals():
    return dict(
        lang=session.get('lang', 'ru'),
        theme=session.get('theme', 'light'),
        get_text=get_text
    )

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    tasks = db.relationship('Task', backref='owner', lazy=True)

    def set_password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf8')

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

task_tags = db.Table('task_tags',
    db.Column('task_id', db.Integer, db.ForeignKey('task.id'), primary_key=True),
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'), primary_key=True)
)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(200), nullable=False)
    added = db.Column(db.DateTime, default=datetime.utcnow)
    completed_date = db.Column(db.Date, nullable=True)
    deadline = db.Column(db.Date, nullable=True)
    status = db.Column(db.String(50), default='не выполнено')
    is_archived = db.Column(db.Boolean, default=False)
    priority = db.Column(db.Integer, default=2)
    sort_order = db.Column(db.Integer, nullable=False, default=0)
    attachment_filename = db.Column(db.String(200), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    tags = db.relationship('Tag', secondary=task_tags, backref=db.backref('tasks', lazy='dynamic'))

class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)

@app.route('/language/<lang>')
def set_language(lang):
    session['lang'] = lang
    return redirect(request.referrer or url_for('index'))

@app.route('/theme/<theme_name>')
def set_theme(theme_name):
    session['theme'] = theme_name
    return redirect(request.referrer or url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if User.query.filter_by(username=username).first():
            return render_template('register.html', error='Имя пользователя уже занято')
        new_user = User(username=username)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)
        return redirect(url_for('index'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    if request.method == 'POST':
        user = User.query.filter_by(username=request.form.get('username')).first()
        if user and user.check_password(request.form.get('password')):
            login_user(user)
            return redirect(url_for('index'))
        else:
            return render_template('login.html', error='Неверное имя пользователя или пароль')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/')
@login_required
def index():
    query = Task.query.filter_by(is_archived=False, owner=current_user)
    search_term = request.args.get('search', '')
    status_filter = request.args.get('status', 'all')
    tag_filter_id = request.args.get('tag', type=int)

    if search_term:
        query = query.filter(Task.description.ilike(f'%{search_term}%'))
    if status_filter != 'all':
        query = query.filter_by(status=status_filter)
    if tag_filter_id and (tag := Tag.query.get(tag_filter_id)):
        query = query.with_parent(tag)

    tasks = query.order_by(Task.sort_order).all()
    all_tags = Tag.query.all()
    
    return render_template('index.html', tasks=tasks, all_tags=all_tags, today=date.today(),
                           search_term=search_term, status_filter=status_filter, tag_filter_id=tag_filter_id)

@app.route('/analytics')
@login_required
def analytics():
    today = date.today()
    start_of_week = today - timedelta(days=today.weekday())
    start_of_month = today.replace(day=1)
    
    tasks_this_week = Task.query.filter(
        Task.owner == current_user,
        Task.status == 'выполнено',
        Task.completed_date >= start_of_week
    ).count()

    tasks_this_month = Task.query.filter(
        Task.owner == current_user,
        Task.status == 'выполнено',
        Task.completed_date >= start_of_month
    ).count()

    last_30_days = [today - timedelta(days=i) for i in range(29, -1, -1)]
    tasks_by_day = db.session.query(
        Task.completed_date, db.func.count(Task.id)
    ).filter(
        Task.owner == current_user,
        Task.status == 'выполнено',
        Task.completed_date.in_(last_30_days)
    ).group_by(Task.completed_date).all()

    completion_data = {d.strftime('%Y-%m-%d'): c for d, c in tasks_by_day}
    chart_labels = [d.strftime('%d.%m') for d in last_30_days]
    chart_data = [completion_data.get(d.strftime('%Y-%m-%d'), 0) for d in last_30_days]

    return render_template('analytics.html', tasks_this_week=tasks_this_week, tasks_this_month=tasks_this_month,
                           chart_labels=chart_labels, chart_data=chart_data)

@app.route('/add', methods=['POST'])
@login_required
def add_task():
    description = request.form.get('description')
    if not description: return redirect(url_for('index'))

    max_order = db.session.query(db.func.max(Task.sort_order)).filter_by(owner=current_user).scalar() or -1
    new_task = Task(description=description, owner=current_user, sort_order=max_order + 1)
    new_task.priority = request.form.get('priority', 2, type=int)
    if deadline_str := request.form.get('deadline'):
        new_task.deadline = datetime.strptime(deadline_str, '%Y-%m-%d').date()

    if tags_str := request.form.get('tags'):
        for name in {name.strip() for name in tags_str.split(',') if name.strip()}:
            tag = Tag.query.filter_by(name=name).first() or Tag(name=name)
            new_task.tags.append(tag)

    if 'attachment' in request.files and (file := request.files['attachment']).filename:
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        new_task.attachment_filename = filename
            
    db.session.add(new_task)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/uploads/<filename>')
@login_required
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/update_order', methods=['POST'])
@login_required
def update_order():
    task_ids = request.json.get('order', [])
    for index, task_id in enumerate(task_ids):
        if task := Task.query.filter_by(id=task_id, owner=current_user).first():
            task.sort_order = index
    db.session.commit()
    return jsonify({'status': 'success'})

@app.route('/complete/<int:task_id>')
@login_required
def complete_task(task_id):
    task = Task.query.filter_by(id=task_id, owner=current_user).first_or_404()
    task.status = "выполнено"
    task.completed_date = date.today()
    db.session.commit()
    return redirect(request.referrer or url_for('index'))

@app.route('/archive_task/<int:task_id>')
@login_required
def archive_task(task_id):
    task = Task.query.filter_by(id=task_id, owner=current_user).first_or_404()
    task.is_archived = True
    db.session.commit()
    return redirect(request.referrer or url_for('index'))

@app.route('/delete/<int:task_id>')
@login_required
def delete_task(task_id):
    task = Task.query.filter_by(id=task_id, owner=current_user).first_or_404()
    if task.attachment_filename:
        try: os.remove(os.path.join(app.config['UPLOAD_FOLDER'], task.attachment_filename))
        except OSError: pass
    db.session.delete(task)
    db.session.commit()
    return redirect(request.referrer or url_for('index'))

@app.route('/archive')
@login_required
def archive():
    archived_tasks = Task.query.filter_by(is_archived=True, owner=current_user).order_by(Task.added.desc()).all()
    return render_template('archive.html', tasks=archived_tasks)

@app.route('/restore_task/<int:task_id>')
@login_required
def restore_task(task_id):
    task = Task.query.filter_by(id=task_id, owner=current_user).first_or_404()
    task.is_archived = False
    task.status = 'не выполнено'
    task.completed_date = None
    db.session.commit()
    return redirect(url_for('archive'))

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True, port=5001)