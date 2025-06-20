from atproto_client import Client
import os


def bsky_login() -> Client:

    username = os.environ["username"]
    password = os.environ["password"]

    c = Client()
    c.login(username, password)

    return c


if __name__ == "__main__":
    try:
        client = bsky_login()
        print(f"Successfully logged into: @{client.me.handle}")
    except Exception as error:
        print("Unable to log into account.\n")
        raise
