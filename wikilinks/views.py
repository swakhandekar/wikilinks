from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from wikilinks.models  import MyUser,Question
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.contrib.auth import *
from django.contrib.auth import authenticate
from django.core.context_processors import csrf
import random
# Create your views here.
@csrf_exempt
def home(request):
	if request.method=="GET":
		return render(request,"wikilinks/LoginRegistrationForm/rulespage.html",{})

@csrf_exempt
def index(request):
	if request.method=="POST":
		if request.POST['submit']=="login":
			user = authenticate(username=request.POST['username'],password=request.POST['password'])
			if user is not None:
				if user.is_active:
					x= User.objects.get(username=user.get_username())
					m= MyUser.objects.get(user=x)
					if m.attempt_no>3:
						x.is_active= False
						return render(request,"index.html")
					x.level=1
					x.save()
					login(request,user)
					print request.user
					return question(request)

			return HttpResponse("INVALID ENTRY")
		else:
			if User.objects.filter(username= request.POST['usernamesignup']).exists():
				a={'message':'Username already exists!!','flag':True}
				return render(request,"index.html",a)
				
			if MyUser.objects.filter(user_receiptno=request.POST['youreceipt']).exists():
				a={'message':'Receipt number already exists!!','flag':True}
				return render(request,"index.html",a)

			else:
				user_name=request.POST.get('usernamesignup')
				user_password=request.POST.get('passwordsignup')
				user_receiptno=request.POST.get('youreceipt')
				userstatus=request.POST.get('submit')
				x = User.objects.create_user(username=user_name,password=user_password)
				user=authenticate(username=user_name,password=user_password)
				login(request,user)
				MyUser.objects.create(user_receiptno=user_receiptno,user_status=userstatus,user=x)
				login(request,x)
				#context={'question_start':question.objects.question_start,'question_end':question.objects.question_end}
				
				return question(request)
	else:
		return render(request,'index.html')
	
@csrf_exempt
def question(request):
	print request.user
	if request.user.is_authenticated():
		x = User.objects.filter(username=request.user)
		print x
		m = MyUser.objects.get(user=x)

		q = Question.objects.filter(question_level=m.level)
		l=[]
		for j in q:
			l.append(j)
			print j.question_start
		return HttpResponse("Done")

	else:
		return HttpResponse("Error")
