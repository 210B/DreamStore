from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from .models import Dream, Producer
# Create your views here.


class DreamList(ListView):
    model = Dream
    ordering = '-pk'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(DreamList, self).get_context_data()
        context['producer'] = Producer.objects.all()
        context['no_producer_dream_count'] = Dream.objects.filter(producer=None).count
        return context
    # 템플릿은 모델명_list.html : dream_list.html
    # 매개변수 모델명_list : dream_list


class DreamDetail(DetailView):
    model = Dream

    def get_context_data(self, **kwargs):
        context = super(DreamDetail, self).get_context_data()
        context['producer'] = Producer.objects.all()
        context['no_producer_dream_count'] = Dream.objects.filter(producer=None).count
        return context

    # 템플릿은 모델명_detail.html : dream_detail.html
    # 매개변수 모델명 : dream