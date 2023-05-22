import random
from django.conf import settings
#from django.utils.http import is_safe_url
from django.http import HttpRequest, HttpResponse, Http404, JsonResponse, HttpResponseRedirect
from django.shortcuts import render,redirect



from .models import Tweet
from .forms import TweetForm

ALLOWED_HOSTS = settings.ALLOWED_HOSTS

# Create your views here.
def home_view(request,*args, **kwargs):
    print(args, kwargs)
    #return HttpResponse('<h1>Hello world</h1>')
    return render(request, "pages/home.html", context={}, status=200)    # render is used for templates

def tweet_create_view(request : HttpRequest, *args, **kwargs):
    # VERIFYING IF AJAX
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
    form = TweetForm(request.POST or None)
    next_url  = request.POST.get("next") or None
    if form.is_valid():
        obj = form.save(commit=False)
        obj.save()

        if is_ajax:
            return JsonResponse(obj.serialize(), status=201)

        if next_url != None: #and is_safe_url(next_url, ALLOWED_HOSTS):
            return redirect(next_url)
        form = TweetForm()

    # handling tweet errors
    if form.errors:
       if is_ajax:
            return JsonResponse(form.errors, status=400)
    return render(request, "components/form.html", context={"form":form})



def tweet_list(request, *args, **kwargs):
    """ 
    REST API VIEW
    """
    
    qs = Tweet.objects.all()
    tweets_list = [ x.serialize() for x in qs]
    data = {
        "isUser": False,
        "response": tweets_list
    }
    return JsonResponse(data)


def tweets_detail_view(request, tweet_id, *args, **kwargs):
    """ 
    Coverting the dynamic view into REST View(Jason Format)
    """
    print(args,kwargs)

    # json data
    data = {
        "id" : tweet_id,
    }
    status = 200
    try:
        obj = Tweet.objects.get(id = tweet_id)
        data['content'] = obj.content  # if id exist add content to json data
    except:
        data['message'] = "Not Found"
        status = 404
    
    return JsonResponse(data=data, status=status)