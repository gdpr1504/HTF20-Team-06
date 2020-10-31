from django.contrib.auth import login, authenticate
from mysite.core.forms import SignUpForm
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
import requests
import json
import os
from django.http.request import QueryDict
from django.http import HttpResponse
from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.contrib import messages
from django.core.mail import send_mail
from django.core.mail import EmailMessage
from django.conf import settings
from django.template.loader import render_to_string
p={}
t=''
l=''
k={}
j=''
oid=''
def home(request):
    count = User.objects.count()
    return render(request, 'home.html', {
        'count': count
    })

def help(request):
    count = User.objects.count()
    return render(request, 'help.html', {
        'count': count
    })

def students(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            ausername=str(form.cleaned_data.get('username'))
            apassword=str(form.cleaned_data.get('password1'))
            aname=str(form.cleaned_data.get('first_name'))+str(form.cleaned_data.get('last_name'))
            adept=str(form.cleaned_data.get('Department'))
            aemail=str(form.cleaned_data.get('email'))
            template=render_to_string('email_template.html',{'name':aname,'uname':ausername,'password':apassword,'fname':val})
            email=EmailMessage('Password',template,settings.EMAIL_HOST_USER,[aemail])
            email.fail_silently=False
            email.send()
            det={"sname":aname,"pword":apassword,"aid":j,"branch":adept,"roll":ausername,"email":aemail}
            addstudent=requests.post("https://antirag-api.herokuapp.com/add-student",det,headers = {'Authorization':f'Bearer {l}'})        
            return render(request,'registration/helloworld.html')
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})


def signup1(request):
    return render(request,'registration/helloworld.html')
def home1(request):
    if (request.method)=="POST":
        ausername=request.POST['Username']
        apassword =request.POST['pwd']
        det = { "aid":ausername,"pword":apassword}
        token = requests.post("https://antirag-api.herokuapp.com/admin-login",det)
        global p
        p=token.json()
        if(len(p)!=1):
            global l
            l=token.json()['access_token']
            global j
            j=token.json()['aid']
            det={"aid":j}
            resp=requests.get("https://antirag-api.herokuapp.com/admin-details",det,headers = {'Authorization':f'Bearer {l}'})
            global val
            rsp=resp.json()
            for i in range(len(rsp)):
                if(rsp[i]['Aid']==j):
                    global val
                    val=rsp[i]['fname']
            global resp1
            resp1=requests.get("https://antirag-api.herokuapp.com/admin-students",det,headers = {'Authorization':f'Bearer {l}'})
            return render(request,'registration/helloworld.html',{'values':val,'values1':resp1.json()})
        else:
            det={"roll":ausername,"pword":apassword}
            token=requests.post("https://antirag-api.herokuapp.com/student-login",det,)
            
            p=token.json()
            if(len(p)==3):
                global k
                l=token.json()['access_token']
                global sid
                sid=token.json()['roll']
                det={'roll':sid}
                global sname
                resp=requests.get("https://antirag-api.herokuapp.com/student-details",det,headers = {'Authorization':f'Bearer {l}'})
                for i in range(len(resp.json())):
                    if(resp.json()[i]['roll']==sid):
                        sname=resp.json()[i]['sname']
                        global t
                        t=resp.json()[i]['Aid']
                        if(resp.json()[i]['phone']==None):
                            return render(request,'filldetails.html')
                return render(request,'registration/login2.html',{'values':sname})
            else:    
                return render(request,'registration/login.html',{'data':p})    
def home3(request):
    if (request.method)=="POST":
        phonenumber=request.POST['phonenumber']
        pphonenumber=request.POST['phonenumber']
        address=request.POST['address']
        password=request.POST['pwd']
        det={'roll':sid,'pword':password,'phone':phonenumber,'pphone':pphonenumber,'address':address}
        resp=requests.post("https://antirag-api.herokuapp.com/first-login",det,headers = {'Authorization':f'Bearer {l}'})
        return render(request,'registration/login2.html',{'values':sname})
def homepage(request):
        return render(request,'registration/login.html',{'data':p})
def allstudents(request):
    det={"aid":j}
    resp1=requests.get("https://antirag-api.herokuapp.com/admin-students",det,headers = {'Authorization':f'Bearer {l}'})
    return render(request,'allstudents.html',{'values':val,'values1':resp1.json()})
def home2(request):

    return render(request,'addstudent.html')
