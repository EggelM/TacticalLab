from playwright.sync_api import sync_playwright
import json
from pathlib import Path

# 📌 Raíz del proyecto (TacticalLab/)
BASE_DIR = Path(__file__).resolve().parents[3]

DATA_RAW_LINEUPS = BASE_DIR / "data" / "raw" / "lineups"


def fetch_lineups(event_id: int):
    url = f"https://api.sofascore.com/api/v1/event/{event_id}/lineups"

    DATA_RAW_LINEUPS.mkdir(parents=True, exist_ok=True)

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

    output_path = DATA_RAW_LINEUPS / f"{event_id}.json"
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

    print(f"✅ Lineups guardados en {output_path}")


if __name__ == "__main__":
    fetch_lineups(13445957)
