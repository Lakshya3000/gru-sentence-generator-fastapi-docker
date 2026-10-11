import re
import unicodedata


def clean_text(text: str) -> str:
    """Match the text normalization used in the Colab training notebook."""
    text = unicodedata.normalize("NFKC", str(text)).lower()
    text = text.replace("’", "'").replace("‘", "'")
    text = re.sub(r"([.!?])", r" \1 ", text)
    text = re.sub(r"[^a-z0-9'\s.,!?;:]", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def format_generated_text(tokens: list[str]) -> str:
    text = " ".join(tokens)
    text = re.sub(r"\s+([.,!?;:])", r"\1", text)
    text = re.sub(r"\s+", " ", text).strip()
    if not text:
        return text
    text = text[0].upper() + text[1:]
    text = re.sub(r"([.!?]\s+)([a-z])", lambda m: m.group(1) + m.group(2).upper(), text)
    if text[-1] not in ".!?":
        text += "."
    return text
