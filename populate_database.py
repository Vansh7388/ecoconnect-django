#!/usr/bin/env python
"""
Database Population Script for EcoConnect - WITH EVENTTAGS
Run this script from the project root directory: python populate_database.py
"""

import os
import sys
import django
import random
from datetime import datetime, timedelta

# Setup Django FIRST
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecoconnect.settings')
django.setup()

# Import Django modules AFTER setup
from django.conf import settings
from django.utils import timezone
from django.contrib.auth.models import User
from users.models import UserProfile
from events.models import Event, EventCategory
from search.models import Location, SearchHistory, EventTag  # Added EventTag
from interaction.models import EventParticipation, UserHistory

def clear_existing_data():
    """Clear all existing user-generated data"""
    print("🗑️  Clearing existing data...")
    
    # Clear in proper order to avoid foreign key constraints
    EventParticipation.objects.all().delete()
    UserHistory.objects.all().delete()
    SearchHistory.objects.all().delete()
    Event.objects.all().delete()
    UserProfile.objects.all().delete()
    
    # Delete users except superuser
    User.objects.filter(is_superuser=False).delete()
    
    print("✅ Old data cleared!")

def create_users():
    """Create the 4 team members"""
    users_data = [
        {
            'username': 'vansh_patel',
            'first_name': 'Vansh',
            'last_name': 'Patel',
            'email': 'vansh.patel@email.com',
            'bio': 'Environmental data analyst passionate about using technology to track and improve our environmental impact. Love creating analytics dashboards!',
            'location': 'Oshawa',
            'interests': 'Data Analytics, Environmental Monitoring, Tree Planting'
        },
        {
            'username': 'raj_patel',
            'first_name': 'Raj',
            'last_name': 'Patel',
            'email': 'raj.patel@email.com',
            'bio': 'Security-focused developer who believes in creating safe digital spaces for environmental activism. Interested in user authentication and privacy.',
            'location': 'Whitby',
            'interests': 'Digital Security, Beach Cleanup, Community Organizing'
        },
        {
            'username': 'kirtan_prajapati',
            'first_name': 'Kirtan',
            'last_name': 'Prajapati',
            'email': 'kirtan.prajapati@email.com',
            'bio': 'Event management enthusiast who loves bringing people together for environmental causes. Experienced in organizing large-scale community events.',
            'location': 'Ajax',
            'interests': 'Event Management, Community Gardens, Sustainability Workshops'
        },
        {
            'username': 'dhruv_patel',
            'first_name': 'Dhruv',
            'last_name': 'Patel',
            'email': 'dhruv.patel@email.com',
            'bio': 'Photography and media specialist documenting environmental change. Believes that visual storytelling can inspire environmental action.',
            'location': 'Pickering',
            'interests': 'Environmental Photography, Wildlife Conservation, Media Production'
        }
    ]
    
    created_users = []
    for user_data in users_data:
        # Create Django user
        user, created = User.objects.get_or_create(
            username=user_data['username'],
            defaults={
                'first_name': user_data['first_name'],
                'last_name': user_data['last_name'],
                'email': user_data['email'],
                'is_active': True
            }
        )
        
        if created:
            user.set_password('password123')  # Simple password for demo
            user.save()
            print(f"Created user: {user_data['first_name']} {user_data['last_name']}")
        
        # Create user profile
        profile, created = UserProfile.objects.get_or_create(
            user=user,
            defaults={
                'bio': user_data['bio'],
                'location': user_data['location'],
                'environmental_interests': user_data['interests'],
                'join_date': timezone.now() - timedelta(days=random.randint(30, 180))
            }
        )
        
        created_users.append(user)
    
    return created_users

