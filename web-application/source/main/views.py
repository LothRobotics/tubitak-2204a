import hashlib
import datetime
import math
import os
import random
import requests
import bs4
import uuid    


from django.shortcuts import render, redirect
from django.contrib import messages

from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.core.mail import send_mail

from database_handler import db_conn




NOTIFICATION_TAGS = {
    'success': 'ph-check-circle',
    'error': 'ph-x-circle',
    'warning': 'ph-warning-circle',
    'info': 'ph-info'
}

# Create your views here.

def is_authenticated(request):
    try: 
      request.session['authentication_account']
    except KeyError:
      return False 
    else:
      return True 

def only_non_authenticated(func):

    def wrapper(*args, **kwargs):
        return func(*args, **kwargs) if not is_authenticated(args[0]) else redirect('index-page')

    return wrapper


def only_authenticated(func):

    def wrapper(*args, **kwargs):
        return func(*args, **kwargs) if is_authenticated(args[0]) else redirect('index-page')

    return wrapper

def IndexView(request):
    if is_authenticated(request):
      return render(request, 'index.html', request.session['authentication_account']) 
    else:
      return redirect('login-page')
        
@only_non_authenticated
def LoginView(request, registered_now: bool = False):
    if request.POST:
        username, password = request.POST['username'], request.POST['password']

        if username and password:
            password_hashed: str = hashlib.sha256(password.encode()).hexdigest()
            user = db_conn.get('accounts', [f'username == {username}', f'password == {password_hashed}'], False)

            if user:
                user = user[0]
                

                if user.to_dict()['2fa_verification']:
                  try: 
                    request.session['2fa_verified']
                  except KeyError:

                    seed = str(random.randint(100000, 999999))
                    random_seed = hashlib.sha256(seed.encode()).hexdigest()
                    
                    request.session['2fa_verified'] = False 
                    request.session['2fa_code'] = random_seed
                    request.session['2fa_account'] = user.to_dict() 
                    request.session['2fa_id'] = user.id 

                    send_mail('akillitahliyesistemi.gov.tr - Girişinizi Onaylayın!', f'Merhaba! 2 faktörlü doğrulamanız aktif olduğu için, siteye aşağıdıdaki kodu girin: \n {seed}', 'tubitak2204a@gmail.com', [ user.to_dict()['email']])

                    context = user.to_dict()
                    context['2fa_enabled'] = True

                    return render(request, '2fa_verification.html', context)
                  else:
                    if not request.session['2fa_verified']:
                      context = user.to_dict()
                      context['2fa_enabled'] = True

                      return render(request, '2fa_verification.html', context)  
                    

                AttemptLogin(request, user, username, registered_now)

                return redirect('index-page')
            else:
                messages.error(request, f'Giriş yapılamadı: {username}', extra_tags=NOTIFICATION_TAGS['error'])
                return render(request, 'login.html')
    else:
        return render(request, 'login.html')

def AttemptLogin(request, user, username, user_id, registered_now = False):
    if not isinstance(user, dict):
      user_id = user.id
      user = user.to_dict()


    request.session['authentication_account'] = user
    request.session['authentication_id'] = user_id
    
    if not registered_now:
      messages.success(request, f'Başarıyla giriş yaptın: {username}', extra_tags=NOTIFICATION_TAGS['success'])
      last_login = datetime.datetime.now().strftime("%d.%m.%Y - %H.%M:%S")
      try:
        serialnumbers = user['motherboard_serialnumber'] 
      except KeyError:
        serialnumbers = []
      current_serialnumber = str(uuid.UUID(int=uuid.getnode()))
      if current_serialnumber not in serialnumbers:
        send_mail('akillitahliyesistemi.gov.tr - Yeni Konumdan Giriş!', f'Merhaba! Hesabınıza yeni bir lokasyondan giriş yapıldı. [İstanbul / Türkiye | {last_login}]', 'tubitak2204a@gmail.com', [ user['email']])

      serialnumbers.append(current_serialnumber)


      db_conn.update('accounts', user_id, {
        'last_login': last_login, 
        'last_login_ip': request.META.get("REMOTE_ADDR"),
        'osuser_logged_in': os.getlogin(),
        'motherboard_serialnumbers': serialnumbers
        })
                  

