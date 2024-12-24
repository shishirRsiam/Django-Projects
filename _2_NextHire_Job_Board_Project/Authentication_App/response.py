def get_successful_login_response(user, token):
    response = {
        "status": True,
        "title": "Login successful",
        "message": "You are now logged in",
        "token": token.key,
        "refresh_token": str('refresh_token'),
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
        'title': f'{name} already exists!',
        'message': f'Please use another {name}!',
    }
    return response

def get_successful_account_activation_response():
    response = {
        "status": True,
        "title": "Activation Successful.",
        "message": "Your account is now activated. You are now logged in.",
        }
    return response

def get_failed_account_activation_response():
    response = {
        "status": False,
        "title": "Activation Failed!",
        "message": "Invalid activation link!",
        'is_already_activated': False,
    }
    return response

def get_already_account_activation_response():
    response = {
        "status": True,
        "title": "Account Already Activated.",
        "message": "Your Account Is Already Activated. Please Login.",
        'is_already_activated': True
    }   
    return response

def get_failed_login_response():
    response = {
        "status": False,
        "title": "Login failed!",
        "message": "Invalid credentials!",
    }
    return response


def get_successful_account_registration_response():
    response = {
        'status': True,
        'title': 'User created successfully.',
        'message': 'Check your mail for Activate your account.',
    }
    return response

def name():
    response = False
    return response
