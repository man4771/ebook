import profile
from threading import _profile_hook
from urllib import request
from xml.dom.pulldom import default_bufsize
from django.conf import settings
from django.core.mail import send_mail 
from django.shortcuts import redirect, render
from .models import *
from random import randint

default_data = {
    'no__header_page' : ['login_page','register_page','otp_page'],
    'current_page' : None,
    'userrole' : UserRole.objects.all(),
    'gender_choice' : [],
}

for gc in gender_choices:
    default_data['gender_choice'].append({'short_text':gc[0],'text':gc[1]})

print(default_data['gender_choice'])
#[
 #   {
  #  'short_text' : 'm',
  #  'text' : 'f',
   # },
#]


def index(request):
    return redirect(login_page)
    #return render(request, 'index.html', default_data)

def login_page(request):
    default_data['current_page'] = 'login_page'
    return render(request, 'login_page.html', default_data)

def register_page(request):
    default_data['current_page'] = 'register_page'
    return render(request, 'register_page.html', default_data)

def profile_page(request):
    if 'email' in request.session: 
        default_data['current_page'] = 'profile_page'
    
        profile_data(request)
    
        return render(request, 'profile_page.html', default_data)
    
    return render(login_page)

    
def login(request):
    print(request.POST)
    
    try:
        master = Master.objects.get(
            Email = request.POST['email']
        )
        if master.Password == request.POST['password']:
            request.session['email'] = master.Email
            return redirect(profile_page)
        else:
            #alert('danger', 'incorrect password!')
            print('incorrect password')
        
    except Master.DoesNotExist as err:
        #alert('warning', 'your account is in active')
        print('record not founds')
        
    
    return redirect(login_page)

def register(request):
    print(request.POST)
    
    userrole = UserRole.objects.get(id=int(request.POST['userrole']))
    master = Master.objects.create(
        UserRole = request.POST['userrole'],
        Email = request.POST['email'],
        Password = request.POST['password'],
    )
    
    Profile.objects.create(
        Master = master,
    
    )
    return redirect(register_page)


def profile_data(request):
    master = Master.objects.get(Email = request.session['email'])
    profile = Profile.objects.get(Master = master)
    splitted_names = profile.FullName.split()
    profile.FirstName = splitted_names[0]
    
    if len(splitted_names) > 1:
        profile.LastName = splitted_names[1]

    default_data['profile_data'] = profile

def update_profile(request):
    master = Master.objects.get(Email = request.session['email'])
    profile = Profile.objects.get(Master = master)
    
    print('update data' , request.POST )

    profile.FullName = f"{request.POST['first_name']} {request.POST['last_name']}"
    profile.Gender = request.POST['gender']
    profile.BirthDate = request.POST['BirthDate']
    profile.Mobile = request.POST['mobile']
    profile.Country = request.POST['Country']
    profile.State = request.POST['State']
    profile.City = request.POST['city']
    profile.Pincode = request.POST['pincode']
    profile.Addresss = request.POST['addresss']

    profile.save()
    return redirect(profile_page)

from pathlib import Path

# upload profile image
def upload_image(request):
    master = Master.objects.get(Email = request.session['email'])
    profile = Profile.objects.get(Master = master)

    if 'profile_image' in request.FILES:
        image = request.FILES['profile_image']
        print('old name', image.name)
        image_type = image.name.split('.')[-1]
        new_name = master.Email.split('@')[0]
        old_name = profile.ProfileImage.name.split('/')[-1]
        image.name = f"{new_name}.{image_type}"
        print('new name', image.name)
        
        base_dir = Path(__file__).resolve().parent.parent
        image_path = Path.joinpath(settings.MEDIA_ROOT, f"profiles/{image.name}")

        print(image.name, old_name)
        
        print(image.name == old_name)
        
        if image.name == old_name:
            Path(image_path).unlink()
        
        profile.ProfileImage = image

        profile.save()

    return redirect(profile_page)

# remove profile photo
def remove_profile_image(request):
    master = Master.objects.get(Email = request.session['email'])
    profile = Profile.objects.get(Master = master)
    
    # print('image path: ', user.Image.url.split('/')[-1])
    upload_path = Path.joinpath(settings.MEDIA_ROOT, f"profiles/{profile.ProfileImage.url.split('/')[-1]}")
    Path(upload_path).unlink()
    
    profile.ProfileImage = ""
    profile.save()
    

    print('image removed.')
    default_data['image_uploaded'] = 'false'

    return redirect(profile_page)

# change password functionality
def change_password(request):
    master = Master.objects.get(Email = request.session['email'])

    if master.Password == request.POST['current_password']:
        master.Password = request.POST['new_password']
        master.save()
    else:
        print('incorrect current password.')

    return redirect(profile_page)

# logout
def logout(request):
    if 'email' in request.session:
        del request.session['email']
    return redirect(login_page)

def otp_page(request):
    default_data['current_page'] = 'otp_page'
    return render(request, 'otp_page.html', default_data)

def otp(request):
    otp_number = randint(1000, 9999)
    print('otp is :',otp_number)
    request.session['otp'] = otp_number

def send_otp(request,otp_for = 'reg'):
    otp(request)
    print(email , request.POST['email'])
    request.session['reg_data'] = {
      'email':request.POST['email'],
      'password':request.POST['password']
    }
    mail_of_list = [request.POST['email'],]   
    subject = f'otp for ebook registation'
    email_from =  settings.EMAIL_HOST_USER
    message = f"one time otp is : {request.session['otp']}."
    send_mail(subject,message,email_from,mail_of_list)
    
    return redirect(otp_page)

#verify otp 
def verify_otp(request, verify_for="register "):

    if request.session['otp'] == int(request.POST['otp']):

        if verify_for == 'activate':
            master = Master.objects.get(Email=request.session['reg_data']['email'])
            master.Password = request.session['reg_data']['password']
            master.IsActive = True
            master.save()


            return redirect(profile_page)
        elif verify_for == 'recover_pwd':
            master = Master.objects.get(Email=request.session['email'])
            master.Password = request.session['password']
            master.save()
        else:
            userrole = UserRole.objects.get(id=request.session['reg_data']['userrole'])
            master = Master.objects.create(
                UserRole = userrole,
                Email = request.session['reg_data']['email'],
                Password = request.session['reg_data']['password'],
                IsActive = True,
            )

            Profile.objects.create(
                Master = master,
            )

        print("verified.")
        #alert('success', 'An OTP verified.')

    else:
        print("Invalid OTP")
        
        #alert('danger', 'Invalid OTP')

        return redirect(otp_page)
    
    return redirect(login_page)

#def book_store(request):
    #master = Master.objects.get()


def My_Profile(request):
    Profile = Profile.objects.get(Email = request.session['email'])

    if Profile.FullName == request.POST['Profile']:
        Profile.Gender = request.POST['Profile']
        Profile.save()
    else:
        print('incorrect current password.')

    return redirect(profile_page)
