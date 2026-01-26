from django.shortcuts import render, get_object_or_404
from .models import Question, Choice
from django.db.models import F
from django.urls import reverse_lazy,reverse
from django.http import HttpResponseRedirect
from django.views import generic
from django.utils import timezone
# # index(최신글 list)
# def index(request):
# 	# return HttpResponse("Hello) 기존코드	
# 	latest_question_list = Question.objects.order_by("-pub_date")[:5]
# 	context = {"latest_question_list": latest_question_list}
# 	return render(request, "polls/index.html", context)
class IndexView(generic.ListView):
    template_name = "polls/index.html" #이동할 위치
    context_object_name = "latest_question_list" #부를 이름 

    def get_queryset(self):
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by("-pub_date")[:5]


# def detail(request, question_id):
# 	question = get_object_or_404(Question, pk=question_id)
# 	return render(request, "polls/detail.html", {"question": question})
class DetailView(generic.DetailView):
    model = Question
    template_name = "polls/detail.html"
    context_object_name = "question"
    
    def get_queryset(self):
        """상세 페이지에서도 미래 날짜 질문은 404를 내도록 필터링"""
        return Question.objects.filter(pub_date__lte=timezone.now())


# def results(request, question_id):
#     question = get_object_or_404(Question, pk=question_id)
#     return render(request, "polls/results.html", {"question": question})
class ResultsView(generic.DetailView):
    model = Question
    template_name = "polls/results.html"
    context_object_name = "question"
    
	
# def vote(request, question_id):
#     return HttpResponse(f"You're voting on question {question_id}.")
def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST["choice"])
    except (KeyError, Choice.DoesNotExist):
        return render(
            request,
            "polls/detail.html",
            {
                "question": question,
                "error_message":"You didn't select a choice.",
            },
        )
    else:
        selected_choice.votes = F("votes") + 1
        selected_choice.save()
        return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))

# def aa_page(request):
#     all_questions = Question.objects.all()
#     return render(request, 'polls/aa.html', {'questions': all_questions})

#CRUD - Create
class QuestionCreateView(generic.CreateView):
    model = Question #Question 테이블을 모델로 
    fields = ["question_text","pub_date"] #Question테이블의 text,date 필드만 가져옴
    template_name = "polls/question_form.html" #경로는 question_form
    success_url = reverse_lazy("polls:index") #실행 후 돌아가는 페이지는 index

class QuestionUpdateView(generic.UpdateView):
    model = Question
    fields = ["question_text","pub_date"]
    template_name = "polls/question_form.html"
    success_url = reverse_lazy("polls:index")

class QuestionDeleteView(generic.DeleteView):
    model = Question
    template_name= "polls/question_confirm_delete.html"
    success_url = reverse_lazy("polls:index")
    #위 클래스엔 fields가 없어도 되는 이유 : 입력할게 없고 지우는 역할이라
    #따로 html에 기능만 만들어주면 됨