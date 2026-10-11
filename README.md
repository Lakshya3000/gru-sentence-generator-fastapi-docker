# 02_Project_Sentence_Generator_GRU — FastAPI + Docker

A production-oriented refactor of the Colab-trained GRU text-generation model. The trained model is reused; this project does **not** retrain it. FastAPI exposes a JSON API and serves a small browser UI from the same process.

## Features

- Loads the `.keras` model, Keras `Tokenizer`, and `max_len.pkl` once at startup.
- `POST /api/v1/generate` generates text with temperature and top-k sampling.
- `GET /health/live` and `GET /health/ready` support container health checks.
- Interactive UI at `/`; Swagger/OpenAPI docs at `/docs`.
- Docker image runs as a non-root user.
- Request validation and bounded generation settings.

## Project structure

```text
02_Project_Sentence_Generator_GRU/
├── app/
│   ├── main.py                 # FastAPI app and lifespan startup
│   ├── api/routes.py           # HTTP endpoints
│   ├── core/config.py          # Environment-based configuration
│   ├── schemas/generation.py   # Request/response validation
│   ├── services/
│   │   ├── model_service.py    # Model loading and inference
│   │   └── text_utils.py       # Training-compatible text cleanup
│   └── static/index.html       # Browser UI calling the API
├── artifacts/
│   ├── sentence_generator_gru.keras
│   ├── tokenizer.pkl
│   └── max_len.pkl
├── notebooks/Sentence_Generator_GRU.ipynb
├── tests/test_text_utils.py
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md
```

## 1. Run locally on Windows

Use Python 3.13 and a virtual environment. From this project root in PowerShell:

```powershell
py -3.13 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000
```

Open:

- UI: <http://127.0.0.1:8000>
- Swagger docs: <http://127.0.0.1:8000/docs>
- Readiness: <http://127.0.0.1:8000/health/ready>

Model startup can take a few seconds. Keep the terminal running while testing the app.

### Example API request

PowerShell:

```powershell
$body = @{
  prompt = "success comes from"
  sentence_count = 4
  max_words_per_sentence = 20
  max_new_tokens = 120
  temperature = 0.8
  top_k = 8
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://127.0.0.1:8000/api/v1/generate" -Method Post -ContentType "application/json" -Body $body
```

Example JSON shape:

```json
{
  "prompt": "success comes from",
  "generated_text": "...generated text...",
  "sentence_count_requested": 4,
  "max_words_per_sentence": 20,
  "temperature": 0.8,
  "top_k": 8
}
```

Generated text will vary because sampling is stochastic; the example above shows the response shape, not a guaranteed output.

## 2. Run with Docker

Install and start Docker Desktop first. From the project root:

```powershell
docker compose build
docker compose up
```

Then open <http://localhost:8000>. Stop with `Ctrl+C`; to stop/remove the container:

```powershell
docker compose down
```

The first build downloads TensorFlow and can take a while. The model artifacts are copied into the image, so the image is larger than a basic API image.

### Build and run without Compose

```powershell
docker build -t gru-sentence-generator:1.0.0 .
docker run --rm -p 8000:8000 gru-sentence-generator:1.0.0
```

## 3. Run tests

```powershell
python -m pip install -r requirements-dev.txt
python -m pytest -q
```

## API contract

### `POST /api/v1/generate`

Request fields:

| Field | Type | Default | Allowed range |
|---|---|---:|---|
| `prompt` | string | required | 1–2000 characters, not blank |
| `sentence_count` | integer | 4 | 1–10 |
| `max_words_per_sentence` | integer | 20 | 5–80 |
| `max_new_tokens` | integer | 120 | 1–250 |
| `temperature` | number | 0.8 | 0.3–1.5 |
| `top_k` | integer | 8 | 1–50 |

Errors from request validation return HTTP 422. Readiness returns HTTP 503 if the model has not loaded.

## Important implementation notes

1. **Training preprocessing is preserved.** The Colab notebook lowercases text, normalizes Unicode/apostrophes, separates `. ! ?`, and filters unsupported characters. Inference uses the same cleanup.
2. **Padding was aligned with training.** Your notebook used `padding="post"` and `truncating="pre"`; inference now does the same. This differs from the older Streamlit script, which used pre-padding.
3. **Inference uses `compile=False`.** Optimizer/loss state is unnecessary for generation and is not loaded.
4. **Trusted pickle files only.** `tokenizer.pkl` and `max_len.pkl` use Python pickle. Never replace these with files from an untrusted source, because unpickling can execute code.
5. **One worker by default.** The model is loaded once per process. Each additional Uvicorn worker loads another copy of the model and increases RAM usage. Start with one worker and measure before scaling.
6. **Not fully secured for public internet exposure yet.** Before making this public, add authentication/rate limiting, request and concurrency limits, HTTPS at a reverse proxy, structured monitoring, and a deployment secret/configuration strategy. Do not expose the development server directly to the internet.
7. **Text quality is separate from API reliability.** This API serves your existing trained model. Better coherence may require improved training data, model evaluation, and retraining; FastAPI/Docker do not improve model quality by themselves.

## Environment configuration

The defaults work for local development and Docker. Optional variables:

- `APP_NAME`
- `APP_VERSION`
- `MODEL_DIR`
- `MODEL_FILE`
- `TOKENIZER_FILE`
- `MAX_LEN_FILE`

For Docker, `MODEL_DIR` defaults to `/app/artifacts`.
