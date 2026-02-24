import os
import django
import random
from faker import Faker

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'event_management.settings')
django.setup()

from events.models import Category, Event, Participant

def populate_db():
    fake = Faker()

    categories_names = ['Music', 'Corporate', 'Sports', 'Art', 'Tech']
    categories = []
    for name in categories_names:
        category, created = Category.objects.get_or_create(
            name=name,
            description=fake.sentence()
        )
        categories.append(category)
    print(f"Created {len(categories)} categories.")

    participants = [Participant.objects.create(
        name=fake.name(),
        email=fake.unique.email()
    ) for _ in range(15)]
    print(f"Created {len(participants)} participants.")

    events = []
    for _ in range(10):
        event = Event.objects.create(
            category=random.choice(categories),
            name=fake.catch_phrase(),
            description=fake.paragraph(),
            date=fake.date_this_year(),
            time=fake.time(),
            location=fake.address()[:70]
        )
        event.participants.set(random.sample(participants, random.randint(3, 8)))
        events.append(event)
    
    print(f"Created {len(events)} events with participants.")
    print("Database populated successfully!")

if __name__ == '__main__':
    populate_db()