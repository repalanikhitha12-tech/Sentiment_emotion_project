import pandas as pd


ALLOWED_EXTENSIONS = {".txt", ".csv"}


def validate_text(text):
    """Check whether text is valid and non-empty."""

    if text is None:
        return False, "No text was provided."

    if not isinstance(text, str):
        return False, "Input must be text."

    if text.strip() == "":
        return False, "Input text is empty."

    return True, "Valid text."


def read_txt_file(file):
    """Read text from a TXT file."""

    try:
        content = file.read().decode("utf-8")

        valid, message = validate_text(content)

        if not valid:
            return None, message

        return content, "TXT file read successfully."

    except UnicodeDecodeError:
        return None, "TXT file must use UTF-8 encoding."

    except Exception as e:
        return None, f"Error reading TXT file: {e}"


def read_csv_file(file):
    """Read text from a CSV file."""

    try:
        df = pd.read_csv(file)

        if df.empty:
            return None, "CSV file is empty."

        # Look for a column named 'text'
        if "text" not in df.columns:
            return None, "CSV must contain a 'text' column."

        # Remove empty values
        text_data = df["text"].dropna().astype(str)

        # Remove rows containing only spaces
        text_data = text_data[text_data.str.strip() != ""]

        if text_data.empty:
            return None, "CSV does not contain valid text."

        # Combine all text rows
        combined_text = "\n".join(text_data.tolist())

        return combined_text, "CSV file read successfully."

    except Exception as e:
        return None, f"Error reading CSV: {e}"