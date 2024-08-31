import nltk
import ssl
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from docx import Document
import os

# SSL workaround for NLTK downloads, _creat_unver....function modifies the transport layer security
try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

# Download necessary NLTK data
nltk.download('wordnet')
nltk.download('omw-1.4')
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('punkt_tab') 

# Print NLTK data path
print("NLTK Data Path:", nltk.data.path)

# Function to extract text from a .docx file
def read_docx(file_path):
    doc = Document(file_path)
    full_text = []
    for para in doc.paragraphs:
        full_text.append(para.text)
    return ' '.join(full_text)

# Function to clean and tokenize text
def clean_and_tokenize(text):
    try:
        # Convert to lowercase
        text = text.lower()
        # Tokenize text
        tokens = word_tokenize(text)
        # Remove stopwords
        stop_words = set(stopwords.words('english'))
        filtered_tokens = [word for word in tokens if word not in stop_words and word.isalnum()]
        return filtered_tokens
    except LookupError as e:
        print(f"Error: {e}")
        print("NLTK data might not be properly installed or accessible.")
        return []

# List of file paths
file_paths = ['data1.docx', 'BitcoindocforNLP.docx', 'data101.docx']

# Loop through each file path, read and process the document
all_tokens = []
for file_path in file_paths:
    try:
        if not os.path.exists(file_path):
            print(f"File not found: {file_path}")
            continue
        text = read_docx(file_path)
        tokens = clean_and_tokenize(text)
        all_tokens.append(tokens)
    except Exception as e:
        print(f"Error processing file {file_path}: {e}")

# Now all_tokens contains the tokens of each document
for i, tokens in enumerate(all_tokens):
    print(f"Tokens from document {i+1}:")
    print(tokens[:50] if tokens else "No tokens found")  # Print first 50 tokens or a message if empty
    print("\n")

