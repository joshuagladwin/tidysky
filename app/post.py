from auth import bsky_login
from util import parse_date, get_delete_date
from atproto_client import Client
from atproto_client.models.app.bsky.feed.defs import ReasonRepost
from datetime import datetime


def get_posts(c: Client):
    params = {"actor": c.me.handle}
    posts = []
    print("Getting Posts...")

    while True:
        fetched = c.app.bsky.feed.get_author_feed(params)
        if not fetched.feed:
            break
        posts += fetched.feed
        if not fetched.cursor:
            break
        params["cursor"] = fetched.cursor

    return posts


def filter_posts_to_delete(post_list, del_date):
    print("Filtering Old Posts to Delete...")
    filtered_posts = [post for post in post_list if get_post_date(post) < del_date]
    if len(filtered_posts) < 1:
        print("No Old Posts to Delete!")
    return filtered_posts


def get_post_date(post):
    if isinstance(post.reason, ReasonRepost):
        return parse_date(post.reason.indexed_at)
    else:
        return parse_date(post.post.record.created_at)


def delete_posts(c: Client, post_list):
    print("Deleting Old Posts...")
    for i, post in enumerate(post_list):
        if isinstance(post.reason, ReasonRepost):
            deleted_post = c.delete_repost(post.reason.model_extra["uri"])
        else:
            deleted_post = c.delete_post(post.post.uri)
        if deleted_post:
            print(f"Old Post Deleted! ({i+1}/{len(post_list)})", end="\n")
    print("Old Posts Deleted!")


def delete_old_posts(c: Client, del_date: datetime):
    posts = get_posts(c)
    print(f"Total Posts: {len(posts)}")
    posts_to_delete = filter_posts_to_delete(posts, del_date)
    if posts_to_delete:
        print(f"Total Old Posts to Delete: {len(posts_to_delete)}")
        delete_posts(c, posts_to_delete)


if __name__ == "__main__":
    delete_date = get_delete_date()
    client = bsky_login()
    delete_old_posts(client, delete_date)
