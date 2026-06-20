import os
import json
import re
from dotenv import load_dotenv
from google import genai
from google.genai import types
import streamlit as st
load_dotenv()

GEMINI_API_KEY = st.secrets.get(
    "GEMINI_API_KEY",
    os.getenv("GEMINI_API_KEY")
)
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")

client = genai.Client(api_key=GEMINI_API_KEY)


def clean_json(text: str):
    if not text:
        return []

    text = text.strip()
    text = re.sub(r"```json|```", "", text).strip()

    try:
        return json.loads(text)
    except Exception:
        match = re.search(r"(\[.*\]|\{.*\})", text, re.DOTALL)
        if match:
            return json.loads(match.group(1))
        return []


def extract_claims(document_text: str):
    prompt = f"""
You are an expert claim extraction engine.

Your task is to identify the PRIMARY statements in a document that are worth fact-checking.

A claim is a meaningful assertion that a reviewer would reasonably investigate for accuracy, credibility, or currency.

IMPORTANT:

The goal is NOT to extract every factual statement.

The goal is to identify only the primary assertions that carry the document's main meaning.

Extract only claims that are central to the author's argument, conclusions, findings, recommendations, or key messages.

If removing a statement would not significantly change the meaning of the document, do not extract it.

Prefer broader claims over supporting details.

Treat a main statement and its supporting statistics, dates, percentages, measurements, and evidence as a single claim whenever they support the same assertion.

Do not extract background information, examples, definitions, descriptions, explanations, citations, references, or minor supporting facts.

Do not extract multiple claims from the same sentence unless they are clearly independent and could be fact-checked separately.

Preserve the original wording whenever possible.

Do not rewrite claims.

Remove duplicate and overlapping claims.

Focus on quality rather than quantity.

Return ONLY valid JSON.

Format:

[
  {{
    "id": 1,
    "claim": "full claim sentence"
  }}
]

DOCUMENT:

{document_text}
"""

    response = client.models.generate_content(
        model=GEMINI_MODEL,
        contents=prompt,
        config=types.GenerateContentConfig(
            response_mime_type="application/json"
        )
    )

    data = clean_json(response.text)

    if isinstance(data, dict):
        data = data.get("claims", [])

    final_claims = []
    for i, item in enumerate(data, start=1):
        if isinstance(item, dict) and item.get("claim"):
            final_claims.append({
                "id": i,
                "claim": item["claim"].strip()
            })

    return final_claims


def verify_claim_with_gemini(claim: str, evidence: str):
    prompt = f"""
You are a professional fact-checking assistant.

Your task is NOT only to decide true or false.

Your task is to classify the claim into the most accurate verification category.

You MUST choose exactly one status from this list:

True
False
Misleading
Outdated
Opinion
Mixed
Unverifiable

IMPORTANT CLASSIFICATION RULES:

Use "Opinion" when the claim is subjective, preference-based, emotional, promotional, value-based, or cannot be objectively proven true or false.

Use "Outdated" when the claim was previously accepted or true, but newer information, newer definitions, newer data, or newer classifications make it no longer current.

Use "Misleading" when the claim contains some truth but exaggerates, omits important context, overgeneralises, or may create a wrong impression.

Use "Mixed" when the claim contains multiple factual parts and some are supported while others are contradicted or uncertain.

Use "Unverifiable" when the available evidence is not enough to confidently verify the claim.

Use "False" only when reliable evidence clearly contradicts the claim.

Use "True" only when reliable evidence clearly supports the claim and none of the more specific categories above apply.

CATEGORY PRIORITY:

Before selecting True or False, first check whether the claim is:
1. Opinion
2. Outdated
3. Misleading
4. Mixed
5. Unverifiable

Only use True or False if none of the above categories fit.

Return ONLY valid JSON.

Format:

{{
  "status": "Misleading",
  "confidence": 85,
  "reason": "short explanation",
  "evidence_summary": "short evidence summary"
}}

CLAIM:
{claim}

WEB EVIDENCE:
{evidence}
"""

    response = client.models.generate_content(
        model=GEMINI_MODEL,
        contents=prompt,
        config=types.GenerateContentConfig(
            response_mime_type="application/json"
        )
    )

    result = clean_json(response.text)

    if not isinstance(result, dict):
        result = {}

    return {
        "status": result.get("status", "Unverifiable"),
        "confidence": result.get("confidence", 0),
        "reason": result.get("reason", "No clear reason returned."),
        "evidence_summary": result.get("evidence_summary", "")
    }