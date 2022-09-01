from distutils.command.upload import upload
import email
from email.policy import default
from logging import RootLogger
from sre_parse import State
from tabnanny import verbose
from turtle import title
from wsgiref.util import request_uri
from xml.sax import default_parser_list
from django.db import models

class UserRole(models.Model):
    Role = models.CharField(max_length=10)
    
    class Meta:
        db_table = 'userrole'
        
    def __str__(self) -> str:
        return self.Role
        
class Master(models.Model):
    UserRole = models.ForeignKey(UserRole,on_delete=models.CASCADE)
    Email = models.EmailField(unique=True)
    Password = models.CharField(max_length=12)
    IsActive = models.BooleanField(default=False)
    RegData = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'master'

    def __str__(self) -> str:
        return self.Email 
        
gender_choices = (
    ('m','male'),
    ('f','female'),
)
        
class Profile(models.Model):
    Master = models.ForeignKey(Master,on_delete=models.CASCADE)
    ProfileImage = models.FileField(upload_to='profiles/',default='avatar.png')
    FullName = models.CharField(max_length=25,default='',blank=True)
    Gender = models.CharField(max_length=5,choices=gender_choices)
    BirthDate = models.DateField(auto_created=True,default='1991-01-01')
    Mobile = models.CharField(max_length=10,default='',blank=True)
    Country = models.CharField(max_length=25,default='',blank=True)
    State = models.CharField(max_length=25,default='',blank=True) 
    City = models.CharField(max_length=25,default='',blank=True) 
    Pincode = models.CharField(max_length=6,default='',blank=True)
    Addresss = models.TextField(max_length=150,default='',blank=True)
    
    class Meta:
        db_table = 'Profile'
        
class Category(models.Model):
    Name = models.CharField(max_length=20)
    
    class Meta:
        db_table = 'categories'
        verbose_name_plural = 'categories'
    
class Book(models.Model):
    Author = models.ForeignKey(Profile,on_delete=models.CASCADE)
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    Title = models.CharField(max_length=100)
    ISBN = models.CharField(max_length=18)
    content = models.TextField(max_length=5000)
    PublishDate = models.DateField(auto_now_add=True)
    UpdateDate = models.DateField(auto_now_add=True)
    
    class Meta:
        db_table = 'book'
        
class book_Content(models.Model):
    Book_Title = models.CharField(max_length=100)
    Page_No = models.IntegerField(max_length=1000)
    Content = models.CharField(max_length=1000)
    
    class Meta:
        db_table = 'book_content'
    

