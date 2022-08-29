from django.http import HttpResponse
from rest_framework.decorators import action

from .serializers import (
    UserSerializer,
    BlockUserSerializer,
    UnblockUserSerializer,
    LoginUserSerializer,
    RefreshTokenSerializer,
)

from rest_framework import viewsets, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from .permissions import OwnUserAccount, IsAdmin
from django.contrib.auth import get_user_model
from .token import generate_token

from .services import (
    block_user,
    unblock_user,
    verify_user_login,
    verify_refresh_token,
    save_path,
)

from .s3_storage import get_presigned_url

from django.conf import settings

import logging

User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    permissions_dict = {
        "create": [AllowAny],
        "list": [IsAuthenticated],
        "retrieve": [IsAuthenticated],
        "update": [OwnUserAccount],
        "partial_update": [OwnUserAccount | IsAdmin],
        "destroy": [OwnUserAccount | IsAdmin],
        "block_id": [IsAdmin],
        "unblock_id": [IsAdmin],
        "get_url_to_upload_picture": [OwnUserAccount],
        "get_url_to_picture": [OwnUserAccount],
        "get_url_to_delete_picture": [OwnUserAccount],
    }

    def create(self, request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            User.objects.create_user(**serializer.validated_data)
            return Response(serializer.validated_data, status=status.HTTP_201_CREATED)

        return Response({'status': 'Bad Request',
                         'message': serializer.is_valid()},
                        status=status.HTTP_400_BAD_REQUEST)

    def get_permissions(self):
        self.permission_classes = self.permissions_dict.get(self.action)
        return super(self.__class__, self).get_permissions()

    @action(detail=True, methods=("patch",), permission_classes=[IsAdmin])
    def block_id(self, request, **kwargs):

        """
        Block user account: Permission is given to Admin only.
        **kwargs contains "pk" of the target user
        """

        admin = request.user.id
        user_to_block = int(self.kwargs['pk'])
        blocked_user = block_user(admin, user_to_block)
        serializer = BlockUserSerializer(blocked_user)
        return Response(serializer.data)

    @action(detail=True, methods=("patch",), permission_classes=[IsAdmin])
    def unblock_id(self, request, **kwargs):

        """
        Unblock user account: Permission is given to Admin only.
        **kwargs contains "pk" of the target user
        """

        admin = request.user.id
        blocked_user = int(self.kwargs['pk'])
        unblocked_user = unblock_user(admin, blocked_user)
        serializer = UnblockUserSerializer(unblocked_user)
        return Response(serializer.data)

    @action(detail=True, methods=("post",), permission_classes=[OwnUserAccount])
    def get_url_to_upload_picture(self, request, **kwargs):
        logging.info(request)
        file = request.data.get('file')
        file_name = f'user_{request.user.id}/{file}'
        method = 'put_object'
        save_path(request.user.id, file_name)
        logging.info(file_name)
        data = get_presigned_url(file_name,method)
        return HttpResponse(data, content_type='json')

    @action(detail=True, methods=("post",), permission_classes=[OwnUserAccount])
    def get_url_to_picture(self, request, **kwargs):
        logging.info(request)
        file_name = request.user.image_s3_path
        method = 'get_object'
        logging.info(file_name)
        data = get_presigned_url(file_name, method)
        return HttpResponse(data, content_type='json')

    @action(detail=True, methods=("post",), permission_classes=[OwnUserAccount])
    def get_url_to_delete_picture(self, request, **kwargs):
        logging.info(request)
        file_name = request.user.image_s3_path
        method = 'delete_object'
        logging.info(file_name)
        data = get_presigned_url(file_name, method)
        return HttpResponse(data, content_type='json')


class LoginViewSet(viewsets.ViewSet):
    queryset = User.objects.all()
    serializer = LoginUserSerializer
    permission_classes = (AllowAny,)

    @action(detail=True, methods=("post",), permission_classes=[AllowAny])
    def login_user(self, request):

        """
        Login user function authenticates user and generates access/refresh tokens
        """

        serializer = LoginUserSerializer(data=request.data)
        username = request.data.get('username')
        password = request.data.get('password')
        response = Response()
        user = verify_user_login(username, password)
        serialized_user = LoginUserSerializer(user).data
        access_token = generate_token(settings.JWT_ACCESS_EXP, user)
        refresh_token = generate_token(settings.JWT_REFRESH_EXP, user)

        response.set_cookie(key='refresh_token', value=refresh_token, httponly=True)
        response.data = {
            'access_token': access_token,
            'refresh_token': refresh_token,
            'user': serialized_user,
        }

        return response


class RefreshTokenViewSet(viewsets.ViewSet):
    queryset = User.objects.all()
    serializer = RefreshTokenSerializer
    permission_classes = (AllowAny,)

    @action(detail=True, methods=("post",), permission_classes=[AllowAny])
    def auth_with_refresh_token(self, request):

        """
        Auth with refresh token function is used to regenerate access token after its expiry
        """

        refresh_token = request.COOKIES.get("refresh_token")
        user = verify_refresh_token(refresh_token)
        access_token = generate_token(settings.JWT_ACCESS_EXP, user)
        return Response({"access_token": access_token})
