from fastapi import APIRouter, HTTPException, Request, status

from app.core.config import APP_VERSION
from app.schemas.generation import GenerationRequest, GenerationResponse, HealthResponse

router = APIRouter()


@router.get("/health/live", tags=["health"])
def liveness() -> dict[str, str]:
    """Indicates that the API process is running."""
    return {"status": "alive"}


@router.get("/health/ready", response_model=HealthResponse, tags=["health"])
def readiness(request: Request) -> HealthResponse:
    service = getattr(request.app.state, "model_service", None)
    loaded = bool(service and service.is_loaded)
    if not loaded:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="Model is not ready")
    return HealthResponse(
        status="ready", model_loaded=True, model_name="sentence_generator_gru", version=APP_VERSION
    )


@router.post("/api/v1/generate", response_model=GenerationResponse, tags=["generation"])
def generate_text(payload: GenerationRequest, request: Request) -> GenerationResponse:
    service = getattr(request.app.state, "model_service", None)
    if not service or not service.is_loaded:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="Model is not ready")
    try:
        generated = service.generate(
            prompt=payload.prompt,
            sentence_count=payload.sentence_count,
            max_words_per_sentence=payload.max_words_per_sentence,
            max_new_tokens=payload.max_new_tokens,
            temperature=payload.temperature,
            top_k=payload.top_k,
        )
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(exc)) from exc
    except Exception as exc:
        # Keep internals out of the response; the full exception is logged by the server.
        import logging
        logging.getLogger(__name__).exception("Text generation failed")
        raise HTTPException(status_code=500, detail="Text generation failed") from exc

    return GenerationResponse(
        prompt=payload.prompt,
        generated_text=generated,
        sentence_count_requested=payload.sentence_count,
        max_words_per_sentence=payload.max_words_per_sentence,
        temperature=payload.temperature,
        top_k=payload.top_k,
    )
