"""
Management command to send morning email reminders for tasks due today.
Run daily via cron (e.g., 7:00 AM): python manage.py send_morning_reminders
"""

from datetime import date

from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.models import User

from tasks.models import Task


class Command(BaseCommand):
    help = "Send email reminders to users about tasks due today"

    def add_arguments(self, parser):
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Print what would be sent without sending emails",
        )

    def handle(self, *args, **options):
        dry_run = options["dry_run"]
        today = date.today()

        users_with_tasks = (
            User.objects.filter(tasks__due_date=today, tasks__completed=False)
            .distinct()
        )

        for user in users_with_tasks:
            tasks = Task.objects.filter(
                user=user, due_date=today, completed=False
            ).order_by("course", "title")

            subject = f"CMU Todo: {tasks.count()} task(s) due today"
            lines = [
                f"Good morning, {user.username}!",
                "",
                "Here are your tasks due today:",
                "",
            ]
            for t in tasks:
                course = f" [{t.course}]" if t.course else ""
                lines.append(f"  • {t.title}{course}")
            lines.extend(["", "Log in to CMU Todo to manage your tasks."])

            body = "\n".join(lines)
            email = user.email or f"{user.username}@localhost"

            if dry_run:
                self.stdout.write(f"Would send to {email}:\n{body}\n---")
            else:
                send_mail(
                    subject,
                    body,
                    settings.DEFAULT_FROM_EMAIL or "noreply@cmutodo.local",
                    [email],
                    fail_silently=True,
                )
                self.stdout.write(self.style.SUCCESS(f"Sent reminder to {email}"))

        if not users_with_tasks:
            self.stdout.write("No users with tasks due today.")
