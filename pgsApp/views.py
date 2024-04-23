from django.shortcuts import redirect, render
import json
from django.contrib import messages
from django.contrib.auth.models import User
from django.http import HttpResponse
from pgsApp import models, forms
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required



def context_data():
    context = {
        'page_name' : '',
        'page_title' : '',
        'system_name' : 'Photo Gallery System',
        'topbar' : True,
        'footer' : True,
    }

    return context
    
def userregister(request):
    context = context_data()
    context['topbar'] = False
    context['footer'] = False
    context['page_title'] = "User Registration"
    if request.user.is_authenticated:
        return redirect("home-page")
    return render(request, 'register.html', context)

@login_required
def upload_modal(request):
    context = context_data()
    return render(request, 'upload.html', context)


def save_register(request):
    resp={'status':'failed', 'msg':''}
    if not request.method == 'POST':
        resp['msg'] = "No data has been sent on this request"
    else:
        form = forms.SaveUser(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Your Account has been created succesfully")
            resp['status'] = 'success'
        else:
            for field in form:
                for error in field.errors:
                    if resp['msg'] != '':
                        resp['msg'] += str('<br />')
                    resp['msg'] += str(f"[{field.name}] {error}.")
            
    return HttpResponse(json.dumps(resp), content_type="application/json")


@login_required
def update_profile(request):
    context = context_data()
    context['page_title'] = 'Update Profile'
    user = User.objects.get(id = request.user.id)
    if not request.method == 'POST':
        form = forms.UpdateProfile(instance=user)
        context['form'] = form
        print(form)
    else:
        form = forms.UpdateProfile(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile has been updated")
            return redirect("profile-page")
        else:
            context['form'] = form
            
    return render(request, 'manage_profile.html',context)


@login_required
def update_password(request):
    context =context_data()
    context['page_title'] = "Update Password"
    if request.method == 'POST':
        form = forms.UpdatePasswords(user = request.user, data= request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"Your Account Password has been updated successfully")
            update_session_auth_hash(request, form.user)
            return redirect("profile-page")
        else:
            context['form'] = form
    else:
        form = forms.UpdatePasswords(request.POST)
        context['form'] = form
    return render(request,'update_password.html',context)


# Create your views here.
def login_page(request):
    context = context_data()
    context['topbar'] = False
    context['footer'] = False
    context['page_name'] = 'login'
    context['page_title'] = 'Login'
    return render(request, 'login.html', context)

def login_user(request):
    logout(request)
    resp = {"status":'failed','msg':''}
    username = ''
    password = ''
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                resp['status']='success'
            else:
                resp['msg'] = "Incorrect username or password"
        else:
            resp['msg'] = "Incorrect username or password"
    return HttpResponse(json.dumps(resp),content_type='application/json')

@login_required
def home(request):
    context = context_data()
    context['page'] = 'home'
    context['page_title'] = 'Home'
    context['uploads'] = models.Gallery.objects.filter(delete_flag = 0, user = request.user).count()
    context['trash'] = models.Gallery.objects.filter(delete_flag = 1, user = request.user).count()
    print(context)
    return render(request, 'home.html', context)

def logout_user(request):
    logout(request)
    return redirect('login-page')
    
@login_required
def profile(request):
    context = context_data()
    context['page'] = 'profile'
    context['page_title'] = "Profile"
    return render(request,'profile.html', context)

@login_required
def save_upload(request):
    resp ={'status':'failed', 'msg':''}
    if not request.method == 'POST':
        resp['msg'] = "No data has been sent on this request"
    else:
        form = forms.SaveUpload(request.POST, request.FILES)
    if form.is_valid():
        form.save()
        messages.success(request, "New Upload has been save succesfully.")
        resp['status'] = 'success'
    else:
        for field in form:
            for error in field.errors:
                    if resp['msg'] != '':
                        resp['msg'] += str('<br />')
                    resp['msg'] += str(f"[{field.name}] {error}.")
    return HttpResponse(json.dumps(resp), content_type="application/json")

@login_required
def view_gallery(request):
    context = context_data()
    context['page_title'] ="Gallery"
    context['photos'] = models.Gallery.objects.filter(user = request.user, delete_flag = 0).all()
    return render(request, 'gallery.html', context) 

@login_required
def view_trash(request):
    context = context_data()
    context['page_title'] ="Trashed Images"
    context['photos'] = models.Gallery.objects.filter(user = request.user, delete_flag = 1).all()
    return render(request, 'trash.html', context) 

@login_required
def trash_upload(request, pk =None):
    resp = {'status':'failed', 'msg':''}
    if pk is None:
        resp['msg'] = 'No data sent in this request'
    else:
        try:
            upload = models.Gallery.objects.filter(id=pk).update(delete_flag = 1)
            resp['status'] = 'success'
            messages.success(request, 'Image has been moved to trash successfully')
        except:
            resp['msg'] = 'Invalid data to delete'
    return HttpResponse(json.dumps(resp), content_type="application/json")

@login_required
def restore_upload(request, pk =None):
    resp = {'status':'failed', 'msg':''}
    if pk is None:
        resp['msg'] = 'No data sent in this request'
    else:
        try:
            upload = models.Gallery.objects.filter(id=pk).update(delete_flag = 0)
            resp['status'] = 'success'
            messages.success(request, 'Image has been restore successfully')
        except:
            resp['msg'] = 'Invalid data to delete'
    return HttpResponse(json.dumps(resp), content_type="application/json")

@login_required
def delete_upload(request, pk =None):
    resp = {'status':'failed', 'msg':''}
    if pk is None:
        resp['msg'] = 'No data sent in this request'
    else:
        try:
            upload = models.Gallery.objects.get(id=pk).delete()
            resp['status'] = 'success'
            messages.success(request, 'Image has been deleted forever successfully')
        except:
            resp['msg'] = 'Invalid data to delete'
    return HttpResponse(json.dumps(resp), content_type="application/json")
    