def get_tags_for_event(event_title, category_name):
    """Get appropriate tags for an event based on its title and category"""
    tags = []
    
    # Get all available tags
    all_tags = {tag.name: tag for tag in EventTag.objects.all()}
    
    title_lower = event_title.lower()
    category_lower = category_name.lower()
    
    # Educational events
    if any(word in title_lower for word in ['workshop', 'learn', 'training', 'analytics', 'data']):
        tags.append(all_tags.get('Educational'))
    
    # Outdoor events  
    if any(word in title_lower for word in ['tree', 'planting', 'beach', 'cleanup', 'outdoor', 'garden']):
        tags.append(all_tags.get('Outdoor'))
    
    # Community events
    if any(word in title_lower for word in ['community', 'festival', 'large scale', 'coordination']):
        tags.append(all_tags.get('Community'))
    
    # Volunteer opportunities
    if any(word in title_lower for word in ['join', 'help', 'volunteer', 'drive', 'cleanup']):
        tags.append(all_tags.get('Volunteer'))
    
    # Corporate/Professional
    if any(word in title_lower for word in ['corporate', 'business', 'professional', 'secure', 'digital']):
        tags.append(all_tags.get('Corporate'))
    
    # Research/Technical
    if any(word in title_lower for word in ['data', 'analytics', 'gps', 'technology', 'documentation', 'media']):
        tags.append(all_tags.get('Research'))
    
    # Seasonal (if mentions specific timing)
    if any(word in title_lower for word in ['winter', 'summer', 'spring', 'fall', 'seasonal']):
        tags.append(all_tags.get('Seasonal'))
    
    # Youth focused (if mentions youth, family, etc)
    if any(word in title_lower for word in ['youth', 'student', 'family', 'kids']):
        tags.append(all_tags.get('Youth'))
    
    # Remove None values and ensure we have at least 1-3 tags
    tags = [tag for tag in tags if tag is not None]
    
    # If no specific tags matched, add some based on category
    if not tags:
        if 'workshop' in category_lower:
            tags.append(all_tags.get('Educational'))
        elif 'tree' in category_lower:
            tags.extend([all_tags.get('Outdoor'), all_tags.get('Volunteer')])
        elif 'beach' in category_lower:
            tags.extend([all_tags.get('Outdoor'), all_tags.get('Community')])
        elif 'recycling' in category_lower:
            tags.extend([all_tags.get('Community'), all_tags.get('Volunteer')])
        elif 'garden' in category_lower:
            tags.extend([all_tags.get('Outdoor'), all_tags.get('Community')])
        elif 'wildlife' in category_lower:
            tags.extend([all_tags.get('Outdoor'), all_tags.get('Research')])
    
    # Ensure we have 1-3 tags max and remove duplicates
    tags = list(set([tag for tag in tags if tag is not None]))
    if len(tags) > 3:
        tags = random.sample(tags, 3)
    elif len(tags) == 0:
        # Default fallback
        tags = [all_tags.get('Community')]
    
    return tags

