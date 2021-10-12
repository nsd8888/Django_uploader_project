from boto3 import Session
from django.shortcuts import render,HttpResponseRedirect
import facebook
import tweepy
import os

from .ml_model.reverse_image import training_model
from .models import Image
from .forms import ImageUpload, SignUpForm,face_form,twitter_form,all_form
# Create your views here.
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm,PasswordChangeForm
from django.contrib.auth import authenticate,login,logout,update_session_auth_hash
from django.contrib import messages
from django.contrib.auth.forms import User



def home(request):
    return render(request, 'enroll/home.html')

def Sign_Up(request):
    if request.method == "POST":
        fm = SignUpForm(request.POST)
        if fm.is_valid():
            fm.save()
    else:
        fm = SignUpForm()
    return render(request, 'enroll/sign.html', {'form': fm})

def Log_In(request):
    if request.method == "POST":
        fm = AuthenticationForm(request=request, data=request.POST)
        if fm.is_valid():
            uname = fm.cleaned_data['username']
            pword = fm.cleaned_data['password']
            user = authenticate(username=uname, password=pword)
            if user is not None:
                login(request, user)
                messages.success(request, 'Logged in successfully')
                return HttpResponseRedirect('/profile/')
    else:
        fm = AuthenticationForm()
    return render(request, 'enroll/login.html', {'form': fm})

def profile(request):
    if request.user.is_authenticated:
        if request.method=='POST':
            fm=ImageUpload(request.POST, request.FILES)
            if fm.is_valid():
                instance=fm.save(commit=False)
                instance.user=request.user
                instance.save()
                fm.save()
        else:
            fm=ImageUpload(instance=request.user)
            print('hello i am in non post')
        img=Image.objects.filter(user=request.user)
        return render(request,'enroll/profile.html',{'form':fm,'img':img})
    else:
        return HttpResponseRedirect('/login/')

def delete_image(request,id):
    if request.method=='GET':
        img=Image.objects.get(id=id)
        img.delete()
    return HttpResponseRedirect('/profile/')

def Log_out(request):
    logout(request)
    return HttpResponseRedirect('/login/')

