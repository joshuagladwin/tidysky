from atproto import AtUri
from auth import bsky_login
from util import get_delete_date, get_record_date
from atproto_client import Client
from datetime import datetime


def get_old_posts(c: Client, del_date):
    print("Getting Old Posts...")
    post_records_ids = get_post_record_ids(c)
    old_post_records = get_old_post_records(c, post_records_ids, del_date)
    return old_post_records


def get_post_record_ids(c: Client):
    print("Getting Post Record IDs...")
    record_ids = []
    cursor = None
    while True:
        fetched = c.app.bsky.feed.post.list(repo=c.me.did, cursor=cursor, reverse=True)
        if not fetched.records:
            break
        record_ids += fetched.records
        if not fetched.cursor:
            break
        cursor = fetched.cursor
    return record_ids


def get_old_post_records(c: Client, p_record_ids, del_date):
    print("Getting Old Post Records...")
    records = []
    for r_id in p_record_ids:
        r_obj = c.app.bsky.feed.post.get(c.me.did, AtUri.from_str(r_id).rkey)
        if get_record_date(r_obj) < del_date:
            records.append(r_obj)
        else:
            break
    return records


def delete_posts(c: Client, post_list):
    print("Deleting Posts...")
    for i, post in enumerate(post_list):
        deleted_post = c.delete_post(post.uri)
        if deleted_post:
            print(f"Post Deleted! ({i+1}/{len(post_list)})", end="\n")


def delete_old_posts(c: Client, del_date: datetime):
    old_posts = get_old_posts(c, del_date)
    if old_posts:
        print(f"Total Old Posts to Delete: {len(old_posts)}")
        delete_posts(c, old_posts)
        print("Old Posts Deleted!")
    else:
        print("No Old Posts to Delete!")


if __name__ == "__main__":
    delete_date = get_delete_date()
    client = bsky_login()
    delete_old_posts(client, delete_date)
