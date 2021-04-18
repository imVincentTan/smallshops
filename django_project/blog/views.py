from django.http import HttpResponse
from django.views import View

from django.shortcuts import (
    render,
    get_object_or_404
)
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    UserPassesTestMixin
)
from django.contrib.auth.models import User
from django.views.generic import (
    ListView, 
    DetailView, 
    CreateView,
    UpdateView,
    DeleteView
)
from .models import Post
from .context_processors import tags_processor
# from .forms import SearchForm, TagSearchForm
from django import forms

# class BaseView():
#     tags = Tag.objects.all()

# def base(render):
#     context = {
#         'tags' : Tag.objects.all()
#     }
#     return render(request, 'blog/base.html', context)

# handle home page of the blog
def home(request):
    # if request.method == 'GET':
    #     search = request.GET.get('search')
    #     context = {
    #         'posts': Post.objects.filter(description__icontains=search)
    #     }
    # else:
    context = {
        'posts': Post.objects.all()
    }
    return render(request, 'blog/home.html', context)



class PostListView(ListView):
    # class SearchForm(forms.Form):
    #     search = forms.CharField(label='search', max_length=100, initial=request.GET['search'])
    #     tag_search = forms.CharField(label='tag search', max_length=100, initial=request.GET['search'])

    # class TagSearchForm(forms.Form):
    #     search = forms.CharField(label='search', max_length=100, initial=request.GET['search'])
    #     tag_search = forms.CharField(label='tag search', max_length=100, initial=request.GET['search'])
    
    model = Post
    template_name = 'blog/home.html'    # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 5

    

    # def get_queryset(self):
    def get(self, request, *args, **kwargs):

        city_search = request.GET.get('city_search')
        search = request.GET.get('search')
        tag_search = request.GET.get('tag_search')
        tag_filter = request.GET.getlist('selected_tag')
        remove_tags = request.GET.getlist('remove_tag')

        # remove tags from tag filter
        tag_filter = list(set(tag_filter))
        remove_tags = set(remove_tags)

        for ind, a in enumerate(tag_filter):
            if a in remove_tags:
                tag_filter[ind] = None
        
        tag_filter = list(filter(None, tag_filter))

        # instantiate context 
        context = {
            'posts': Post.objects.all(),
            'messages': [request.GET],
            'has_search_parameters': False
        }
        
        # filter posts by city
        if city_search:
            context['posts'] = context['posts'].filter(city__icontains=city_search)
            if not context['posts']:
                if 'messages' in context:
                    context['messages'].append('Sorry. No post with your search query was found.')
                else:
                    context['messages'] = ['Sorry. No post with your search query was found.']
            else:
                context['has_search_parameters'] = True

        # filter posts by search
        if search:
            context['posts'] = context['posts'].filter(description__icontains=search)
            # context['posts'] = Post.objects.filter(description__icontains=search)
            if not context['posts']:
                if 'messages' in context:
                    context['messages'].append('Sorry. No post with your search query was found.')
                else:
                    context['messages'] = ['Sorry. No post with your search query was found.']
            else:
                context['has_search_parameters'] = True
            
        # search for tag
        if tag_search:
            context['tag_search'] = tags_processor(request)['tags'].filter(name__icontains=tag_search)
            if not context['tag_search']:
                if 'messages' in context:
                    context['messages'].append('Sorry. No post with a similar tag was found.')
                else:
                    context['messages'] = ['Sorry. No post with a similar tag was found.']
            
        # filter posts by tags
        if tag_filter:
            context['posts'] = context['posts'].filter(tags__name__in=tag_filter)
            if not context['posts']:
                if 'messages' in context:
                    context['messages'].append('Sorry. No post with your search query was found.')
                else:
                    context['messages'] = ['Sorry. No post with your search query was found.']
            else:
                context['has_search_parameters'] = True

        if tag_filter:
            context['tag_filter'] = tag_filter

        return render(request, self.template_name, context)



class UserPostListView(ListView):
    model = Post
    template_name = 'blog/user_posts.html'    # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')

class PostDetailView(DetailView):
    model = Post

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['business_name', 'country', 'state_or_province', 'city', 'address', 'additional_address_info', 'description', 'contact_email', 'tags']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['business_name', 'country', 'state_or_province', 'city', 'address', 'additional_address_info', 'description', 'contact_email', 'tags']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author

def about(request):
    context = {
        'title': 'About'
    }
    return render(request, 'blog/about.html', context)