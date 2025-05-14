# ScubaDiveIn - Scuba Diving Services Website

A complete web platform for a scuba diving business, offering course information, booking services, and online payments.

## Project Overview

ScubaDiveIn is a Django-based website for a scuba diving business that allows customers to:
- Browse available diving courses and services
- View instructor profiles
- Read blog content about diving
- Book diving services with online payment integration (Razorpay)

## Project Structure

```
ScubaDiveIn/
├── db.sqlite3               # SQLite database
├── manage.py                # Django management script
├── mainSite/                # Main Django application
│   ├── models.py            # Database models
│   ├── views.py             # View functions
│   ├── urls.py              # URL routing
│   └── admin.py             # Admin panel configuration
├── ScubaDiveIn/             # Project settings
│   ├── settings.py          # Django configuration
│   └── urls.py              # Main URL routing
├── static/                  # Static assets
│   ├── images/              # Image files
│   └── videos/              # Video files
└── templates/               # HTML templates
    ├── base.html            # Base template with common elements
    ├── payment.html         # Payment processing templates
    └── mainSite/            # Main site templates
        ├── index.html       # Homepage
        ├── courses.html     # Courses listing
        ├── instructors.html # Instructor profiles
        ├── blogs.html       # Blog listing
        └── about-us.html    # About page
```

## Features

- **Service Catalog**: Browsable catalog of diving services and courses
- **Category Management**: Services organized by categories
- **Course Details**: Detailed information about each diving course
- **Instructor Profiles**: Information about diving instructors
- **Blog System**: Informational articles about diving
- **Online Booking**: Service reservation system
- **Payment Integration**: Secure online payments via Razorpay
- **Responsive Design**: Mobile-friendly interface

## Technical Stack

- **Backend**: Django 4.2
- **Database**: SQLite (development)
- **Frontend**: HTML, CSS, JavaScript
- **Payment Gateway**: Razorpay
- **Deployment**: Production server with Apache/Nginx

## Current Status

The website includes:
- Main informational pages (home, about, courses, instructors)
- Blog functionality
- Payment processing system with Razorpay integration
- Basic user account functionality

## Installation and Setup

1. Clone the repository
2. Install requirements: `pip install -r requirements.txt`
3. Run migrations: `python manage.py migrate`
4. Create a superuser: `python manage.py createsuperuser`
5. Run the development server: `python manage.py runserver`
6. Access the admin panel at `http://localhost:8000/admin/`

## Payment Integration

The website uses Razorpay for payment processing. Test credentials are included in the settings file. For production, replace these with actual API keys. 