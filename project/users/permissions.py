from rest_framework.permissions import BasePermission

# from tweets.models import Page


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == "admin"

    def has_object_permission(self, request, view, obj):
        return request.user.role == "admin"


class IsModerator(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == "moderator"


class IsUser(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == "user"


class OwnUserAccount(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj == request.user


class IsOwnerOfPage(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user


class IsOwnerOfTweetOrComment(BasePermission):
    def has_object_permission(self, request, view, obj):
        owner_request = request.data.get("owner")
        return obj.owner_id == int(owner_request)


class IsPublicPageOrFollower(BasePermission):
    def has_object_permission(self, request, view, obj):
        page_id = request.data.get("page_id")
        user_id = request.user.id
        page = Page.objects.get(pk=page_id)
        page_queryset = Page.objects.filter(pk=page_id)
        followers = page_queryset.values_list("followers", flat=True)
        if (not request.user.is_authenticated) or (user_id not in followers):
            return False
        if page.is_private and user_id in followers:
            return True
        return False
