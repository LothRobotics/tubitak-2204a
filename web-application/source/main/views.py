import hashlib

from django.shortcuts import render, redirect
from django.contrib import messages

import sys

sys.path.insert(1, '.') #also look for 1 folder back
sys.path.insert(1, '..') 
sys.path.insert(1, '...')
sys.path.insert(1, '....')
sys.path.insert(1, '.....')
#print("SYS PATHS ARE HERE",sys.path[:3])

from database_handler import DatabaseHandler

db_conn = DatabaseHandler("db_credentials.json")

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

def RegisterView(request):
    if request.POST and not is_authenticated(request):
        pass
    else:
        return render(request, 'register.html')
      
  
def LogoutView(request):
    if is_authenticated(request):
        username = request.session['authentication_account']['username']
        messages.info(request, f'Başarıyla çıkış yapıldı: { username }', extra_tags=NOTIFICATION_TAGS['error'])
        del request.session['authentication_account'] 
    return redirect('login-page')
