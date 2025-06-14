import json
from seleniumbase import SB

with SB(test=True, uc=True) as sb:

    sb.open("https://google.com/ncr")
    sb.type('[title="Search"]', "Tawhid Monowar\n")
    print(sb.get_page_title())

    results = []
    results.append({
        "text": sb.get_page_title(),
    })

    # Write the extracted data to a JSON file
    with open("data.json", "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
