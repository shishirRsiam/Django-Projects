from .Authentication_App_Import import *


class UserViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

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
        user = authenticate(request, username=username, password=password)
        if user:
            if not user.is_active:
                response = get_account_not_active_response()
                return Response(response, status=400)
            print('-> user nam', user)
            print('&&'*20)
            print(request.user.is_authenticated)
            login(request, user)  
            print(request.user.is_authenticated)
            print('&&'*20)
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

        if user:
            if user.is_active:
                response = get_already_account_activation_response()
                return Response(response, status=200)
            
            else:
                user.is_active = True
                user.save()

                login(request, user)
                
                response = get_successful_account_activation_response()
                return Response(response, status=200)

        response = get_failed_account_activation_response()
        return Response(response, status=400)
    
    
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        try:
            token = Token.objects.get(user=request.user)
            token.delete()
            logout(request)
            return Response({"message": "Logged out successfully."})
        except Token.DoesNotExist:
            return Response({"error": "Token not found."})
        
class UserView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = request.user
        serializer = UserSerializer(user.userprofile)
        return Response(serializer.data)
    
