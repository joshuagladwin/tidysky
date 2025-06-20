from app.auth import bsky_login
from app.like import delete_old_likes
from app.post import delete_old_posts
from app.util import get_delete_date


def main():

    delete_date = get_delete_date()
    client = bsky_login()
    delete_old_likes(client, delete_date)
    delete_old_posts(client, delete_date)


if __name__ == "__main__":
    main()
