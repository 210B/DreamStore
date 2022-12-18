from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from .models import Dream, Producer, Theme
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from django.utils.text import slugify

from django.shortcuts import get_object_or_404
from django.db.models import Q
# Create your views here.


#class HomeList(ListView):
#    model = Dream
#    ordering = '-pk'
#    paginate_by = 3

#    def get_context_data(self, *, object_list=None, **kwargs):
#        context = super(HomeList, self).get_context_data()
#        context['producer'] = Producer.objects.all()
#        context['no_producer_dream_count'] = Dream.objects.filter(producer=None).count
#        return context


class DreamList(ListView):
    model = Dream
    ordering = '-pk'
    paginate_by = 9

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
        dream_list = Dream.objects.filter(Q(name__contains=q) | Q(producer__name__contains=q) | Q(themes__name__contains=q)).distinct()
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


def producer_page(request,slug):
    producer = Producer.objects.get(slug=slug)
    dream_list = Dream.objects.filter(producer=producer)

    return render(request, 'dream/dream_list.html', {
        'producer': producer,
        'dream_list': dream_list,
        'producers': Producer.objects.all(),
    })


def theme_page(request, slug):
    theme = Theme.objects.get(slug=slug)
    dream_list = theme.dream_set.all()
    return render(request, 'dream/dream_list.html', {
        'theme': theme,
        'dream_list': dream_list,
        'no_producer_dream_count': Dream.objects.filter(producer=None).count
    })


def home_page(request):
    dream_list = Dream.objects.all().order_by('-pk')[:3]
    context = {
        'dream_list':dream_list,
    }
    return render(request, 'dream/dream_list.html', context)
