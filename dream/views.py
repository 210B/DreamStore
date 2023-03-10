from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Dream, Producer, Theme, Comment, Distributor
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from django.utils.text import slugify
from .forms import CommentForm
from django.shortcuts import get_object_or_404
from django.db.models import Q
import random
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
    # ?????????_form.html

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
            return redirect('/dream/')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(DreamCreate, self).get_context_data()
        context['producers'] = Producer.objects.all()
        return context


class DreamList(ListView):
    model = Dream
    ordering = '-pk'
    paginate_by = 8

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(DreamList, self).get_context_data()
        context['producer'] = Producer.objects.all()
        context['no_producer_dream_count'] = Dream.objects.filter(producer=None).count
        return context
    # ???????????? ?????????_list.html : dream_list.html
    # ???????????? ?????????_list : dream_list


class DreamSearch(DreamList):
    paginate_by = None

    def get_queryset(self):
        q = self.kwargs['q']
        dream_list = Dream.objects.filter(Q(name__contains=q) | Q(producer__name__contains=q) |
                                          Q(themes__name__contains=q)).distinct()
        return dream_list

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(DreamSearch, self).get_context_data()
        q = self.kwargs['q']
        context['search_info'] = f'Search: {q} ({self.get_queryset().count()})'
        return context


def my_page(request):
    comment_list = Comment.objects.filter(author=request.user).order_by('-pk')
    context = {
        'comment_list':comment_list,
    }
    return render(request, 'dream/my_page.html', context)


class DreamDetail(DetailView):
    model = Dream

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        dream = get_object_or_404(Dream, pk=self.kwargs['pk'])
        related_list = Dream.objects.all().order_by('-pk')[:4]

        context = super(DreamDetail, self).get_context_data()
        context['related_list'] = related_list
        context['comment_form'] = CommentForm
        return context

   # def get_context_data(self, pk, *, object_list=None, **kwargs):
    #    dream = get_object_or_404(Dream, pk=pk)
     #   context = super(DreamDetail, self, pk).get_context_data()
      #  context['comment_form'] = CommentForm
       # return context


    # ???????????? ?????????_detail.html : dream_detail.html
    # ???????????? ????????? : dream


def new_comment(request,pk):
    if request.user.is_authenticated:
        dream = get_object_or_404(Dream,pk=pk)
        if request.method == 'POST':
            comment_form = CommentForm(request.POST)
            if comment_form.is_valid():
                comment = comment_form.save(commit=False)
                comment.dream = dream
                comment.author = request.user
                comment.save()
                return redirect(comment.get_absolute_url())
        else: # GET
            return redirect(dream.get_absolute_url())
    else: # ????????? ?????? ?????????
        raise PermissionDenied


def delete_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    dream = comment.dream
    if request.user.is_authenticated and request.user == comment.author:
        comment.delete()
        return redirect(dream.get_absolute_url())
    else:
        PermissionDenied


class CommentUpdate(LoginRequiredMixin,UpdateView):
    model = Comment
    form_class = CommentForm
    # ????????? : comment_form

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user == self.get_object().author:
            return super(CommentUpdate, self).dispatch(request, *args, **kwargs)


def producer_page(request, slug):
    producer = Producer.objects.get(slug=slug)
    dream_list = Dream.objects.filter(producer=producer)

    return render(request, 'dream/dream_list.html', {
        'producer': producer,
        'dream_list': dream_list,
        'producers': Producer.objects.all(),
    })


def distributor_page(request, slug):
    distributor = Distributor.objects.get(slug=slug)
    dream_list = Dream.objects.filter(distributor=distributor)

    return render(request, 'dream/dream_list.html', {
        'distributor': distributor,
        'dream_list': dream_list,
        'distributors': Distributor.objects.all(),
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

