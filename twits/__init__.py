from django.conf import settings
from django.db.models.signals import post_save

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
            api = twitter.Api(username=settings.TWITTER_USER, password=settings.TWITTER_PASS)
            api.PostUpdate("%s %s %s" % (instance.hate_company, twit_string, url))
        except:
            pass

