# 📰 News Portal (Django Web Application)

## 📌 Overview
A fully functional role-based news publishing and moderation platform built with Django. The system supports journalist submissions, editor moderation, reader subscriptions, and article management through both UI and RESTful API endpoints.

---

## 📁 Project Structure
news-app/
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
| | 
| ├──Dockerfile
| ├──.dockerignore
| ├──docker-compose.yaml
| └── Docs/ _build/html...
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
## 📚 Sphinx Documentation Setup (For Developers)
This section provides setup and usage instructions for the Sphinx-based documentation system used in this project.
---

#### 🧱 Prerequisites
Ensure you have the following installed:
- Python environment (activate your virtualenv)
- Django properly configured
- Sphinx and the ReadTheDocs theme installed:

```bash
    pip install sphinx sphinx-rtd-theme
```
---

### ⚙️ Configuration
Create a file named conf.py under the /docs directory with the following at the top:

    import os
    import sys
    import django

    sys.path.insert(0, os.path.abspath('..'))
    os.environ['DJANGO_SETTINGS_MODULE'] = 'news_portal.settings'  # Replace if different
    django.setup()

📌 This enables autodoc to load your Django models, views, and serializers.

---

### 🏗️ Generating Documentation

1. Navigate to the /docs directory:
```bash
   cd docs
```

2. Run the autodoc command to generate .rst files:

       sphinx-apidoc -o . ../core

3. Build HTML docs:

       make html

4. Output will be in:
```bash
       docs/_build/html/
```
5. To view the docs, open the file:
```ash
       docs/_build/html/index.html
```
---

🚀 Git & Deployment Notes
To ensure Sphinx HTML build is pushed:
- Add this to .gitignore to include only Sphinx output:
```bash
      # Ignore all build folders...
      build/

      # ...but include this Sphinx folder
      !docs/_build/html/
```
- On Windows/PowerShell, run the following inside /docs/_build/html:
```bash
      echo "" > .nojekyll
```
This ensures GitHub Pages doesn’t ignore folders starting with underscores.


---
##🐳 Docker Setup

This project supports containerized development using Docker and Docker Compose. It includes:

- Django (Python 3.11)
- MariaDB 10.6+
- Volume mapping for live code editing
- Optional SQLite fallback for lightweight testing

### ⚙️ Requirements

- Docker Desktop or Play with Docker (labs.play-with-docker.com)
- A GitHub account (if testing from a public repo)

### 📁 Project Structure

news-app/
├── news_portal/
│   ├── Dockerfile
│   ├── docker-compose.yaml
│   ├── manage.py
│   ├── core/
│   └── ...

> `manage.py` and `docker-compose.yaml` must be in the same directory (`news_portal/`).

### 🔐 Important: Set Your Own MariaDB Password
For security and compatibility:

Replace all occurrences of "yourpassword" with your own secure password.

This applies to both:

  1. In docker-compose.yaml:
    environment:
      MYSQL_ROOT_PASSWORD: your_secure_password
      MYSQL_DATABASE: news_db
  Also update under web.environment:
    - DB_PASSWORD=your_secure_password

### 🚀 Quick Start (Local)

Clone and run the project locally with:

git clone https://github.com/your-username/your-repo.git
cd your-repo/news_portal

docker-compose up --build

Then open: http://localhost:8000

To create an admin user:

docker-compose exec web python manage.py createsuperuser

### 🌐 Quick Start (Play with Docker)

1. Open: https://labs.play-with-docker.com/
2. Create a new session and select a node.
3. Run:

   git clone https://github.com/your-username/your-repo.git
   cd your-repo/news_portal
   docker-compose up --build

4. Wait for the server to start (look for “Starting development server at http://0.0.0.0:8000/”)
5. Click **Expose Port** and enter `8000`
6. Visit the generated URL in your browser

### 🔐 Creating the Superuser

docker-compose exec web python manage.py createsuperuser

#### 🧠 Switching Between MariaDB and SQLite

This project uses an environment variable to toggle the database engine:

Mode     | IN_DOCKER Value | Behavior
---------|------------------|---------
Docker   | 0                | Uses MariaDB
Fallback | 1                | Uses SQLite

This is handled inside settings.py:

IN_DOCKER = os.environ.get("IN_DOCKER") == "1"

if IN_DOCKER:
    # Use SQLite
else:
    # Use MariaDB

### 📄 Useful Commands

docker-compose up -d        # Start in background
docker-compose down         # Stop all services
docker-compose exec web bash   # Shell into Django container
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser

### 🧼 Clean Build

If anything breaks or changes:

docker-compose down -v
docker-compose build --no-cache
docker-compose up

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
