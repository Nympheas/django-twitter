from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.decorators import action 
from rest_framework.permissions import AllowAny 
from accounts.api.serializers import UserSerializer
from django.contrib.auth import (
    authenticate as django_authenticate,
    login as django_login,
    logout as django_logout,
)
from accounts.api.serializers import SignupSerializer, LoginSerializer

class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

class AccountViewSet(viewsets.ViewSet):
    permission_classes = (AllowAny,)
    serializer_class = SignupSerializer

    @action(methods=['POST'], detail=False)
    def signup(self, request):
        """
        使用 username, email, password 进行注册
        """

        serializer = SignupSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({
                'success': False,
                'message': "Plase check input",
                'errors': serializer.errors,
            }, status=400)

        user = serializer.save()
        django_login(request, user)
        return Response({
            'success': True,
            'user': UserSerializer(user).data,
        }, status=201)

    @action(methods=['POST'], detail=False)
    def login(self, request):
        """
        默认的 username 是 admin, password 也是 admin
        """
        serializer = LoginSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({
                'success': False,
                'message': "Plase check input",
                'errors': serializer.errors,
            }, status=400)
        
        username = serializer.validated_data['username']
        password = serializer.validated_data['password']
        user = django_authenticate(username=username, password=password)
        if not user or user.is_anonymous:
            return Response({
                'success': False,
                'message': "username and password does not match",
            }, status=400)
        django_login(request, user)
        return Response({
            'success': True,
            'user': UserSerializer(instance=user).data,
        })

    @action(methods=['GET'], detail=False)
    def login_status(self, request):
        """
        查看用户当前登录状态和具体信息
        """

        data = {
            'has_logged_in': request.user.is_authenticated,
            'ip': request.META['REMOTE_ADDR'],
        }
        if request.user.is_authenticated:
            data['user'] = UserSerializer(request.user).data
        return Response(data)

    @action(methods=['POST'], detail=False)
    def logout(self, request):
        """
        登出当前用户
        """
        django_logout(request)
        return Response({'success': True})
# Create your views here.
