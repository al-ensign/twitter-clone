from datetime import datetime

from .models import Page, Tweet


def save_path_s3(page_id, file_name):

    """
    Sets s3 path to a file.
    """

    page = Page.objects.get(pk=page_id)
    page.path = file_name
    return page.save()


def get_page_s3_path(page_id):

    """
    Returns s3 path to a file.
    """

    page = Page.objects.get(pk=page_id)
    return page.path


def block_page_temporary(page_id, unblock_date):
    """
    Block a Page for a specific time period.
    Sets Page.unblock_date to the requested date.
    """

    page = Page.objects.get(pk=page_id)
    page.is_blocked = True
    page.unblock_date = unblock_date
    return page.save()


def block_page_unlimited(page_id):
    """
    Block a Page forever.
    Sets Page.unblock_date = datetime.max.
    """

    page = Page.objects.get(pk=page_id)
    page.is_blocked = True
    page.unblock_date = datetime.max
    return page.save()


def send_follow_request(user_id, page_to_follow_id):
    """
    Send a follow request to someone's Page.
    User can follow a Page only from one of their pages.
    If the Target Page is Private, User's ID will be stored in Page.follow_requests.
    However, if the Page is Public, User's ID will be directly stored in Page.followers.
    """

    target_page = Page.objects.get(pk=page_to_follow_id)
    page_queryset = Page.objects.filter(pk=page_to_follow_id)
    follow_requests = page_queryset.values_list("follow_requests", flat=True)
    followers = page_queryset.values_list("followers", flat=True)
    if target_page.is_private:
        if int(user_id) in follow_requests:
            return None
        elif int(user_id) in followers:
            return None
        else:
            target_page.follow_requests.add(user_id)
            return target_page.save()
    else:
        if int(user_id) in followers:
            return None
        else:
            target_page.followers.add(user_id)
            return target_page.save()


def accept_one_follow_request(page_id, user_id):
    """
    Accept a specific follow request.
    Moves User's ID from Page.follow_requests to Page.followers.
    """

    page_queryset = Page.objects.filter(pk=page_id)
    page = Page.objects.get(pk=page_id)
    follow_requests = page_queryset.values_list("follow_requests", flat=True)

    if int(user_id) in follow_requests:
        page.followers.add(user_id)
        page.follow_requests.remove(user_id)
        return page.save()


def accept_all_follow_requests(page_id):
    """
    Accept all the incoming follow requests.
    Moves all the Users' IDs from Page.follow_requests to Page.followers.
    """

    page = Page.objects.get(pk=page_id)
    page_queryset = Page.objects.filter(pk=page_id)
    follow_requests = page_queryset.values_list("follow_requests", flat=True)
    for user_id in follow_requests:
        page.followers.add(user_id)
        page.follow_requests.remove(user_id)
        return page.save()


def reject_one_follow_request(page_id, user_id):
    """
    Delete/Reject a specific follow request.
    Removes User's ID from Page.follow_requests.
    """

    page = Page.objects.get(pk=page_id)
    page_queryset = Page.objects.filter(pk=page_id)
    follow_requests = page_queryset.values_list("follow_requests", flat=True)
    if int(user_id) in follow_requests:
        page.follow_requests.remove(user_id)
        return page.save()


def reject_all_follow_requests(page_id):
    """
    Delete/Reject all follow requests.
    Removes all the Users' IDs from Page.follow_requests.
    """

    page = Page.objects.get(pk=page_id)
    page_queryset = Page.objects.filter(pk=page_id)
    follow_requests = page_queryset.values_list("follow_requests", flat=True)
    for user_id in follow_requests:
        page.follow_requests.remove(user_id)
        return page.save()


def unfollow(page_id, user_id):
    """
    Unfollow a Page.
    Removes User's ID from Page.followers.
    """

    page = Page.objects.get(pk=page_id)
    page_queryset = Page.objects.filter(pk=page_id)
    followers = page_queryset.values_list("followers", flat=True)
    if int(user_id) not in followers:
        return None
    else:
        page.followers.remove(user_id)
        return page.save()


def like(tweet_id, user_id):
    """
    Like a Tweet.
    Stores User's ID in Tweet.like
    """

    tweet = Tweet.objects.get(pk=tweet_id)
    tweet_queryset = Tweet.objects.filter(pk=tweet_id)
    likes = tweet_queryset.values_list("like", flat=True)
    if user_id in likes:
        return None
    else:
        tweet.like.add(user_id)
        return tweet.save()


def unlike(tweet_id, user_id):
    """
    Unlike a Tweet.
    Removes User's ID from Tweet.like
    """
    tweet = Tweet.objects.get(pk=tweet_id)
    tweet_queryset = Tweet.objects.filter(pk=tweet_id)
    likes = tweet_queryset.values_list("like", flat=True)

    if user_id not in likes:
        return None
    else:
        tweet.like.remove(user_id)
        return tweet.save()
