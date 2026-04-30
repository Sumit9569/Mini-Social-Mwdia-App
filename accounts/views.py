import random
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from .models import OTP, Profile, Follow
from .forms import ProfileForm
from posts.models import Post


def register_view(request):
    error = None

    if request.method == 'POST':
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password != confirm_password:
            error = "Password and Confirm Password do not match."
            return render(request, 'register.html', {'error': error})

        otp = str(random.randint(100000, 999999))

        OTP.objects.create(email=email, otp=otp)

        print("YOUR OTP IS:", otp)

        request.session['email'] = email
        request.session['username'] = username
        request.session['password'] = password

        return redirect('verify_otp')

    return render(request, 'register.html')


def verify_otp(request):
    if request.method == 'POST':
        otp = request.POST.get('otp')
        email = request.session.get('email')

        otp_obj = OTP.objects.filter(email=email).last()

        if otp_obj and otp_obj.otp == otp:
            user = User.objects.create_user(
                username=request.session.get('username'),
                email=email,
                password=request.session.get('password')
            )

            Profile.objects.create(user=user)
            login(request, user)
            return redirect('home')

        return render(request, 'verify_otp.html', {'error': 'Invalid OTP'})

    return render(request, 'verify_otp.html')


def login_view(request):
    error = None

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            error = 'Invalid username or password'

    return render(request, 'login.html', {'error': error})


def logout_view(request):
    logout(request)
    return redirect('login')


@login_required
def profile_view(request, username):
    profile_user = get_object_or_404(User, username=username)
    profile, created = Profile.objects.get_or_create(user=profile_user)

    posts = Post.objects.filter(
        author=profile_user,
        is_archived=False
    ).order_by('-created_at')

    archived_posts = Post.objects.filter(
        author=profile_user,
        is_archived=True
    ).order_by('-created_at')

    followers_count = Follow.objects.filter(following=profile_user).count()
    following_count = Follow.objects.filter(follower=profile_user).count()

    is_following = Follow.objects.filter(
        follower=request.user,
        following=profile_user
    ).exists()

    return render(request, 'profile.html', {
        'profile_user': profile_user,
        'profile': profile,
        'posts': posts,
        'archived_posts': archived_posts,
        'followers_count': followers_count,
        'following_count': following_count,
        'is_following': is_following,
    })

@login_required
def edit_profile(request):
    profile, created = Profile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)

        if form.is_valid():
            form.save()
            return redirect('profile', username=request.user.username)
    else:
        form = ProfileForm(instance=profile)

    return render(request, 'edit_profile.html', {'form': form})


@login_required
def follow_user(request, username):
    following_user = get_object_or_404(User, username=username)

    if request.user != following_user:
        follow_obj = Follow.objects.filter(
            follower=request.user,
            following=following_user
        )

        if follow_obj.exists():
            follow_obj.delete()
        else:
            Follow.objects.create(
                follower=request.user,
                following=following_user
            )

    return redirect('profile', username=username)

    # 🔹 Forgot Password - send OTP
def forgot_password(request):
    error = None

    if request.method == 'POST':
        email = request.POST.get('email')

        if not User.objects.filter(email=email).exists():
            error = "Email not registered"
            return render(request, 'forgot_password.html', {'error': error})

        otp = str(random.randint(100000, 999999))
        OTP.objects.create(email=email, otp=otp)

        print("RESET OTP:", otp)

        request.session['reset_email'] = email

        return redirect('reset_password')

    return render(request, 'forgot_password.html')


# 🔹 Reset Password
def reset_password(request):
    error = None

    if request.method == 'POST':
        otp = request.POST.get('otp')
        password = request.POST.get('password')
        confirm = request.POST.get('confirm_password')

        email = request.session.get('reset_email')

        otp_obj = OTP.objects.filter(email=email).last()

        if not otp_obj or otp_obj.otp != otp:
            error = "Invalid OTP"
            return render(request, 'reset_password.html', {'error': error})

        if password != confirm:
            error = "Passwords do not match"
            return render(request, 'reset_password.html', {'error': error})

        user = User.objects.get(email=email)
        user.set_password(password)
        user.save()

        return redirect('login')

    return render(request, 'reset_password.html')