"""
URL configuration for code_tutors project.

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
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from tutorials.views import login_views
from tutorials.views import booking_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', login_views.home, name='home'),
    path('dashboard/', include([
        path('', login_views.dashboard, name='dashboard'),
        path('admin/', login_views.dashboard, name='admin_dashboard'),
        path('student/', login_views.dashboard, name='student_dashboard'),
        path('tutor/', login_views.dashboard, name='tutor_dashboard'),
        path('student/book_session', booking_views.create_booking, name='create_booking')
    ])),
    path('log_in/', login_views.LogInView.as_view(), name='log_in'),
    path('log_out/', login_views.log_out, name='log_out'),
    path('password/', login_views.PasswordView.as_view(), name='password'),
    path('profile/', login_views.ProfileUpdateView.as_view(), name='profile'),
    path('sign_up/', include([
        path('student/', login_views.StudentSignUpView.as_view(), name='student_sign_up'),
        path('tutor/', login_views.TutorSignUpView.as_view(), name='tutor_sign_up'),
    ]))
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
