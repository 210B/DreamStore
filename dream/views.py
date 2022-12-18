from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from .models import Dream, Producer
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from django.utils.text import slugify

from django.shortcuts import get_object_or_404
from django.db.models import Q
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


class DreamSearch(DreamList):
    paginate_by = None

    def get_queryset(self):
        q = self.kwargs['q']
        dream_list = Dream.objects.filter(Q(name__contains=q)).distinct()
        return dream_list

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(DreamSearch, self).get_context_data()
        q = self.kwargs['q']
        context['search_info'] = f'Search: {q} ({self.get_queryset().count()})'
        return context


class DreamDetail(DetailView):
    model = Dream

    def get_context_data(self, **kwargs):
        context = super(DreamDetail, self).get_context_data()
        context['producer'] = Producer.objects.all()
        context['no_producer_dream_count'] = Dream.objects.filter(producer=None).count
        return context

    # 템플릿은 모델명_detail.html : dream_detail.html
    # 매개변수 모델명 : dream