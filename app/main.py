from auth import bsky_login
from like import delete_old_likes
from post import delete_old_posts
from util import get_delete_date


def main():

    delete_date = get_delete_date()
    client = bsky_login()
    delete_old_likes(client, delete_date)
    delete_old_posts(client, delete_date)


if __name__ == "__main__":
    main()
