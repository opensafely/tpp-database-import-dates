import functools
import json
import os

import dateutil.parser

from analysis import OUTPUT_DIR

makedirs = functools.partial(os.makedirs, exist_ok=True)


def get_log():
    return [
        json.loads(line)
        for line in (OUTPUT_DIR / "query" / "log.json").read_text().splitlines()
    ]


def get_run_date():
    by_event = {d["event"]: d for d in get_log()}
    timestamp = by_event.get("finish_executing_sql_query", {}).get(
        "timestamp", "9999-01-01T00:00:00"
    )
    return dateutil.parser.parse(timestamp)