@only_non_authenticated
def RegisterView(request):
    if request.POST:
      
          
          username, full_name, email, phone_number, password, re_password, school_url, *_ = request.POST['username'], request.POST['fullname'], request.POST['email'], request.POST['phonenumber'], request.POST['password'], request.POST['repassword'], request.POST['schoolurl']
          
          if password == re_password:
            try:
              validate_email(email)
            except ValidationError:
              messages.error(request, f'Elektronik postanızda hata var, kontrol ediniz.', extra_tags=NOTIFICATION_TAGS['error'])
            else:
              wrequest = requests.get(school_url)
              soup = bs4.BeautifulSoup(wrequest.text, 'html.parser')
              school_name = soup.title.text    
              
              if isinstance(school_name, str):
              
                query = db_conn.get('accounts', [f'username == {username}', f'school_name == {school_name}', f'email == {email}', f'full_name == {full_name}', f'phone_number == {phone_number}'], False, 'or')
                
                if not query:
                  password = hashlib.sha256(password.encode()).hexdigest()
                  school_location = school_name.split('-')[0].strip()
                  registiration_date = datetime.datetime.now().strftime("%d.%m.%Y - %H.%M:%S")
                  
                  db_conn.create('accounts', None, {
                    'username': username,
                    'full_name': full_name,
                    'email': email, 
                    'phone_number': phone_number,
                    'password': password, 
                    'school': {
                      'school_website_url':school_url,
                      'school_name': school_name,
                      'school_location': school_location,
                    },
                    'clasrooms': {},
                    'registiration_date': registiration_date,
                    'last_login': registiration_date,
                    'last_login_ip': request.META.get("REMOTE_ADDR"), 
                    'osuser_logged_in': os.getlogin(),
                    'motherboard_serialnumbers': [str(uuid.UUID(int=uuid.getnode()))],
                    '2fa_verification': False
                  })

                  
                  
                  messages.success(request, f'Hesabınız oluşturuldu: {username}', extra_tags=NOTIFICATION_TAGS['success'])
                  return LoginView(request, True)
                else:
                  messages.error(request, f'Girilen bilgilerinizde hata mevcut.', extra_tags=NOTIFICATION_TAGS['error'])
                  return RegisterView(request)
              else:
                messages.error(request, f'Böyle bir okul MEB veritabanında bulunamadı, kontrol edin.', extra_tags=NOTIFICATION_TAGS['error'])
                return RegisterView(request)
                
          else:
            messages.error(request, f'Girilen şifreler uyuşmuyor, kontrol ediniz.', extra_tags=NOTIFICATION_TAGS['error'])
            return RegisterView(request)
    
    return render(request, 'register.html')
      
@only_authenticated
def LogoutView(request):    
    try:
      username = request.session['authentication_account']['username']
      messages.info(request, f'Başarıyla çıkış yapıldı: { username }', extra_tags=NOTIFICATION_TAGS['info']) 
      db_conn.update('accounts', request.session['authentication_id'], {'logged_in': False})
    except KeyError:
      del request.session['authentication_account']
    except AssertionError:
      del request.session['authentication_account']
    else: 
      del request.session['authentication_account'], request.session['authentication_id']

    return redirect('login-page')


@only_authenticated 
def UserPreferencesView(request):
  if request.POST:
      username, full_name, email, phone_number, _2fa_verification = request.POST['username'], request.POST['fullname'], request.POST['email'], request.POST['phonenumber'], request.POST['2fa-verif'] 
      db_conn.update('accounts', request.session['authentication_id'], {'username': username, 'full_name': full_name, 'email': email, 'phone_number': phone_number, '2fa_verification': True if _2fa_verification == "true" else False})
      
      user = db_conn.get('accounts', [f'username == {username}'], False)

      if user:
          user = user[0]
              
          request.session['authentication_account'] = user.to_dict()
          
          messages.success(request, f'Başarıyla hesap tercihleri değiştirildi: {username}', extra_tags=NOTIFICATION_TAGS['success'])

      else:
          messages.error(request, f'Hesap tercihleri değişirken hata oluştu: {username}', extra_tags=NOTIFICATION_TAGS['error'])

      return redirect('user-preferences')

  
  return render(request, 'user-preferences.html',  request.session['authentication_account'])


@only_authenticated 
def ChangePasswordView(request):
  if request.POST:
    password, new_password, new_password_re = request.POST['old-password'], request.POST['new-password'], request.POST['new-password-re']

    password_hashed = hashlib.sha256(password.encode()).hexdigest()
    
    if password_hashed == request.session['authentication_account']['password']:
      if new_password == new_password_re:
        new_hashed_password = hashlib.sha256(new_password.encode()).hexdigest()

        db_conn.update('accounts', request.session['authentication_id'], {'password': new_hashed_password})
        messages.success(request, f'Başarıyla şifreniz değiştirildi!', extra_tags=NOTIFICATION_TAGS['success'])
        
        request.session['authentication_account']['password'] = new_hashed_password

        return redirect('index-page')

      else:
        messages.error(request, 'Yeni şifreleriniz eşleşmiyor.', extra_tags=NOTIFICATION_TAGS['error'])
    else:

      messages.error(request, 'Şifreniz doğru değil', extra_tags=NOTIFICATION_TAGS['error'])
 
    return redirect('change-password')

  return render(request, 'change-password.html',  request.session['authentication_account'])

def DoubleFactorVerificationView(request):
  verification_code = request.POST['2fa-code']
  hashed_code = hashlib.sha256(verification_code.encode()).hexdigest()
  if hashed_code == request.session['2fa_code']:
    request.session['2fa_verified'] = True
    del request.session['2fa_code']
  try:
    AttemptLogin(request, request.session['2fa_account'], request.session['2fa_account']['username'], request.session['2fa_id'], False)
    del request.session['2fa_verified'], request.session['2fa_id'], request.session['2fa_account']
  except KeyError:
    pass 
  return redirect('index-page')

  