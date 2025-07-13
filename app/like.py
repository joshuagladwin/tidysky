from auth import bsky_login
from atproto import AtUri
from atproto_client import Client
from util import get_delete_date, get_record_date


def get_old_likes(c: Client, del_date):
    print("Getting Old Likes...")
    like_records_ids = get_like_record_ids(c)
    old_like_records = get_old_like_records(c, like_records_ids, del_date)
    return old_like_records


def get_like_record_ids(c: Client):
    print("Getting Like Record IDs...")
    record_ids = []
    cursor = None
    while True:
        fetched = c.app.bsky.feed.like.list(repo=c.me.did, cursor=cursor, reverse=True)
        if not fetched.records:
            break
        record_ids += fetched.records
        if not fetched.cursor:
            break
        cursor = fetched.cursor
    return record_ids


def get_old_like_records(c: Client, l_record_ids, del_date):
    print("Getting Old Like Records...")
    records = []
    for r_id in l_record_ids:
        r_obj = c.app.bsky.feed.like.get(c.me.did, AtUri.from_str(r_id).rkey)
        if get_record_date(r_obj) < del_date:
            records.append(r_obj)
        else:
            break
    return records


def delete_likes(c, likes_list):
    print("Deleting Likes...")
    for i, like in enumerate(likes_list):
        deleted_like = c.unlike(like.uri)
        if deleted_like:
            print(f"Like Deleted! ({i+1}/{len(likes_list)})", end="\n")


def delete_old_likes(c: Client, del_date):
    old_likes = get_old_likes(c, del_date)
    if old_likes:
        print(f"Total Old Likes to Delete Likes: {len(old_likes)}")
        delete_likes(c, old_likes)
        print("Old Likes Deleted!", end="\n\n")
    else:
        print("No Old Likes to Delete!")


if __name__ == "__main__":
    delete_date = get_delete_date()
    client = bsky_login()
    delete_old_likes(client, delete_date)
