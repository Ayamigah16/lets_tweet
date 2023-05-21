from django.http import HttpResponse, Http404, JsonResponse
from django.shortcuts import render

from .models import Tweet

# Create your views here.
def home_view(request,*args, **kwargs):
    print(args, kwargs)
    #return HttpResponse('<h1>Hello world</h1>')
    return render(request, "pages/home.html", context={}, status=200)    # render is used for templates

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