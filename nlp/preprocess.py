
import re
import string

def preprocess_text(text):
    text = text.lower()
    text = re.sub(f"[{string.punctuation}]", "", text)
    text = re.sub("\s+", " ", text)
    return text.strip()
