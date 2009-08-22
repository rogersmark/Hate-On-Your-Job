from hateonyourjob.twits import models
from django import template

register = template.Library()

def sidebar():
    categories = models.Category.objects.all().order_by('category_name')
    companies = models.Company.objects.all().order_by('-created_date')[:10]
    return {'companies': companies, 'categories': categories}

register.inclusion_tag('sidebar.html')(sidebar)
