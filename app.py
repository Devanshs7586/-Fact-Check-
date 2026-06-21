import streamlit as st
import fitz
import pandas as pd

from llm import extract_claims, verify_claim_with_gemini
from tav import search_evidence


st.set_page_config(
    page_title="AI Claim Assessment Tool",
    layout="wide"
)


def extract_text_from_pdf(uploaded_file):
    text = ""

    pdf = fitz.open(stream=uploaded_file.read(), filetype="pdf")

    for page in pdf:
        text += page.get_text() + "\n"

    return text.strip()


st.title("AI Claim Assessment Tool")
st.write("Upload a PDF, extract primary claims, and verify them usi ng Gemini + Tavily.")

uploaded_file = st.file_uploader("Upload PDF", type=["pdf"])

if uploaded_file:
    document_text = extract_text_from_pdf(uploaded_file)

    st.subheader("Extracted Document Text")
    with st.expander("View text"):
        st.write(document_text)

    if st.button("Extract Claims"):
        with st.spinner("Extracting primary claims..."):
            claims = extract_claims(document_text)
            st.session_state["claims"] = claims

        st.success(f"Extracted {len(claims)} primary claims.")

if "claims" in st.session_state:
    st.subheader("Primary Claims")

    claims = st.session_state["claims"]

    for claim in claims:
        st.write(f"**{claim['id']}.** {claim['claim']}")

    if st.button("Verify Claims"):
        verified_results = []

        progress = st.progress(0)

        for index, claim in enumerate(claims):
            with st.spinner(f"Verifying claim {claim['id']}..."):
                evidence_text, sources = search_evidence(claim["claim"])
                verification = verify_claim_with_gemini(
                    claim=claim["claim"],
                    evidence=evidence_text
                )

                source_links = []
                for source in sources:
                    if source.get("url"):
                        source_links.append(source["url"])

                verified_results.append({
                    "ID": claim["id"],
                    "Claim": claim["claim"],
                    "Status": verification["status"],
                    "Confidence": verification["confidence"],
                    "Reason": verification["reason"],
                    "Evidence Summary": verification["evidence_summary"],
                    "Sources": "\n".join(source_links)
                })

            progress.progress((index + 1) / len(claims))

        st.session_state["verified_results"] = verified_results
        st.success("Verification completed.")

if "verified_results" in st.session_state:
    st.subheader("Final Assessment Report")

    df = pd.DataFrame(st.session_state["verified_results"])

    # -----------------------------
    # Summary counts
    # -----------------------------
    total_claims = len(df)

    status_counts = df["Status"].value_counts().to_dict()

    summary_data = {
        "Total Claims": total_claims,
        "True": status_counts.get("True", 0),
        "False": status_counts.get("False", 0),
        "Misleading": status_counts.get("Misleading", 0),
        "Outdated": status_counts.get("Outdated", 0),
        "Opinion": status_counts.get("Opinion", 0),
        "Mixed": status_counts.get("Mixed", 0),
        "Unverifiable": status_counts.get("Unverifiable", 0),
    }

    summary_df = pd.DataFrame(
        list(summary_data.items()),
        columns=["Category", "Count"]
    )

    st.subheader("Verification Summary")
    st.table(summary_df)

    # Optional metric cards
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Claims", total_claims)
    col2.metric("True", summary_data["True"])
    col3.metric("False", summary_data["False"])
    col4.metric("Unverifiable", summary_data["Unverifiable"])

    col5, col6, col7, col8 = st.columns(4)
    col5.metric("Misleading", summary_data["Misleading"])
    col6.metric("Outdated", summary_data["Outdated"])
    col7.metric("Opinion", summary_data["Opinion"])
    col8.metric("Mixed", summary_data["Mixed"])

    # -----------------------------
    # Detailed table
    # -----------------------------
    st.subheader("Verified Claims")

    st.dataframe(df, use_container_width=True)

    csv = df.to_csv(index=False).encode("utf-8")

    st.download_button(
        label="Download CSV Report",
        data=csv,
        file_name="claim_assessment_report.csv",
        mime="text/csv"
    )