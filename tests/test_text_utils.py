from app.services.text_utils import clean_text, format_generated_text


def test_clean_text_matches_training_normalization():
    assert clean_text("Success comes from YOU!") == "success comes from you !"


def test_format_generated_text_punctuation():
    assert format_generated_text(["hello", ",", "world", "!"]) == "Hello, world!"


def test_format_generated_text_adds_final_period():
    assert format_generated_text(["hello", "world"]) == "Hello world."
