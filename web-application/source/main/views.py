import hashlib

from django.shortcuts import render, redirect
from django.contrib import messages

from database_handler import db_conn 

NOTIFICATION_TAGS = {
    'success': 'checkmark-circle-outline',
    'error': 'close-circle-outline',
    'warning': 'alert-circle-outline',
    'info': 'information-circle-outline'
}

# Create your views here.

def IndexView(request):
    try:
         request.session['authentication_account']
    except KeyError:
        return redirect('login-page')
    else:
        return render(request, 'index.html', request.session['authentication_account'])

def LoginView(request):
    if request.POST:
        try: 
            request.session['authentication_account']
        except KeyError:
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
            return IndexView(request)

    else:
        return render(request, 'login.html')

def RegisterView(request):
    return render(request, 'register.html')
def LogoutView(request):
    try: 
        request.session['authentication_account']
    except KeyError:
        return redirect('index-page')
    else:
        username = request.session['authentication_account']['username']
        messages.info(request, f'Başarıyla çıkış yapıldı: { username }', extra_tags=NOTIFICATION_TAGS['error'])
        del request.session['authentication_account'] 
        return redirect('login-page')
