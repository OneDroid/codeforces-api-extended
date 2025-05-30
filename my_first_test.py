import json
from seleniumbase import SB

with SB(test=True, uc=True) as sb:
    sb.open("https://google.com/ncr")
    sb.type('[title="Search"]', "SeleniumBase GitHub page\n")
    sb.click('[href*="github.com/seleniumbase/"]')
    print(sb.get_page_title())

    results = []
    results.append({
        "text": "Hello World222!!!!!!!!!5!",
    })

    # Write the extracted data to a JSON file
    with open("data.json", "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
