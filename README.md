# WeatherDataCollectorMini

**Ultra-simple, free, no API key** weather-to-CSV demo using the **Open-Meteo** API.
- One tiny script
- No scheduling
- GitHub Actions CI included

## Run locally

```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python -m src.collect --city "London"
```

This writes `data/weather_YYYY-MM-DD.csv`.

## Project layout

```
WeatherDataCollectorMini/
├─ src/
│  └─ collect.py
├─ data/                      # CSV output
├─ tests/
│  └─ test_collect.py
├─ .github/workflows/
│  └─ ci.yml                  # CI on push/PR
├─ .gitignore
├─ requirements.txt
└─ README.md
```

## GitHub Actions (CI/CD)

1. Create a new GitHub repo and push this folder.
2. Actions will run automatically on push and Pull Requests:
   - Install deps
   - Run tests (fast, offline; API calls are mocked)

### Optional: manual "Collect Weather" run
You can trigger the included workflow **manually** from the Actions tab (workflow: *Collect Weather*).  
It will run the script against the live API and upload the CSV as a build artifact for download.

> We keep CI fast and reliable by mocking HTTP calls in tests. The manual job is there if you want to verify the end-to-end call without committing files back to the repo.

## Learn more

- Open-Meteo API: https://open-meteo.com/en/docs
- Python requests: https://requests.readthedocs.io/
- CSV module: https://docs.python.org/3/library/csv.html
- Pytest: https://docs.pytest.org/
