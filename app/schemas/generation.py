from pydantic import BaseModel, Field, field_validator


class GenerationRequest(BaseModel):
    prompt: str = Field(min_length=1, max_length=2000, description="Text that seeds generation")
    sentence_count: int = Field(default=4, ge=1, le=10)
    max_words_per_sentence: int = Field(default=20, ge=5, le=80)
    max_new_tokens: int = Field(default=120, ge=1, le=250)
    temperature: float = Field(default=0.8, ge=0.3, le=1.5)
    top_k: int = Field(default=8, ge=1, le=50)

    @field_validator("prompt")
    @classmethod
    def prompt_must_not_be_blank(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("prompt must not be blank")
        return value


class GenerationResponse(BaseModel):
    prompt: str
    generated_text: str
    sentence_count_requested: int
    max_words_per_sentence: int
    temperature: float
    top_k: int


class HealthResponse(BaseModel):
    status: str
    model_loaded: bool
    model_name: str
    version: str
