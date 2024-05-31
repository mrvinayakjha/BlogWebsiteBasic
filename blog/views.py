from django.shortcuts import render, HttpResponseRedirect
from .forms import SignUpForm, LoginForm, BlogForm, OTPForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .models import Blog
from django.contrib.auth.models import Group
from django.core.mail import send_mail
from .otp_util import generate_otp, verify_otp

from .models import Post
from .utils import send_email

def post_detail(request, pk):
    # Your existing code

    if request.method == 'POST':
        # Your existing code

        # Send email notification to the post author
        subject = 'New Comment on Your Post'
        message = f'Hi {post.author.username},\n\nA new comment has been added to your post "{post.title}".\n\nRegards,\nYour Blog Team'
        recipient_list = [post.author.email]
        send_email(subject, message, recipient_list)

        return redirect('post_detail', pk=post.pk)


# Create your views here.
def home(request):
    blogs = Blog.objects.all()
    return render(request, 'blog/home.html', {'blogs': blogs})

def user_signup(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            messages.success(request, "CONGRATULATION, You are Registered!")
            user = form.save()
            group = Group.objects.get(name='Author')
            user.groups.add(group)
    else:
        form = SignUpForm()
    return render(request, 'blog/signup.html', {'form': form})

def user_login(request):
    if not request.user.is_authenticated:
        if request.method == "POST":
            form = LoginForm(request=request, data=request.POST)
            if form.is_valid():
                uname = form.cleaned_data['username']
                pwd = form.cleaned_data['password']
                user = authenticate(username=uname, password=pwd)
                if user is not None:
                    otp = generate_otp(user)
                    send_mail(
                        'Your OTP Code',
                        f'Your OTP code is {otp}',
                        'from@example.com',
                        [user.email],
                        fail_silently=False,
                    )
                    request.session['otp_user_id'] = user.id
                    return HttpResponseRedirect('/otp-verify/')
        else:
            form = LoginForm()
        return render(request, 'blog/login.html', {'form': form})
    else:
        return HttpResponseRedirect('/dashboard/')

def otp_verify(request):
    if request.method == 'POST':
        form = OTPForm(request.POST)
        if form.is_valid():
            otp = form.cleaned_data['otp']
            user_id = request.session.get('otp_user_id')
            if user_id:
                user = user.objects.get(id=user_id)
                if verify_otp(user, otp):
                    login(request, user)
                    return HttpResponseRedirect('/dashboard/')
                else:
                    messages.error(request, 'Invalid OTP')
    else:
        form = OTPForm()
    return render(request, 'blog/otp_verify.html', {'form': form})

def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/')

def dashboard(request):
    if request.user.is_authenticated:
        blogs = Blog.objects.all()
        user = request.user
        full_name = user.get_full_name()
        gps = user.groups.all()
        return render(request, 'blog/dashboard.html', {'blogs': blogs, 'full_name': full_name, 'groups': gps})
    else:
        return HttpResponseRedirect('/login/')

def add_blog(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            form = BlogForm(request.POST)
            if form.is_valid():
                title = form.cleaned_data['title']
                cont = form.cleaned_data['cont']
                blg = Blog(title=title, cont=cont)
                blg.save()
                form = BlogForm()
        else:
            form = BlogForm()
        return render(request, 'blog/addblog.html', {'form': form})
    else:
        return HttpResponseRedirect('/login/')

def update_blog(request, id):
    if request.user.is_authenticated:
        if request.method == 'POST':
            pi = Blog.objects.get(pk=id)
            form = BlogForm(request.POST, instance=pi)
            if form.is_valid():
                form.save()
        else:
            pi = Blog.objects.get(pk=id)
            form = BlogForm(instance=pi)
        return render(request, 'blog/updateblog.html', {'form': form})
    else:
        return HttpResponseRedirect('/login/')

def delete_blog(request, id):
    if request.user.is_authenticated:
        if request.method == 'POST':
            pi = Blog.objects.get(pk=id)
            pi.delete()
            return HttpResponseRedirect('/dashboard/')
    else:
        return HttpResponseRedirect('/login/')

def about(request):
    return render(request, 'blog/about.html')

def contact(request):
    return render(request, 'blog/contact.html')
