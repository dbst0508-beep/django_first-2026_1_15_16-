import datetime
from django.http import HttpResponse, JsonResponse
from django.utils import timezone
from django.views import generic

from .models import Question

def parse_yyyy_mm_dd(value: str):
    """
    'YYYY-MM-DD' → date로 변환
    실패하면 None
    """
    try:
        return datetime.date.fromisoformat(value)
    except (TypeError, ValueError):
        return None


def practice_1(request):
    q = request.GET.get("q") #q라는 파라미터 값을 읽어옴
    return HttpResponse(f"q는 지금: {q}")

def practice_api_1(request):
    q = request.GET.get("q")
    return JsonResponse({"q": q}) # 딕셔너리 구조로 json이 읽을 수 있게 변환

def practice_2(request):
    qs = Question.objects.all()#Question 모델에 모든 데이터를 긁어옴
    q = request.GET.get("q")#q라는 이름의 파라미터 값을 읽어옴

    #만약 q가 있다면 qs= 질문 목록을 대소문자 상관없이 q에 저장 화면에는 q의 질문목록과 질문 개수를 보여줌
    if q: 
        qs = qs.filter(question_text__icontains=q)
        return HttpResponse(f"검색어: {q}/결과 개수 :{qs.count()}")

def practice_api_2(request):
    qs = Question.objects.all()
    q = request.GET.get("q")

    if q:
        qs = qs.filter(question_text__icontains=q)

    #json이 읽을 수 있게 질문,질문의 개수 results: 이 후 10까지의 데이터의 id와 질문을 보여줌 
    return JsonResponse({
        "q" : q,
        "count" : qs.count(),
        "results":[{"id":x.id,"text": x.question_text}for x in qs[:10]]
    })

def practice_3(request):
    qs = Question.objects.all()
    show = request.GET.get("show") #show가 포함되 파라미터를 읽어옴

    if show != "future": #읽어온 파라미터가 미래에 작성된 글이 아니라면
        qs = qs.filter(pub_date__lte=timezone.now())#발행일 보다 과거 또는 같은 발행일을 가져와라
    return HttpResponse(f"show={show}/ 결과:{qs.count()}")#현재 발행일의 개수와 과거 발행일의 개수를 화면에 띄워줌

def practice_api_3(request):
    qs = Question.objects.all()
    show = request.GET.get("show")
    if show != "future":
        qs = qs.filter(pub_date__lte=timezone.now())
    
    #json 데이터로 읽을 수 있게 바꿔주면서 results: 이 후 qs쿼리의 10개까지의 데이터의 id와 질문을 보여줌
    return JsonResponse({ 
        "show":show,
        "count":qs.count(),
        "results":[{"id":x.id,"text":x.question_text}for x in qs[:10]]
    })

def practice_5(request):
    qs = Question.objects.all()

    start_raw = request.GET.get("start") #start 파라미터와 end 파라미터가 담긴 데이터를 읽어옴
    end_raw = request.GET.get("end")
    #start_raw,end_raw의 년-월-일을 date로 변환
    start = parse_yyyy_mm_dd(start_raw)
    end = parse_yyyy_mm_dd(end_raw)

    if start: #start의 쿼리셋이 있다면 현재 발행일 보다 크거나 같은 데이터를 가져옴
        qs = qs.filter(pub_date__date__gte=start)
    
    if end: #end의 쿼리셋이 있다면 현재 발행일 보다 작거나 같은 데이터를 가져옴
        qs = qs.filter(pub_date__date__lte=end)

    return HttpResponse(f"start = {start} end={end}/ 결과 : {qs.count()}")

def practice_api_5(request):
    qs = Question.objects.all()#Question 모델안 모든 데이터를 긁어옴
    start_raw = request.GET.get("start") 
    end_raw = request.GET.get("end")

    start = parse_yyyy_mm_dd(start_raw)
    end = parse_yyyy_mm_dd(end_raw)

    if start:
        qs = qs.filter(pub_date__date__gte=start)
    if end:
        qs = qs.filter(pub_date__date__lte=end)
    
    #json 데이터로 읽을 수 있게 변환 start_raw,end_raw의 파라미터를 읽음 
    #start,end의 날짜 데이터가 들어있을 경우 isoformat을 이용해 json이 읽을 수 있게 변환, 데이터가 없을경우 none
    return JsonResponse({
        "start_raw": start_raw,
        "end_raw":end_raw,
        "start": start.isoformat() if start else None,
        "end" : end.isoformat() if end else None,
        "count":qs.count(),
    })

def practice_6 (request):
    qs = Question.objects.all()
    order = request.GET.get("order") #order 파라미터가 포함된 데이터를 읽어옴

    if order == "oldset": #?order == oldset일 경우 
        qs = qs.order_by("pub_date") # qs 데이터는 오름차순
    else:
        qs = qs.order_by("-pub_date") # 아닐경우 내림차순
    
    first = qs.first() # qs의 첫 번째 데이터
    return HttpResponse(f"order={order}/첫 데이터 : {first.pub_date if first else None}")#첫번째 데이터의 발행일이 없을 경우 none

def practice_api_6(request):
    qs = Question.objects.all()
    order = request.GET.get("order")

    if order == "oldset":
        qs = qs.order_by("pub_date")
    else: 
        qs = qs.order_by("-pub_date")

    #json으로 읽을 수 있게하며 데이터가 있을 경우 첫 번째 데이터의 발행일을 국제표준시간으로 변경 후 띄워줌 이후 정렬 한 순서에 맞게 5개까지의 데이터를 보여줌
    return JsonResponse({
        "order":order,
        "first_pub_date": qs.first().pub_date.isoformat() if qs.exists()
        else None,
            "results":[{"id":x.id,"pub_date":x.pub_date.isoformat()}for x in qs[:5]]
    })