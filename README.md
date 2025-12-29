EduRAG: Smart Education using RAG (Streamlit Edition)

EduRAG is an AI-powered educational tool designed to provide fact-grounded answers to student queries directly from NCERT textbooks. This project leverages a Retrieval-Augmented Generation (RAG) pipeline to ensure that the information provided is accurate, relevant, and free from the noise of unverified internet sources.

This version features a simple and interactive frontend built with Streamlit.

How to Run This Project

Follow these steps to get your EduRAG application running locally.

Prerequisites:
- Python 3.8 or higher
- pip (Python package installer)

Step 1: Set Up Your Project Folder

Create a new folder for your project (e.g., EduRAG_Streamlit). Inside this folder, create the following files:

- `streamlit_app.py`
- `ingest.py`
- `requirements.txt`
- `README.md` (this file)

Create a folder named `data`. This is where you will place your NCERT textbook PDFs.

Example folder structure:

EduRAG_Streamlit/
├── data/
│   └── (Your NCERT PDFs go here)
├── streamlit_app.py
├── ingest.py
├── requirements.txt
└── README.md

Step 2: Create a Virtual Environment

Open your terminal, navigate into your project folder, and run the following commands to create and activate a Python virtual environment:

# On macOS/Linux
python -m venv venv
source venv/bin/activate

# On Windows (PowerShell)
python -m venv venv
venv\Scripts\Activate.ps1

Step 3: Install Dependencies

With your virtual environment active, install all required libraries from `requirements.txt`:

pip install -r requirements.txt

Step 4: Add Your API Key

In the main project folder, create a file named `.env` and add your API key(s). Example:

GEMINI_API_KEY="YOUR_API_KEY_HERE"

Step 5: Process Your Textbooks

Put your NCERT PDFs into the `data` folder. Run the ingestion script to process them and build a local vector index:

python ingest.py

This may take a few minutes depending on the number and size of PDFs.

Step 6: Run the Streamlit App

Start the application:

streamlit run streamlit_app.py

Your browser should open with the EduRAG interface. Start asking questions!

Notes
- The `chroma_db/` directory contains a local vector DB used during development and is excluded from the repository via `.gitignore`.
- Keep secrets (API keys) out of the repository — store them in `.env` which is ignored.

Contributing

Contributions and improvements are welcome. Open issues or pull requests on the project repository.
