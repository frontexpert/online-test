from django.shortcuts import render, redirect
from admins.models import *
from django.http import JsonResponse
from django.core import serializers
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
import uuid
from django.conf import settings
import json

def is_admin_authenticated(request):
	if not request.user.is_authenticated:
		return 0
	else:
		is_superuser = request.user.is_superuser
		if is_superuser != 1:
			return 0

def get_login(request):
	return render(request, 'admins/login.html')

def index(request):
	if is_admin_authenticated(request) == 0:
		logout(request)
		return redirect(get_login)

	params = {
		'page_title': 'Dashboard'
	}
	return render(request, 'admins/index.html', params)

def post_login(request):
	email = request.POST.get('email')
	password = request.POST.get('password')
	auth_res = authenticate(request, email=email, password=password)
	if auth_res is not None:
		# getting group id of user
		try:
			is_superuser = User.objects.get(email=email).is_superuser
			if is_superuser == 1:
				ret = {
					'msg': 'ok'
				}
				login(request, auth_res)
			else:
				ret = {
					'msg': 'noadmin'
				}	
		except AttributeError:
			ret = {
				'msg': 'noadmin'
			}
	else:
		ret = {
			'msg': 'fail'
		}
	return JsonResponse(ret)

def adminlogout(request):
	logout(request)
	return redirect(get_login)

def list_subject(request):
	if is_admin_authenticated(request) == 0:
		logout(request)
		return redirect(get_login)

	subjects = Subject.objects.all()
	params = {
		'page_title': 'Subjects',
		'subjects': subjects
	}
	return render(request, 'admins/subject.html', params)

def create_subject(request):
	subject_name = request.POST.get('subject_name')
	subject = Subject(name=subject_name)
	subject.save()

	return redirect(list_subject)

def get_subject(request, subject_id):
	subject = Subject.objects.get(id=subject_id)
	rst = {
		'subject': serializers.serialize('json', [subject])
	}
	return JsonResponse(rst)

def edit_subject(request):
	subject_id = request.POST.get('subject_id')
	subject_name = request.POST.get('subject_name')

	subject = Subject.objects.get(id=subject_id)
	subject.name = subject_name
	subject.save()

	return redirect(list_subject)

def delete_subject(request):
	subject_id = request.POST.get('del_subject_id')
	subject = Subject.objects.get(id=subject_id)
	subject.delete()

	return redirect(list_subject)

def list_section(request):
	if is_admin_authenticated(request) == 0:
		logout(request)
		return redirect(get_login)

	sections = []
	subject_id = 0
	subjects = Subject.objects.all()
	if len(subjects) > 0:
		sections = Section.objects.filter(subject_id=subjects[0].id)
		subject_id = subjects[0].id

	params = {
		'page_title': 'Sections',
		'sections': sections,
		'subjects': subjects,
		'subject_id': subject_id
	}
	return render(request, 'admins/section.html', params)

def list_section_subject_id(request, subject_id):
	if is_admin_authenticated(request) == 0:
		logout(request)
		return redirect(get_login)
		
	subjects = Subject.objects.all()
	sections = Section.objects.filter(subject_id=subject_id)
	params = {
		'page_title': 'Sections',
		'sections': sections,
		'subjects': subjects,
		'subject_id': subject_id
	}
	return render(request, 'admins/section.html', params)

def create_section(request):
	subject_id = request.POST.get('subject_id')
	section_name = request.POST.get('section_name')
	section = Section(name=section_name, subject_id=subject_id)
	section.save()

	return redirect(reverse('list section subject id', kwargs={"subject_id": subject_id}))

def get_section(request, section_id):
	section = Section.objects.get(id=section_id)
	rst = {
		'section': serializers.serialize('json', [section])
	}
	return JsonResponse(rst)