def create_events_for_each_user():
    """Create EXACTLY 4 events per user with EventTags"""
    
    # Get categories, locations, and tags
    categories = list(EventCategory.objects.all())
    locations = list(Location.objects.all())
    available_tags = list(EventTag.objects.all())
    
    if not categories or not locations:
        print("❌ Error: Make sure to load fixtures first!")
        print("Run: python manage.py loaddata events/fixtures/initial_categories.json")
        print("Run: python manage.py loaddata search/fixtures/initial_locations.json")
        print("Run: python manage.py loaddata search/fixtures/initial_tags.json")
        return []
    
    if not available_tags:
        print("⚠️  Warning: No EventTags found! Events will be created without tags.")
    else:
        print(f"🏷️  Found {len(available_tags)} EventTags: {[tag.name for tag in available_tags]}")
    
    # Get users by username to ensure correct assignment
    vansh = User.objects.get(username='vansh_patel')
    raj = User.objects.get(username='raj_patel') 
    kirtan = User.objects.get(username='kirtan_prajapati')
    dhruv = User.objects.get(username='dhruv_patel')
    
    print(f"👥 Found users: {vansh.first_name}, {raj.first_name}, {kirtan.first_name}, {dhruv.first_name}")
    
    created_events = []
    
    # VANSH'S 4 EVENTS
    print(f"\n🎯 Creating 4 events for {vansh.first_name} {vansh.last_name}:")
    vansh_events = [
        {
            'title': 'Environmental Data Collection Workshop',
            'description': 'Learn how to collect and analyze environmental data using modern technology. We will use sensors to measure air quality, water quality, and noise pollution.',
            'category': 'Workshop'
        },
        {
            'title': 'Smart City Sustainability Analytics', 
            'description': 'Explore how data analytics can help create smarter, more sustainable cities. We will discuss IoT sensors, data visualization, and predictive modeling.',
            'category': 'Workshop'
        },
        {
            'title': 'Tree Planting with GPS Mapping',
            'description': 'Plant native trees while learning to use GPS technology to map and track our reforestation efforts.',
            'category': 'Tree Planting'
        },
        {
            'title': 'Climate Data Visualization Challenge',
            'description': 'Join our hackathon-style event where we create data visualizations showing local climate trends.',
            'category': 'Workshop'
        }
    ]
    
    for i, event_data in enumerate(vansh_events):
        event = create_single_event(vansh, event_data, i, categories, locations)
        # Add tags to event
        if available_tags:
            tags_for_event = get_tags_for_event(event.title, event.category.name)
            event.tags.set(tags_for_event)
            tag_names = [tag.name for tag in tags_for_event]
            print(f"  ✅ {event.title} ({event.status}) - Tags: {tag_names}")
        else:
            print(f"  ✅ {event.title} ({event.status})")
        created_events.append(event)
    
    # RAJ'S 4 EVENTS  
    print(f"\n🎯 Creating 4 events for {raj.first_name} {raj.last_name}:")
    raj_events = [
        {
            'title': 'Digital Environmental Activism Workshop',
            'description': 'Learn how to use digital tools safely and effectively for environmental advocacy. We will cover online organizing and social media campaigns.',
            'category': 'Workshop'
        },
        {
            'title': 'Community Beach Cleanup & Safety',
            'description': 'Join our well-organized beach cleanup with focus on volunteer safety and efficient waste collection systems.',
            'category': 'Beach Cleanup'
        },
        {
            'title': 'Secure Community Organizing for Environment',
            'description': 'Learn best practices for organizing environmental groups while maintaining member privacy and safety.',
            'category': 'Workshop'
        },
        {
            'title': 'Electronic Waste Secure Destruction Drive',
            'description': 'Bring your old electronics for secure data destruction and proper recycling.',
            'category': 'Recycling Drive'
        }
    ]
    
    for i, event_data in enumerate(raj_events):
        event = create_single_event(raj, event_data, i, categories, locations)
        # Add tags to event
        if available_tags:
            tags_for_event = get_tags_for_event(event.title, event.category.name)
            event.tags.set(tags_for_event)
            tag_names = [tag.name for tag in tags_for_event]
            print(f"  ✅ {event.title} ({event.status}) - Tags: {tag_names}")
        else:
            print(f"  ✅ {event.title} ({event.status})")
        created_events.append(event)
    
    # KIRTAN'S 4 EVENTS
    print(f"\n🎯 Creating 4 events for {kirtan.first_name} {kirtan.last_name}:")
    kirtan_events = [
        {
            'title': 'Large Scale Community Garden Project',
            'description': 'Help establish our biggest community garden yet! This multi-day project will involve site preparation and plot planning.',
            'category': 'Community Garden'
        },
        {
            'title': 'Environmental Festival Planning Committee',
            'description': 'Join the organizing committee for our upcoming Environmental Action Festival. Learn event planning and vendor coordination.',
            'category': 'Workshop'
        },
        {
            'title': 'Multi-Location Tree Planting Coordination',
            'description': 'Help coordinate simultaneous tree planting events across multiple locations.',
            'category': 'Tree Planting'
        },
        {
            'title': 'Corporate Sustainability Workshop Series',
            'description': 'Organize and facilitate workshops for local businesses on implementing sustainable practices.',
            'category': 'Workshop'
        }
    ]
    
    for i, event_data in enumerate(kirtan_events):
        event = create_single_event(kirtan, event_data, i, categories, locations)
        # Add tags to event
        if available_tags:
            tags_for_event = get_tags_for_event(event.title, event.category.name)
            event.tags.set(tags_for_event)
            tag_names = [tag.name for tag in tags_for_event]
            print(f"  ✅ {event.title} ({event.status}) - Tags: {tag_names}")
        else:
            print(f"  ✅ {event.title} ({event.status})")
        created_events.append(event)
    
    # DHRUV'S 4 EVENTS
    print(f"\n🎯 Creating 4 events for {dhruv.first_name} {dhruv.last_name}:")
    dhruv_events = [
        {
            'title': 'Environmental Photography Workshop',
            'description': 'Learn to capture compelling images that tell environmental stories. We will cover composition, lighting, and ethical wildlife photography.',
            'category': 'Workshop'
        },
        {
            'title': 'Wildlife Conservation Media Project',
            'description': 'Create a multimedia project documenting local wildlife and their habitats using cameras and video.',
            'category': 'Wildlife Conservation'
        },
        {
            'title': 'Before/After Environmental Documentation',
            'description': 'Participate in environmental restoration while creating professional documentation of our impact.',
            'category': 'Tree Planting'
        },
        {
            'title': 'Community Environmental Storytelling',
            'description': 'Help create a digital archive of community environmental stories through interviews, photos, and videos.',
            'category': 'Workshop'
        }
    ]
    
    for i, event_data in enumerate(dhruv_events):
        event = create_single_event(dhruv, event_data, i, categories, locations)
        # Add tags to event
        if available_tags:
            tags_for_event = get_tags_for_event(event.title, event.category.name)
            event.tags.set(tags_for_event)
            tag_names = [tag.name for tag in tags_for_event]
            print(f"  ✅ {event.title} ({event.status}) - Tags: {tag_names}")
        else:
            print(f"  ✅ {event.title} ({event.status})")
        created_events.append(event)
    
    print(f"\n✅ Created {len(created_events)} events total (4 per person)")
    return created_events

