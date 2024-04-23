from django.contrib import admin
from django.urls import path,include
from . import views
from django.contrib.auth import views as auth_views
from django.views.generic.base import RedirectView

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('qr_code/', include('qr_code.urls', namespace="qr_code")),
    path('',views.home),
    path('login',views.login_page,name='login-page'),
    path('register',views.userregister,name='register-page'),
    path('save_register',views.save_register,name='register-user'),
    path('user_login',views.login_user,name='login-user'),
    path('home',views.home,name='home-page'),
    path('logout',views.logout_user,name='logout'),
    path('profile',views.profile,name='profile-page'),
    path('update_password',views.update_password,name='update-password'),
    path('update_profile',views.update_profile,name='update-profile'),
    path('upload_modal',views.upload_modal,name='upload-modal'),
    path('save_upload',views.save_upload,name='save-upload'),
    path('gallery',views.view_gallery,name='gallery-page'),
    path('trash',views.view_trash,name='trash-page'),
    path('trash_image/<int:pk>',views.trash_upload,name='trash-upload'),
    path('restore_image/<int:pk>',views.restore_upload,name='restore-upload'),
    path('delete_image/<int:pk>',views.delete_upload,name='delete-upload'),
]+ static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
