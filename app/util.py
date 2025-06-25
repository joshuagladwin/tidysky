from datetime import datetime, UTC, timedelta
import os


def parse_date(d: str) -> datetime:
    return datetime.fromisoformat(d)


def get_delete_date() -> datetime:
    delete_days_old = int(os.environ["DELETE_DAYS_OLD"])

    if delete_days_old < 0:
        raise ValueError("DELETE_DAYS_OLD must be number greater than 0")

    del_date = datetime.now(UTC) - timedelta(days=delete_days_old)
    print(
        f"Deleting Likes & Posts Before: {del_date.strftime('%a %d %b %Y %H:%M(%Z)')}",
        end="\n",
    )
    return del_date


if __name__ == "__main__":
    delete_date = get_delete_date()
    print(delete_date)
