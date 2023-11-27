from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
import os
from PIL import Image
from django.conf import settings
from django.conf import settings



# create meep model
class Meep(models.Model):
    user = models.ForeignKey(User, related_name='meeps',on_delete=models.DO_NOTHING)
    body = models.CharField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name='meep_like', blank=True)
    
    # Keep track or count of like

    def number_of_likes(self):
        return self.likes.count()


    def __str__(self):
        return (
            f'{self.user}'
            f'({self.created_at:%d-%m-%Y %H:%M}):'
            f'{self.body}...'
        )


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    follows = models.ManyToManyField(
        "self",
        related_name="followed_by",
        symmetrical=False,
        blank=True
    )
    date_modified = models.DateTimeField(User, auto_now=True)
    profile_image = models.ImageField(null=True, blank=True, upload_to="images/profile/")
    profile_bio = models.CharField(null=True, blank=True, max_length=500)
    homepage_link = models.CharField(null=True, blank=True, max_length=200)
    facebook_link = models.CharField(null=True, blank=True, max_length=200)
    instagram_link = models.CharField(null=True, blank=True, max_length=200)
    linkedin_link = models.CharField(null=True, blank=True, max_length=200)


    @staticmethod
    def resize_image(img, new_width=200):
        img_full_path = os.path.join(settings.MEDIA_ROOT, img.name)
        img_pil = Image.open(img_full_path)
        orginal_width, orginal_height = img_pil.size

        if orginal_width <= new_width:
            print('retornando, largura original menor que nova largura')
            img_pil.close()
            return

        new_height = round((new_width * orginal_height) / orginal_width)

        new_img = img_pil.resize((new_width, new_height), Image.LANCZOS)
        new_img.save(
            img_full_path,
            optimize=True,
            quality=70
        )
        print('Imagem redimensionada!')

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.profile_image:
            self.resize_image(self.profile_image)

    def __str__(self):
        return self.user.username
    

# Create Profile when new user signs up

#@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        user_profile = Profile(user=instance)
        user_profile.save()
        # Have the user follow themselves
        user_profile.follows.set([instance.profile.id])
        user_profile.save()





post_save.connect(create_profile, sender=User)