from django.core.management.base import BaseCommand
from accounts.models import User
from tasks.models import Task
from datetime import date, timedelta


class Command(BaseCommand):
    help = 'Seed sample users and tasks for demo'

    def handle(self, *args, **options):
        # Create users
        alice, _ = User.objects.get_or_create(
            username='alice',
            defaults={'email': 'alice@example.com'}
        )
        alice.set_password('Alice@1234')
        alice.save()

        bob, _ = User.objects.get_or_create(
            username='bob',
            defaults={'email': 'bob@example.com'}
        )
        bob.set_password('Bob@1234')
        bob.save()

        self.stdout.write(self.style.SUCCESS('Users created: alice, bob'))

        # Personal tasks for alice
        Task.objects.get_or_create(
            title='Set up project repository',
            created_by=alice,
            defaults={
                'description': 'Initialize git repo, create .gitignore, push to GitHub',
                'status': 'done', 'priority': 'high',
                'due_date': date.today() - timedelta(days=3)
            }
        )
        Task.objects.get_or_create(
            title='Write unit tests',
            created_by=alice,
            defaults={
                'description': 'Cover all model methods and view logic with tests',
                'status': 'in_progress', 'priority': 'medium',
                'due_date': date.today() + timedelta(days=5)
            }
        )
        Task.objects.get_or_create(
            title='Deploy to production',
            created_by=alice,
            defaults={
                'description': 'Set up CI/CD pipeline and deploy app',
                'status': 'todo', 'priority': 'high',
                'due_date': date.today() + timedelta(days=10)
            }
        )

        # Assigned task: alice assigns to bob
        Task.objects.get_or_create(
            title='Review pull request #42',
            created_by=alice,
            assigned_to=bob,
            defaults={
                'description': 'Review the authentication refactoring PR',
                'status': 'todo', 'priority': 'high',
                'due_date': date.today() + timedelta(days=2)
            }
        )
        Task.objects.get_or_create(
            title='Fix login page bug',
            created_by=alice,
            assigned_to=bob,
            defaults={
                'description': 'The password reset flow fails on mobile browsers',
                'status': 'in_progress', 'priority': 'medium',
                'due_date': date.today() + timedelta(days=4)
            }
        )

        # Personal tasks for bob
        Task.objects.get_or_create(
            title='Update documentation',
            created_by=bob,
            defaults={
                'description': 'Update API docs with new endpoints',
                'status': 'todo', 'priority': 'low',
                'due_date': date.today() + timedelta(days=7)
            }
        )

        self.stdout.write(self.style.SUCCESS('Sample tasks created!'))
        self.stdout.write(self.style.SUCCESS('\nSample credentials:'))
        self.stdout.write('  alice / Alice@1234')
        self.stdout.write('  bob   / Bob@1234')
