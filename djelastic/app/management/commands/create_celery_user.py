from django.core.management.base import BaseCommand
from django.contrib.auth.models import User, Group


class Command(BaseCommand):
    help = 'Create a new user and add to the celery_user group'

    def handle(self, *args, **options):
        username = 'celery_user'  # todo will be changed
        password = 'password123'  # todo will be changed
        group_name = 'celery_user'  # todo will be changed


        try:
            # Check if the group already exists
            group = Group.objects.get(name=group_name)
        except Group.DoesNotExist:
            # Create the group if it doesn't exist
            group = Group.objects.create(name=group_name)
            self.stdout.write(self.style.SUCCESS(f"Group {group_name} created successfully."))

        try:
            # Check if the user already exists
            user = User.objects.get(username=username)
            self.stdout.write(self.style.SUCCESS(f"User {username} already exists."))
            return
        except User.DoesNotExist:
            pass

        # Create a new user
        try:
            # Create the user object
            user = User.objects.create_user(username=username, password=password)
            user.is_superuser = True
            user.is_staff = True
            user.save()

            # Add the user to the group
            user.groups.add(group)

            self.stdout.write(self.style.SUCCESS(f"User {username} created successfully and added to {group_name} group."))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error creating user {username}: {e}"))
