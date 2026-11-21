import csv
import math
from datetime import date, datetime, timedelta, timezone
from io import StringIO
from urllib.parse import urlencode
from urllib.request import urlopen


def read_vintage(text, vintage):
    reader = csv.DictReader(StringIO(text))
    series = f"DGS10_{vintage:%Y%m%d}"
    if reader.fieldnames not in (["observation_date", series], ["DATE", series]):
        raise ValueError("ALFRED CSV does not identify the requested DGS10 vintage.")
    observations = {}
    for row in reader:
        day = date.fromisoformat(row[reader.fieldnames[0]])
        value = row[series]
        if value in ("", "."):
            continue
        rate = float(value)
        if day > vintage or day in observations or not math.isfinite(rate):
            raise ValueError("Invalid DGS10 observations in the vintage.")
        observations[day] = rate
    day = max(observations, default=None)
    if day is None or (vintage - day).days > 7:
        raise ValueError("No valid DGS10 observation within seven days of the vintage.")
    return day, observations[day]


def fetch_signal(decision_date):
    vintage = decision_date - timedelta(days=1)
    params = urlencode({"id": "DGS10", "vintage_date": vintage.isoformat(),
                        "cosd": (vintage - timedelta(days=14)).isoformat(),
                        "coed": vintage.isoformat()})
    url = "https://alfred.stlouisfed.org/graph/alfredgraph.csv?" + params
    with urlopen(url, timeout=12) as response:
        observation, rate = read_vintage(response.read().decode("utf-8-sig"), vintage)
    return vintage, observation, rate, datetime.now(timezone.utc).isoformat(), url
