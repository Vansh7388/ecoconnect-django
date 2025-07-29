# EcoConnect Setup Instructions

## 1. Install Dependencies
```bash
pip install -r requirements.txt
```

## 2. Environment Configuration
Create `.env` file with:
```env
GMAIL_USER=your-email@gmail.com
GMAIL_APP_PASSWORD=your-gmail-app-password
```

## 3. Database Setup
```bash
# Create database
python manage.py makemigrations
python manage.py migrate

# Load initial data
python manage.py loaddata events/fixtures/initial_categories.json
python manage.py loaddata search/fixtures/initial_locations.json
python manage.py loaddata search/fixtures/initial_tags.json

# Create superuser
python manage.py createsuperuser
```

## 4. Run Development Server
```bash
python manage.py runserver
```

## 5. Test Features
- Visit: http://localhost:8000
- Test password reset functionality
- Upload photos for events
- Use advanced search filters

## 6. Export Database (for submission)
```bash
python manage.py dumpdata --indent 2 > database_export.json
```