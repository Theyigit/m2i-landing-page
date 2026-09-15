#!/usr/bin/env python3
"""
Pushes every URL in the live sitemap to IndexNow (Bing, Yandex, Seznam, Naver
and others pick it up within minutes). Google does not support IndexNow; for
Google the sitemap is resubmitted from Search Console.

The key is in scripts/indexnow.key and the matching public/<key>.txt is
deployed with the site, which is how IndexNow verifies ownership.
"""

import json
import re
import subprocess
import sys
from pathlib import Path

SITE = "https://www.movingtoireland.co"
KEY = (Path(__file__).with_name("indexnow.key")).read_text().strip()


def fetch(url: str) -> str:
    # curl rather than urllib: the python.org build has no CA bundle by default.
    return subprocess.run(["curl", "-sSf", url], check=True, capture_output=True, text=True).stdout


def sitemap_urls() -> list[str]:
    index = fetch(f"{SITE}/sitemap-index.xml")
    urls: list[str] = []
    for sm in re.findall(r"<loc>(.*?)</loc>", index):
        urls += re.findall(r"<loc>(.*?)</loc>", fetch(sm))
    return sorted(set(urls))


def main() -> None:
    urls = sitemap_urls()
    if len(sys.argv) > 1:
        urls = [u for u in urls if any(p in u for p in sys.argv[1:])]
    body = json.dumps({"host": "www.movingtoireland.co", "key": KEY, "keyLocation": f"{SITE}/{KEY}.txt", "urlList": urls}).encode()
    status = subprocess.run(
        ["curl", "-s", "-o", "/dev/null", "-w", "%{http_code}", "-X", "POST",
         "-H", "Content-Type: application/json; charset=utf-8", "--data-binary", "@-",
         "https://api.indexnow.org/indexnow"],
        input=body, capture_output=True, check=True,
    ).stdout.decode()
    print(f"IndexNow: HTTP {status} for {len(urls)} URLs")


if __name__ == "__main__":
    main()
