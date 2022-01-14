
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
from urllib.parse import urlparse
from urllib.parse import parse_qs
from django.forms import ModelForm


def register(request):
    return render(request=request, template_name='register.html')


def register_user(request):
    if request.POST:

        f_name = request.POST.get('f_name')
        l_name = request.POST.get('l_name')
        email = request.POST.get('email')
        pw = request.POST.get('pw')
        pw_confirm = request.POST.get('pw_confirm')
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
    try:   
        if category[0]==',':
            category=category[1:]
            if category[0]==',':
                category=category[1:]
    except:
        return redirect('dashboard')
    posted_by=request.session['cur_user']
    posted_on=localdate()

    
    job=Jobs(title=title,location=location,email=email,category=category,description=description,posted_by=posted_by,posted_on=posted_on)
    

    
    job.save()    
    messages.info(request, "Job registered")
    
    return redirect('dashboard')

def logout_request(request):
    logout(request)
    return redirect(reverse('register'))

def getJobData(request):
    jobData=list(MyJobs.objects.values().filter(email=request.session['username']))
    content=JSONRenderer().render(jobData)
    return HttpResponse(content,content_type="application/json")

def getJobDataAll(request):
    jobData=list(Jobs.objects.values())
    
    checklist=list(MyJobs.objects.values())
    for i in range(0,len(jobData)):
        for j in range(0,len(checklist)):
            try:
                if jobData[i]['job_id']==checklist[j]['job_id']:
                    jobData[i]=""
            except:
                pass
            
            #if jobData[i]['job_id']==checklist[j]['job_id']:
             #   jobData[i]=""
    jobData[:] = [x for x in jobData if x != ""]
    content=JSONRenderer().render(jobData)
    return HttpResponse(content,content_type="application/json")

@csrf_exempt
def my_jobs(request):
    job_id=urlparse(str(request))
    job_id=parse_qs(job_id.query)['id'][0]
    job_id=job_id[:-2]
    id,button=job_id.split('_')
    
    if button=="add":
        job=MyJobs(email=request.session['username'],title=Jobs.objects.values().filter(job_id=id)[0]['title'],job_id=id)
        try:    
            job.save()
        except:
            print("Same job added")
        
    if button=="view":
        job=MyJobs.objects.values().filter(job_id=id)[0]['job_id']

        request.session['job']=job
        return redirect('view')

    if button=="done":
        job=MyJobs.objects.values().filter(job_id=id)[0]['job_id']
        request.session['job']=job
        return redirect('done')

    if button=="giveup":
        print(job_id)
        job=MyJobs.objects.values().filter(job_id=id)[0]['job_id']
        print(job)
        request.session['job']=job
        return redirect('giveup')

    return redirect('dashboard')
    
def all_jobs(request):
    job_id=urlparse(str(request))
    job_id=parse_qs(job_id.query)['id'][0]
    job_id=job_id[:-2]
    id,button=job_id.split('_')
    if button=="add":
        job=MyJobs(email=request.session['username'],title=Jobs.objects.values().filter(job_id=id)[0]['title'],job_id=id)
        try:    
            job.save()
        except:
            print("Same job added")
        
    if button=="view":
        job=Jobs.objects.values().filter(job_id=id)[0]['job_id']
        request.session['job']=job
        request.session['id']=id
        return redirect('view')

    if button=="remove":
        job=Jobs.objects.values().filter(job_id=id)[0]['job_id']
        request.session['job']=job
        return redirect('remove')

    if button=="edit":
        job=Jobs.objects.values().filter(job_id=id)[0]['job_id']
        request.session['job']=job
        request.session['id']=job_id
        return redirect('edit')

    return redirect('dashboard')
   

def view(request):
    job=Jobs.objects.values().filter(job_id=request.session['job'])
    return render(request,'JobDetails.html',{'id':request.session['id'],'title':job[0]['title'],'name':request.session['cur_user'],"description":job[0]['description'],"location":job[0]['location'],"category":job[0]['category']})

def giveup(request):
    id=request.session['job']
    job=MyJobs.objects.filter(job_id=id)
    job.delete()
    return redirect('dashboard')

def remove(request):
    id=request.session['job']
    job=Jobs.objects.filter(job_id=id)
    #print(job)
    job.delete()
    return redirect('dashboard')

def done(request):
    id=request.session['job']
    job=MyJobs.objects.filter(job_id=id)
    job.delete()
    job=Jobs.objects.filter(job_id=id)
    job.delete()
    return redirect('dashboard')

def edit(request):
    #print(request.session['id'])
    job_id,button=request.session['id'].split("_")
    job_id=int(job_id)
    job = Jobs.objects.get(job_id=job_id)
    return render(request,'editJob.html',{'name':request.session['cur_user'],'id':request.session['id'],'title':job.title,'location':job.location,'description':job.description})

    
def edit_job(request):
    if request.POST.get('cancel')!='Cancel':
        title=request.POST.get('title')
        location=request.POST.get('location')
        description=request.POST.get('desc')
        job_id,button=request.session['id'].split("_")
        job_id=int(job_id)
        job = Jobs.objects.get(job_id=job_id)
        job.title=title
        if len(title)<3:
            messages.info(request, 'Title cannot be less than 3 characters.')
            return redirect('edit')
        print(location)
        if location=="":
            messages.info(request, 'A location must be provided')
            return redirect('edit')
        job.location=location
        job.description=description
        job.save()
    return redirect('dashboard')