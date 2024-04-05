
def transform_title(text: str):
    new_text = text.strip()
    if "-" in text:
        new_text = text.split("-")[0]
    return new_text


def check_nan_columns(df):
    empty_cols = {}
    for col in df.columns:
        num_empty = sum(df[col].isna())
        if num_empty > 0:
            empty_cols[col] = num_empty
    return empty_cols