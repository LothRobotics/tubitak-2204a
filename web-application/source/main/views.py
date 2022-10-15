import hashlib

from django.shortcuts import render, redirect
from django.contrib import messages

from django.core.validators import validate_email
from django.core.exceptions import ValidationError

from database_handler import DatabaseHandler
db_conn = DatabaseHandler('../../db_credentials.json')

import requests
import bs4

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

def IndexView(request):
    if is_authenticated(request):
      return render(request, 'index.html', request.session['authentication_account']) 
    else:
      return redirect('login-page')
        

def LoginView(request):
    if request.POST and not is_authenticated(request):
        username, password = request.POST['username'], request.POST['password']

        if username and password:
            password_hashed: str = hashlib.md5(password.encode()).hexdigest()
            user = db_conn.get('accounts', [f'username == {username}', f'password == {password_hashed}'], True)

            if user:
                request.session['authentication_account'] = user[0]
                messages.success(request, f'Başarıyla giriş yaptın: {username}', extra_tags=NOTIFICATION_TAGS['success'])
                return redirect('index-page')
            else:
                messages.error(request, f'Giriş yapılamadı: {username}', extra_tags=NOTIFICATION_TAGS['error'])
                return render(request, 'login.html')
    else:
        return render(request, 'login.html')

# FIXME: Kullanıcı adı, email, okul sitesi sorguya dahil edilecek.
def RegisterView(request):
    if request.POST and not is_authenticated(request):
      
          
          username, full_name, email, phone_number, password, re_password, school_url, *_ = request.POST['username'], request.POST['fullname'], request.POST['email'], request.POST['phonenumber'], request.POST['password'], request.POST['repassword'], request.POST['schoolurl']
          
          if password == re_password:
            try:
              validate_email(email)
            except ValidationError:
              messages.error(request, f'Elektronik postanızda hata var, kontrol ediniz.', extra_tags=NOTIFICATION_TAGS['error'])
            else:
              wrequest = requests.get(school_url)
              soup = bs4.BeautifulSoup(wrequest.text, 'html.parser')
              title = soup.title.text
              
              if title:
              
                query = db_conn.get('accounts', [f'username == {username}'], False)
                
                if not query:
                  password = hashlib.md5(password.encode()).hexdigest()
                  
                  user = db_conn.create('accounts', None, {
                    'username': username,
                    'full_name': full_name,
                    'email': email, 
                    'phone_number': phone_number,
                    'password': password, 
                    'school_website_url':school_url,
                    'title': title
                  })
                  messages.success(request, f'Hesabınız oluşturuldu: {username}', extra_tags=NOTIFICATION_TAGS['success'])
                  return render(request, 'register.html')
                else:
                  messages.error(request, f'Girilen şifreler uyuşmuyor, kontrol ediniz.', extra_tags=NOTIFICATION_TAGS['error'])
              else:
                messages.error(request, f'Böyle bir okul MEB veritabanında bulunamadı, kontrol edin.', extra_tags=NOTIFICATION_TAGS['error'])
                
          else:
            messages.error(request, f'Girilen şifreler uyuşmuyor, kontrol ediniz.', extra_tags=NOTIFICATION_TAGS['error'])
    
    return render(request, 'register.html')
      
  
def LogoutView(request):
    if is_authenticated(request):
        username = request.session['authentication_account']['username']
        messages.info(request, f'Başarıyla çıkış yapıldı: { username }', extra_tags=NOTIFICATION_TAGS['error'])
        del request.session['authentication_account'] 
    return redirect('login-page')
