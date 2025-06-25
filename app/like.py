from auth import bsky_login
from atproto import AtUri
from atproto_client import Client
from util import get_delete_date, parse_date


def get_likes(c: Client):
    like_posts = get_liked_posts(c)
    like_records = get_like_records(c, like_posts)
    return like_records


def get_liked_posts(c: Client):
    params = {"actor": c.me.handle}
    liked = []
    print("Getting Liked Posts...")

    while True:
        fetched = c.app.bsky.feed.get_actor_likes(params)
        if not fetched.feed:
            break
        liked += fetched.feed
        if not fetched.cursor:
            break
        params["cursor"] = fetched.cursor

    return liked


def get_like_records(c: Client, liked_list):
    print("Getting Like Records...")
    records = []
    for liked in liked_list:
        r = c.app.bsky.feed.like.get(
            c.me.did, AtUri.from_str(liked.post.viewer.like).rkey
        )
        records.append(r)

    return records


def filter_likes_to_delete(like_list, del_date):
    return [r for r in like_list if get_like_date(r) < del_date]


def get_like_date(r):
    return parse_date(r.value.created_at)


def delete_likes(c, likes_list):
    for i, like in enumerate(likes_list):
        deleted_like = c.unlike(like.uri)
        if deleted_like:
            print(print(f"Old Like deleted! ({i+1}/{len(likes_list)})", end="\n"))


def delete_old_likes(c: Client, del_date):
    print("Getting Likes...")
    likes = get_likes(c)
    print(f"Total Likes: {len(likes)}")
    print("Filtering Old Likes to Delete...")
    likes_to_delete = filter_likes_to_delete(likes, del_date)
    if len(likes_to_delete) < 1:
        print("No Old Likes to Delete!")
        return
    print(f"Total Old Likes to Delete: {len(likes_to_delete)}")
    delete_likes(c, likes_to_delete)
    print("Old Likes Deleted!", end="\n\n")


if __name__ == "__main__":
    delete_date = get_delete_date()
    client = bsky_login()
    delete_old_likes(client, delete_date)
