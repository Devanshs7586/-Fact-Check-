AI Claim Assessment Tool

This project is an AI-based fact-checking and claim assessment system.

It allows users to upload a PDF, extract the main fact-checkable claims, verify them using web evidence, and generate an assessment report.

Features
Upload PDF documents
Extract primary claims from document text
Avoid extracting every minor fact or supporting detail
Search web evidence using Tavily
Verify claims using Gemini
Classify claims as:
True
False
Misleading
Outdated
Opinion
Mixed
Unverifiable
Display final report in Streamlit
Export results as CSV
Project Structure
FactCheck/
│-- app.py
│-- llm.py
│-- tavily_service.py
│-- requirements.txt
│-- .env
│-- README.md
Installation
python -m pip install -r requirements.txt
Environment Variables

Create a .env file:

GEMINI_API_KEY=your_gemini_api_key
TAVILY_API_KEY=your_tavily_api_key
GEMINI_MODEL=gemini-2.5-flash
GEMINI_FALLBACK_MODEL=gemini-2.0-flash
Run the App
streamlit run app.py
How It Works
PDF Upload
↓
Extract Text
↓
Gemini extracts primary claims
↓
Tavily searches web evidence
↓
Gemini verifies each claim
↓
Final assessment report is generated
Claim Extraction Logic

The system does not extract every factual sentence.

It extracts only important claims that are central to the document's meaning, conclusion, findings, recommendations, or main message.

Verification Categories
Status	Meaning
True	Evidence supports the claim
False	Evidence contradicts the claim
Misleading	Claim has some truth but misses important context
Outdated	Claim was once true but is no longer current
Opinion	Claim is subjective or preference-based
Mixed	Some parts are true and some are false or uncertain
Unverifiable	Evidence is insufficient
Notes

Gemini free tier may have request limits. If you receive a 429 RESOURCE_EXHAUSTED error, wait and retry, reduce the number of claims, or enable billing.

For better efficiency, verify claims in batches instead of sending one Gemini request per claim.