from django.shortcuts import render,redirect,get_object_or_404
from basic_app.forms import UserForm, UserProfileInfoForm

from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponseRedirect,HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.views.generic import View, TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView
from . import models
from django.utils.decorators import method_decorator
from django.contrib.auth.models import User
import random

# Create your views here.
class IndexView(View):
    def get(self,request):
        #context_dict = {'text':'hello world', 'num':55}
        return render(request,'basic_app/index.html')

class HomeView(View):
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get(self,request):
        #context_dict = {'text':'hello world', 'num':55}
        #user = request.session.get('user')
        subject_list = models.Subject.objects.all()
        return render(request,'basic_app/home.html',{'subject_list':subject_list})

class LoginView(View):
    def post(self,request):
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(username=username,password=password)

        if user:
            if user.is_active:
                login(request,user)
                #return HttpResponseRedirect(reverse('index'))
                return redirect('/basic_app/home/',{'username':username})
            else:
                return render(request,'basic_app/login.html',{'loginError':"User Not Active !"})
                #return HttpResponse("User Not Active !")
        else:
            return render(request,'basic_app/login.html',{'loginError':"Invalid Login !"})
            #return HttpResponse("Invalid Login !")
    def get(self,request):
           
        if request.user.is_authenticated:
            return redirect('/basic_app/home/',{'username':request.user.username})
        else:
            return render(request,'basic_app/login.html',{})


class LogoutView(View):
    
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get(self,request):
        logout(request)
        return HttpResponseRedirect(reverse('index'))

class RegisterView(View):
    def post(self,request):
        registered = False
        user_form = UserForm(data = request.POST)
        profile_form = UserProfileInfoForm(data = request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            profile = profile_form.save(commit=False)
            profile.user = user            
            profile.save()
            registered = True
        else:
            print(user_form.errors,profile_form.errors)
        return render(request,'basic_app/registration.html',{'user_form':user_form,'profile_form':profile_form,'registered':registered})
    def get(self,request):        
        if request.user.is_authenticated:
            return redirect('/basic_app/home/',{'username':request.user.username})
        else:
            user_form = UserForm()
            profile_form = UserProfileInfoForm()
            return render(request,'basic_app/registration.html',{'user_form':user_form,'profile_form':profile_form,'registered':False})

class SubjectView(View):
    
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get(self,request, pk):
        
        subject = models.Subject.objects.filter(id=pk)
        topics_list = models.Topic.objects.filter(subject=pk)

        data = {
            'topics_list':topics_list,
            'subject' : subject
        }
        return render(request,'basic_app/subject.html',data)

class FrameView(View):
    
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get(self,request, sid, tid):
        
        frames_list = models.Frame.objects.filter(topic=tid)
        topic = models.Topic.objects.filter(id=tid)
        subject = models.Subject.objects.filter(id=sid)
        test = models.Test.objects.filter(topic=tid).exists()
        if test:
            user_test = models.TestResult.objects.filter(test=models.Test.objects.get(topic=tid)).filter(user=request.user.id).exists()
        else:
            user_test = False
        
        data = {
            'frames_list' : frames_list,
            'topic' : topic,
            'subject' : subject,
            'test' : test,
            'user_test' : user_test,
            'user' : request.user
        }
        return render(request,'basic_app/frames.html',data)

class TestView(View):
    
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get(self,request, sid, tid):
        data = dict()
        topic = models.Topic.objects.filter(id=tid)
        subject = models.Subject.objects.filter(id=sid)
        frames = models.Frame.objects.filter(topic=tid)
        data['topic'] = topic
        data['subject'] = subject
        test = models.Test.objects.filter(topic=tid)
        max_qns = 0
        for t in test: 
            max_qns = t.max_questions
                
        if test:
            valid_question_id_list = models.Question.objects.filter(frame__in=frames.all()).values_list('id', flat=True)
            random_question_id_list = random.sample(list(valid_question_id_list), min(len(valid_question_id_list),max_qns))
            question_list = models.Question.objects.filter(id__in=random_question_id_list)
            #question_list = models.Question.objects.filter(frame__in=frames.all())        
            
            data['question_list'] = question_list
            option_list = models.Option.objects.filter(question__in=question_list.all())
            data['option_list'] = option_list           
            answer_paper = models.TestResult.objects.filter(test=models.Test.objects.get(topic=tid)).filter(user=request.user.id)
            data['test_taken'] = models.TestResult.objects.filter(test=models.Test.objects.get(topic=tid)).filter(user=request.user.id).exists()
            data['answer_paper'] = answer_paper
        else:
            data["test_not_found"] = True

        return render(request,'basic_app/test.html',data)

    def post(self,request, sid, tid):
        if request.POST.get("numberOfQns"):
            for x in range(1,int(request.POST.get("numberOfQns"))+1):
                testAnswers = models.TestResult()
                testAnswers.user = get_object_or_404(User, id=request.user.id)
                testAnswers.test = get_object_or_404(models.Test, id=1)
                testAnswers.question = get_object_or_404(models.Question, id=request.POST.get("qn"+str(x)))
                testAnswers.user_answer = get_object_or_404(models.Option, id=request.POST.get("qn"+str(x)+"Ans"))
                testAnswers.save()
            return HttpResponse("Success")
        return render(request,'basic_app/test.html',{})

