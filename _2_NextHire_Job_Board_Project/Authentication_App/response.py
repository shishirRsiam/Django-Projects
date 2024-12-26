def get_successful_login_response(user, token):
    response = {
        "status": True,
        "title": "Login successful",
        "message": "You are now logged in",
        "token": f'Token {token.key}',
        'user': {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            'role': user.userprofile.role,
            'company_name': user.userprofile.company_name,
            'name': user.first_name + ' ' + user.last_name,
        }}
    return response

def get_username_or_email_already_exists_response(name):
    response = {
        'status': False,
        'title': f'This {name} already exists!',
        'message': f'Please use another {name}!',
    }
    return response

def get_successful_account_activation_response():
    response = {
        "status": True,
        "title": "Account Activation Successful.",
        "message": "Your account is now activated. You can now login.",
        }
    return response

def get_failed_account_activation_response():
    response = {
        "status": False,
        "title": "Opps! Account Activation Failed!",
        "message": "Invalid activation link!",
        'is_already_activated': False,
    }
    return response

def get_already_account_activation_response():
    response = {
        "status": True,
        "title": "Account Already Activated.",
        "message": " Your Account Is Already Activated. Please Login.",
        'is_already_activated': True
    }   
    return response

def get_failed_login_response(**kwargs):
    response = {
        "status": False,
        "title": "Opps! Login failed!",
        "message": kwargs.get('message') or "Invalid credentials!",
    }
    return response

def get_account_not_active_response(**kwargs):
    response = {
        "status": False,
        "title": "Opps! Login failed!",
        "message": "Account is not active! Check your email to activate your account.",
    }
    return response


def get_successful_account_registration_response():
    response = {
        'status': True,
        'title': 'Wow! Account created successfully.',
        'message': 'Check your mail for Activate your account.',
    }
    return response

def name():
    response = False
    return response
