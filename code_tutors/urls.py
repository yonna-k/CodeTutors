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
from tutorials.views import login_views, booking_views, admin_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', login_views.home, name='home'),

    path('dashboard/', include([
        path('', login_views.dashboard, name='dashboard'),
        path('admin/', login_views.dashboard, name='admin_dashboard'),
        path('student/', login_views.dashboard, name='student_dashboard'),
        path('tutor/', login_views.dashboard, name='tutor_dashboard'),
    ])

    path('log_in/', login_views.LogInView.as_view(), name='log_in'),
    path('log_out/', login_views.log_out, name='log_out'),
    path('password/', login_views.PasswordView.as_view(), name='password'),
    path('profile/', login_views.ProfileUpdateView.as_view(), name='profile'),

    path('dashboard/student/', login_views.student_dashboard, name='student_dashboard'),
    path('dashboard/tutor/', login_views.tutor_dashboard, name='tutor_dashboard'),
    path('create-booking/', booking_views.create_booking, name='create_booking'),

    path('sign_up/', include([
        path('student/', login_views.StudentSignUpView.as_view(), name='student_sign_up'),
        path('tutor/', login_views.TutorSignUpView.as_view(), name='tutor_sign_up'),
    ])),

    path('manage/', include([   
        path('user/', admin_views.manage_users, name='manage_users'),
        path('student/', admin_views.manage_students, name='manage_students'),
        path('tutor/', admin_views.manage_tutors, name='manage_tutors'),
        path('booking/', admin_views.manage_bookings, name='manage_bookings'),
        path('lesson/', admin_views.manage_lessons, name='manage_lessons'),
    ])
     
    path('user/<int:id>/', admin_views.get_user, name='get_user'),
    path('student/<int:id>/', admin_views.get_student, name='get_student'),
    path('tutor/<int:id>/', admin_views.get_tutor, name='get_tutor'),
    path('booking/<int:id>/', admin_views.get_booking, name='get_booking'),
    path('lesson/<int:id>/', admin_views.get_lesson, name='get_lesson'),

    path('delete_user/<int:id>/', admin_views.delete_user, name='delete_user'),
    path('delete_student/<int:id>/', admin_views.delete_student, name='delete_student'),
    path('delete_tutor/<int:id>/', admin_views.delete_tutors, name='delete_tutor'),
    path('delete_booking/<int:id>/', admin_views.delete_booking, name='delete_booking'),
    path('delete_lesson/<int:id>/', admin_views.delete_lesson, name='delete_lesson'),

    path('update_user/<int:id>/', admin_views.update_user, name='update_user'),
    path('update_lesson/<int:id>/', admin_views.update_lesson, name='update_lesson'),
    path('update_booking/<int:id>/', admin_views.update_booking, name='update_booking'),

    path('dashboard/student/book_session', booking_views.create_booking, name='create_booking')

    path('dashboard/admin/<int:booking_id>/assign_tutor/', lesson_views.assign_tutor, name="assign_tutor")

]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)