def create_single_event(user, event_data, index, categories, locations):
    """Create a single event with proper timing"""
    
    # Timing pattern: completed, ongoing, upcoming, upcoming
    if index == 0:
        event_date = timezone.now() - timedelta(days=random.randint(7, 30))
        status = 'completed'
    elif index == 1:
        event_date = timezone.now() - timedelta(days=random.randint(1, 5))
        status = 'ongoing'  
    else:
        event_date = timezone.now() + timedelta(days=random.randint(5, 45))
        status = 'upcoming'
    
    # Get random location and matching category
    location = random.choice(locations)
    category = EventCategory.objects.filter(name=event_data['category']).first()
    if not category:
        category = random.choice(categories)
    
    # Create the event
    event = Event.objects.create(
        title=event_data['title'],
        description=event_data['description'],
        date_time=event_date,
        location=location,
        address_details=f"{random.choice(['Community Center', 'Park Pavilion', 'Library Meeting Room'])}, {location.name}",
        organizer=user,
        category=category,
        max_participants=random.randint(20, 80),
        status=status,
        created_at=timezone.now() - timedelta(days=random.randint(5, 60))
    )
    
    return event

def create_event_participations(events):
    """Have users join each other's events"""
    users = User.objects.filter(is_superuser=False)
    users_list = list(users)
    
    participations_created = 0
    
    for event in events:
        # Random number of participants (but don't exceed max and exclude organizer)
        available_users = [u for u in users_list if u != event.organizer]
        num_participants = random.randint(2, min(len(available_users), 3))  # 2-3 participants per event
        
        participants = random.sample(available_users, num_participants)
        
        for user in participants:
            participation, created = EventParticipation.objects.get_or_create(
                user=user,
                event=event,
                defaults={
                    'joined_date': event.created_at + timedelta(days=random.randint(0, 7)),
                    'attended': event.status == 'completed' and random.choice([True, True, True, False]),  # 75% attendance
                    'feedback': random.choice([
                        'Great event! Really enjoyed contributing to our community.',
                        'Well organized and informative. Looking forward to the next one!',
                        'Amazing to see so many people caring about our environment.',
                        'Learned a lot and made new friends. Thank you for organizing!',
                        ''  # Some don't leave feedback
                    ]) if event.status == 'completed' else ''
                }
            )
            
            if created:
                participations_created += 1
    
    print(f"Created {participations_created} event participations")

