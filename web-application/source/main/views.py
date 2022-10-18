import hashlib
import datetime
import os
import requests
import bs4


from django.shortcuts import render, redirect
from django.contrib import messages

from django.core.validators import validate_email
from django.core.exceptions import ValidationError

from database_handler import db_conn




NOTIFICATION_TAGS = {
    'success': 'checkmark-circle-outline',
    'error': 'close-circle-outline',
    'warning': 'alert-circle-outline',
    'info': 'information-circle-outline'
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
            password_hashed: str = hashlib.md5(password.encode()).hexdigest()
            user = db_conn.get('accounts', [f'username == {username}', f'password == {password_hashed}'], False)

            if user:
                user = user[0]
              
                request.session['authentication_account'] = user.to_dict()
                request.session['authentication_id'] = user.id
                  
                if not registered_now:
                  messages.success(request, f'Başarıyla giriş yaptın: {username}', extra_tags=NOTIFICATION_TAGS['success'])
                  last_login = datetime.datetime.now().strftime("%d.%m.%Y - %H.%M:%S")
                  db_conn.update('accounts', user.id, {
                    'last_login': last_login, 
                    'last_login_ip': request.META.get("REMOTE_ADDR"),
                    'osuser_logged_in': os.getlogin()
                    })
                  
                return redirect('index-page')
            else:
                messages.error(request, f'Giriş yapılamadı: {username}', extra_tags=NOTIFICATION_TAGS['error'])
                return render(request, 'login.html')
    else:
        return render(request, 'login.html')

# FIXME: Kullanıcı adı, email, okul sitesi sorguya dahil edilecek.
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
              
                query = db_conn.get('accounts', [f'username == {username}'], False)
                
                if not query:
                  password = hashlib.md5(password.encode()).hexdigest()
                  school_location = school_name.split('-')[0].strip()
                  registiration_date = datetime.datetime.now().strftime("%d.%m.%Y - %H.%M:%S")
                  
                  db_conn.create('accounts', None, {
                    'username': username,
                    'full_name': full_name,
                    'email': email, 
                    'phone_number': phone_number,
                    'password': password, 
                    'school_website_url':school_url,
                    'school_name': school_name,
                    'school_location': school_location,
                    'registiration_date': registiration_date,
                    'last_login': registiration_date,
                    'last_login_ip': request.META.get("REMOTE_ADDR"), 
                    'osuser_logged_in': os.getlogin()
                  })
                  
                  messages.success(request, f'Hesabınız oluşturuldu: {username}', extra_tags=NOTIFICATION_TAGS['success'])
                  return LoginView(request, True)
                else:
                  messages.error(request, f'Girilen şifreler uyuşmuyor, kontrol ediniz.', extra_tags=NOTIFICATION_TAGS['error'])
              else:
                messages.error(request, f'Böyle bir okul MEB veritabanında bulunamadı, kontrol edin.', extra_tags=NOTIFICATION_TAGS['error'])
                
          else:
            messages.error(request, f'Girilen şifreler uyuşmuyor, kontrol ediniz.', extra_tags=NOTIFICATION_TAGS['error'])
    
    return render(request, 'register.html')
      
@only_authenticated
def LogoutView(request):    
    try:
      username = request.session['authentication_account']['username']
      messages.info(request, f'Başarıyla çıkış yapıldı: { username }', extra_tags=NOTIFICATION_TAGS['info']) 
      db_conn.update('accounts', request.session['authentication_id'], {'logged_in': False})
    except KeyError:
      del request.session['authentication_account']
    else: 
      del request.session['authentication_account'], request.session['authentication_id']

    return redirect('login-page')
