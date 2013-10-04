from operator import itemgetter

from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, render_to_response
from django.contrib.auth.models import User
from django.core.context_processors import csrf
from django.views.generic import UpdateView, CreateView, DetailView

from .forms import feed_form
from .models import feed, Article

from get_new_articles import run


def home(request): 

    if request.user.id == None: # Get the currently logged in user. If there is not one, use AnonymousUser (demo)
        current_user = 2
    else:
        current_user = request.user.id
    feeds_for_topics = feed.objects.filter(user=current_user).values('topic').distinct() # For sidebar, get each topic
    starred_articles = Article.objects.filter(starred=True, user=current_user) 

    return render(request, 'reader/home.html', {'feeds_for_topics': feeds_for_topics, 'starred_articles': starred_articles})

def reader(request, topic):
    
    if request.user.id == None: # Get the currently logged in user. If there is not one, use AnonymousUser (demo)
        current_user = 2
    else:
        current_user = request.user.id
    
    feeds_for_topics = feed.objects.filter(user=current_user).values('topic').distinct()
    feeds_for_articles = feed.objects.filter(topic=topic, user=current_user).values('id')
    starred_articles = Article.objects.filter(starred=True, user=current_user) 

    articles_unsorted = []
    articles = []
    for d in feeds_for_articles:
        articles_in_feed = Article.objects.filter(feed_id=d['id']).values()
        for article in articles_in_feed:
            articles_unsorted.append(article)
    articles = sorted(articles_unsorted, key=itemgetter('published_date'), reverse=True)

    return render(request, 'reader/reader.html', {'feeds_for_topics': feeds_for_topics, 'articles': articles, 
        'starred_articles': starred_articles})

def display_starred_articles(request):

    if request.user.id == None: # Get the currently logged in user. If there is not one, use AnonymousUser (demo)
        current_user = 2
    else:
        current_user = request.user.id

    feeds_for_topics = feed.objects.filter(user=current_user).values('topic').distinct()
    articles = Article.objects.filter(starred=True, user=current_user).order_by('-published_date')
    starred_articles = Article.objects.filter(starred=True, user=current_user) 

    return render(request, 'reader/starred.html', {'feeds_for_topics': feeds_for_topics, 'articles': articles, 
        'starred_articles': starred_articles})

def manage_feeds(request):
    if request.POST:
        form = feed_form(request.POST)
        if form.is_valid():
            new_feed = form.save(commit=False)
            new_feed.user = request.user
            new_feed.save()
            return HttpResponseRedirect('/manage-feeds')
    else:
        form = feed_form()
        feeds = feed.objects.filter(user=request.user)

        return render(request, 'reader/manage_feeds.html', {'form': form, 'feeds': feeds})

def delete_feed(request, id):
    current_user = request.user.id
    # select owner of feed. check to make sure owner is current logged in user, then delete. if not, 404
    feed_owner = feed.objects.get(id=id).user.id

    if current_user == feed_owner:
        feed.objects.filter(id=id).delete()
        print "deleted"
        return HttpResponseRedirect('/manage-feeds')
    else: 
        print "REJECTED"
        return HttpResponseRedirect('/manage-feeds')

def star_article(request, id):
    a = Article.objects.get(id=id)
    current_user = request.user.id
    article_owner = Article.objects.get(id=id).user.id

    if current_user == article_owner:
        if a.starred == False:
            a.starred = True
        else:
            a.starred = False
        a.save()
    else:
        pass

    return HttpResponseRedirect('')

def run_get_new_articles(request, id):
    run()

    return HttpResponseRedirect('')


