import os, re, time, json
from bs4 import BeautifulSoup
import requests
from datetime import datetime
from tqdm import tqdm

BASE_URL = "https://discourse.onlinedegree.iitm.ac.in"
CATEGORY_URL = BASE_URL + "/c/courses/tds-kb/34?page={}"
THREAD_JSON_URL = BASE_URL + "/t/{slug}/{tid}.json"

HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Cookie":"_forum_session=uXSAzwkmweovjGToFIm0w%2FzwbespVKQBJ9vqmXYmEBOJ9FlVTg9rcRW9yjwDL7y4Ecl8nCZvSHrXEiBsjnN%2F0P7UknjYRJxtTyStn05umPHEyTlZsjbzyVNgh%2BcAu5xDC1I2LUatsICt5dpE0oHLiiK0x5agr3Zadj2s7QMAcScyU1UYimEYJTKBpgS9pmGRhZp64ddyY6V7GOKAMlRJmk9a99vubKt7B8VoJlk5G6Z3Y6s%2Bi86q2XJjUq%2FyHM2wQ5m%2BSj5w3UYMAZjgxwZVM063KwR5EZZsMt0MHw5aIf%2FFvjxjlthi8j5Ao%2BSW8kBWMS7VZrRASfxJpW5tLzwAfV4OkmHimqjjJq91hwkoldUpgC%2FmmWclaQrdWJeM8g%3D%3D--ntqfuZXcJC7gu9oo--8IX6iVeX4SRHUa%2BlRdemCw%3D%3D;_t=2y97jNOtI4SEuOjNHijqgCGp0rclozcLDzvmLKRlQjcLaKAPcKbH1Ro%2BJvI%2BS7mlXwKPdqtfuwWkUYL3a%2BHvCmjq0Y7X1mcpUqCe8oMs3HEulnr84CNmBH6Ea%2FD9zhXef5FAs3lUXP1Q7YZqqEmRebobRM6kT18ZBNIBNJh1NjX63HL9YxqixyaEXWRUzDkwuhlq2ARpTmmHoLgMn5E6hFzDk18F7s9AntI5lNbww%2FNWVyCLsjB4UgW2tM3POtq%2BvOv1usHCI%2BSuc3pq1YmV7R1plL8vNipdYTyCNI%2BRwxWJdlyX1j9q1g%3D%3D--lo9GhtNRYiuBwQRf--EXII8lIqxHWBMQ2eFDgeMQ%3D%3D"#add this to your env
}

JSON_DIR = "data/discourse_json"
MD_DIR = "data/markdowns"
os.makedirs(JSON_DIR, exist_ok=True)
os.makedirs(MD_DIR, exist_ok=True)

START_DATE = datetime.strptime("2025-01-01", "%Y-%m-%d").date()
END_DATE = datetime.strptime("2025-04-14", "%Y-%m-%d").date()

def fetch_html(page_num):
    r = requests.get(CATEGORY_URL.format(page_num), headers=HEADERS)
    return r.text if r.status_code == 200 else None
def extract_links(html):
    soup = BeautifulSoup(html, "html.parser")
    topics = []
    for a in soup.select("a.title"):
        href = a.get("href")
        print("🔗 Found href:", href)
        match = re.match(r"https?://[^/]+/t/([^/]+)/(\d+)", href or "")#type:ignore
        if match:
            slug, tid = match.groups()
            topics.append((slug, tid))
            print(f"✅ Matched: slug={slug}, tid={tid}")
        else:
            print("❌ No match:", href)
    return topics

def fetch_and_save_thread(slug, tid):
    url = THREAD_JSON_URL.format(slug=slug, tid=tid)
    r = requests.get(url, headers=HEADERS)
    if r.status_code == 200:
        data = r.json()
        with open(f"{JSON_DIR}/{tid}.json", "w") as f:
            json.dump(data, f, indent=2)

        posts = data.get("post_stream", {}).get("posts", [])
        title = data.get("title", "Untitled")
        date = datetime.strptime(posts[0]["created_at"][:10], "%Y-%m-%d").date()

        if not (START_DATE <= date <= END_DATE):
            return

        md_path = os.path.join(MD_DIR, f"discourse_{tid}.md")
        url_header = f"[Discourse Source]({BASE_URL}/t/{slug}/{tid})\n\n"
        body = f"# {title}\n\n" + url_header + "\n\n---\n\n".join(
            BeautifulSoup(p["cooked"], "html.parser").get_text() for p in posts
        )

        with open(md_path, "w", encoding="utf-8") as f:
            f.write(body)

def main():
    page = 0
    seen = set()
    while True:
        html = fetch_html(page)
        if not html:
            break
        new_links = extract_links(html)
        if not new_links:
            break  

        for slug, tid in tqdm(new_links, desc=f"Page {page}"):
            if tid not in seen:
                seen.add(tid)
                fetch_and_save_thread(slug, tid)
                time.sleep(1)

        page += 1

if __name__ == "__main__":
    main()