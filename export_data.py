import os
import django
import json

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "seo.settings")  # Change if needed
django.setup()

from django.apps import apps
from django.core.serializers import serialize

all_objects = []

# Exclude Django internal apps
exclude_apps = {
    "contenttypes",
    "auth",
    "sessions",
    "admin",
}

for model in apps.get_models():
    if model._meta.app_label in exclude_apps:
        continue

    print(f"Exporting {model.__name__}...")
    queryset = model.objects.all()

    data = json.loads(serialize("json", queryset))
    all_objects.extend(data)

with open("data.json", "w", encoding="utf-8") as f:
    json.dump(all_objects, f, ensure_ascii=False, indent=2)

print("✅ Export completed successfully -> data.json")