from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.response import Response
from rest_framework.authtoken.models import Token

from users.serializers import UserLoginSerializer, UserRegisterSerializer, UserProfilesSerializer


# JWT - JSON Web Token

@api_view(['POST'])
def register(request):
    # 0 - validate data
    serializer = UserRegisterSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    # 1 - создать пользователя
    user = User.objects.create_user(is_active=False, **serializer.validated_data)

    # password: 123 -> greknfg4237hf82b82b873grf827g3827gb*G#R@*&G#@R*&G#

    # 2 Создать токен
    token, created = Token.objects.get_or_create(user=user)

    return Response(
        {
            'token': token.key,
            'data': serializer.data,
        }  
    )

@api_view(['POST'])
def login(request):
    # 0 - validate data
    serializer = UserLoginSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    # 1 - получить данные из запроса
    # username = serializer.validated_data.get('username', None)
    # password = serializer.validated_data.get('password', None)

    # serializer.validated_data -> dict
    # {
    #    'username': 'admin',
    #    'password': 'admin'
    # }

    # 2 - найти пользователя в базе данных
    user = authenticate(**serializer.validated_data) # User | None
    
    if user:
        if not user.is_active:
            return Response({'error': 'User is not active!'})
        
        # 3 - если пользователь найден, то создать токен
        token, created = Token.objects.get_or_create(user=user) # (token, True) or (token, False)

        # 4 - вернуть токен
        return Response(
            {
                'token': token.key,
                'username': user.username,
                'email': user.email,
            }
        )

    return Response({'error': 'Wrong credentials!'})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def logout(request):
    # request.user - текущий пользователь -> User | AnonymousUser
    request.user.auth_token.delete()
    return Response({'message': 'Successfully logout!'})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def profile(request):
    serializer = UserProfilesSerializer(instance=request.user, many=False)
    return Response(serializer.data)
