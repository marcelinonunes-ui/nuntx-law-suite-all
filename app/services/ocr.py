import os, requests
from pdfminer.high_level import extract_text
from docx import Document
API = os.getenv("OCR_SPACE_API_KEY")
def extract_text_from_file(path: str) -> str:
    try:
        if path.lower().endswith(".pdf"):
            txt = extract_text(path) or ""
            if not txt.strip() and API:
                with open(path, "rb") as f:
                    resp = requests.post("https://api.ocr.space/parse/image", data={"OCREngine": 2, "scale": True, "language": "por"}, files={"filename": f}, headers={"apikey": API})
                if resp.ok:
                    j = resp.json(); return "\n".join([p.get("ParsedText","") for p in j.get("ParsedResults", [])])
            return txt
        elif path.lower().endswith(".docx"):
            d = Document(path); return "\n".join([p.text for p in d.paragraphs])
        return ""
    except Exception: return ""