def edit_section(request):
	subject_id = request.POST.get('subject_id')
	section_id = request.POST.get('section_id')
	section_name = request.POST.get('section_name')

	section = Section.objects.get(id=section_id)
	section.name = section_name
	section.save()

	return redirect(reverse('list section subject id', kwargs={"subject_id": subject_id}))

def delete_section(request):
	section_id = request.POST.get('del_section_id')
	subject_id = request.POST.get('subject_id')
	section = Section.objects.get(id=section_id)
	section.delete()

	return redirect(reverse('list section subject id', kwargs={"subject_id": subject_id}))

def list_question(request):
	if is_admin_authenticated(request) == 0:
		logout(request)
		return redirect(get_login)

	questions = Question.objects.all()
	params = {
		'page_title': 'Questions',
		'questions': questions
	}
	return render(request, 'admins/question.html', params)

def create_question(request):
	if is_admin_authenticated(request) == 0:
		logout(request)
		return redirect(get_login)

	subjects = Subject.objects.all()
	sections = []
	if len(subjects) > 0:
		sections = Section.objects.filter(subject_id=subjects[0].id)
	params = {
		'page_title': 'Questions',
		'subjects': subjects,
		'sections': sections
	}
	return render(request, 'admins/question_create.html', params)

def get_sections_by_subject_id(request, subject_id):
	sections = Section.objects.filter(subject_id=subject_id)
	ret = {
        'sections': serializers.serialize('json', sections)
    }

	return JsonResponse(ret)

def save_question(request):
	# saving question
	title = request.POST.get('title')
	subject_id = request.POST.get('subject')
	section_id = request.POST.get('section')
	ease_level = request.POST.get('ease_level')
	answer_type = request.POST.get('answer_type')
	explanation = request.POST.get('explanation')
	paths = []
	try:
		files = request.FILES.getlist('file')
		for f in files:
			filename = f._get_name()
			ext = filename[filename.rfind('.'):]
			file_name = str(uuid.uuid4()) + ext
			path = '/explanation_images/'
			full_path = str(path) + str(file_name)
			paths.append(full_path)
			fd = open('%s/%s' % (settings.STATICFILES_DIRS[0], str(path) + str(file_name)), 'wb')
			for chunk in f.chunks():
				fd.write(chunk)
			fd.close()
	except:
		paths = []
	path_list = json.dumps(paths)

	question = Question(title=title, subject_id=subject_id, section_id=section_id, qlevel=ease_level, answer_type=answer_type, explanation=explanation, path=path_list)
	question.save()

	# saving answer
	answer_list = request.POST.get('answers')
	answers = json.loads(answer_list)
	last_question = Question.objects.all().latest('id')
	last_question_id = last_question.id
	i = 1
	for answer in answers:
		if answer_type == 'single':
			correct_answer = request.POST.get('answer')
		else:
			name_str = "answer" + str(i)
			correct_answer = request.POST.get(name_str)
			i += 1

		if answer == correct_answer:
			ans = Answer(content=answer, question_id=last_question_id, correct_type=True)
		else:
			ans = Answer(content=answer, question_id=last_question_id, correct_type=False)
		ans.save()

	return redirect(create_question)

def edit_question(request, question_id):
	if is_admin_authenticated(request) == 0:
		logout(request)
		return redirect(get_login)

	question = Question.objects.get(pk=question_id)
	answers = Answer.objects.filter(question_id=question_id)
	subjects = Subject.objects.all()
	sections = Section.objects.filter(subject_id=question.subject_id)

	question.files = json.loads(question.path)

	if question.answer_type == "single":
		radiobox_idx = len(answers)
		checkbox_idx = 0
	else:
		checkbox_idx = len(answers)
		radiobox_idx = 0

	params = {
		'page_title': 'Questions',
		'subjects': subjects,
		'sections': sections,
		'question': question,
		'answers': answers,
		'radiobox_idx': radiobox_idx,
		'checkbox_idx': checkbox_idx
	}

	return render(request, 'admins/question_edit.html', params)

