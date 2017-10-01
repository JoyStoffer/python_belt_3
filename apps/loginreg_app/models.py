from __future__ import unicode_literals
from django.db import models
import bcrypt

# Create your models here.
class UserManager(models.Manager):
    def current_user(self, request):
        return self.get(id=request.session['user_id'])
    
    def validate_registration(self, form_data):
        errors = []

        #Name
        if len(form_data['name']) == 0:
            errors.append("Name is required.")
        #Alias
        if len(form_data['alias']) == 0:
            errors.append("Alias is required.")
        #Email
        if len(form_data['email']) == 0:
            errors.append("Email is required.")
        #Password
        if len(form_data['password']) == 0:
            errors.append("Password is required.")
        #Password Confirmation
        if form_data['password'] != form_data['password_confirmation']:
            errors.append("Passwords must match.")

        return errors

    def create_user(self, form_data):
        hashedpw = bcrypt.hashpw(form_data['password'].encode(), bcrypt.gensalt())
        return User.objects.create(
            name = form_data['name'],
            alias = form_data['alias'],
            email = form_data['email'],
            password = hashedpw,
        )

    def validate_login(self, form_data):
        errors = []
        #Email
        if len(form_data['email']) == 0:
            errors.append ("Email is required")
        #Password
        if len(form_data['password']) == 0:
            errors.append ("Password is required")

        user = User.objects.filter(email = form_data['email']).first()

        if user:
            user_password = form_data['password'].encode()
            db_password = user.password.encode()

            if bcrypt.checkpw(user_password, db_password):
                return {'user': user}

        errors.append("Email or password does not match.")
        return {'errors': errors}

class User(models.Model):
    name = models.CharField(max_length = 45)
    alias = models.CharField(max_length = 45)
    email = models.CharField(max_length = 45)
    password = models.CharField(max_length = 45)
    friended = models.ManyToManyField("self", related_name="friended_by")
    created_at = models.DateTimeField(auto_now_add =True)
    updated_at = models.DateTimeField(auto_now =True)

    objects = UserManager()

    def __str__(self):
        return "{} {} {} {} {}".format(self.id, self.name, self.alias, self.email, self.password)
