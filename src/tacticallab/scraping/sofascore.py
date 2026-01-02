import requests
import os
import json


def fetch_event(event_id):
    """
    Consulta el endpoint de SofaScore emulando la app móvil
    y guarda el JSON crudo en data/raw/events/
    """

    url = f"https://api.sofascore.com/api/v1/event/{event_id}"

    headers = {
        "User-Agent": "okhttp/4.9.3",
        "Accept": "application/json",
        "Accept-Language": "es-ES",
        "Accept-Encoding": "gzip",
        "Connection": "close",
        "X-Requested-With": "com.sofascore.results"
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()

    except requests.exceptions.RequestException as e:
        print(f"Error al consultar SofaScore: {e}")
        return
    except json.JSONDecodeError:
        print("Error: la respuesta no es un JSON válido")
        return

    raw_dir = "data/raw/events"
    os.makedirs(raw_dir, exist_ok=True)

    file_path = os.path.join(raw_dir, f"{event_id}.json")

    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

    print(f"✅ JSON crudo guardado en: {file_path}")


if __name__ == "__main__":
    fetch_event(13445957)
