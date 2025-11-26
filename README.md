# 🏢 Enterprise Django

A comprehensive enterprise-grade Django web application featuring order management, user authentication, email notifications, and a powerful admin interface. Built with modern best practices and production-ready features.

## ✨ Key Features

### 🔐 Authentication & User Management
- User registration with email confirmation
- Secure login/logout with "Remember Me" functionality (2-week sessions)
- Password reset via email
- User profile management (view/edit profile, change password)
- Activity audit logging with IP tracking

### 📦 Order Management System
- Create and track orders with real-time status updates
- Order status tracking: Pending → Processing → Shipped → Delivered
- Priority levels (Normal/Urgent) with visual indicators
- Advanced search functionality (by title, client, description)
- Pagination (15 orders per page)
- Email notifications for order confirmations and status updates

### 📧 Email System
- Professional HTML email templates
- Welcome emails for new users
- Order confirmation emails
- Order status update notifications
- Contact form submission confirmations

### �️ Security Features
- Rate limiting on sensitive endpoints (login, signup, contact forms)
- CSRF protection
- XSS protection
- Secure password hashing
- Input validation and sanitization
- Custom 429 rate limit error page

### 🎨 User Interface
- Responsive Bootstrap 5 design
- AJAX form submissions for better UX
- Breadcrumb navigation
- Custom form template tags
- Dynamic service page content (CMS)
- Partner logo management

### �‍💼 Enhanced Admin Interface
- Color-coded status badges
- Advanced filters and search
- Soft delete functionality (restore deleted items)
- Bulk actions for order status updates
- Activity audit log viewer
- Rich text editor support
- Database optimization with indexes

### 🔍 Advanced Features
- Multi-field search with Q objects
- Soft delete with recovery option
- Comprehensive audit logging (9 action types)
- Phone number validation with regional support
- Dynamic content management (Service pages)
- Database query optimization

## 🛠️ Tech Stack

- **Backend:** Django 5.1.1 (Python 3.12.3)
- **Frontend:** Bootstrap 5, JavaScript (AJAX)
- **Database:** SQLite3 (development) / PostgreSQL ready (production)
- **Email:** Django Email Backend (SMTP ready)
- **Rate Limiting:** django-ratelimit 4.1.0
- **Image Processing:** Pillow 11.0.0
- **Phone Numbers:** django-phonenumber-field 7.3.0

## 🚀 Quick Start

### Prerequisites
- Python 3.12+ installed
- Git installed
- Virtual environment support

### Installation Steps

1. **Clone the repository:**
   ```bash
   git clone https://github.com/tahagill/Enterprise-Django.git
   cd Enterprise-Django
   ```

2. **Create and activate virtual environment:**
   ```bash
   # Create virtual environment
   python -m venv .venv
   
   # Activate on Windows:
   .venv\Scripts\activate
   
   # Activate on macOS/Linux:
   source .venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables (optional):**
   ```bash
   # Copy the example environment file
   cp .env.example .env
   
   # Edit .env with your settings (email, API keys, etc.)
   ```

5. **Run database migrations:**
   ```bash
   python manage.py migrate
   ```

6. **Create a superuser:**
   ```bash
   python manage.py createsuperuser
   ```

7. **Collect static files:**
   ```bash
   python manage.py collectstatic --noinput
   ```

8. **Run the development server:**
   ```bash
   python manage.py runserver
   ```

9. **Access the application:**
   - **Main App:** http://127.0.0.1:8000/
   - **Admin Panel:** http://127.0.0.1:8000/admin/

## 📱 Application Structure

```
Enterprise-Django/
├── Hello/                  # Project settings
│   ├── settings.py        # Main configuration
│   ├── urls.py            # URL routing
│   └── wsgi.py            # WSGI configuration
├── home/                   # Main application
│   ├── models.py          # Database models
│   ├── views.py           # Business logic
│   ├── forms.py           # Form definitions
│   ├── admin.py           # Admin customization
│   ├── utils/             # Utility functions
│   │   ├── email_utils.py # Email handling
│   │   └── mixins.py      # Reusable mixins
│   ├── templates/         # HTML templates
│   │   ├── emails/        # Email templates
│   │   └── *.html         # Page templates
│   ├── static/            # Static files
│   │   ├── css/           # Stylesheets
│   │   ├── js/            # JavaScript
│   │   └── images/        # Images
│   ├── migrations/        # Database migrations
│   └── templatetags/      # Custom template tags
├── staticfiles/           # Collected static files
├── manage.py              # Django CLI
├── requirements.txt       # Python dependencies
├── .env.example           # Environment template
├── .gitignore            # Git ignore rules
├── SECURITY.md           # Security documentation
└── README.md             # This file
```

## 🎯 Key Pages & URLs

| Page | URL | Description |
|------|-----|-------------|
| Home/Login | `/` | Landing page and login |
| Sign Up | `/signup/` | User registration |
| Profile | `/profile/` | User profile management |
| Orders | `/orders/` | Create and view orders |
| Order Status | `/status/` | Track order status |
| Contact | `/contact/` | Contact form |
| Services | `/services/` | Dynamic services page |
| About | `/about/` | About page |
| Admin Panel | `/admin/` | Django admin interface |
| Password Reset | `/accounts/password_reset/` | Reset password |

## 🔧 Configuration

### Email Settings
Configure email in `.env` or `settings.py`:
```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your-email@gmail.com'
EMAIL_HOST_PASSWORD = 'your-app-password'
```

### Rate Limiting
Configured limits:
- Login: 5 attempts per 5 minutes
- Signup: 3 attempts per 5 minutes
- Contact Form: 10 submissions per hour
- Order Creation: 20 per hour

### Database Optimization
- 7 single-field indexes
- 2 composite indexes
- Optimized query patterns

## 🧪 Testing

Run the comprehensive test suite:
```bash
# Run all tests
python manage.py test home

# Run with verbose output
python manage.py test home --verbosity=2

# Run specific test class
python manage.py test home.tests.OrderTests
```

**Test Coverage:** 37 tests covering models, views, authentication, orders, contacts, search, audit logging, and more.

## 🚀 Deployment

### Production Checklist
- [ ] Set `DEBUG = False` in settings
- [ ] Configure `ALLOWED_HOSTS`
- [ ] Set up PostgreSQL database
- [ ] Configure production email backend
- [ ] Set strong `SECRET_KEY`
- [ ] Enable HTTPS (`SECURE_SSL_REDIRECT = True`)
- [ ] Configure static/media file serving
- [ ] Set up logging and monitoring
- [ ] Configure backup strategy

### Environment Variables for Production
```bash
DJANGO_SECRET_KEY=your-production-secret-key
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
DATABASE_URL=postgresql://user:password@localhost:5432/dbname
EMAIL_HOST_PASSWORD=your-email-password
```

## 📚 Documentation

- **[SECURITY.md](SECURITY.md)** - Security guidelines and best practices
- **[TESTING_REPORT.md](TESTING_REPORT.md)** - Comprehensive testing documentation
- **[.env.example](.env.example)** - Environment configuration template

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is open source and available under the MIT License.

## 👨‍💻 Author

**Taha Gill**
- GitHub: [@tahagill](https://github.com/tahagill)

## 🎉 Acknowledgments

- Django Framework
- Bootstrap 5
- All contributors and supporters

---

**⭐ Star this repository if you find it helpful!**
