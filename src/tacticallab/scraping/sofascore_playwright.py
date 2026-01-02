from playwright.sync_api import sync_playwright
import json
import os


def fetch_event(event_id: int):
    url = f"https://api.sofascore.com/api/v1/event/{event_id}"
    os.makedirs("data/raw/events", exist_ok=True)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent=(
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/117.0.0.0 Safari/537.36"
            ),
            locale="es-ES"
        )

        response = context.request.get(url)

        if response.status != 200:
            browser.close()
            raise Exception(f"HTTP {response.status}")

        data = response.json()
        browser.close()

    path = f"data/raw/events/{event_id}.json"
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

    print(f"✅ JSON guardado en {path}")


if __name__ == "__main__":
    fetch_event(13445957)
