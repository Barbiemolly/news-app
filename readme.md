# 📰 News Portal (Django Web Application)

## 📌 Overview
A fully functional role-based news publishing and moderation platform built with Django. The system supports journalist submissions, editor moderation, reader subscriptions, and article management through both UI and RESTful API endpoints.

---

## 📁 Project Structure
News Application/
├── news_portal/ # Django project folder
│ ├── news_portal/ # Django project settings
│ │ ├── init.py
│ │ ├── settings.py
│ │ ├── urls.py
│ │ └── wsgi.py
│ │
│ ├── core/ # Main application folder
│ │ ├── api/ # API views and routing
│ │ ├── forms/ # Form logic (login, registration, article)
│ │ ├── models/ # Modular model files (article.py, user.py, publisher.py)
│ │ ├── serializers/ # DRF serializers
│ │ ├── signals/ # Signal handlers (e.g., notifications)
│ │ ├── templates/ # All HTML templates
│ │ │ ├── articles/
│ │ │ ├── auth/
│ │ │ ├── partials/
│ │ │ └── base.html
│ │ ├── templatetags/ # Custom template filters (e.g., form_tags.py)
│ │ ├── tests/ # All test files (API and Django tests)
│ │ │ ├── test_api.py
│ │ │ ├── test_article_approval_api.py
│ │ │ ├── test_model_article.py
│ │ │ ├── test_form_signup.py
│ │ │ └── test_view_home.py
│ │ ├── views/ # Modular views (home.py, article.py, export.py, etc.)
│ │ ├── admin.py
│ │ ├── urls.py
│ │ └── apps.py
│
├── planning/ # Contains diagrams and planning docs
│ ├── architecture_digram.drawio
│ ├── class_structure.png
│ └── architecture_diagram.pdf
│
├──readme.md
|
└── manage.py


---

## ✅ Features

### 🔐 Authentication
- Custom user model with roles: `Reader`, `Journalist`, `Editor`
- Readers register via the form; journalists/editors added via Django Admin
- Login/logout functionality with Bootstrap alert feedback
- Role-based dashboard redirects on login

### 📰 Articles
- Journalists:
  - Create, edit, resubmit rejected articles
  - Submit articles to publishers (optional)
- Editors:
  - View all submissions
  - Approve or reject articles with comments
- Readers:
  - View and search all approved articles
  - Access detail pages
- Public/unauthenticated visitors can view approved articles but not interact

### 📋 Moderation Tools
- Editors can soft-delete or restore articles
- Rejected articles require a rejection reason
- Article status flow: `submitted` → `approved` or `rejected`

### 🔍 Article Discovery
- Tag-based search (via query or filter)
- Top 5 trending tags
- Trending articles based on view count
- Reader-specific recommendations (subscriptions)
- Full-text search across title, content, and tags

### 📦 Export & Reporting
- Export individual articles to **PDF** or **CSV**
- Only authenticated users can download articles
- Article `view_count` tracked per visit

### 📨 Notifications & Subscriptions
- Readers can subscribe to journalists and publishers
- Email alerts sent when a new article is approved (via signals)
- Readers can manage subscriptions
- Subscriber count shown on profiles

### 🌐 RESTful API (via Django REST Framework)
- `GET /api/articles/` – List all approved articles (public)
- `GET /api/publisher/<publisher_id>/articles/` – List all articles by a publisher
- `GET /api/journalist/<journalist_id>/articles/` – List all articles by a journalist
- `POST /api/token/` – Obtain authentication token
- `POST /api/articles/create/ `– Submit new article (journalists only)
- `POST /api/articles/<pk>/approve/` – Approve article (editors only)
- `POST /api/articles/<pk>/reject/ `– Reject article with feedback (editors only)

---

## 🧪 Testing

All tests are organized in modular files:

- ✅ `test_api.py` — Submission and status APIs
- ✅ `test_article_approval_api.py` — API validation for duplicates, etc.
- ✅ `test_model_article.py` — Article model and methods
- ✅ `test_form_signup.py` — Login, logout, and registration
- ✅ `test_view_home.py` — Editor workflows, permission checks

Run tests with:

```bash
python manage.py test core.tests

```

---
## 💻 Setup & Installation

### 1. Clone & Setup Environment

```bash
git clone <https://github.com/hyperiondev-bootcamps/MN25030017735 >
cd news_portal

```
### 2. Create and activate virtual environment

```bash
python -m venv venv
venv\Scripts\activate   
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```
### 4. Configure Database (MariaDB)
Update settings.py:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'news_db',
        'USER': 'root',
        'PASSWORD': 'yourpassword',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
```
### 5. Apply migrations and run the development server

```bash
python manage.py migrate
python manage.py runserver
```

### 6. Create Superuser

```bash
python manage.py createsuperuser

```

---
## 🚀 Running the Server

```bash 
python manage.py runserver

```

Visit: http://localhost:8000

---

## 🔧 Tech Stack

Python 3.11+
Django 5.2.3
MariaDB 
Django REST Framework
Bootstrap 5.3
ReportLab (PDF)
Pillow, Paginator
Flake8
Black
HTML5

---

## 📚 Developer Notes

Readers can register, login, view, search, subscribe
Editors must log in via Django Admin
All form validations and messages are styled with Bootstrap
Custom 403 and 404 templates added
Public homepage displays articles even when not logged in

---

## 👤 Author

Molemo Khethwa
💻 Junior Web Developer | Software engineering student
