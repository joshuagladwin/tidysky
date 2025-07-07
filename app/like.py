from auth import bsky_login
from atproto import AtUri
from atproto_client import Client
from util import get_delete_date, parse_date


def get_likes(c: Client):
    print("Getting Likes...")
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
    print("Filtering Old Likes to Delete...")
    filtered_likes = [r for r in like_list if get_like_date(r) < del_date]
    if len(filtered_likes) < 1:
        print("No Old Likes to Delete!")
    return filtered_likes


def get_like_date(r):
    return parse_date(r.value.created_at)


def delete_likes(c, likes_list):
    print("Deleting Old Likes...")
    for i, like in enumerate(likes_list):
        deleted_like = c.unlike(like.uri)
        if deleted_like:
            print(f"Old Like Deleted! ({i+1}/{len(likes_list)})", end="\n")
    print("Old Likes Deleted!", end="\n\n")


def delete_old_likes(c: Client, del_date):
    likes = get_likes(c)
    print(f"Total Likes: {len(likes)}")
    likes_to_delete = filter_likes_to_delete(likes, del_date)
    if likes_to_delete:
        print(f"Total Old Likes to Delete: {len(likes_to_delete)}")
        delete_likes(c, likes_to_delete)


if __name__ == "__main__":
    delete_date = get_delete_date()
    client = bsky_login()
    delete_old_likes(client, delete_date)
