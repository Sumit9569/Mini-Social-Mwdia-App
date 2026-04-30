import re
import requests
from urllib.parse import quote

from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from .models import Post, Comment
from .forms import PostForm


@login_required
def home(request):
    posts = Post.objects.filter(is_archived=False).order_by('-created_at')
    return render(request, 'home.html', {'posts': posts})


@login_required
def create_post(request):
    users = User.objects.exclude(id=request.user.id)

    locations = [
        "Gorakhpur, Uttar Pradesh",
        "Lucknow, Uttar Pradesh",
        "Noida, Uttar Pradesh",
        "Delhi, India",
        "Mumbai, Maharashtra",
        "Bangalore, Karnataka",
    ]

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)

        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('home')
    else:
        form = PostForm()

    return render(request, 'create_post.html', {
        'form': form,
        'users': users,
        'locations': locations,
    })


@login_required
def search_song(request):
    query = request.GET.get('q', '')
    results = []

    if query:
        url = "https://www.youtube.com/results?search_query=" + quote(query + " song")
        html = requests.get(url, timeout=5).text

        video_ids = re.findall(r"watch\?v=(\S{11})", html)
        unique_ids = list(dict.fromkeys(video_ids))[:8]

        for video_id in unique_ids:
            results.append({
                "title": query,
                "artist": "YouTube Music",
                "link": f"https://www.youtube.com/watch?v={video_id}"
            })

    return JsonResponse({"results": results})


@login_required
def like_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if request.user in post.likes.all():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)

    return redirect('home')


@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if request.method == 'POST':
        text = request.POST.get('text')

        if text:
            Comment.objects.create(post=post, user=request.user, text=text)

    return redirect('home')

@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id, author=request.user)
    post.delete()
    return redirect('profile', username=request.user.username)


@login_required
def archive_post(request, post_id):
    post = get_object_or_404(Post, id=post_id, author=request.user)
    post.is_archived = True
    post.save()
    return redirect('profile', username=request.user.username)