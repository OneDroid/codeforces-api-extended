import json
from seleniumbase import SB

with SB(uc=True, test=True, locale_code="en", pls="none") as sb:
    url = "https://www.nike.com/"
    sb.activate_cdp_mode(url)
    sb.sleep(2.5)
    sb.cdp.mouse_click('div[data-testid="user-tools-container"]')
    sb.sleep(1.5)
    search = "Nike Air Force 1"
    sb.cdp.press_keys('input[type="search"]', search)
    sb.sleep(4)
    elements = sb.cdp.select_all('ul[data-testid*="products"] figure .details')

    results = []
    for element in elements:
        # Extract text content
        text = element.text.strip()
        # Extract additional attributes if needed
        # For example, to get the href of a link inside the element:
        # link_element = element.query_selector('a')
        # href = link_element.get_attribute('href') if link_element else None

        results.append({
            "text": text,
            # "href": href  # Uncomment if extracting href
        })

    # Write the extracted data to a JSON file
    with open("data.json", "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

    sb.sleep(2)