def filecomplaint(request):
    name=request.GET.get('sname')
    det={'roll':sid}
    resp1=requests.get("https://antirag-api.herokuapp.com/student-details",det,headers = {'Authorization':f'Bearer {l}'})
    for i in range(len(resp1.json())):
        if(resp1.json()[i]['roll']==sid):
            val=resp1.json()[i]
    return render(request,'form2.html',{'values':val,'name':name})
def complaintregistered(request):
    if(request.method)=="POST":
        culprit=request.POST['culprit']
        roll=sid
        aid=t
        time_c=request.POST['time']
        place=request.POST['place']
        threat=int(request.POST['level ofthreat'])
        details=request.POST['details']
        resolved="0"


        threats={'1':'low','2':'medium','3':'moderate','4':'high','5':'super high'}
        det={'roll':roll,'aid':aid,'culprit':culprit,'time_c':time_c,'place':place,'details':details,'resolved':resolved,'level_of_threat':threat}
        resp1=requests.post("https://antirag-api.herokuapp.com/add-complaint",det,headers = {'Authorization':f'Bearer {l}'})
        return render(request,'registration/login2.html',{'values':sname})
def studentprofile(request):
    det={'roll':sid}
    resp1=requests.get("https://antirag-api.herokuapp.com/student-details",det,headers = {'Authorization':f'Bearer {l}'})
    for i in range(len(resp1.json())):
        if(resp1.json()[i]['roll']==sid):
            val=resp1.json()[i]
    return render(request,"studentdetails.html",{'values1':val})
@login_required
def secret_page(request):
    return render(request, 'secret_page.html')

class SecretPage(LoginRequiredMixin, TemplateView):
    template_name = 'secret_page.html'
def login_successful(request):
    det={'aid':j}
    resp=requests.get("https://antirag-api.herokuapp.com/admin-details",det,headers = {'Authorization':f'Bearer {l}'})
    val1=resp.json()
    for i in range(len(val1)):
        if(val1[i]['Aid']==j):
            value=val1[i]['fname']
    rsp=requests.get("https://antirag-api.herokuapp.com/admin-complaints",det,headers = {'Authorization':f'Bearer {l}'})
    val=rsp.json()
    a=[]
    for i in range(len(val)):
        if(val[i]['resolved']==0):
            a.append(val[i])
    return render(request,'registration/login1.html',{'val':a,'value':value})
def complaintdetails(request):
    aid=request.GET.get('aid')
    global roll
    roll=request.GET.get('roll')
    global cid
    cid=request.GET.get('cid')
    det={'aid':j}
    det1={'roll':roll}
    resp1=requests.get("https://antirag-api.herokuapp.com/student-details",det1,headers = {'Authorization':f'Bearer {l}'})
    rsp=requests.get("https://antirag-api.herokuapp.com/admin-complaints",det,headers = {'Authorization':f'Bearer {l}'})
    rp=requests.get("https://antirag-api.herokuapp.com/admin-details",det,headers = {'Authorization':f'Bearer {l}'})
    rp1=rp.json()
    resp=rsp.json()
    resp2=resp1.json()
    for i in range(len(resp2)):
        if(resp2[i]['roll']==roll):
            val=resp2[i]
            global semail
            semail=resp2[i]['email']
    for i in range(len(resp)):
        if(resp[i]['Aid']==j):
            value=resp[i]
    for i in range(len(rp1)):
                if(rp1[i]['Aid']==j):
                    global valname
                    valname=rp1[i]['fname']
    
    return render(request,'complaintdetails.html',{'value':value,'val':val,'valname':valname,'cid':cid})
def home4(request):
    if(request.method)=="POST":
        message=request.POST['message']
    det={'cid':cid,'roll':roll,'message':message}
    resp1=requests.get("https://antirag-api.herokuapp.com/student-details",det,headers = {'Authorization':f'Bearer {l}'})
    rp=requests.post("https://antirag-api.herokuapp.com/send-message",det,headers = {'Authorization':f'Bearer {l}'})

    rp1=rp.json()
    for i in range(len(resp1.json())):
        if(resp1.json()[i]['roll']==roll):
            semail=resp1.json()[i]['email']
    email=EmailMessage('Message from '+valname,message,settings.EMAIL_HOST_USER,[semail])
    email.fail_silently=False
    email.send()    
    return render(request,'registration/helloworld.html')

