# PDF Text Extractor

**PDF Text Extractor** is a tool that extracts text from PDF files and returns the extracted content in a structured JSON format. It uses **Flask** for the web interface, **PyPDF2** for PDF text extraction, and **spaCy** for advanced NLP tasks.

## Features

- **Upload PDFs** and extract text from them.
- **Extracted text** is returned in a structured JSON format.
- **spaCy integration** for advanced natural language processing tasks such as Named Entity Recognition (NER).

## Installation

1. Clone the repository or download the project.
2. Navigate to the project directory and set up a virtual environment:
   ```bash
   python -m venv .venv
   .\.venv\Scripts\Activate
   ```
3. Install the necessary dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Install **spaCy** and download the English language model:
   ```bash
   pip install spacy
   python -m spacy download en_core_web_sm
   ```

## Usage

1. **Run the Flask app**:

   ```bash
   python textExtract.py
   ```

2. Open your browser and go to `http://127.0.0.1:5000`.

3. **Upload a PDF** via the `/extract` route. The tool will extract the text and return it in JSON format.

## Example

- **Upload PDF**: Make a POST request to `/extract` with the PDF file.
- **Response**: The response will contain the extracted text in JSON format, like this:
  ```json
  {
    "success": true,
    "data": {
      "section_name": "Section Content",
      "another_section": "Another Section Content"
    }
  }
  ```

## Notes

- **spaCy** is used for advanced NLP tasks. Ensure that the spaCy library and the English language model are installed as shown in the installation steps.

## License

Open Source

---
