AI Claim Assessment Tool

An AI-powered document assessment and fact-checking application built with Streamlit, Gemini, and Tavily.

The application extracts the most important claims from a PDF document, searches for supporting evidence on the web, and evaluates each claim using AI-assisted fact-checking.

Features
Upload PDF documents
Extract primary fact-checkable claims
Ignore minor supporting details and background information
Search evidence using Tavily Search API
Verify claims using Google Gemini
Classify claims into:
True
False
Misleading
Outdated
Opinion
Mixed
Unverifiable
Display verification confidence and reasoning
Export assessment results as CSV
Streamlit web interface
Technology Stack
Python
Streamlit
Google Gemini API
Tavily Search API
PyMuPDF
Pandas
Project Structure
FactCheck/
│
├── app.py
├── llm.py
├── tavily_service.py
├── requirements.txt
├── README.md
├── .gitignore
└── .env
Installation

Clone the repository:

git clone https://github.com/YOUR_USERNAME/YOUR_REPOSITORY.git
cd YOUR_REPOSITORY

Install dependencies:

pip install -r requirements.txt
Environment Variables

Create a .env file:

GEMINI_API_KEY=your_gemini_api_key
TAVILY_API_KEY=your_tavily_api_key

GEMINI_MODEL=gemini-2.5-flash
GEMINI_FALLBACK_MODEL=gemini-2.0-flash
Running Locally

Start the application:

streamlit run app.py

The application will be available at:

http://localhost:8501
Workflow
PDF Upload
     ↓
Text Extraction
     ↓
Claim Extraction (Gemini)
     ↓
Evidence Search (Tavily)
     ↓
Claim Verification (Gemini)
     ↓
Assessment Report
Verification Categories
Category	Description
True	Evidence strongly supports the claim
False	Evidence contradicts the claim
Misleading	Claim contains partial truth but lacks context
Outdated	Claim was previously accurate but is no longer current
Opinion	Subjective statement that cannot be objectively verified
Mixed	Some parts supported and some contradicted
Unverifiable	Insufficient evidence available
Example Output
Claim	Status	Confidence
The Earth revolves around the Sun once every 365 days.	True	98%
Pluto is the ninth planet in the Solar System.	Outdated	95%
The Great Wall of China is visible from the Moon.	False	97%
Deployment
Streamlit Community Cloud
Push the project to GitHub.
Open Streamlit Community Cloud.
Create a new app.
Connect your GitHub repository.
Set app.py as the entry point.
Add API keys in Streamlit Secrets:
GEMINI_API_KEY = "your_gemini_api_key"
TAVILY_API_KEY = "your_tavily_api_key"
Deploy.
Future Improvements
PDF report export
Batch claim verification
Multi-language support
Citation scoring
Claim severity analysis
Source credibility scoring
Dashboard analytics
Disclaimer

This tool provides AI-assisted fact-checking and should be used as a decision-support system. Human review is recommended for critical assessments.
