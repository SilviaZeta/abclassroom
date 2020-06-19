from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	full_name = models.CharField(max_length=100, blank=True)
	bio = models.TextField(max_length=500, blank=True)
	picture = models.ImageField(null=True, blank=True, default='default-profile-picture.png')

	def __str__(self):
		return self.user.username



@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()


'''
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
	#links user creationg to profile creation
	if created:
		Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
	#links user saving to profile creation
	instance.profile.save()
'''