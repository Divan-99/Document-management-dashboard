"""
Usage:
    python manage.py stopall
    python manage.py stopall --group ocr
"""

from django.core.management.base import BaseCommand
from dashboard.process_registry import PROCESSES
from dashboard import process_manager as pm


class Command(BaseCommand):
    help = "Stop all running processes (or a specific group)"

    def add_arguments(self, parser):
        parser.add_argument(
            "--group",
            type=str,
            default=None,
            help="Only stop processes in this group: 'webapp' or 'ocr'",
        )

    def handle(self, *args, **options):
        group_filter = options.get("group")
        targets = [
            p for p in PROCESSES
            if group_filter is None or p["group"] == group_filter
        ]

        for p in targets:
            self.stdout.write(f"Stopping {p['label']}... ", ending="")
            result = pm.stop_process(p["id"])
            if result["ok"]:
                self.stdout.write(self.style.SUCCESS("OK"))
            else:
                self.stdout.write(self.style.WARNING(result["error"]))

        self.stdout.write(self.style.SUCCESS("\nDone."))
