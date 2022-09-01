from django.http import HttpResponse
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated

from .models import Page, Tag, Tweet, Comment

from .serializers import (
    PageSerializer,
    OnePageSerializer,
    TempBlockPageSerializer,
    AcceptRejectFollowerSerializer,
    TweetSerializer,
    CommentSerializer,
    TagSerializer,
    LikeUnlikeTweetSerializer,
)

from rest_framework import viewsets, status

from users.permissions import (
    IsOwnerOfPage,
    IsAdmin,
    IsModerator,
    IsOwnerOfTweetOrComment,
    IsPublicPageOrFollower,
)

from rest_framework.response import Response
from .services import (
    block_page_temporary,
    block_page_unlimited,
    send_follow_request,
    accept_one_follow_request,
    accept_all_follow_requests,
    reject_all_follow_requests,
    reject_one_follow_request,
    unfollow,
    like,
    unlike,
    save_path_s3,
    get_page_s3_path,
    handle_page_image
)

from users.aws import S3Client


class PageViewSet(viewsets.ModelViewSet):
    queryset = Page.objects.all()
    serializer_class = PageSerializer

    permissions_dict = {
        "create": [IsAuthenticated],
        "list": [IsAuthenticated],
        "retrieve": [IsAuthenticated],
        "update": [IsOwnerOfPage],
        "partial_update": [IsOwnerOfPage],
        "destroy": [IsOwnerOfPage | IsAdmin],
        "send_follow_request_to_page": [IsAuthenticated],
        "accept_follow_request_to_page": [IsOwnerOfPage],
        "reject_follow_request_to_page": [IsOwnerOfPage],
        "accept_all_follow_requests_to_page": [IsOwnerOfPage],
        "reject_all_follow_requests_to_page": [IsOwnerOfPage],
        "unfollow_page": [IsAuthenticated],
        "temporary_block_page": [IsModerator | IsAdmin],
        "unlimited_block_page": [IsAdmin],
        "get_url_to_upload_picture": [IsOwnerOfPage],
        "get_url_to_picture": [IsOwnerOfPage],
        "get_url_to_delete_picture": [IsOwnerOfPage],
    }

    def get_permissions(self):
        self.permission_classes = self.permissions_dict.get(self.action)
        return super().get_permissions()

    # TODO: add customized create and update methods to upload images via multipart/form-data
    # TODO: custom funcs for the create method are in tweets.tools.py
    # def create(self, request, *args, **kwargs):
    #     image = request.FILES.get('image')
    #     if image:
    #         handle_page_image(image, request)
    #         print(request)
    #     return super().create(request, *args, **kwargs)

    @action(detail=True, methods=("post",), permission_classes=[IsOwnerOfPage])
    def get_url_to_upload_picture(self, request, **kwargs):

        """
        Generates a pre-signed url to upload a file to s3 bucket.
        Sets Page.path to file's s3 path (key).
        """

        page_id = kwargs.get("pk")
        file = request.data.get('file')
        file_name = f'page_{page_id}/{file}'
        save_path_s3(page_id, file_name, )
        data = S3Client.get_presigned_url(file_name, method='put_object')
        return HttpResponse(data, content_type='json')

    @action(detail=True, methods=("post",), permission_classes=[IsOwnerOfPage])
    def get_url_to_picture(self, request, **kwargs):

        """
        Generates pre-signed url to get a file from s3 bucket.
        """

        page_id = kwargs.get("pk")
        file_name = get_page_s3_path(page_id)
        data = S3Client.get_presigned_url(file_name, method='get_object')
        return HttpResponse(data, content_type='json')

    @action(detail=True, methods=("post",), permission_classes=[IsOwnerOfPage])
    def get_url_to_delete_picture(self, request, **kwargs):

        """
        Generates a pre-signed url to delete file from s3 bucket.
        """

        page_id = kwargs.get("pk")
        file_name = get_page_s3_path(page_id)
        data = S3Client.get_presigned_url(file_name, method="delete_object")
        save_path_s3(page_id, None)
        return HttpResponse(data, content_type='json')

    @action(detail=True, methods=("patch",), permission_classes=[IsAuthenticated])
    def send_follow_request_to_page(self, request, **kwargs):

        """
        Send a follow request to someone's Page.
        User can follow a Page only from one of their pages.
        """

        serializer = OnePageSerializer(data=request.data)
        if serializer.is_valid():
            page_to_follow_id = serializer.validated_data.get("page_id")
            user_id = request.user.id
            send_follow_request(user_id, page_to_follow_id)
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(
        detail=True,
        methods=("patch",),
        permission_classes=[IsOwnerOfPage],
        url_path=r"accept_follow_request"
    )
    def accept_follow_request_to_page(self, request, **kwargs):

        """
        Accept an incoming follow request.
        """

        serializer = AcceptRejectFollowerSerializer(data=request.data)
        if serializer.is_valid():
            page_id = self.kwargs["pk"]
            user_id = serializer.validated_data.get("user_id")
            accept_one_follow_request(page_id, user_id)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(
        detail=True,
        methods=("patch",),
        permission_classes=[IsOwnerOfPage],
        url_path=r"reject_follow_request",
    )
    def reject_follow_request_to_page(self, request, **kwargs):

        """
        Reject an incoming follow request.
        """

        serializer = AcceptRejectFollowerSerializer(data=request.data)
        if serializer.is_valid():
            page_id = self.kwargs["pk"]
            user_id = serializer.validated_data.get("user_id")
            reject_one_follow_request(page_id, user_id)
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(
        detail=True,
        methods=("patch",),
        permission_classes=[IsOwnerOfPage],
        url_path=r"accept_all_follow_requests",
    )
    def accept_all_follow_requests_to_page(self, request, **kwargs):

        """
        Accept all incoming follow requests.
        """

        serializer = OnePageSerializer(data=request.data)
        if serializer.is_valid():
            page_id = serializer.validated_data.get("page_id")
            accept_all_follow_requests(page_id)
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(
        detail=True,
        methods=("patch",),
        permission_classes=[IsOwnerOfPage],
        url_path=r"reject_all_follow_requests",
    )
    def reject_all_follow_requests_to_page(self, request, **kwargs):

        """
        Reject all incoming follow requests.
        """

        serializer = OnePageSerializer(data=request.data)
        if serializer.is_valid():
            page_id = serializer.validated_data.get("page_id")
            reject_all_follow_requests(page_id)
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=("patch",), permission_classes=[IsAuthenticated])
    def unfollow_page(self, request, **kwargs):

        """
        Unfollow a Page.
        """

        serializer = OnePageSerializer(data=request.data)
        if serializer.is_valid():
            page_id = serializer.validated_data.get("page_id")
            user_id = request.user.id
            unfollow(page_id, user_id)
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=("patch",), permission_classes=[IsModerator | IsAdmin])
    def temporary_block_page(self, request, **kwargs):

        """
        Block a Page for a specific time period.
        Permission is given to Moderator and Admin.
        """

        serializer = TempBlockPageSerializer(data=request.data)
        if serializer.is_valid():
            page_id = serializer.validated_data.get("page_id")
            unblock_date = serializer.validated_data.get("unblock_date")
            block_page_temporary(page_id, unblock_date)
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=("patch",), permission_classes=[IsAdmin])
    def unlimited_block_page(self, request, **kwargs):

        """
        Block a Page forever.
        Permission is given to Admin only.
        """

        serializer = OnePageSerializer(data=request.data)
        if serializer.is_valid():
            page_id = serializer.validated_data.get("page_id")
            block_page_unlimited(page_id)
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TweetViewSet(viewsets.ModelViewSet):
    queryset = Tweet.objects.all()
    serializer_class = TweetSerializer

    permissions_dict = {
        "create": [IsOwnerOfPage],
        "list": [IsAuthenticated],
        "retrieve": [IsAuthenticated],
        "update": [IsOwnerOfTweetOrComment],
        "partial_update": [IsOwnerOfTweetOrComment],
        "destroy": [IsOwnerOfTweetOrComment | IsModerator | IsAdmin],
        "like_tweet": [IsPublicPageOrFollower],
        "unlike_tweet": [IsPublicPageOrFollower],
    }

    def get_permissions(self):
        self.permission_classes = self.permissions_dict.get(self.action)
        return super().get_permissions()

    @action(detail=True, methods=("patch",), permission_classes=[IsPublicPageOrFollower])
    def like_tweet(self, request, **kwargs):

        """
        Like a Tweet.
        Permission is given to an Authenticated User.
        """

        serializer = LikeUnlikeTweetSerializer(data=request.data)
        if serializer.is_valid():
            tweet_id = serializer.validated_data.get("tweet_id")
            user_id = request.user.id
            like(tweet_id, user_id)
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=("patch",), permission_classes=[IsPublicPageOrFollower])
    def unlike_tweet(self, request, **kwargs):

        """
        Unlike a Tweet.
        Permission is given to an Authenticated User.
        """

        serializer = LikeUnlikeTweetSerializer(data=request.data)
        if serializer.is_valid():
            tweet_id = serializer.validated_data.get("tweet_id")
            user_id = request.user.id
            unlike(tweet_id, user_id)
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    permissions_dict = {
        "create": [IsPublicPageOrFollower],
        "list": [IsPublicPageOrFollower | IsAdmin | IsModerator],
        "retrieve": [IsPublicPageOrFollower | IsAdmin | IsModerator],
        "update": [IsOwnerOfTweetOrComment],
        "partial_update": [IsOwnerOfTweetOrComment],
        "destroy": [IsOwnerOfTweetOrComment | IsModerator | IsAdmin],
    }

    def get_permissions(self):
        self.permission_classes = self.permissions_dict.get(self.action)
        return super().get_permissions()


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [IsAuthenticated]

