from .constImport import *


class UserViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserSerializer

class UserRegistrationApiView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        first_name = request.data.get('first_name')
        last_name = request.data.get('last_name')
        role = request.data.get('role')
        company_name = request.data.get('company_name')
        resume = request.data.get('resume')
        username = request.data.get('username')
        password = request.data.get('password')
        email = request.data.get('email')
        
        user = User.objects.filter(username=username).first()
        if user:
            response = {
                'status': False,
                'title': 'Username already exists',
                'message': 'Please use another username',
            }
            return Response(data=response, status=400)

        user = User.objects.filter(email=email).first()
        if user:
            response = {
                'status': False,
                'title': 'Email already exists',
                'message': 'Please use another email',
            }
            return Response(data=response, status=400)
        
        user = User.objects.create_user(
            first_name=first_name, last_name=last_name,
            username=username, password=password,
            email=email, is_active=False,
        )
        user_profile = UserProfile.objects.create(user=user, role=role, company_name=company_name, resume=resume)
        user.save()
        user_profile.save()

        user = User.objects.get(id=1)

        email_sent.sent_account_registration_activation_email(user)

        response = {
            'status': True,
            'title': 'User created successfully',
            'message': 'Check your mail for Activate your account',
        }
        return Response(data=response, status=201)
        # return Response(data=serializer.errors, status=400)


class LoginApiView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        # Extract username and password from request data
        username = request.data.get('username')
        password = request.data.get('password')

        # Attempt to authenticate the user
        print('(-)' * 20)
        print(username, password)
        print('(-)' * 20)
        user = authenticate(username = username, password = password)
        if user:
            login(request, user)   
            return Response({
                "status": True,
                "title": "Login successful",
                "message": "You are now logged in",
                "access_token": 'access_token',
                "refresh_token": str('refresh_token'),
                'user': {
                    "id": user.id,
                    "username": user.username,
                    "email": user.email,
                    'role': user.userprofile.role,
                    'company_name': user.userprofile.company_name,
                    'name': user.first_name + ' ' + user.last_name,
                },
            }, status=200)
        
        return Response({
            "status": False,
            "title": "Login failed",
            "message": "Invalid credentials",
        }, status=400)