from django.contrib import messages
from django.http import HttpResponse, HttpResponseNotAllowed, JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.urls import reverse
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes  # force_bytes burada değiştirildi
from django.template.loader import render_to_string
from .tokens import account_activation_token  # Token jeneratörünüzü içe aktarın
from .forms import *  # Formunuzu içe aktardığınızdan emin olun
from django.contrib.auth import get_user_model
from django.core.mail import EmailMessage  
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str  # force_str burada değiştirildi
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from .models import UserAddress
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.utils.encoding import force_str
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.tokens import default_token_generator

# KULLANICI PROFİLİ *
@login_required
def profil(request):
    if request.method == "GET":
        if request.user.is_authenticated:
            full_name = f"{request.user.first_name} {request.user.last_name}"
            addresses = list(UserAddress.objects.filter(user_id=request.user).values())
            # AJAX isteği olup olmadığını kontrol et
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                # AJAX isteği ise JSON döndür
                return JsonResponse({'full_name': full_name, 'addresses': addresses})
            else:
                # Normal bir GET isteği ise HTML sayfasını döndür
                return render(request, 'user/profil.html')
        else:
            return redirect('main_home:index')
    else:
        return HttpResponseNotAllowed(['GET'])  # Sadece GET isteğine izin ver


# ***BU OTURUM AÇMIŞ KİŞİNİN PROFİL SAYFASINDAN ŞİFRE DEĞİŞTİRME FONKSİYONU ****
@login_required
def change_password(request):
    if request.method == "POST":
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # User is logged in again after password change
            return JsonResponse({'status': 'success', 'message': 'Şifreniz başarıyla değiştirildi.'})
        else:
            # Hata mesajlarını kontrol et ve döndür
            error_messages = []
            for field in form:
                for error in field.errors:
                    error_messages.append(error)
            return JsonResponse({'status': 'error', 'message': error_messages})
    return render(request, 'user/profil.html') 







 # BU OTURUM AÇMIŞ KİŞİNİN PROFİL SAYFASINDAN ADINI-SOYADINI-EMAİL DEĞİŞTİRME FONKSİYONU
@csrf_exempt  # CSRF korumasını devre dışı bırakıyor, bunu kullanmak yerine frontend'de CSRF token'ı kullanmak daha güvenli
def update_name_email(request):
    if request.method == "POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')

        if not all([first_name, last_name, email]):
            return JsonResponse({'status': 'error', 'message': 'Lütfen tüm alanları doldurun.'})

        try:
            user = request.user
            user.first_name = first_name
            user.last_name = last_name
            user.email = email
            user.save()

            full_name = f"{user.first_name} {user.last_name}"  # Güncellenmiş tam adı oluştur
            return JsonResponse({'status': 'success', 'full_name': full_name})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})

    return JsonResponse({'status': 'error', 'message': 'Geçersiz istek.'})





# KULLANICI ADRES KAYIT KODU *
@login_required
def address_create(request):
    if request.method == 'POST':
        form = UserAddressForm(request.POST)
        if form.is_valid():
            address = form.save(commit=False)
            address.user = request.user
            address.save()
            messages.success(request, 'Adres başarıyla oluşturuldu.')
            return redirect('user:profil')  # Profil sayfasına yönlendiriyoruz
        else:
            # Form geçerli değilse hata mesajlarını göster
            messages.error(request, 'Lütfen adres bilgilerinizi eksiksiz doldurun.')
    else:
        form = UserAddressForm()

    return render(request, 'user/profil.html', {'form': form})



# KULLANICI ADRES SİLME KODU *
@login_required
def delete_address(request, address_id):
    if request.method == "POST" and request.user.is_authenticated:
        address = get_object_or_404(UserAddress, id=address_id, user_id=request.user)
        address.delete()
        return JsonResponse({'status': 'success', 'message': 'Adres silindi.'})
    return JsonResponse({'status': 'error', 'message': 'İstek geçersiz.'})


# KULLANICI KAYIT KODU *
def register(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            mail_subject = 'Aktivasyon bağlantısı e-posta kimliğinize gönderildi'
            message = render_to_string('user/activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(mail_subject, message, to=[to_email])
            email.send()
            return render(request, 'user/email.html', {'msg': 'Kaydı tamamlamak için lütfen e-posta adresinizi doğrulayın.'})
    else:
        form = SignupForm()
    return render(request, 'user/signup.html', {'form': form, 'title': 'kayıt ol!'})


# KULLANICI GİRİŞ KODU *
def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('main_home:index')
            else:
                # Kullanıcı adı veya şifre yanlışsa, mesaj göster
                messages.error(request, 'Geçersiz kullanıcı adı veya şifre.')
        else:
            # Form doğrulama başarısız olsa da aynı hata mesajını göster
            messages.error(request, 'Geçersiz kullanıcı adı veya şifre.')
    else:
        form = AuthenticationForm()
    return render(request, 'user/login.html', {'form': form})



# KULLANICI (MAİL) AKTİFLEME KODU *
def activate(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))  # force_str kullanımı
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Hesabınız başarıyla aktifleştirildi!')
        return redirect('user:login')
    else:
        messages.error(request, 'Aktivasyon bağlantısı geçersiz!')
        return redirect('user:register')





# KULLANICI (ŞİFRE) SIFIRLAMA KODU *
def password_reset_request(request):
    if request.method == "POST":
        email = request.POST['email']
        associated_users = User.objects.filter(email=email)
        if associated_users.exists():
            for user in associated_users:
                subject = "Parola Sıfırlama İsteği"
                email_template_name = "user/user_password_reset_email_send/password_reset_email.html"
                c = {
                    "email": user.email,
                    "domain": request.META["HTTP_HOST"],
                    "site_name": "Siteniz",
                    "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                    "user": user,
                    "token": default_token_generator.make_token(user),
                    "protocol": "http",
                }
                email = render_to_string(email_template_name, c)
                send_mail(subject, email, "quizkutusu.com", [user.email], fail_silently=False)
            return HttpResponse('E-posta ile parola sıfırlama bağlantısı gönderildi.')
        else:
            return HttpResponse('Bu e-posta adresiyle ilişkili bir hesap bulunamadı.')
    return render(request, "user/user_password_reset_email_send/password_reset_form.html")



# KULLANICI ŞİFRE  ONAYLAMA KODU *
def password_reset_confirm(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        if request.method == 'POST':
            form = CustomPasswordChangeForm(user, request.POST)
            if form.is_valid():
                user = form.save()
                # Kullanıcının oturumunu güncelleyin
                update_session_auth_hash(request, user)
                return HttpResponse("Parola başarıyla değiştirildi. Tekrardan giriş yapınız.")
                

        else:
            form = CustomPasswordChangeForm(user)
        return render(request, 'user/user_password_reset_email_send/password_change_form.html', {'form': form})
    else:
        return HttpResponse("Geçersiz parola sıfırlama bağlantısı!")






# KULLANICI ÇIKIŞ KODU *
def user_logout(request):
    logout (request)
    return redirect("main_home:index")




# KULLANICININ VERDİĞİ SİPARİŞLERİ *
def orders(request):

    return render(request, "orders/my_orders.html")



