# Jewelry Recommender - Setup & Deployment Guide

## 🏃‍♂️ Quick Start (Local Development)

### Prerequisites
- Python 3.8+ installed
- Git installed
- Terminal/Command Prompt access

### Step 1: Setup Project Structure
```bash
# Create project directory
mkdir jewelry-recommender
cd jewelry-recommender

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate
```

### Step 2: Create Required Files

**requirements.txt:**
```
fastapi==0.104.1
uvicorn[standard]==0.24.0
python-multipart==0.0.6
pydantic==2.4.2
python-dateutil==2.8.2
Pillow==10.0.1
```

**File Structure:**
```
jewelry-recommender/
├── main.py                 # Backend API (from document 2)
├── static/
│   └── index.html         # Frontend (from document 1)
├── requirements.txt       # Dependencies
├── sample_data.json       # Data (from document 3)
├── test_api.py           # Testing script (from document 4)
├── README.md             # Documentation (from document 5)
└── startup.py            # Startup script
```

### Step 3: Install Dependencies & Run
```bash
# Install dependencies
pip install -r requirements.txt

# Create static directory and add index.html
mkdir static

# Run the application
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Visit: `http://localhost:8000`

---
