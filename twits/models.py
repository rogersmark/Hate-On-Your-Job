import random
import re,urllib
import twitter
import secretballot
from django.db.models.signals import post_save
from captcha.fields import CaptchaField
import datetime
from django.template import defaultfilters
from django.db.models import permalink
from django.forms import ModelForm
from django import forms
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
            #api = twitter.Api(username="hateonyourjob", password="bl00drun3")
            #api.PostUpdate("%s just received some hate-o-rade! %s" % (self.hate_company, self.get_absolute_url()))
        super(Hate, self).save()


    @permalink
    def get_absolute_url(self):
        return ("twit-hate", (), {'id':self.id})

class CompanyForm(ModelForm):
    captcha = CaptchaField()
    company_description = forms.CharField(max_length=200, help_text="200 Character Max. This field for Company Desc, not for hating. Please enter 'Get Your Hate On' for hating!", widget=forms.Textarea)
    class Meta:
        model = Company
        fields = ('company_name', 'company_category', 'company_description')

class HateForm(ModelForm):
    captcha = CaptchaField()
    hate_entry = forms.CharField(max_length=200, help_text="200 Character Max", widget=forms.Textarea)
    class Meta:
        model = Hate 
        fields = ('hate_company', 'hate_title', 'hate_entry')

secretballot.enable_voting_on(Hate)

def tiny_url(url):
    apiurl = "http://tinyurl.com/api-create.php?url="
    tinyurl = urllib.urlopen(apiurl + url).read()
    return tinyurl

def content_tiny_url(content):
    
    regex_url = r'http:\/\/([\w.]+\/?)\S*'
    for match in re.finditer(regex_url, content):
        url = match.group(0)
        content = content.replace(url,tiny_url(url))
    
    return content

def hate_tweet(sender, instance, created, **kwargs):
    if created:
        try:
            random_num = random.randrange(0,3)
            if random_num == 0:
                twit_string = "just received some hate-o-rade!"

            elif random_num == 1:
                twit_string = "has some unhappy employees!"

            else:
                twit_string = "apparently needs to throw a company picnic!"

            url = content_tiny_url("http://www.hateonyourjob.com/%s" % instance.get_absolute_url())
            api = twitter.Api(username="hateonyourjob", password="bl00drun3")
            api.PostUpdate("%s %s %s" % (instance.hate_company, twit_string, url))
        except:
            pass

post_save.connect(hate_tweet, sender=Hate)
