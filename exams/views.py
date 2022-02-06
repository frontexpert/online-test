from django.http import HttpResponseRedirect, JsonResponse
from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from django.core import serializers
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from datetime import datetime
from admins.models import *
from exams.models import *
import json

def loginn(request):
	email = request.POST.get('login_email')
	password = request.POST.get('login_password')
	user = authenticate(request, email=email, password=password)
	if user is not None:
		login(request, user)
	return HttpResponseRedirect(request.META['HTTP_REFERER'])

def logoutt(request):
	logout(request)
	return HttpResponseRedirect(request.META['HTTP_REFERER'])

def register(request):
	firstname = request.POST.get('first_name')
	lastname = request.POST.get('last_name')
	email = request.POST.get('email')
	password = request.POST.get('password')
	# saving user
	username = firstname + "." + lastname
	user = User(first_name=firstname, last_name=lastname, email=email, password=password, username=username)
	user.set_password(password)
	user.save()

	# authenticating user
	user = authenticate(request, email=email, password=password)
	if user is not None:
		login(request, user)
	# reloading current url
	return HttpResponseRedirect(request.META['HTTP_REFERER'])

def index(request):
	# if not request.user.is_authenticated:
	# 	return redirect('/login')
	return render(request, 'exams/index.html')

def contact(request):
	return render(request, 'exams/contact.html')

def membership(request):
	return render(request, 'exams/membership.html')

def exam_dashboard(request):
	if not request.user.is_authenticated:
		return redirect(reverse('login'))
	user_id = request.user.id

	scores = Score.objects.filter(user_id=user_id)
	passed_paper_ids = scores.values_list('paper_id', flat=True)
	passed_paper_ids = list(map(int, passed_paper_ids))

	schedules = Schedule.objects.filter(user_id=user_id).exclude(paper_id__in=passed_paper_ids)

	params = {
		'schedules': schedules,
		'scores': scores
	}

	return render(request, 'exams/exam_dashboard.html', params)

def exam_goto(request, schedule_id):
	if not request.user.is_authenticated:
		return redirect(reverse('login'))

	schedule = Schedule.objects.get(pk=schedule_id)

	params = {
		'schedule': schedule,
	}

	return render(request, 'exams/exam_splash.html', params)

def exam_start(request, schedule_id):
	if not request.user.is_authenticated:
		return redirect(reverse('login'))

	schedule = Schedule.objects.get(pk=schedule_id)
	question_ids =  json.loads(schedule.paper.question_ids)

	question = Question.objects.get(pk=int(question_ids[0]))
	answers = Answer.objects.filter(question_id=int(question_ids[0]))

	params = {
		'question': question,
		'answers': answers,
		'paper_id': schedule.paper_id,
		'time_limit': schedule.paper.time_limit
	}

	return render(request, 'exams/exam.html', params)
	
def exam_next_question(request):
	paper_id = request.POST.get('paper_id')
	question_id = request.POST.get('question_id')

	paper = Paper.objects.get(pk=paper_id)
	question_ids =  list(map(int, json.loads(paper.question_ids)))

	question = None
	answers = []
	for i in range(len(question_ids)-1):
		if int(question_id) == question_ids[i]:
			q_id = question_ids[i + 1]
			question = Question.objects.get(pk=q_id)
			answers = Answer.objects.filter(question_id=q_id)
	
	if question is not None:
		question = serializers.serialize('json', [question])

	params = {
		'question': question,
		'answers': serializers.serialize('json', answers),
		'paper_id': paper_id
	}

	return JsonResponse(params)

def exam_prev_question(request):
	paper_id = request.POST.get('paper_id')
	question_id = request.POST.get('question_id')

	paper = Paper.objects.get(pk=paper_id)
	question_ids =  list(map(int, json.loads(paper.question_ids)))

	question = None
	answers = []
	for i in range(1, len(question_ids)):
		if int(question_id) == question_ids[i]:
			q_id = question_ids[i - 1]
			question = Question.objects.get(pk=q_id)
			answers = Answer.objects.filter(question_id=q_id)
	
	if question is not None:
		question = serializers.serialize('json', [question])

	params = {
		'question': question,
		'answers': serializers.serialize('json', answers),
		'paper_id': paper_id
	}

	return JsonResponse(params)

def exam_submit(request):
	if not request.user.is_authenticated:
		return redirect(reverse('login'))

	paper_id = request.POST.get('paper_id')
	process = request.POST.get('process')
	questions = json.loads(process)

	correct_question_ids = []
	for question in questions:
		selected_ids = question['checked_ids']
		is_right = True
		for id in selected_ids:
			answer = Answer.objects.get(pk=int(id))
			if answer.correct_type == 0:
				is_right = False
				break
		
		if is_right:
			correct_question_ids.append(question['question_id'])
	
	attempt_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
	correct_ids = json.dumps(correct_question_ids)
	complete_terminate = True
	subject_id = Paper.objects.get(pk=paper_id).subject.id
	user_id = request.user.id

	score = Score (
		attempt_at=attempt_at, 
		correct_question_ids=correct_ids, 
		complete_terminate=complete_terminate, 
		paper_id=paper_id, 
		subject_id=subject_id, 
		user_id=user_id
	)
	score.save()

	last_score = Score.objects.all().latest('id')
	last_score_id = last_score.id
	for question in questions:
		process = Process (
			score_id = last_score_id,
			question_id = question['question_id'],
			user_answer_ids = json.dumps(question['checked_ids'])
		)
		process.save()

	paper = Paper.objects.get(pk=paper_id)
	paper_title = paper.name
	total_question_amount = len(json.loads(paper.question_ids))
	correct_question_amount = len(correct_question_ids)
	score = round(correct_question_amount / total_question_amount * 100, 2)
	params = {
		'paper_title': paper_title,
		'total_question_amount': total_question_amount,
		'correct_question_amount': correct_question_amount,
		'score': score
	}
	return render(request, 'exams/exam_result.html', params)

def exam_prompted(request, score_id):
	if not request.user.is_authenticated:
		return redirect(reverse('login'))

	paths = []

	score = Score.objects.get(pk=score_id)
	question_ids = list(map(int, json.loads(score.paper.question_ids)))
	questions = Question.objects.filter(id__in=question_ids)
	for question in questions:
		answers = Answer.objects.filter(question_id=question.id)
		for answer in answers:
			process = Process.objects.filter(score_id=score_id).filter(question_id=question.id)
			answer_ids = []
			if len(process) > 0:
				answer_ids = list(map(int, json.loads(process[0].user_answer_ids)))
			
			answer.background = ""
			if answer.id in answer_ids:
				answer.background = "bg-danger"

			if answer.correct_type == True:
				answer.background = "bg-info"
				
		question.answers = answers

		question.paths = json.loads(question.path)

	params = {
		'score': score,
		'questions': questions,
	}

	return render(request, 'exams/exam_prompted.html', params)