import os
from pathlib import Path

md_dir = Path("data/course_markdowns")

for md_file in md_dir.glob("*.md"):
    if "discourse" in md_file.name.lower():  
        continue

    with md_file.open("r+", encoding="utf-8") as f:
        content = f.read()
        if "tds.s-anand.net" in content:
            continue

        base_name = md_file.stem  
        course_url = f"https://tds.s-anand.net/#{base_name}"
        link = f"\n\n[Course Source Link]({course_url})\n"

        f.seek(0, os.SEEK_END)
        f.write(link)
        print(f"✅ Added link to {md_file.name}")
