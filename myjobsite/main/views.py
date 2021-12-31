
from django.http import HttpResponse,JsonResponse
from django.shortcuts import HttpResponse,render,HttpResponseRedirect,redirect,reverse
from django.contrib import auth,messages
from django.contrib.auth import authenticate,logout
from django.contrib.auth.models import User
import json
from .forms import AdminRegistrationForm
from .models import Jobs,MyJobs
from django.contrib import messages
from django.utils.timezone import localdate
from rest_framework.renderers import JSONRenderer
from django.views.decorators.csrf import csrf_exempt,csrf_protect


def register(request):
    return render(request=request, template_name='register.html')


def register_user(request):
    if request.POST:

        f_name = request.POST.get('f_name')
        l_name = request.POST.get('l_name')
        email = request.POST.get('email')
        pw = request.POST.get('pw')
        pw_confirm = request.POST.get('pw_confirm')
        #print(f_name, l_name, email, pw, pw_confirm)
        user = User()
        user.first_name = f_name
        user.last_name = l_name
        user.username = email
        if pw == pw_confirm:
            user.set_password(pw)
        else:
            return HttpResponse(json.dumps([{"validation": "Password does not match", "status": False}]),
                                content_type="application/json")
        user.is_staff = True
        user.save()
        register_success = [{"validation": "Registration Successful", "status": True}]
        return HttpResponse(json.dumps(register_success), content_type="application/json")
    else:
        return HttpResponse(json.dumps([{"validation": "I am watching you (0_0)", "status": False}]),
                            content_type="application/json")


def login(request):
    if request.POST:
        email = request.POST.get('email')
        pw = request.POST.get('pw')
        log_user = authenticate(username=email, password=pw)
        #print(log_user)

        if log_user is not None:
            authentication_success = [{"validation": "Authentication Successful", "status": True}]
           
            request.session['cur_user'] = log_user.first_name
            request.session['username'] = log_user.username
            request.session.save()
            return redirect('dashboard')
       
        else:
           # authentication_failure = [{"validation": "Authentication Failed", "status": True}]
           # return HttpResponse(json.dumps(authentication_failure), content_type="application/json")
           messages.info(request, 'Not valid credentials')
           
           return redirect(reverse('register'))


def dashboard(request):
   job=Jobs.objects.values().filter(email=request.session['username'])
   
  # print(job)
   return render(request,'dashboard.html',{"name":request.session['cur_user'],"email":request.session['username']})
  
def job_create(request):
   return render(request,'newJob.html',{"name":request.session['cur_user']})

def add_job(request):
    title=request.POST.get('title')
    location=request.POST.get('location')
    email=request.session['username']
    description=request.POST.get('desc')
    category=""
    if request.POST.get('sub1')!=None:
        category=category+",Pet Care"
    if request.POST.get('sub2')!=None:
       category=category+",Electrical"
    if request.POST.get('sub3')!=None:
        category=category+",Garden"
    if request.POST.get('others')!=None:
        category=","+category+request.POST.get('others')
    if category[0]==',':
        category=category[1:]
    posted_by=request.session['cur_user']
    posted_on=localdate()
    #print(title,location,email,category,description,posted_by,posted_on)
    
    job=Jobs(title=title,location=location,email=email,category=category,description=description,posted_by=posted_by,posted_on=posted_on)
    
   # print("Hello")
    
    job.save()    
    messages.info(request, "Job registered")
    
    return redirect('dashboard')

def logout_request(request):
    logout(request)
    return redirect(reverse('register'))

def getJobData(request):
    jobData=list(Jobs.objects.values().filter(email=request.session['username']))
    #print(Jobs.objects.values().filter(email=request.session['username']))
    content=JSONRenderer().render(jobData)
    return HttpResponse(content,content_type="application/json")

def getJobDataAll(request):
    jobData=list(Jobs.objects.values())
    content=JSONRenderer().render(jobData)
    return HttpResponse(content,content_type="application/json")

@csrf_exempt
def my_jobs(request):
    #job=MyJobs(email=request.session['username'],title=request.POST.get(''))
    #job.save()
    #print(job.email)
    print("hi")
    print(request.body)
    return redirect('dashboard')

