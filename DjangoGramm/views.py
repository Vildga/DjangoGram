from django.http import HttpResponseRedirect
from django.shortcuts import reverse, get_object_or_404
from .forms import UploadForm, RegistrationForm
from datetime import datetime
from django.core.files.storage import FileSystemStorage
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.contrib.auth import logout
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .models import Post, Like, Dislike, Following
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from djangoProject import settings
from django.db import transaction
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import require_POST
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse


def home(request):
    posts = Post.objects.all().order_by('-publication_date')

    context = {
        'posts': posts,
    }

    return render(request, 'home.html', context)


def post(request, post_id):
    try:
        post = Post.objects.get(id=post_id)
        return render(request, 'post.html', {'post': post})
    except Post.DoesNotExist:
        return render(request, 'post.html', {'post': None})


@login_required
def upload(request):
    if request.method == 'POST':
        form = UploadForm(request.POST, request.FILES)
        if form.is_valid():
            photo = form.cleaned_data['photo']
            description = form.cleaned_data['description']

            storage = FileSystemStorage(location=settings.MEDIA_ROOT)

            filename = storage.save(photo.name, photo)
            photo.name = filename

            current_user = request.user

            post = Post(
                count_likes=0,
                count_dislikes=0,
                description=description,
                publication_date=datetime.now(),
                images=photo,
                author_id=current_user,
            )
            post.save()

            return HttpResponseRedirect(reverse('post_detail', args=[post.id]))
        else:
            return render(request, 'upload.html', {'form': form})
    else:
        form = UploadForm()

    return render(request, 'upload.html', {'form': form})


def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    context = {
        'post': post,
    }

    return render(request, 'post_detail.html', context)


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.last_login = timezone.now()
            user.save()
            login(request, user)
            return HttpResponseRedirect(reverse('profile', args=[user.username]))
    else:
        form = RegistrationForm()

    return render(request, 'registration.html', {'form': form})


@login_required
def profile(request, login):
    user = User.objects.get(username=login)
    is_following = request.user.following.filter(following_user=user).exists()

    context = {
        'user': user,
        'is_following': is_following
    }
    return render(request, 'profile.html', context)


def user_login(request):
    if request.user.is_authenticated:
        messages.success(request, 'Ви вже увійшли до системи.')
        return redirect('recommendations')

    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('recommendations')
            else:
                messages.error(request, 'Неправильний логін чи пароль.')
    else:
        form = AuthenticationForm()

    context = {
        'form': form,
    }
    return render(request, 'login.html', context)


@login_required
def logout_view(request):
    logout(request)
    return redirect('login')


@login_required
def edit_profile(request):
    user = request.user
    context = {
        'user': user,
    }
    return render(request, 'edit_profile.html', context)


@login_required
def save_profile_changes(request):
    if request.method == 'POST':
        user = request.user

        user.first_name = request.POST.get('first_name', '')
        user.last_name = request.POST.get('last_name', '')
        user.email = request.POST.get('email', '')

        user.save()

        messages.success(request, 'Profile changes saved successfully.')

    return redirect('edit_profile')


@login_required
def like_post(request, post_id):
    with transaction.atomic():
        if request.method == 'POST':
            post = Post.objects.select_for_update().get(pk=post_id)

            if not Like.objects.filter(user=request.user, post=post).exists():
                like = Like.objects.create(user=request.user, post=post)

                post.count_likes += 1
                post.save()

                return JsonResponse({'status': 'success'})
            else:
                return JsonResponse({'status': 'error', 'message': 'You have already liked this post.'}, status=400)
        return JsonResponse({'status': 'error', 'message': 'Invalid method.'}, status=405)


@login_required
def dislike_post(request, post_id):
    with transaction.atomic():
        if request.method == 'POST':
            post = Post.objects.select_for_update().get(pk=post_id)

            if not Dislike.objects.filter(user=request.user, post=post).exists():
                dislike = Dislike.objects.create(user=request.user, post=post)

                post.count_dislikes += 1
                post.save()

                return JsonResponse({'status': 'success'})
            else:
                return JsonResponse({'status': 'error', 'message': 'You have already disliked this post.'}, status=400)
        return JsonResponse({'status': 'error', 'message': 'Invalid method.'}, status=405)


@login_required
def following_list(request, username):
    user = User.objects.get(username=username)
    following = user.following.all()
    return render(request, 'following_list.html', {'following': following})


@login_required
def follow_user(request, login):
    user_to_follow = get_object_or_404(User, username=login)

    if request.user == user_to_follow:
        messages.error(request, "Ви не можете підписатися на себе!")
        return JsonResponse({'status': 'error', 'message': 'Ви не можете підписатися на себе!'}, status=400)

    is_following = request.user.following.filter(following_user=user_to_follow).exists()

    if not is_following:
        Following.objects.create(follower=request.user, following_user=user_to_follow)
        return JsonResponse({'status': 'success', 'action': 'followed'})
    else:
        return JsonResponse({'status': 'success', 'action': 'unfollowed'})


@login_required
def unfollow_user(request, login):
    user_to_unfollow = get_object_or_404(User, username=login)

    if request.user == user_to_unfollow:
        messages.error(request, "Ви не можете відписатися від себе!")
        return JsonResponse({'status': 'error', 'message': 'Ви не можете відписатися від себе!'})

    is_following = request.user.following.filter(following_user=user_to_unfollow).exists()

    if not is_following:
        Following.objects.create(follower=request.user, following_user=user_to_unfollow).delete()
        return JsonResponse({'status': 'success', 'action': 'unfollowed'})
    else:
        return JsonResponse({'status': 'success', 'action': 'followed'})


@login_required
def recommendations(request):
    user_following_ids = request.user.following.values_list('following_user__id', flat=True)
    recommended_posts = Post.objects.exclude(author_id__in=user_following_ids).order_by('-publication_date')
    return render(request, 'recommendations.html', {'posts': recommended_posts})


@login_required
def subscriptions(request):
    user_following_ids = request.user.following.values_list('following_user__id', flat=True)
    subscribed_posts = Post.objects.filter(author_id__id__in=user_following_ids).order_by('-publication_date')
    return render(request, 'subscriptions.html', {'posts': subscribed_posts})

