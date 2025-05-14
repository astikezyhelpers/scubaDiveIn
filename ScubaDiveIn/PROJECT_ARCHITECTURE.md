# ScubaDiveIn Project Architecture

## Overview
ScubaDiveIn is a Django-based web application for managing scuba diving services and bookings. The project follows Django's MVT (Model-View-Template) architecture pattern.

## Project Structure

### Root Directory
```
ScubaDiveIn/
├── manage.py                 # Django's command-line utility
├── db.sqlite3               # SQLite database file
├── .env-example             # Example environment variables
├── .gitignore              # Git ignore rules
├── README.md               # Project documentation
├── ENHANCEMENTS.md         # Future enhancements documentation
├── media/                  # User-uploaded media files
├── static/                 # Static files (CSS, JS, images)
├── templates/              # HTML templates
├── mainSite/              # Main application
├── accounts/              # User authentication app
└── ScubaDiveIn/          # Project configuration
```

### Main Application (mainSite)
```
mainSite/
├── models.py              # Database models
├── views.py              # View logic
├── urls.py               # URL routing
├── admin.py              # Admin interface configuration
├── tests.py              # Test cases
├── apps.py               # App configuration
├── razorpay_utils.py     # Payment integration utilities
└── management/
    └── commands/
        └── add_sample_data.py  # Custom management command
```

### User Authentication (accounts)
```
accounts/
├── models.py              # User-related models
├── views.py              # Authentication views
├── urls.py               # Authentication URLs
├── forms.py              # User forms
├── signals.py            # Django signals
├── admin.py              # Admin interface configuration
└── apps.py               # App configuration
```

### Templates
```
templates/
├── base.html                     # Base template with common layout
├── payment.html                  # Payment processing page
├── payment_success.html          # Payment success confirmation
├── payment_failed.html           # Payment failure notification
│
├── mainSite/                     # Main application templates
│   ├── index.html               # Homepage with featured services
│   ├── about-us.html            # About page with company info
│   ├── courses.html             # List of all diving courses
│   ├── courseDetail.html        # Detailed course information
│   ├── instructors.html         # List of diving instructors
│   ├── blogs.html               # Blog listing page
│   ├── blogDetail.html          # Individual blog post view
│   ├── contact.html             # Contact form and information
│   ├── service_detail.html      # Detailed service information
│   └── base.html                # Main site base template
│
└── accounts/                     # Authentication templates
    ├── login.html               # User login form
    ├── signup.html              # User registration form
    └── profile.html             # User profile management
```

### Template Details

#### Main Application Templates
1. **index.html** (45KB)
   - Homepage layout
   - Featured services showcase
   - Quick navigation sections

2. **about-us.html** (11KB)
   - Company information
   - Team details
   - Mission and vision

3. **courses.html** (11KB)
   - Course catalog
   - Filtering options
   - Course categories

4. **courseDetail.html** (9.7KB)
   - Detailed course information
   - Pricing and schedule
   - Enrollment options

5. **instructors.html** (24KB)
   - Instructor profiles
   - Qualifications
   - Specializations

6. **blogs.html** (7.3KB)
   - Blog post listings
   - Categories
   - Search functionality

7. **blogDetail.html** (5.0KB)
   - Full blog post content
   - Comments section
   - Related posts

8. **contact.html** (11KB)
   - Contact form
   - Location information
   - Support details

9. **service_detail.html**
   - Individual service information
   - Booking options
   - Service specifications

#### Authentication Templates
1. **login.html** (2.4KB)
   - User login form
   - Password recovery
   - Remember me option

2. **signup.html** (6.6KB)
   - Registration form
   - Terms and conditions
   - Email verification

3. **profile.html**
   - User profile management
   - Account settings
   - Booking history

#### Payment Templates
1. **payment.html** (4.8KB)
   - Payment form
   - Order summary
   - Payment options

2. **payment_success.html** (2.3KB)
   - Success confirmation
   - Booking details
   - Next steps

3. **payment_failed.html**
   - Error notification
   - Retry options
   - Support contact

## Key Components

### Models
- **ServiceCategory**: Categories for diving services
- **DivingService**: Individual diving services with details
- **ServiceImage**: Images associated with diving services
- **User**: Custom user model for authentication

### Features
1. User Authentication
   - Registration
   - Login/Logout
   - Profile management

2. Diving Services
   - Service categories
   - Service listings
   - Service details
   - Image management

3. Payment Integration
   - Razorpay integration
   - Payment processing
   - Success/Failure handling

### Static Files
- CSS stylesheets
- JavaScript files
- Images and media

### Media
- User-uploaded content
- Service images
- Profile pictures

## Development Tools
- Django Management Commands
- Custom sample data generation
- Admin interface customization

## Security
- Environment variables for sensitive data
- User authentication
- Secure payment processing

## Future Enhancements
See `ENHANCEMENTS.md` for planned features and improvements. 