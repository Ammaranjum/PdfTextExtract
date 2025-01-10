import spacy
import os
from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
from PyPDF2 import PdfReader
from docx import Document  # For reading .docx files
import mammoth  # Optional: For .doc files
import tempfile

# Load the pre-trained spaCy model for Named Entity Recognition (NER)
nlp = spacy.load('en_core_web_sm')

# Initialize Flask app
app = Flask(__name__)

# Configuration
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Function to extract text from docx files
def extract_text_from_docx(filepath):
    document = Document(filepath)
    text = '\n'.join([para.text for para in document.paragraphs])
    return text

# Function to extract text from doc files (using mammoth)
def extract_text_from_doc(filepath):
    with open(filepath, "rb") as doc_file:
        result = mammoth.extract_raw_text(doc_file)
        return result.value

# Route for the root URL with the form
@app.route('/')
def index():
    return '''
        <h1>Welcome to the Resume Text Extractor</h1>
        <h4>Rights owned by Ammar Anjum</h4>
        <p>Upload a PDF, DOCX, or DOC to extract text:</p>
        <form action="/extract" method="post" enctype="multipart/form-data">
            <input type="file" name="file" accept=".pdf,.docx,.doc" required>
            <button type="submit">Upload and Extract</button>
        </form>
    '''

# Route to upload a file and extract text
@app.route('/extract', methods=['POST'])
def extract_text():
    if 'file' not in request.files:
        return jsonify({"success": False, "message": "No file part in the request"}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({"success": False, "message": "No selected file"}), 400

    if file:
        try:
            # Save file to upload folder
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)

            # Determine file type and extract text
            text = ''
            if filename.lower().endswith('.pdf'):
                # Extract text from PDF
                with open(filepath, 'rb') as f:
                    reader = PdfReader(f)
                    for page in reader.pages:
                        text += page.extract_text()
            elif filename.lower().endswith('.docx'):
                # Extract text from DOCX
                text = extract_text_from_docx(filepath)
            elif filename.lower().endswith('.doc'):
                # Extract text from DOC
                text = extract_text_from_doc(filepath)
            else:
                return jsonify({"success": False, "message": "Unsupported file type"}), 400

            # Cleanup uploaded file
            os.remove(filepath)

            if not text.strip():
                return jsonify({"success": False, "message": "No text extracted from the file"}), 500

            # Analyze text using spaCy's NER (Named Entity Recognition)
            doc = nlp(text)
            extracted_data = {"names": [], "organizations": [], "dates": [], "skills": []}
            
            for ent in doc.ents:
                if ent.label_ == "PERSON":
                    extracted_data["names"].append(ent.text)
                elif ent.label_ == "ORG":
                    extracted_data["organizations"].append(ent.text)
                elif ent.label_ == "DATE":
                    extracted_data["dates"].append(ent.text)
            
            # Example: Search for skills
            skills = ['Python', 'Java', 'C++', 'SQL', 'JavaScript', 'Machine Learning', 'Data Science']
            for skill in skills:
                if skill.lower() in text.lower():
                    extracted_data["skills"].append(skill)

            return jsonify({"success": True, "data": extracted_data})

        except Exception as e:
            return jsonify({"success": False, "message": str(e)}), 500


if __name__ == '__main__':
    app.run(port=5000, debug=True)
