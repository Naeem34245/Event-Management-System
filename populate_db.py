import os
import django
import random
from faker import Faker

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'event_management.settings')
django.setup()

from events.models import Employee, Project, Task, TaskDetail

def populate_db():
    fake = Faker()

    projects = [Project.objects.create(
        name=fake.company() + " Event",
        description=fake.paragraph(),
        start_date=fake.date_this_year()
    ) for _ in range(5)]
    print(f"Created {len(projects)} projects.")

    employees = [Employee.objects.create(
        name=fake.name(),
        email=fake.unique.email()
    ) for _ in range(10)]
    print(f"Created {len(employees)} employees.")

    tasks = []
    for _ in range(20):
        task = Task.objects.create(
            project=random.choice(projects),
            title=fake.catch_phrase(),
            description=fake.paragraph(),
            due_date=fake.date_this_year(),
            status=random.choice(['PENDING', 'IN_PROGRESS', 'COMPLETED']),
            is_completed=random.choice([True, False])
        )
        task.assigned_to.set(random.sample(employees, random.randint(1, 3)))
        tasks.append(task)
    print(f"Created {len(tasks)} tasks.")

    for task in tasks:
        TaskDetail.objects.create(
            task=task,
            priority=random.choice(['H', 'M', 'L']),
            notes=fake.sentence()
        )
    print("Populated TaskDetails for all tasks.")
    print("Database populated successfully!")

if __name__ == '__main__':
    populate_db()