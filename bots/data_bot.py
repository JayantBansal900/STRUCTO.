import os
import pandas as pd
import io
import fitz  # PyMuPDF for PDFs
from PIL import Image
import pytesseract
import requests

# Set path to tesseract.exe
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# Set environment variable for tessdata
os.environ["TESSDATA_PREFIX"] = r"C:\Program Files\Tesseract-OCR"

OPENROUTER_DATA_KEY = os.getenv("OPENROUTER_DATA_KEY")

def summarize_text_with_llm(text: str) -> str:
    try:
        headers = {
            "Authorization": f"Bearer {OPENROUTER_DATA_KEY}",
            "Content-Type": "application/json",
            "HTTP-Referer": "http://localhost",
            "X-Title": "PDF Summary Bot"
        }

        data = {
            "model": "openai/gpt-3.5-turbo",
            "messages": [
                {
                    "role": "system",
                    "content": "You are a summarizer bot. Read the given text and generate a clear, concise summary or notes in bullet points if possible."
                },
                {
                    "role": "user",
                    "content": f"Please summarize this PDF content:\n\n{text[:3000]}"
                }
            ]
        }

        response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=data)
        response.raise_for_status()
        result = response.json()
        return result["choices"][0]["message"]["content"].strip()

    except Exception as e:
        return f"Error while summarizing PDF: {str(e)}"

def analyze_file(file) -> str:
    filename = file.filename.lower()

    try:
        if filename.endswith('.csv'):
            content = file.read()
            df = pd.read_csv(io.BytesIO(content))
            summary = df.describe(include='all').to_string()
            return f"CSV Summary:\n\n{summary}"

        elif filename.endswith('.xlsx'):
            content = file.read()
            df = pd.read_excel(io.BytesIO(content))
            summary = df.describe(include='all').to_string()
            return f"Excel Summary:\n\n{summary}"

        elif filename.endswith('.pdf'):
            content = file.read()
            doc = fitz.open(stream=content, filetype='pdf')
            text = ""
            for page in doc:
                text += page.get_text()

            cleaned_text = text.strip()
            if not cleaned_text:
                return "PDF Extracted Text:\n\nNo readable text found."

            # Summarize using LLM
            summary = summarize_text_with_llm(cleaned_text)
            return f"📄 PDF Summary:\n\n{summary}"

        elif filename.endswith(('.png', '.jpg', '.jpeg')):
            image = Image.open(file.stream)
            text = pytesseract.image_to_string(image)
            return f"Image Extracted Text:\n\n{text.strip() or 'No text detected in image.'}"

        else:
            return "Unsupported file format. Only CSV, XLSX, PDF, JPG, PNG are supported."

    except Exception as e:
        return f"Error processing file: {str(e)}"
