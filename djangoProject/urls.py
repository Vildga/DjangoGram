"""
URL configuration for djangoProject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from djangoProject import settings
from django.conf.urls.static import static
from DjangoGramm import views

urlpatterns = [
    path('', views.recommendations, name='recommendations'),
    path('registration/', views.register, name='registration'),
    path('login/', views.user_login, name='login'),
    path('upload/', views.upload, name='upload'),
    path('post/<int:post_id>', views.post_detail, name='post_detail'),
    path('profile/<str:login>/', views.profile, name='profile'),
    path('logout/', views.logout_view, name='logout'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('save_profile_changes/', views.save_profile_changes, name='save_profile_changes'),
    path('post/<int:post_id>/like/', views.like_post, name='like_post'),
    path('post/<int:post_id>/dislike/', views.dislike_post, name='dislike_post'),
    path('profile/<str:username>/following_list/', views.following_list, name='following_list'),
    path('follow/<str:login>/', views.follow_user, name='follow_user'),
    path('unfollow/<str:login>/', views.unfollow_user, name='unfollow_user'),
    # path('recommendations/', views.recommendations, name='recommendations'),
    path('subscriptions/', views.subscriptions, name='subscriptions'),
    path('social-auth/', include('social_django.urls', namespace='social')),
    path('admin/', admin.site.urls),

]


# urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