def update_question(request):
	question_id = request.POST.get('question_id')
	title = request.POST.get('title')
	subject_id = request.POST.get('subject')
	section_id = request.POST.get('section')
	ease_level = request.POST.get('ease_level')
	answer_type = request.POST.get('answer_type')
	explanation = request.POST.get('explanation')
	paths_json = request.POST.get('previous_imgs')
	paths = json.loads(paths_json)

	try:
		files = request.FILES.getlist('file')
		for f in files:
			filename = f._get_name()
			ext = filename[filename.rfind('.'):]
			file_name = str(uuid.uuid4()) + ext
			path = '/explanation_images/'
			full_path = str(path) + str(file_name)
			paths.append(full_path)
			fd = open('%s/%s' % (settings.STATICFILES_DIRS[0], str(path) + str(file_name)), 'wb')
			for chunk in f.chunks():
				fd.write(chunk)
			fd.close()
	except:
		print("occur exception")
	path_list = json.dumps(paths)

	question = Question.objects.get(pk=question_id)
	question.title = title
	question.subject_id = subject_id
	question.section_id = section_id
	question.qlevel = ease_level
	question.answer_type = answer_type
	question.explanation = explanation
	question.path = path_list
	question.save()

	# deleting old answers and saving new answers
	Answer.objects.filter(question_id=question_id).delete()

	answer_list = request.POST.get('answers')
	answers = json.loads(answer_list)
	i = 1
	for answer in answers:
		if answer_type == 'single':
			correct_answer = request.POST.get('answer')
		else:
			name_str = "answer" + str(i)
			correct_answer = request.POST.get(name_str)
			i += 1

		if answer == correct_answer:
			ans = Answer(content=answer, question_id=question_id, correct_type=True)
		else:
			ans = Answer(content=answer, question_id=question_id, correct_type=False)
		ans.save()
	return redirect(list_question)

def delete_question(request):
	question_id = request.POST.get('del_question_id')
	
	# deleting answers with this question
	Answer.objects.filter(question_id=question_id).delete()
	question = Question.objects.get(pk=question_id)
	question.delete()

	return redirect(list_question)

def list_paper(request):
	if is_admin_authenticated(request) == 0:
		logout(request)
		return redirect(get_login)

	papers = Paper.objects.all()

	params = {
		'page_title': 'Papers',
		'papers': papers
	}
	return render(request, 'admins/paper.html', params)

def create_paper(request):
	if is_admin_authenticated(request) == 0:
		logout(request)
		return redirect(get_login)

	subjects = Subject.objects.all()
	sections = []
	if len(subjects) > 0:
		sections = Section.objects.filter(subject_id=subjects[0].id)

	questions = Question.objects.filter(subject_id=subjects[0].id).filter(section_id=sections[0].id)
	params = {
		'page_title': 'Papers',
		'subjects': subjects,
		'sections': sections,
		'questions': questions
	}
	return render(request, 'admins/paper_create.html', params)

def get_questions(request):
	subject_id = request.POST.get('subject_id')
	section_id = request.POST.get('section_id')

	try:
		questions = Question.objects.filter(subject_id=subject_id).filter(section_id=section_id)
	except:
		questions = []

	ret = {
        'questions': serializers.serialize('json', questions)
    }

	return JsonResponse(ret)

def save_paper(request):
	# saving question
	paper_name = request.POST.get('paper_name')
	time_limit = request.POST.get('time_limit')
	subject_id = request.POST.get('subject')
	section_id = request.POST.get('section')
	
	questions = Question.objects.filter(subject_id=subject_id).filter(section_id=section_id)

	selected_question_ids = []
	for question in questions:
		selected_question = request.POST.get('q' + str(question.id))
		if selected_question is not None:
			selected_question_ids.append(selected_question)

	question_ids = json.dumps(selected_question_ids)

	paper = Paper(name=paper_name, time_limit=time_limit, subject_id=subject_id, section_id=section_id, question_ids=question_ids)
	paper.save()

	return redirect(create_paper)

