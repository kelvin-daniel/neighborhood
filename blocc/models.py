from django.db import models
from django.contrib.auth.models import User
from tinymce.models import HTMLField
from django.db.models import Q
import datetime as dt
from phonenumber_field.modelfields import PhoneNumberField
from cloudinary.models import CloudinaryField

Priority=(
    ('Informational','Informational'),
    ('High Priority','High Priority'),
)

# Create your models here.
class Block(models.Model):
    block= models.CharField(max_length=100)

    def __str__(self):
        return self.block

    def save_block(self):
        self.save()

    @classmethod
    def delete_block(cls,block):
        cls.objects.filter(block=block).delete()


class Notification(models.Model):
    title = models.CharField(max_length=100)
    notification = HTMLField()
    author = models.ForeignKey(User,on_delete=models.CASCADE)
    block = models.ForeignKey(Block,on_delete=models.CASCADE)
    post_date = models.DateTimeField(auto_now_add=True)
    priority = models.CharField(max_length=15,choices=Priority,default="Informational")

    def __str__(self):
        return self.title


class Business(models.Model):
    logo = CloudinaryField('image', null=True)
    description = HTMLField()
    block = models.ForeignKey(Block,on_delete=models.CASCADE)
    owner = models.ForeignKey(User,on_delete=models.CASCADE)
    name =models.CharField(max_length=100)
    email = models.EmailField()
    address =models.CharField(max_length=100)
    contact = PhoneNumberField()

    def __str__(self):
        return self.name

    @classmethod
    def search_business(cls,search_term):
        businesses = cls.objects.filter(Q(name__icontains=search_term) | Q(block__block=search_term) | Q(description__icontains=search_term))
        return businesses

class Health(models.Model):
    logo = CloudinaryField('image', null=True)
    block = models.ForeignKey(Block,on_delete=models.CASCADE)
    name =models.CharField(max_length=100)
    email = models.EmailField()
    contact = PhoneNumberField()
    address =models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Authorities(models.Model):
    block = models.ForeignKey(Block,on_delete=models.CASCADE)
    name =models.CharField(max_length=100)
    email = models.EmailField()
    contact = PhoneNumberField()
    address =models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Profile(models.Model):
    avatar = CloudinaryField('image', null=True)
    description = HTMLField()
    block = models.ForeignKey(Block,on_delete=models.CASCADE)
    username = models.ForeignKey(User,on_delete=models.CASCADE)
    name =models.CharField(max_length=100)
    email = models.EmailField()

    def __str__(self):
        return self.name

class Post(models.Model):
    title = models.CharField(max_length=150)
    image = CloudinaryField('image', null=True)
    post = HTMLField()
    username = models.ForeignKey(User,on_delete=models.CASCADE)
    block= models.ForeignKey(Block,on_delete=models.CASCADE)
    post_date = models.DateTimeField(auto_now_add=True)
    avatar = CloudinaryField('image', null=True)

    def __str__(self):
        return self.title


class Comment(models.Model):
    comment = models.CharField(max_length=300)
    username = models.ForeignKey(User,on_delete=models.CASCADE)
    post = models.ForeignKey(Post,on_delete=models.CASCADE)