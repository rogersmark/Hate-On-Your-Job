import random, datetime
import re,urllib
import twitter
import secretballot
from captcha.fields import CaptchaField
from django.template import defaultfilters
from django.db.models import permalink
from django.db import models

class Category(models.Model):
    category_name = models.CharField(max_length=100, unique=True)
    category_slug = models.SlugField()   

    def __unicode__(self):
        return self.category_slug 

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['category_name']

    @permalink
    def get_absolute_url(self):
        return ("twit-category", (), {'slug':self.category_slug})

class Company(models.Model):
    """ The companies that tweets will be assigned to """
    company_name = models.CharField(max_length=150, unique=True)
    company_category = models.ForeignKey(Category)
    company_description = models.TextField(max_length=200)
    company_slug = models.SlugField()
    created_date = models.DateTimeField(default=datetime.datetime.now)

    class Meta:
        verbose_name_plural = "Companies"
        ordering = ['-created_date']

    def __unicode__(self):
        return self.company_name

    def save(self):
        if not self.id:
            self.company_slug = defaultfilters.slugify(self.company_name)
        super(Company, self).save()
 
    @permalink
    def get_absolute_url(self):
        return ("twit-company", (), {'slug':self.company_slug})
 
class Hate(models.Model):
    """ The tweets that will be assigned to companies - aka the rants """
    hate_company = models.ForeignKey(Company)
    hate_title = models.CharField(max_length=100)
    hate_entry = models.CharField(max_length=200)
    hate_vote = models.IntegerField(blank=True)
    created_date = models.DateTimeField(default=datetime.datetime.now)

    class Meta:
        verbose_name_plural = "Hates"
        ordering = ['-created_date']

    def __unicode__(self):
        return self.hate_title

    def save(self):
        if not self.id:
            if self.hate_vote is None:
                self.hate_vote = 0
        super(Hate, self).save()


    @permalink
    def get_absolute_url(self):
        return ("twit-hate", (), {'id':self.id})

secretballot.enable_voting_on(Hate)
