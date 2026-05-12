# CryptoGraph

A modern cryptography toolbox combining classic and modern algorithms in one clean interface.

Built as a university project for **Security & Cryptography** (Labs 10–12) and **Web Services and Design**.

## Features

- **Caesar Cipher** — Shift-based encryption with custom shift and alphabet support
- **Vigenère Cipher** — Keyword-based polyalphabetic encryption
- **SHA-256** — Cryptographic hashing for text and files
- **RSA** — 2048-bit key generation, encryption/decryption (OAEP), digital signatures (PSS)
- **REST API** — Full API with Swagger UI at `/docs`
- **Web UI** — Premium handcrafted frontend (HTML/CSS/JS), mobile-first responsive design

## Quick Start

### Prerequisites

- Python 3.12+

### Installation

```bash
# Clone the repository
git clone <repository-url>
cd CryptoGraph

# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Run the Application

```bash
uvicorn main:app --reload
```

Open [http://localhost:8000](http://localhost:8000) in your browser.

API documentation is available at [http://localhost:8000/docs](http://localhost:8000/docs).

### Run Tests

```bash
pytest tests/ -v
```

## API Examples

### Caesar Cipher

```bash
# Encrypt
curl -X POST http://localhost:8000/api/classical/caesar/encrypt \
  -H "Content-Type: application/json" \
  -d '{"text": "Hello Word", "shift": 3}'

# Response: {"algorithm":"Caesar","operation":"encrypt","input":"Hello Word","result":"Khoor Zrug"}
```

### Vigenère Cipher

```bash
# Encrypt with default keyword (cryptolab)
curl -X POST http://localhost:8000/api/classical/vigenere/encrypt \
  -H "Content-Type: application/json" \
  -d '{"text": "Hello Word"}'
```

### SHA-256 Hash

```bash
# Hash text
curl -X POST http://localhost:8000/api/modern/hash/sha256 \
  -H "Content-Type: application/json" \
  -d '{"text": "Hello Word"}'

# Hash file
curl -X POST http://localhost:8000/api/files/hash \
  -F "file=@sample_data/LukaGotsadze.txt"
```

### RSA

```bash
# Generate keys
curl -X POST http://localhost:8000/api/modern/rsa/generate-keys \
  -H "Content-Type: application/json" \
  -d '{"key_size": 2048}'

# Encrypt (use public_key from generate-keys response)
curl -X POST http://localhost:8000/api/modern/rsa/encrypt \
  -H "Content-Type: application/json" \
  -d '{"text": "Hello Word", "public_key": "<paste-public-key-here>"}'
```

## Project Structure

```
CryptoGraph/
├── app/
│   ├── classical/          # Caesar and Vigenère ciphers
│   ├── modern/             # SHA-256, RSA encryption, signatures
│   ├── api/                # FastAPI routes and schemas
│   ├── services/           # Service layer
│   └── utils/              # Text and file utilities
├── static/                 # Frontend (HTML, CSS, JS)
├── tests/                  # Unit and integration tests
├── sample_data/            # Test files
├── main.py                 # Application entry point
├── requirements.txt        # Python dependencies
├── Dockerfile              # Container support
└── render.yaml             # Render deployment config
```

## Deployment

### Render

The project includes a `render.yaml` for one-click Render or Google Cloud Run deployment.

### Docker

```bash
docker build -t cryptograph .
docker run -p 8000:8000 cryptograph
```

## Technology Stack

- **Backend**: Python, FastAPI, uvicorn
- **Crypto**: `cryptography` (RSA/signatures), `hashlib` (SHA-256)
- **Frontend**: Vanilla HTML5, CSS3, JavaScript (no frameworks)
- **Testing**: pytest, httpx

## Author

Luka Gotsadze — Security & Cryptography / Web Services and Design Lab Project, 2026
