from django.shortcuts import redirect, render
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import login, logout, authenticate, update_session_auth_hash
from .models import UserAddress, UserBankAccount

from Transactions import sent_email
from Transactions.models import Transaction


def home(request):
    if request.user.is_authenticated:
        return render(request, 'base.html')
    
    return render(request, 'home.html')


from django.contrib.auth.models import User
def sign_up(request):
    context = {
        'title': 'Sign Up',
    }
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        nid_number = request.POST.get('nid_number')
        birth_day = request.POST.get('birth_day')
        street_address = request.POST.get('street_address')
        city = request.POST.get('city')
        state = request.POST.get('state')
        postal_code = request.POST.get('postal_code')
        account_type = request.POST.get('account_type')
        gender = request.POST.get('gender')
        terms_conditions = request.POST.get('terms_conditions')

        print()

        # Example user creation logic (if passwords match)
        data = {
            'error_msg' : 'Passwords do not match.',
        }
        if password == confirm_password:
            print("User created successfully.")
            if not User.objects.filter(username=username).exists():                
                # Create user
                user = User.objects.create_user(
                    first_name=first_name,
                    last_name=last_name,
                    username=username,
                    email=email,
                    password=password
                )
                user.save()

                # Create UserAddress
                UserAddress.objects.create(
                    user=user,
                    street_address=street_address,
                    city=city,
                    state=state,
                    postal_code=postal_code,
                    user_id=user.id 
                ).save()

                # Create UserBankAccount
                UserBankAccount.objects.create(
                    user=user,
                    nid_number=nid_number,
                    birth_day=birth_day,
                    account_no=15052004000 + user.id,
                    account_type=account_type,
                    gender=gender,
                    user_id=user.id 
                ).save()
                sent_email.sent_account_create_email(user)
                request.session['success_message'] = 'Account created successfully. Please log in.'
                return redirect('login')
            
            data['error_msg'] = 'Username already exists.'
        context.update(data)

    print(context)

    return render(request, 'sign_up.html', context)


def profile(request):
    if not request.user.is_authenticated:
        return redirect('login')
    
    transactions = request.user.transactions.all().order_by('-id')[:10]
    context = {
        'transactions' : transactions,
    }

    return render(request, 'profile.html', context)      


def edit_profile(request):
    if not request.user.is_authenticated:
        return redirect('login')
    
    if request.method == 'POST':
        request.user.username = request.POST['username']
        request.user.email = request.POST['email']
        request.user.first_name = request.POST['first_name']
        request.user.last_name = request.POST['last_name']
        request.user.save()
        return redirect('profile')

    context = {}
    return render(request, 'edit_profile.html', context)


def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')

    success_msg = request.session.pop('success_message', False)
    context = {
        'success_msg': success_msg,
    }
    if request.method == 'POST':
        username_or_email = request.POST['username'] 
        password = request.POST['password']
        user = authenticate(request, username=username_or_email, password=password)
        if not user:
            if User.objects.filter(email=username_or_email).exists():
                user = User.objects.get(email=username_or_email)
                if not user.check_password(password):
                    user = None
            # user = authenticate(request, email=username_or_email, password=password)
        
        # print(user, username_or_email, password)
        if user:
            login(request, user)
            return redirect('home')
        
        context['error_msg'] = 'Invalid email or username or password'
    
    return render(request, 'login.html', context)


def logout_view(request):
    if not request.user.is_authenticated:
        return redirect('login')
    logout(request)
    return redirect('home')


def password_reset(request):
    if not request.user.is_authenticated:
        return redirect('login')
    
    context = {}
    if request.method == 'POST':
        old_password = request.POST['old_password']
        new_password = request.POST['new_password']
        confirm_password = request.POST['confirm_password']
        
        if not request.user.check_password(old_password):
            context['error_msg'] = 'Old password is incorrect!'

        elif new_password != confirm_password:
            context['error_msg'] = 'New password and confirm password do not match!'
        
        else:
            request.user.set_password(new_password)
            request.user.save()

            sent_email.sent_change_password_email(request.user)
            update_session_auth_hash(request, request.user)
            return redirect('profile')
    
    return render(request, 'change_password.html', context)