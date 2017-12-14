# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
import bcrypt

# Create your models here.
class UserManager(models.Manager):
    def current_user(self, request):
        return self.get(id=request.session['user_id'])
    
    def validate_registration(self, form_data):
        print '*****youre in the validate_registration method*****'

        #form_data here is request.POST['whatever form info you need']
        errors = []
        if len(form_data['name']) == 0:
            errors.append('Name can not be blank')
        if len(form_data['alias']) == 0:
            errors.append('Alias can not be blank')
        if len(form_data['email']) == 0:
            errors.append('Email can not be blank')
        # # make sure theyre not a user in the DB already
        # user = User.objects.filter(email=form_data['email']).first()
        # if user:
        #     errors.append('Email already in use')
        if len(form_data['password']) < 8:
            errors.append('Password can not be blank, or less than 8 characters')
        if form_data['password'] != form_data['password_confirmation']:
                errors.append('Passwords do not match')
        return errors

    def create_user(self, form_data):
        print '*****youre in the create_user method*****'

        # form_data is the request.POST argument passed in from the views
        user = User.objects.create(
        #the create function returns the whole user obj.
                name = form_data['name'],
                alias =  form_data['alias'],
                email = form_data['email'],
                password = bcrypt.hashpw(form_data['password'].encode(),bcrypt.gensalt(5))
            )
            # needs form_data passw and the encode(), then we use it to generate a salt
        return user
        #this gets the data out of the function and back into the views file

    def validate_login(self, form_data):

        errors = []
        if len(form_data['email']) == 0:
            errors.append('Email can not be blank')
        if len(form_data['password']) < 4:
            errors.append('Password can not be blank')
            print '*****youre in the validate_login method*****'
        user = User.objects.filter(email = form_data['email']).first()
        if user:
            user_password = form_data['password'].encode()
            db_password = user.password.encode()
            if bcrypt.checkpw(user_password, db_password):
                return {'user':user}
        errors.append('Invalid Credentials')
        # gets passed back as an object because we use it as a key in the views login method
        return {'errors':errors}

class User(models.Model):
    name = models.CharField(max_length=255)
    alias = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    friends = models.ManyToManyField('self', related_name='friender')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager() #now we can say User.objects.validate_registration/any function in the manager
