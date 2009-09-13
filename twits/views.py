import datetime, re
from django.conf import settings
from django import http
from django.views.decorators.cache import cache_page
from django.views.decorators.cache import cache_page
from django.template import defaultfilters
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.db.models import Q
from django.core.paginator import Paginator
from secretballot.middleware import SecretBallotIpUseragentMiddleware
from hateonyourjob.twits import models, forms

@cache_page(300)
def index(request):
    twit_list = Paginator(models.Hate.objects.all(), 25)
    page = int(request.GET.get('page', '1'))
    twits = twit_list.page(page)
    return render_to_response("twits/index.html", {'twits': twits})

def company(request, slug, sort=None):
    company = get_object_or_404(models.Company, company_slug=slug)
    if sort:
        if sort == "votes":
            twit_list = Paginator(models.Hate.objects.filter(hate_company=company).order_by("-hate_vote"), 25)

        elif sort == "newest":
            twit_list = Paginator(models.Hate.objects.filter(hate_company=company).order_by("-created_date"), 25)

        elif sort == "oldest":
            twit_list = Paginator(models.Hate.objects.filter(hate_company=company).order_by("created_date"), 25)

        elif sort == "title":
            twit_list = Paginator(models.Hate.objects.filter(hate_company=company).order_by("hate_title"), 25)

        else:
            twit_list = Paginator(models.Hate.objects.filter(hate_company=company), 25)

    else:
        twit_list = Paginator(models.Hate.objects.filter(hate_company=company), 25)
    page = int(request.GET.get('page', '1'))
    twits = twit_list.page(page)
    return render_to_response("twits/companies.html", {'twits': twits})

def company_id(request, id):
    company = get_object_or_404(models.Company, id=id)
    twit_list = Paginator(models.Hate.objects.filter(hate_company=company), 25)
    page = int(request.GET.get('page', '1'))
    twits = twit_list.page(page)
    return render_to_response("twits/companies.html", {'twits': twits})

def category(request, slug):
    category = get_object_or_404(models.Category, category_slug=slug)
    comps = models.Company.objects.filter(company_category=category.id)
    return render_to_response("twits/categories.html", {'comps': comps})

def hate_on(request, slug=None):
    if request.method == 'POST':
        form = forms.HateForm(request.POST)
        if form.is_valid():
            human = True
            form.save()
            return HttpResponseRedirect('/')
    else:
        if slug:
            item = get_object_or_404(models.Company, company_slug=slug)
            form = forms.HateForm(initial={'hate_company': item.id})
        else:
            form = forms.HateForm()
    return render_to_response("twits/hate_on.html", {'form': form})

def new_company(request):
    if request.method == 'POST':
        form = forms.CompanyForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            human = True
            form.save()
            slug = defaultfilters.slugify(data['company_name'])
            hate_obj = models.Hate()
            hate_obj.hate_company=models.Company.objects.get(company_slug=slug)
            hate_obj.hate_title=data['hate_title']
            hate_obj.hate_entry=data['hate_entry']
            hate_obj.hate_vote=1
            hate_obj.created_date=datetime.datetime.now()
            hate_obj.save()
            return HttpResponseRedirect('/')
    else:
        form = forms.CompanyForm(initial={'company_description': "Please place a short description of the company here."})
    return render_to_response("twits/new_company.html", {'form': form})

def about(request):
    return render_to_response("twits/about.html", {})

def vote_up(request, id):
    twit = get_object_or_404(models.Hate, id=id)
    token = gen_token(request)
    twit.add_vote(token, "1")
    vote = models.Hate.objects.get(id=id)
    vote.hate_vote = vote.vote_total
    vote.save()
    return HttpResponseRedirect('/total_votes/%s' % twit.id)

def vote_down(request, id):
    twit = get_object_or_404(models.Hate, id=id)
    token = gen_token(request)
    twit.add_vote(token, "1")
    vote = models.Hate.objects.get(id=id)
    vote.hate_vote = vote.vote_total
    vote.save()
    return HttpResponseRedirect('/total_votes/%s' % twit.id)

def total_votes(request, id):
    twit = models.Hate.objects.get(id=id) 
    return render_to_response("twits/total_vote.html", {'twit': twit})

def gen_token(request):
    temp = SecretBallotIpUseragentMiddleware()
    token = temp.generate_token(request)
    return token

def greatest_hates(request):
    companies = models.Company.objects.all()[0:9]
    categories = models.Category.objects.all()
    twit_list = Paginator(models.Hate.objects.order_by('-hate_vote'), 25)
    page = int(request.GET.get('page', '1'))
    twits = twit_list.page(page)
    return render_to_response("twits/greatest.html", {'twits': twits})

def search(request):
    if 'q' in request.GET:
        term = request.GET['q']
        comp_list = Paginator(models.Company.objects.filter(Q(company_name__icontains=term) | Q(company_description__icontains=term)), 5)
        page = int(request.GET.get('page', '1'))
        comp = comp_list.page(page)

    if comp is []:
       return HttpResponseRedirect('/')
    return render_to_response("twits/search.html", {'comp': comp})

def hate_id(request, id):
    companies = models.Company.objects.all()[0:9]
    categories = models.Category.objects.all()
    twit = get_object_or_404(models.Hate, id=id)
    return render_to_response("twits/hate.html", {'twit': twit})

def company_list(request):
    companies = models.Company.objects.all()[0:9]
    categories = models.Category.objects.all()
    comp_list = Paginator(models.Company.objects.all(), 25)
    page = int(request.GET.get('page', '1'))
    comp = comp_list.page(page)
    return render_to_response("twits/company_list.html", {'comp': comp})

def cache_view(request):
    """                 
    Tries to import memcache, fails out if it can't and raises a 404. Also
    raises a 404 in the case of unauthenticated users, or memcache not
    being used. Graciously borrowed from:
    http://effbot.org/zone/django-memcached-view.htm
    """
    try:
        import memcache
    except ImportError:
        raise http.Http404

    if not (request.user.is_authenticated() and
            request.user.is_staff):
        raise http.Http404

    # get first memcached URI
    m = re.match(
        "memcached://([.\w]+:\d+)", settings.CACHE_BACKEND
    )
    if not m:
        raise http.Http404

    host = memcache._Host(m.group(1))
    host.connect()
    host.send_cmd("stats")

    class Stats:
        pass

    stats = Stats()

    while 1:
        line = host.readline().split(None, 2)
        if line[0] == "END":
            break
        stat, key, value = line
        try:
            # convert to native type, if possible
            value = int(value)
            if key == "uptime":
                value = datetime.timedelta(seconds=value)
            elif key == "time":
                value = datetime.datetime.fromtimestamp(value)
        except ValueError:
            pass
        setattr(stats, key, value)

    host.close_socket()

    return render_to_response(
        'memcached_status.html', dict(
            stats=stats,
            hit_rate=100 * stats.get_hits / stats.cmd_get,
            time=datetime.datetime.now(), # server time
        ))

