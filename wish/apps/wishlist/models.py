from __future__ import unicode_literals
from django.db import models
import re
import bcrypt
PASS_Regex = re.compile(r'^(?=.{8,15}$)(?=.*[A-Z])(?=.*[0-9]).*$')
EMAIL_Regex = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
NAME_Regex = re.compile(r'^(?=.{2,})([a-zA-z]*)$')



class UserManager(models.Manager):
    def register_validation(self, postData):
        errors = []
        if len(postData['name']) < 3:
            errors.append("A valid name is required")
        if not postData['name'].isalpha():
            errors.append("no numbers or special characters")
        if postData['initial_pw'] != postData['confirm_pw']:
            errors.append("Passwords do not match")
        if len(postData['initial_pw']) < 8 or len(postData['confirm_pw']) < 8:
            errors.append("Password must be at least 8 characters")
        if User.objects.filter(username=postData['username']):
            errors.append("This username has already been registered")
        if len(postData['username']) < 3:
            errors.append("Username must be at least 3 characters")
        if not postData['username'].isalnum():
            errors.append("only numbers and letters")
        if not postData['date_hired']:
            errors.append("Date hired cannot be blank")
        return errors
    def login_validation(self, postData):
        errors= []
        if not User.objects.filter(username=postData['username']):
            errors.append("this user name doesnt exist")
        user =  User.objects.get(username= postData['username'])
        if not bcrypt.checkpw(postData['password'].encode(), user.password.encode()):
            errors.append("failed password")
        return errors

         


class ItemManager(models.Manager):
    def item_validation(self, postData):
        errors = []
        if len(postData['item_name']) < 3:
            errors.append("must be at least 3 characters")
        if not postData['item_name']:
            errors.append("cant be blank")
        if Item.objects.filter(item_name=postData['item_name']).exists():
            errors.append("Item already added by a user")
        return errors


class User(models.Model):
    name = models.CharField(max_length=255)
    username = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    date_hired = models.DateField(auto_now=False)

    objects = UserManager()

    def __repr__(self):
        return "<User {}: {}>".format(self.id, self.name)


class Item(models.Model):
    item_name = models.CharField(max_length=255, unique=True)
    added_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="has_added_items")
    liked_by = models.ManyToManyField(User, related_name='has_liked_items')
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    objects = ItemManager()

    def __repr__(self):
        return "<Item {}: {}>".format(self.id, self.item_name)


# Using a regex in Python, how can I verify that a user's password is:


# At least 8 characters
# Must be restricted to, though does not specifically require any of:
# uppercase letters: A-Z
# lowercase letters: a-z
# numbers: 0-9
# any of the special characters: @  # $%^&+=
# Note, all the letter/number/special chars are optional. I only want to verify that the password is at least 8 chars in length and is restricted to a letter/number/special char. It's up to the user to pick a stronger / weaker password if they so choose. So far what I have is:

# import re
# pattern = "^.*(?=.{8,})(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[@#$%^&+=]).*$"
# password = raw_input("Enter string to test: ")
# result = re.findall(pattern, password)
# if (result):
#     print "Valid password"
# else:
#     print "Password not valid"
