# Inside your app's models.py file
from __future__ import unicode_literals
from django.db import models

import re	
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 
# Our custom manager!
# No methods in our new manager should ever receive the whole request object as an argument! 
# (just parts, like request.POST)
class UserManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        if len(postData['first_name']) ==0:
            errors["first_name"] = "First name should be at least 2 characters"
        if len(postData['last_name']) ==0:
            errors["last_name"] = "Last name should be at least 2 characters"
        if len(postData['email']) ==0:
            errors["email"] = "Please enter email."
        if not EMAIL_REGEX.match(postData['email']):    # test whether a field matches the pattern
            errors["email"] = "Please enter valid email"
        if postData['password'] != postData['password_confirm']:
            errors['password']= "Passwords do not match."
        if len(postData['password']) ==0:
            errors["password_blank"] = "Please enter password."
        return errors
        
    def login_validator(self, postData):
        errors = {}
        if len(postData['login_email']) ==0:
            errors["email"] = "Please enter email."
        if not EMAIL_REGEX.match(postData['login_email']):    # test whether a field matches the pattern
            errors["email"] = "Please enter valid email"
        if len(postData['login_password']) ==0:
            errors["password_blank"] = "Please enter password."
        return errors
    
class User(models.Model):
    first_name = models.CharField(max_length=45)
    last_name = models.CharField(max_length=45)
    email = models.CharField(max_length=45)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects=UserManager()

class BookManager(models.Manager):
    def book_validator(self, postData):
        errors = {}
        if len(postData['address']) <1:
            errors["address"] = "Address needs to be at least 3 characters."
        if len(postData['phone']) <10:
            errors["phone"] = "Phone number needs to be at least 10 characters."
        if len(postData['start']) <1:
            errors["start"] = "Start date needs to be in this format MM/DD/YY."
        if len(postData['end']) <1:
            errors["end"] = "Please enter a valid date."
        return errors

class Book(models.Model):
    address = models.CharField(max_length=255)
    phone = models.IntegerField()
    start = models.DateTimeField(max_length=45)
    end = models.DateTimeField(max_length=45)
    notes = models.CharField(max_length=255)
    creator = models.ForeignKey(User, related_name= "book")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects=BookManager()
