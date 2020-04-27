from django.shortcuts import redirect,render,HttpResponse,get_object_or_404,HttpResponseRedirect,Http404
from .models import Post
from .forms import PostForm,CommentForm
from django.contrib import messages
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from django.utils.text import slugify
from django.db.models import Q
def home_page(request):
    #eger kullanıcıgiris yapmıssa
    content_home={'name':'Blog Ana Sayfasi',}
    return render(request,'home.html',content_home)

def index_page(request):
    posts_list = Post.objects.all()
    query = request.GET.get('q')
    if query:
        posts_list = posts_list.filter(
            Q(title__icontains=query)|
            Q(container__icontains=query)|
            Q(user__first_name__icontains=query)|
            Q(user__last_name__icontains=query)
        ).distinct()
    paginator = Paginator(posts_list,6)
    page = request.GET.get('page')

    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    return render(request, 'post/index.html', {'post_content':posts,})

def detail_page(request,slug):
    posts = get_object_or_404(Post,slug=slug)
    form_detail = CommentForm(request.POST or None)
    if form_detail.is_valid():
        comment  = form_detail.save(commit=False)
        comment.post = posts
        comment.save()
        return HttpResponseRedirect(posts.get_absolute_url())
    context={
        'post_content':posts,
        'form_content':form_detail,
    }
    return render(request, 'post/detail.html', context)

def create_page(request):
    #if not request.user.is_authenticated():
     #   return Http404()

    form_create = PostForm(request.POST or None,request.FILES or None)
    if form_create.is_valid():
        post=form_create.save(commit=False)#(commit=False
        post.user = request.user
        post.save()
        #post.slug = slugify(post.title.replace('ı','i'))
        #post.save()
        messages.success(request,"Basarili bir sekilde olusturuldu")
        return HttpResponseRedirect(post.get_absolute_url())

    context_form={'post_form':form_create,}
    return render(request, 'post/form.html', context_form)

def update_page(request,slug):
    if not request.user.is_authenticated():
        return Http404()
    post = get_object_or_404(Post,slug=slug)
    form = PostForm(request.POST or None, request.FILES or None ,instance=post)
    if form.is_valid():
        form.save()
        messages.success(request, "Basarili bir sekilde guncellendi")
        return HttpResponseRedirect(post.get_absolute_url())
    context_form = {'post_form': form, }
    return render(request, 'post/form.html', context_form)

def delete_page(request,slug):
    if not request.user.is_authenticated():
        return Http404()
    post = get_object_or_404(Post, slug=slug)
    post.delete()
    return redirect("post:index")