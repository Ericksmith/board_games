# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.password_validation import validate_password
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

# Create your models here.
class UserManager(models.Manager):
    def validator(self, postData):
        errors = {
            'error': []
        }
        if len(postData['first_name']) < 2 or len(postData['last_name']) < 2:
            errors['error'].append('Your first and last name must be longer than 1 character')
        if postData['password'] != postData['confirm_password']:
            errors['error'].append('Your password does not match the confim password')
        if EMAIL_REGEX.match(postData['email']) is None:
            errors['error'].append('Invalid email format')
        if User.objects.filter(email=postData['email']):
            errors['error'].append('Email already registered')
        try:
            validate_password(postData['password'])
        except Exception as e:
            errors['password'] = e
        return errors

    def password_hasher(self, pw):
        hashed_password = make_password(pw)
        return hashed_password

    def password_checker(self, pw, encoded_pw):
        return check_password(pw, encoded_pw)

#DB models
class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(max_length=75)
    password = models.CharField(max_length=255)
    isAdmin = models.BooleanField(default=False)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    objects = UserManager()