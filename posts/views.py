from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import Post
from .forms import PostForm, PostFilterForm

@login_required
def home(request):
    posts = Post.objects.all()
    form = PostFilterForm(request.GET)

    if form.is_valid():
        date_order = form.cleaned_data['date_order']
        media_type = form.cleaned_data['media_type']
        author = form.cleaned_data['author']
        search = form.cleaned_data['search']

        if date_order == 'oldest':
            posts = posts.order_by('created_at')
        else:
            posts = posts.order_by('-created_at')

        if media_type == 'text':
            posts = posts.filter(image='')
        elif media_type == 'image':
            posts = posts.exclude(image='')

        if author:
            posts = posts.filter(user__username__icontains=author)

        if search:
            posts = posts.filter(Q(content__icontains=search) | Q(user__username__icontains=search))

    context = {
        'posts': posts,
        'form': form,
    }
    return render(request, 'posts/home.html', context)

@login_required
def profile(request):
    posts = Post.objects.filter(user=request.user)
    form = PostFilterForm(request.GET)

    if form.is_valid():
        date_order = form.cleaned_data['date_order']
        media_type = form.cleaned_data['media_type']
        search = form.cleaned_data['search']

        if date_order == 'oldest':
            posts = posts.order_by('created_at')
        else:
            posts = posts.order_by('-created_at')

        if media_type == 'text':
            posts = posts.filter(image='')
        elif media_type == 'image':
            posts = posts.exclude(image='')

        if search:
            posts = posts.filter(content__icontains=search)

    context = {
        'posts': posts,
        'form': form,
    }
    return render(request, 'posts/profile.html', context)

@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            return redirect('home')
    else:
        form = PostForm()
    return render(request, 'posts/create_post.html', {'form': form})

@login_required
def edit_post(request, post_id):
    post = get_object_or_404(Post, id=post_id, user=request.user)
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = PostForm(instance=post)
    return render(request, 'posts/edit_post.html', {'form': form, 'post': post})

@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id, user=request.user)
    if request.method == 'POST':
        post.delete()
        return redirect('home')
    return render(request, 'posts/delete_post.html', {'post': post})