def ChangePass(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            print(request.user)
            fm = PasswordChangeForm(user=request.user, data=request.POST)
            if fm.is_valid():
                fm.save()
                update_session_auth_hash(request, fm.user)
                return HttpResponseRedirect('/profile/')
        else:
            fm = PasswordChangeForm(user=request.user)
        return render(request, 'enroll/passchange.html', {'form': fm})
    else:
        return HttpResponseRedirect('/login/')

def show(request,id):
    if request.user.is_authenticated:
        img=Image.objects.filter(user=request.user)
        lst1=[]
        for i in img:
            lst1.append(i.photo.name)
        img_search = Image.objects.get(user=request.user,id=id)
        print(lst1)
        print(img_search.photo.name)

        res=training_model(lst1,img_search.photo.name)
        print(res)
        print(img_search)
        final=[]
        for i in res:
            final.append(os.path.join('https://cosmosimages88.s3.ap-south-1.amazonaws.com',i).replace('\\','/'))
        #res=test_model(img_search.photo.name)
        print(final)
        #return render(request, 'enroll/show.html', {'img': img,'img_sh':img_search})
        return render(request, 'enroll/show.html', {'img': final,'img_sh':img_search})
    else:
        return HttpResponseRedirect('/prof/')

def face_section(request):
    if request.method=='POST':
        fm=face_form(request.POST,request.FILES)
        if fm.is_valid():
            #print(request.FILES)
            #print(request.POST)
            photo=request.FILES['photo']
            token_id=request.POST['face_access']
            msg=request.POST['message']
            fp = facebook.GraphAPI(access_token=token_id)
            fp.put_photo(photo, message=msg)

    else:
        fm=face_form()
    return render(request,"enroll/facebook.html",{"fm":fm})

def facebook_form(request, id):
    if request.method=='POST':
        print("I am in POST method of facebook_form")
        fm = face_form(request.POST, request.FILES)
        print(request.POST)
        print(request.FILES)
        if fm.is_valid():
            print(request.FILES)
            print(request.POST)
            photo = request.POST['photo']
            token_id = request.POST['face_access']
            msg = request.POST['message']
            print(token_id)
            print(photo.Image.path)
            print(msg)
            fp = facebook.GraphAPI(access_token=token_id)
            fp.put_photo(photo.path, message=msg)
        return HttpResponseRedirect('/profile/')
    else:
        pho = Image.objects.get(id=id)
        # with open('tweep.jpg', 'wb') as fp:
        # for line in pho.photo:
        # fp.write(line)
        print(pho.photo)
        request.FILES['photo'] = pho.photo
        # fm = face_form(request.FILES['photo'])


        # print(request.FILES)
        # print(request.GET)
        return render(request, "enroll/facebook.html", {"fm": fm})

def tweeter_upload(request):
    if request.method=="POST":
        fm = twitter_form(request.POST, request.FILES)
        if fm.is_valid():
            API_key = request.POST['API_key']
            API_Secrete_key = request.POST['API_Secrete_key']
            Access_token = request.POST['Access_token']
            Access_token_secrete = request.POST['Access_token_secrete']
            photo = request.FILES['photo']
            msg = request.POST['text']
            print(API_key)
            def Auth():
                auth = tweepy.OAuthHandler(API_key, API_Secrete_key)
                auth.set_access_token(Access_token, Access_token_secrete)
                return auth
            tw = Auth()
            api = tweepy.API(tw, wait_on_rate_limit=True)
            with open('tweep.jpg','wb') as fp:
                for line in photo:
                    fp.write(line)
                media = api.media_upload('tweep.jpg')
                api.update_status(msg, media_ids=[media.media_id_string])
            os.remove('tweep.jpg')
    else:
        fm=twitter_form()
    return render(request, "enroll/twitter.html", {"fm": fm})

def all_social(request):
    ms=['Facebook','Tweeter']
    if request.method=='POST':
        fm=all_form(request.POST,request.POST)
        select=request.POST.getlist("select")

        #for tweete
        def tweet():
            API_key ='lmlwxHVW0r49gI8Ws1FaFxhad'
            API_Secrete_key ='afLwJsmcpZ2sgTbxoqLKgRo07NzHkX3ub0yofCNZrupztxv2Ea'
            Access_token ='3244210008-lKr2taD3fQvzgGDGdIDbXnT9bkR9nGeQU92Amzg'
            Access_token_secrete ='vL0wALqLWkJ7gnmjXsyARGua7LvuqtdYcRL6vmbYTaRaU'

            photo = request.FILES['photo']
            msg = request.POST['message']

            def Auth():
                auth = tweepy.OAuthHandler(API_key, API_Secrete_key)
                auth.set_access_token(Access_token, Access_token_secrete)
                return auth

            tw = Auth()
            api = tweepy.API(tw, wait_on_rate_limit=True)
            with open('tweep.jpg', 'wb') as fp:
                for line in photo:
                    fp.write(line)
                media = api.media_upload('tweep.jpg')
                api.update_status(msg, media_ids=[media.media_id_string])
            os.remove('tweep.jpg')

        #for facebook
        def face():
            token_id ='EAABtTGKq4dMBAKEwcZAY3qHJVqGRpZAb8twSZBlmKxIGVMtOSZBVMokmQRAn02j1ZBrFuDOCRTvmcN9swFOKqhyYfbMmiqTZAutJmnuyFGZAdfX4FL5hZCoEmMXh7QKJCus7LQsLZCvZBsG9TmNRbGWlSGoaeN5iRC0AUHA4yAfVcgjeZAdO0ctqwXgNcC6nOODm6GZAol03upW6oNZBRjzvSuLYN'
            photo = request.FILES['photo']
            msg = request.POST['message']
            fp = facebook.GraphAPI(access_token=token_id)
            fp.put_photo(photo, message=msg)

        if select==['Facebook']:
            face()
        if select==['Tweeter']:
            tweet()
        if select==['Facebook','Tweeter']:
            face()
            tweet()
        return HttpResponseRedirect("/profile/")
    else:
        fm=all_form()
        return render(request,'enroll/all.html', {'fm':fm})
