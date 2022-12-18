from django.shortcuts import render, redirect
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


class DreamUpdate(LoginRequiredMixin,UpdateView):
    model = Dream
    fields = ['name', 'description', 'product_image', 'distributor', 'producer', 'themes']
    template_name = 'dream/dream_update_form.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_superuser or self.request.user.is_staff:
            return super(DreamUpdate, self).dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied

    def form_valid(self, form):
        response = super(DreamUpdate, self).form_valid(form)
        self.object.themes.clear()
        themes_str = self.request.POST.get('themes_str')
        if themes_str:
            themes_str = themes_str.strip()
            themes_str = themes_str.replace(',', ';')
            theme_list = themes_str.split(';')
            for t in theme_list:
                t = t.strip()
                theme, is_theme_created = Theme.objects.get_or_create(name=t)
                if is_theme_created:
                    theme.slug = slugify(t, allow_unicode=True)
                    theme.save()
                self.object.themes.add(theme)
        return response

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(DreamUpdate, self).get_context_data()
        if self.object.themes.exists:
            themes_str_list = list()
            for t in self.object.themes.all():
                themes_str_list.append(t.name)
            context['themes_str_default'] = ';'.join(themes_str_list)
        context['producer'] = Producer.objects.all()
        return context


class DreamCreate(LoginRequiredMixin,UserPassesTestMixin,CreateView):
    model = Dream
    fields = ['name', 'description', 'product_image', 'distributor', 'producer', 'themes']
    # 모델명_form.html

    def test_func(self):
        return self.request.user.is_superuser or self.request.user.is_staff

    def form_valid(self, form):
        current_user = self.request.user
        if current_user.is_superuser or current_user.is_staff:
            form.instance.author = current_user
            response = super(DreamCreate, self).form_valid(form)
            themes_str = self.request.POST.get('themes_str')
            if themes_str:
                themes_str = themes_str.strip()
                themes_str = themes_str.replace(',', ';')
                theme_list = themes_str.split(';')
                for t in theme_list:
                    t = t.strip()
                    theme, is_theme_created = Theme.objects.get_or_create(name=t)
                    if is_theme_created:
                        theme.slug = slugify(t, allow_unicode=True)
                        theme.save()
                    self.object.themes.add(theme)
            return response
        else:
            return redirect('/blog/')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(DreamCreate, self).get_context_data()
        context['producers'] = Producer.objects.all()
        return context


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
