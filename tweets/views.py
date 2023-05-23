import random
from django.conf import settings
#from django.utils.http import is_safe_url
from django.http import HttpRequest, HttpResponse, Http404, JsonResponse, HttpResponseRedirect
from django.shortcuts import render,redirect

from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes, authentication_classes  #used to define function-based views as API endpoints
from rest_framework.response import Response


from .models import Tweet
from .forms import TweetForm
from .serializers import TweetSerializer, TweetActionsSerializer

ALLOWED_HOSTS = settings.ALLOWED_HOSTS

# Create your views here.

# DJANGO_REST_FRAMEWORK VIEWS(SERIALIZERS)
def home_view(request,*args, **kwargs):
    #print(args, kwargs)
    #return HttpResponse('<h1>Hello world</h1>')
    return render(request, "pages/home.html", context={}, status=200)    # render is used for templates

@api_view(['POST'])  # client must send a POST request
# @authentication_classes([SessionAuthentication, MyCustomAuth])
@permission_classes([IsAuthenticated])
def tweets_create_view(request, *args, **kwargs):
    serializer = TweetSerializer(data = request.POST)
    if serializer.is_valid():
        serializer.save(user=request.user)
        return Response(serializer.data, status=201)
    return Response({},status=400)

@api_view(['GET'])
def tweets_list_view(request,*args, **kwargs):
    qs= Tweet.objects.all()
    serializer = TweetSerializer(qs, many=True)   
    return Response(serializer.data)

@api_view(['GET'])
def tweets_detail_view(request,tweet_id,*args, **kwargs):
    qs= Tweet.objects.filter(id=tweet_id)
    if not qs.exists():
        return Response({},status=404)
    obj = qs.first()
    serializer = TweetSerializer(qs, many=True)   
    return Response(serializer.data, status=200)

@api_view(['GET','POST', 'DELETE'])
@permission_classes([IsAuthenticated])
def tweets_delete_view(request,tweet_id,*args, **kwargs):
    qs = Tweet.objects.filter(id=tweet_id)
    if not qs.exists():
        return Response({},status=404)
    qs = qs.filter(user=request.user)
    if not qs.exists():
        return Response({"message":"You cannot delete this tweet"},status = 401)
    obj = qs.first()
    obj.delete()
    serializer = TweetSerializer(qs, many=True)   
    return Response({"message":"Tweet removed "}, status=200)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def tweets_action_view(request,*args, **kwargs):
    """ 
    id is required
    ACTIONS --> like, unlike, retweet
    """  
    serializer = TweetActionsSerializer(data = request.POST)
    if serializer.is_valid(raise_exception=True):
        data = serializer.validated_data
        tweet_id = data.get("id")
        action = data.get("action")

    qs = Tweet.objects.filter(id=tweet_id)
    if not qs.exists():
        return Response({},status=404)
    
    obj = qs.first()
    if action == "likes":
        obj.likes.add(request.user)
    elif action == "unlike":
        obj.likes.remove(request.user)
    elif action == "retweet":
        # TODO
        pass
    return Response({"message":"Tweet removed "}, status=200)













# PURE DJANGO VIEWS
def tweet_create_view_pure_django(request : HttpRequest, *args, **kwargs):
    # VERIFYING IF AJAX
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
    
    user = request.user
    if not request.user.is_authenticated:
        user = None
        if is_ajax:
            return JsonResponse({}, status=401)
        return redirect(settings.LOGIN_URL)
    form = TweetForm(request.POST or None)
    next_url  = request.POST.get("next") or None
    if form.is_valid():
        obj = form.save(commit=False)
        obj.user = user
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

def tweet_list_view_pure_django(request, *args, **kwargs):
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


def tweets_detail_view_pure_django(request, tweet_id, *args, **kwargs):
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