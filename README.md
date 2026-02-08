# Patient Clinical Data Management System

A full-stack web application built with Django for managing patient records and clinical data. Designed for lab assistants to register patients, record vital signs (Blood Pressure, Height/Weight, Heart Rate), and generate analytical reports including BMI calculations.

## Features

- **Patient Management** -- Create, view, update, and delete patient records (full CRUD)
- **Clinical Data Entry** -- Record vitals such as Blood Pressure, Height/Weight, and Heart Rate for each patient
- **Data Analysis & Reporting** -- View patient clinical history with auto-calculated BMI from height and weight entries
- **Responsive Table UI** -- Clean tabular interface with styled CSS for easy data browsing

## Tech Stack

| Layer       | Technology          |
|-------------|---------------------|
| Backend     | Python, Django 3.2  |
| Database    | PostgreSQL (default), SQLite (Docker/testing) |
| Frontend    | Django Templates, HTML5, CSS3 |
| Containerization | Docker, Docker Compose |

## Project Structure

```
clinicals/
├── clinicals/                  # Django project settings
│   ├── settings.py             # Configuration (DB, apps, middleware)
│   ├── urls.py                 # Root URL routing
│   ├── wsgi.py                 # WSGI entry point
│   └── asgi.py                 # ASGI entry point
├── clinicalsApp/               # Main application
│   ├── models.py               # Patient & ClinicalData models
│   ├── views.py                # Class-based & function-based views
│   ├── forms.py                # Django ModelForms
│   ├── tests.py                # Unit tests
│   ├── admin.py                # Admin configuration
│   └── migrations/             # Database migrations
├── templates/clinicalsApp/     # HTML templates
│   ├── patient_list.html       # Home page - patient listing
│   ├── patient_form.html       # Create/Update patient form
│   ├── clinicaldata_form.html  # Clinical data entry form
│   ├── generateReport.html     # Analysis report page
│   └── patient_confirm_delete.html
├── static/css/
│   └── clinicals.css           # Application styles
├── Dockerfile                  # Docker image definition
├── docker-compose.yml          # Multi-container orchestration
├── requirements.txt            # Python dependencies
└── manage.py                   # Django management CLI
```

## Data Models

### Patient
| Field     | Type         | Description          |
|-----------|--------------|----------------------|
| id        | BigAutoField | Primary key          |
| firstName | CharField    | Patient first name   |
| lastName  | CharField    | Patient last name    |
| age       | IntegerField | Patient age          |

### ClinicalData
| Field            | Type          | Description                              |
|------------------|---------------|------------------------------------------|
| id               | BigAutoField  | Primary key                              |
| componentName    | CharField     | Type: Height/Weight, Blood Pressure, Heart Rate |
| componentValue   | CharField     | Recorded measurement value               |
| measuredDateTime | DateTimeField | Auto-set timestamp of recording          |
| patient          | ForeignKey    | Reference to Patient (CASCADE delete)    |

## API Endpoints

| Method   | URL                  | Description                    |
|----------|----------------------|--------------------------------|
| GET      | `/`                  | List all patients              |
| GET/POST | `/create/`           | Register a new patient         |
| GET/POST | `/update/<id>`       | Update patient details         |
| GET/POST | `/delete/<id>`       | Delete patient (confirmation)  |
| GET/POST | `/addData/<id>`      | Add clinical data for patient  |
| GET      | `/analyze/<id>`      | View clinical report with BMI  |

## Getting Started

### Option 1: Run with Docker (Recommended)

No need to install Python or PostgreSQL locally.

```bash
# Clone the repository
git clone https://github.com/govicsit/clinicals.git
cd clinicals

# Build and start containers
docker-compose up --build

# Access the application
open http://localhost:8000
```

To stop:
```bash
docker-compose down
```

### Option 2: Run Locally

**Prerequisites:** Python 3.8+, PostgreSQL

```bash
# Clone the repository
git clone https://github.com/govicsit/clinicals.git
cd clinicals

# Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create PostgreSQL database
psql -U postgres -c "CREATE DATABASE clinicalsdb;"

# Update database credentials in clinicals/settings.py if needed

# Run migrations
python manage.py makemigrations
python manage.py migrate

# Start the development server
python manage.py runserver
```

Access the app at `http://localhost:8000`.

## Running Tests

```bash
# Using SQLite (no PostgreSQL required)
python manage.py test clinicalsApp

# With Docker
docker-compose exec web python manage.py test clinicalsApp
```
