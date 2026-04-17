"""
Usage:
    python manage.py startall
    python manage.py startall --group ocr
    python manage.py startall --group webapp
"""

import time
from django.core.management.base import BaseCommand
from dashboard.process_registry import PROCESSES
from dashboard import process_manager as pm


class Command(BaseCommand):
    help = "Start all registered processes (or a specific group)"

    def add_arguments(self, parser):
        parser.add_argument(
            "--group",
            type=str,
            default=None,
            help="Only start processes in this group: 'webapp' or 'ocr'",
        )

    def handle(self, *args, **options):
        group_filter = options.get("group")
        targets = [
            p for p in PROCESSES
            if group_filter is None or p["group"] == group_filter
        ]

        if not targets:
            self.stdout.write(self.style.WARNING("No processes matched."))
            return

        for p in targets:
            self.stdout.write(f"Starting {p['label']}... ", ending="")
            result = pm.start_process(p["id"])
            if result["ok"]:
                self.stdout.write(self.style.SUCCESS(f"OK  (pid={result['pid']})"))
            else:
                self.stdout.write(self.style.ERROR(f"FAILED — {result['error']}"))
            time.sleep(0.3)   # small delay between launches

        self.stdout.write(self.style.SUCCESS("\nDone."))
