# EcoConnect Team Component Assignments

## 🌱 PROJECT OVERVIEW

**EcoConnect** is a local environmental action hub that connects environmentally-conscious individuals and communities to organize and participate in green initiatives. The platform enables users to create, discover, and join environmental events like tree planting, beach cleanups, recycling drives, and sustainability workshops.

### Theme Alignment
- **Environmental Focus:** All features center around ecological impact and community environmental action
- **Green Technology:** Digital platform reducing coordination barriers for environmental initiatives  
- **Sustainability:** Promotes local environmental stewardship through organized community events
- **Impact Tracking:** Photo documentation and participation metrics demonstrate real environmental outcomes

### Core Concept
Users can organize events (tree planting, cleanups), other community members join these events, participants share photos documenting environmental impact, and the platform tracks collective community achievements in environmental conservation.

### Project Statistics
- **Database Tables:** 8 models (User profiles, Events, Categories, Locations, Tags, History, Participation, Photos)
- **View Functions:** 16 total (6 class-based, 10 function-based)
- **Forms:** 10 with validation (Registration, Event creation/editing, Search, Photo upload, Contact)
- **Templates:** 17 responsive HTML pages with Bootstrap styling
- **JSON Fixtures:** 3 files with initial data (Categories, Locations, Tags)

### Key Features Implemented
- **User Management:** Registration, login, profiles, password reset
- **Event System:** Create, edit, join, leave environmental events  
- **Advanced Search:** Multi-criteria filtering by location, category, date, tags
- **Photo Sharing:** Upload and gallery system for event documentation
- **User Dashboard:** Activity tracking, participation history, statistics
- **Analytics:** Search trends, event statistics, user engagement metrics
- **Responsive Design:** Mobile-friendly Bootstrap interface with eco-themed styling

---

## Project Requirements
- **Each student:** 2 forms, 2 models, 2 templates, 2 views
- **Total needed:** 8 models, 8 forms, 8 views, 8 templates (minimum)

---

## 🚀 VANSH - Advanced Search & Discovery + Analytics

### Models (2/2) ✅
- ✅ `Location` (search/models.py)
- ✅ `SearchHistory` (search/models.py)

### Forms (3/2) ✅
- ✅ `AdvancedSearchForm` (search/forms.py)
- ✅ `QuickSearchForm` (search/forms.py)
- ✅ `FilterForm` (search/forms.py)

### Views (7/2) ✅
- ✅ `EventListView` (events/views.py) - Class-based
- ✅ `EventDetailView` (events/views.py) - Class-based
- ✅ `HomeView` (search/views.py) - Class-based
- ✅ `AdvancedSearchView` (search/views.py) - Class-based
- ✅ `SearchResultsView` (search/views.py) - Class-based
- ✅ `AnalyticsView` (search/views.py) - Class-based
- ✅ `contact_view` (search/views.py) - Function-based

### Templates (4/2) ✅
- ✅ `search/home.html`
- ✅ `events/event_list.html` 
- ✅ `search/analytics.html`
- ✅ `search/about.html`

---

## 🔐 RAJ - User Management & Authentication

### Models (2/2) ✅
- ✅ `UserProfile` (users/models.py)
- ✅ `EventTag` (search/models.py)

### Forms (2/2) ✅
- ✅ `UserRegistrationForm` (users/forms.py)
- ✅ `UserProfileForm` (users/forms.py)

### Views (2/2) ✅
- ✅ `login_view` (users/views.py)
- ✅ `register_view` (users/views.py)

### Templates (7) ✅
- ✅ `users/login.html`
- ✅ `users/register.html`
- ✅ `users/password_reset_form.html`
- ✅ `users/password_reset_done.html`
- ✅ `users/password_reset_confirm.html`
- ✅ `users/password_reset_complete.html`
- ✅ `users/password_reset_email.html`

---

## 📅 KIRTAN - Event Management System

### Models (2/2) ✅
- ✅ `Event` (events/models.py)
- ✅ `EventCategory` (events/models.py)

### Forms (2/2) ✅
- ✅ `EventCreationForm` (events/forms.py)
- ✅ `EventEditForm` (events/forms.py)

### Views (5/2) ✅
- ✅ `create_event` (events/views.py)
- ✅ `edit_event` (events/views.py) 
- ✅ `delete_event` (events/views.py)
- ✅ `join_event` (events/views.py)
- ✅ `leave_event` (events/views.py)

### Templates (3/2) ✅
- ✅ `events/create_event.html`
- ✅ `events/edit_event.html`
- ✅ `events/event_detail.html`

---

## 📊 DHRUV - User Interaction & History + Media

### Models (3/2) ✅
- ✅ `EventParticipation` (interaction/models.py)
- ✅ `PhotoUpload` (interaction/models.py)
- ✅ `UserHistory` (interaction/models.py)

### Forms (4/2) ✅
- ✅ `PhotoUploadForm` (interaction/forms.py)
- ✅ `EventFeedbackForm` (interaction/forms.py)
- ✅ `RSVPForm` (interaction/forms.py)
- ✅ `ContactForm` (interaction/forms.py)

### Views (2/2) ✅
- ✅ `dashboard` (interaction/views.py)
- ✅ `upload_photo` (interaction/views.py)

### Templates (3/2) ✅
- ✅ `interaction/dashboard.html`
- ✅ `interaction/upload_photo.html`
- ✅ `search/contact.html`

---

## ✅ COMPLETION STATUS

| Team Member | Models | Forms | Views | Templates | Status |
|-------------|--------|--------|--------|-----------|---------|
| **Vansh** | 2/2 ✅ | 3/2 ✅ | 7/2 ✅ | 4/2 ✅ | **COMPLETE** |
| **Raj** | 2/2 ✅ | 2/2 ✅ | 2/2 ✅ | 7/2 ✅ | **COMPLETE** |
| **Kirtan** | 2/2 ✅ | 2/2 ✅ | 5/2 ✅ | 3/2 ✅ | **COMPLETE** |
| **Dhruv** | 3/2 ✅ | 4/2 ✅ | 2/2 ✅ | 3/2 ✅ | **COMPLETE** |

---

## 🤔 REFLECTIONS

### 1. What did you learn from this project? (not just technical information)
We learned the importance of clear team communication and task coordination when building a full-stack application. Working on an environmental theme taught us how technology can serve meaningful social causes. We discovered that user experience design is just as important as backend functionality - creating intuitive interfaces for community engagement required thinking from the user's perspective. The project also taught us patience and persistence when debugging complex interactions between models, views, and templates.

### 2. Anything you would change or do differently
We would establish better version control practices from the beginning and create a more detailed project timeline with regular integration checkpoints. Earlier testing would have caught edge cases sooner. We'd also spend more time on initial database design to avoid later migrations. Better coordination on CSS styling could have prevented some inconsistencies. Most importantly, we'd start with a shared understanding of the user journey to ensure all features work cohesively together.

### 3. What is your 'best' achievement in the project? What are you most proud of?
We're most proud of creating a fully functional platform that actually serves its environmental mission - users can genuinely organize and participate in real environmental events. The advanced search system with multiple filters works seamlessly, and the photo upload feature creates a meaningful way to document environmental impact. The responsive design means the platform works well on any device, making environmental action more accessible. Overall, we built something that could actually help communities make a positive environmental difference.