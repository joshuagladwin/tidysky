from atproto import AtUri
from auth import bsky_login
from util import get_delete_date, get_record_date
from atproto_client import Client
from datetime import datetime


def get_old_reposts(c: Client, del_date):
    print("Getting Old Reposts...")
    repost_records_ids = get_repost_record_ids(c)
    old_repost_records = get_old_repost_records(c, repost_records_ids, del_date)
    return old_repost_records


def get_repost_record_ids(c: Client):
    print("Getting Repost Record IDs...")
    record_ids = []
    cursor = None
    while True:
        fetched = c.app.bsky.feed.repost.list(
            repo=c.me.did, cursor=cursor, reverse=True
        )
        if not fetched.records:
            break
        record_ids += fetched.records
        if not fetched.cursor:
            break
        cursor = fetched.cursor
    return record_ids


def get_old_repost_records(c: Client, r_record_ids, del_date):
    print("Getting Old Repost Records...")
    records = []
    for r_id in r_record_ids:
        r_obj = c.app.bsky.feed.repost.get(c.me.did, AtUri.from_str(r_id).rkey)
        if get_record_date(r_obj) < del_date:
            records.append(r_obj)
        else:
            break
    return records


def delete_reposts(c: Client, repost_list):
    print("Deleting Reposts...")
    for i, repost in enumerate(repost_list):
        deleted_repost = c.delete_repost(repost.uri)
        if deleted_repost:
            print(f"Repost Deleted! ({i+1}/{len(repost_list)})", end="\n")


def delete_old_reposts(c: Client, del_date: datetime):
    old_reposts = get_old_reposts(c, del_date)
    if old_reposts:
        print(f"Total Old Reposts to Delete: {len(old_reposts)}")
        delete_reposts(c, old_reposts)
        print("Old Reposts Deleted!")
    else:
        print("No Old Reposts to Delete!")


if __name__ == "__main__":
    delete_date = get_delete_date()
    client = bsky_login()
    delete_old_reposts(client, delete_date)
