import json

from django.shortcuts import HttpResponse,render

def json_test_page(request):
    return render(request,'bookapp/json_test.html')

def json_dada(request):
    data = request.GET # <QueryDict:{'data': ['{"num":3,"items":["a","b","c","d"]}']}> <class 'django.http.request.QueryDict'>
    print(data,type(data))
    res = dict(data)['data'][0]  # 这一步比较烦
    print(type(res))
    print(json.loads(res),type(json.loads(res)))
    # data = json.loads(data,strict=False)
    # print(data)
    return HttpResponse(True)