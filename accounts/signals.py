from django.db.models.signals import post_save
from django.dispatch import receiver
from accounts.models import User,Profile
from clients.models import Client



# 🔹 Log user creation (optional)
@receiver(post_save, sender=User)
def create_user_log(sender, instance, created, **kwargs):
    if created:
        print(f"New user created: {instance.email}")


# 🔹 Auto create Client profile
from django.db.models.signals import post_save
from django.dispatch import receiver
from accounts.models import User
from clients.models import Client


@receiver(post_save, sender=User)
def create_client_profile(sender, instance, created, **kwargs):
    if created and instance.role == 'client':
        Client.objects.create(
            user=instance,
            name=instance.first_name or instance.email,
            contact_email=instance.email,   # ✅ correct field
            website="",                     # optional default
            industry=""                     # optional default
        )

# accounts/signals.py

# accounts/signals.py

from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User, Profile

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    if hasattr(instance, 'profile'):
        instance.profile.save()