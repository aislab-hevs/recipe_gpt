
def transform_title(text: str):
    new_text = text.strip()
    if "-" in text:
        new_text = text.split("-")[0]
    return new_text
