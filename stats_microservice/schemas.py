from pydantic import BaseModel
from typing import List


class TweetBase(BaseModel):
    tweet_id: int
    likes: int

    class Config():
        orm_mode = True


class ShowPageWithTweetsList(BaseModel):
    page_id: int
    owner_id: int
    followers: int
    follow_requests: int
    is_blocked: bool
    tweets: List[TweetBase] = []

    class Config():
        orm_mode = True


class Tweet(BaseModel):
    tweet_id: int
    owner_id: int
    likes: int

    class Config():
        orm_mode = True


class Page(BaseModel):
    page_id: int
    owner_id: int
    followers: int
    follow_requests: int
    is_blocked: bool

    class Config():
        orm_mode = True