def edit_paper(request, paper_id):
	if is_admin_authenticated(request) == 0:
		logout(request)
		return redirect(get_login)

	paper = Paper.objects.get(pk=paper_id)
	subjects = Subject.objects.all()
	sections = Section.objects.filter(subject_id=paper.subject_id)
	questions = Question.objects.filter(subject_id=paper.subject_id).filter(section_id=paper.section_id)
	for question in questions:
		if str(question.id) in json.loads(paper.question_ids):
			question.ischeck = 1

	params = {
		'page_title': 'Papers',
		'paper': paper,
		'subjects': subjects,
		'sections': sections,
		'questions': questions
	}

	return render(request, 'admins/paper_edit.html', params)

def update_paper(request):
	# saving question
	paper_id = request.POST.get('paper_id')
	paper_name = request.POST.get('paper_name')
	time_limit = request.POST.get('time_limit')
	subject_id = request.POST.get('subject')
	section_id = request.POST.get('section')
	
	questions = Question.objects.filter(subject_id=subject_id).filter(section_id=section_id)

	selected_question_ids = []
	for question in questions:
		selected_question = request.POST.get('q' + str(question.id))
		if selected_question is not None:
			selected_question_ids.append(selected_question)

	question_ids = json.dumps(selected_question_ids)

	paper = Paper.objects.get(pk=paper_id)
	paper.name = paper_name
	paper.time_limit = time_limit
	paper.subject_id = subject_id
	paper.section_id = section_id
	paper.question_ids = question_ids
	paper.save()

	return redirect(list_paper)

def delete_paper(request):
	paper_id = request.POST.get('del_paper_id')
	
	# deleting answers with this question
	paper = Paper.objects.get(pk=paper_id)
	paper.delete()

	return redirect(list_paper)

def index_schedule(request):
	if is_admin_authenticated(request) == 0:
		logout(request)
		return redirect(get_login)

	users = User.objects.all()
	subjects = Subject.objects.all()

	params = {
		'page_title': 'Schedules',
		'users': users,
		'subjects': subjects,
	}

	return render(request, 'admins/schedule.html', params)

def get_papers(request):
	user_id = request.POST.get('user_id')
	subject_id = request.POST.get('subject_id')

	unschedule_papers = []
	schedule_papers = []
	try:
		schedules = Schedule.objects.filter(user_id=user_id).filter(subject_id=subject_id)
		schedule_paper_ids = schedules.values_list('paper_id', flat=True)
		schedule_paper_ids = list(schedule_paper_ids)
		for schedule in schedules:
			schedule_paper_name = Paper.objects.get(pk=schedule.paper_id).name
			s = {}
			s['id'] = schedule.id
			s['paper_id'] = schedule.paper_id
			s['name'] = schedule_paper_name
			schedule_papers.append(s)
			
		papers = Paper.objects.filter(subject_id=subject_id)
		for paper in papers:
			if paper.id not in schedule_paper_ids:
				unschedule_papers.append(paper)
	except:
		schedule_papers = []
		unschedule_papers = []
	
	ret = {
        'schedule_papers': json.dumps(schedule_papers),
		'unschedule_papers': serializers.serialize('json', unschedule_papers),
    }

	return JsonResponse(ret)

def save_schedule(request):
	user_id = request.POST.get('users')
	subject_id = request.POST.get('subject')
	schedule_paper_ids = request.POST.get('schedule_paper_ids')
	schedule_papers = json.loads(schedule_paper_ids)

	Schedule.objects.filter(user_id=user_id).filter(subject_id=subject_id).delete()

	for paper_id in schedule_papers:
		schedule = Schedule(user_id=user_id, paper_id=paper_id, subject_id=subject_id)
		schedule.save()

	return redirect(index_schedule)
	