def create_user_history():
    """Create user visit history"""
    users = User.objects.filter(is_superuser=False)
    pages = [
        'Homepage', 'Event List', 'Dashboard', 'Create Event', 'Upload Photo',
        'Analytics', 'Profile', 'About Us', 'Contact', 'Search Results'
    ]
    
    history_created = 0
    for user in users:
        # Each user has 10-25 page visits
        num_visits = random.randint(10, 25)
        
        for _ in range(num_visits):
            visit_date = timezone.now() - timedelta(days=random.randint(0, 45))
            UserHistory.objects.create(
                user=user,
                page_visited=random.choice(pages),
                visit_date=visit_date,
                ip_address=f"192.168.1.{random.randint(1, 254)}"
            )
            history_created += 1
    
    print(f"Created {history_created} user history entries")

def create_search_history():
    """Create search history for users including tag-based searches"""
    users = User.objects.filter(is_superuser=False)
    search_terms = [
        'tree planting', 'beach cleanup', 'recycling', 'workshop', 'oshawa events',
        'community garden', 'wildlife conservation', 'sustainable living', 'composting',
        'solar energy', 'climate action', 'native plants', 'environmental', 'green',
        'outdoor activities', 'volunteer opportunities', 'educational workshops',
        'corporate events', 'youth programs', 'research projects'  # Added tag-related searches
    ]
    
    history_created = 0
    for user in users:
        # Each user has 5-12 searches
        num_searches = random.randint(5, 12)
        
        for _ in range(num_searches):
            search_date = timezone.now() - timedelta(days=random.randint(0, 40))
            SearchHistory.objects.create(
                user=user,
                search_query=random.choice(search_terms),
                search_date=search_date,
                results_count=random.randint(1, 10)
            )
            history_created += 1
    
    print(f"Created {history_created} search history entries")

def main():
    """Main function to populate the database"""
    print("🌱 Starting EcoConnect Database Population - WITH EVENTTAGS")
    print("=" * 60)
    
    # Clear old data first
    clear_existing_data()
    
    # Create users
    print("👥 Creating team members...")
    users = create_users()
    
    # Create events - EXACTLY 4 per person WITH TAGS
    print("📅 Creating environmental events with tags - 4 per person...")
    events = create_events_for_each_user()
    
    # Create participations
    print("🤝 Creating event participations...")
    create_event_participations(events)
    
    # Create user history
    print("📊 Creating user history...")
    create_user_history()
    
    # Create search history
    print("🔍 Creating search history...")
    create_search_history()
    
    print("=" * 60)
    print("✅ Database population completed!")
    print(f"Created: {len(users)} users, {len(events)} events with EventTags")
    print("📸 Photos can be added later through the web interface")
    print("\nLogin credentials for testing:")
    print("- Username: vansh_patel, Password: password123")
    print("- Username: raj_patel, Password: password123")
    print("- Username: kirtan_prajapati, Password: password123") 
    print("- Username: dhruv_patel, Password: password123")
    
    # Final verification with tags
    print(f"\n📋 Final Event Breakdown with Tags:")
    for user in User.objects.filter(is_superuser=False).order_by('username'):
        user_events = Event.objects.filter(organizer=user).prefetch_related('tags')
        print(f"  {user.first_name} {user.last_name}: {user_events.count()} events")
        for event in user_events:
            tag_names = [tag.name for tag in event.tags.all()]
            print(f"    - {event.title} ({event.status}) - Tags: {tag_names}")

if __name__ == '__main__':
    main()