from .Authentication_App_Import import *


class UserViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserSerializer

class UserRegistrationApiView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        first_name = request.data.get('first_name')
        last_name = request.data.get('last_name')
        role = request.data.get('role')
        username = request.data.get('username')
        password = request.data.get('password')
        email = request.data.get('email')
        
        user = User.objects.filter(username=username).first()
        if user:
            response = get_username_or_email_already_exists_response('username')
            return Response(data=response, status=400)

        user = User.objects.filter(email=email).first()
        if user:
            response = get_username_or_email_already_exists_response('email')
            return Response(data=response, status=400)
        
        user = User.objects.create_user(
            first_name=first_name, last_name=last_name,
            username=username, password=password,
            email=email, is_active=False,
        )
        user_profile = UserProfile.objects.create(user=user, role=role)
        user.save()
        user_profile.save()

        email_sent.sent_account_registration_activation_email(user)

        response = get_successful_account_registration_response()
        return Response(data=response, status=201)

class LoginApiView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        print(username, password)
        user = authenticate(username=username, password=password)
        if user:
            if not user.is_active:
                response = get_account_not_active_response()
                return Response(response, status=400)
            token, _ = Token.objects.get_or_create(user=user) 
            response = get_successful_login_response(user, token)
            return Response(response, status=200)
        
        response = get_failed_login_response()
        return Response(response, status=400)
    
class ActivateAccountView(APIView):
    permission_classes = [AllowAny]
    def get(self, request, idb64, token):
        id = urlsafe_base64_decode(idb64).decode()
        user = User.objects.get(id=id)
        print('user', user)

        if user and default_token_generator.check_token(user, token):
            if user.is_active:
                response = get_already_account_activation_response()
                return Response(response, status=200)
            
            else:
                user.is_active = True
                user.save()
                
                response = get_successful_account_activation_response()
                return Response(response, status=200)

        response = get_failed_account_activation_response()
        return Response(response, status=400)
    
    