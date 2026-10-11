# GRU Sentence Generator API — FastAPI & Docker

A deep learning text-generation project that serves a trained **Gated Recurrent Unit (GRU)** model through a REST API built with **FastAPI**. The application includes a browser-based interface, interactive API documentation, model health checks, and Docker containerization.

The trained model was originally developed in a Jupyter/Google Colab notebook and is reused for inference in this project.

## Project Links

- **GitHub Repository:** https://github.com/Lakshya3000/gru-sentence-generator-fastapi-docker
- **Docker Hub Image:** https://hub.docker.com/r/lakshyasanatani/gru-sentence-generator
- **Docker Image Tag:** `1.0.0`
- **Live Demo:** Not deployed yet

## Features

- Generate text from a user-provided prompt using a trained GRU model.
- REST API developed with FastAPI.
- Browser-based interface for interactive text generation.
- Swagger UI and OpenAPI documentation.
- Configurable generation settings, including temperature and top-k sampling.
- Request validation using Pydantic.
- Liveness and readiness health-check endpoints.
- Docker image for consistent deployment across environments.
- Automated tests for text-processing utilities.

## Technology Stack

- **Language:** Python
- **Deep Learning:** TensorFlow, Keras, GRU
- **API Framework:** FastAPI
- **ASGI Server:** Uvicorn
- **Validation:** Pydantic
- **Containerization:** Docker, Docker Compose
- **Testing:** Pytest

## Architecture

1. The user enters a prompt through the browser interface or sends an API request.
2. FastAPI validates the request.
3. The model service preprocesses the prompt using the training-compatible text-cleaning logic.
4. The trained GRU model generates text using the saved model and tokenizer artifacts.
5. The API returns the generated text as a JSON response.

## Project Structure

```text
gru-sentence-generator-fastapi-docker/
├── app/
│   ├── api/
│   │   └── routes.py
│   ├── core/
│   │   └── config.py
│   ├── schemas/
│   │   └── generation.py
│   ├── services/
│   │   ├── model_service.py
│   │   └── text_utils.py
│   ├── static/
│   │   └── index.html
│   └── main.py
├── artifacts/
│   ├── sentence_generator_gru.keras
│   ├── tokenizer.pkl
│   └── max_len.pkl
├── notebooks/
│   └── Sentence_Generator_GRU.ipynb
├── scripts/
│   └── smoke_test.ps1
├── tests/
│   └── test_text_utils.py
├── .dockerignore
├── .env.example
├── .gitignore
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── requirements-dev.txt
└── README.md
```

## Getting Started

### Option 1: Run with Docker (Recommended)

Install [Docker Desktop](https://www.docker.com/products/docker-desktop/) and ensure it is running.

Pull the published image:

```bash
docker pull lakshyasanatani/gru-sentence-generator:1.0.0
```

Run the container:

```bash
docker run -d --name gru-sentence-generator -p 8000:8000 lakshyasanatani/gru-sentence-generator:1.0.0
```

Open the application:

- **Browser UI:** http://localhost:8000
- **Swagger API Docs:** http://localhost:8000/docs
- **Readiness Check:** http://localhost:8000/health/ready
- **Liveness Check:** http://localhost:8000/health/live

To view container logs:

```bash
docker logs -f gru-sentence-generator
```

To stop and remove the container:

```bash
docker stop gru-sentence-generator
docker rm gru-sentence-generator
```

### Option 2: Run with Docker Compose

From the project root, run:

```bash
docker compose up --build
```

Open http://localhost:8000 in your browser.

Stop the Compose application with:

```bash
docker compose down
```

### Option 3: Run Locally on Windows

Python 3.13 is used by the current project setup.

Create a virtual environment:

```powershell
py -3.13 -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Install the dependencies:

```powershell
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

Start the API:

```powershell
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000
```

Open http://127.0.0.1:8000.

Keep the terminal running while using the local application.

## API Documentation

FastAPI automatically provides interactive documentation at `/docs`.

### `POST /api/v1/generate`

Example request:

```json
{
  "prompt": "success comes from",
  "sentence_count": 4,
  "max_words_per_sentence": 20,
  "max_new_tokens": 120,
  "temperature": 0.8,
  "top_k": 8
}
```

Example PowerShell request:

```powershell
$body = @{
    prompt = "success comes from"
    sentence_count = 4
    max_words_per_sentence = 20
    max_new_tokens = 120
    temperature = 0.8
    top_k = 8
} | ConvertTo-Json

Invoke-RestMethod `
    -Uri "http://127.0.0.1:8000/api/v1/generate" `
    -Method Post `
    -ContentType "application/json" `
    -Body $body
```

The response includes the generated text and generation settings. The generated output can vary between requests because sampling is stochastic.

### Request Parameters

| Parameter | Default | Allowed range |
|---|---:|---|
| `prompt` | Required | 1–2000 characters |
| `sentence_count` | 4 | 1–10 |
| `max_words_per_sentence` | 20 | 5–80 |
| `max_new_tokens` | 120 | 1–250 |
| `temperature` | 0.8 | 0.3–1.5 |
| `top_k` | 8 | 1–50 |

Invalid requests return a validation error.

## Health Checks

| Endpoint | Purpose |
|---|---|
| `GET /health/live` | Checks whether the application process is alive |
| `GET /health/ready` | Checks whether the model is ready to serve requests |

The readiness endpoint can return HTTP 503 if the model has not loaded successfully.

## Run Tests

Install development dependencies:

```bash
python -m pip install -r requirements-dev.txt
```

Run the test suite:

```bash
python -m pytest -q
```

## Model and Implementation Notes

- The model is loaded from the saved `.keras` file; the application does not retrain it at startup.
- The saved tokenizer and maximum input length are loaded from the artifacts directory.
- Inference preprocessing follows the original training notebook's text-cleaning and padding conventions.
- The API uses one worker by default to avoid loading multiple copies of the model into memory.
- The `tokenizer.pkl` and `max_len.pkl` files use Python pickle and should only be loaded from trusted sources.
- Text quality depends on the trained model and training data. Deploying the model through FastAPI and Docker does not itself improve generation quality.

## Deployment and Security

The Docker image is published on Docker Hub and can be run locally or used as the basis for a cloud deployment.

**A public live demo is not available yet.**

Before exposing the generation API publicly, consider adding rate limiting, request and concurrency limits, monitoring, and appropriate access controls. Do not expose secrets in the repository or Docker image.

A free cloud service may sleep when idle, take time to start, or lack sufficient memory for TensorFlow model inference. Test the deployment and monitor its logs before sharing the URL.

## Future Improvements

- Deploy the API to a cloud hosting platform.
- Add rate limiting and stronger request controls.
- Add integration tests for API endpoints.
- Improve model evaluation and generated-text coherence.
- Add a demo screenshot and a public live-demo link when deployment is complete.

## Author

**Lakshya3000**

If you find this project useful, you can explore the source code and Docker image through the links at the top of this README.
