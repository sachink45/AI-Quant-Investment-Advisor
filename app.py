import streamlit as st
import os
from dotenv import load_dotenv

load_dotenv()

from src.agent.crew import run_financial_crew
from src.shared.database import DatabaseService
from src.shared.storage import StorageService

st.set_page_config(page_title="AI Quant Investment Advisor", layout="wide")

st.title(" AI-Powered Quant Investment Advisor")
st.markdown("Enter a stock ticker to generate financial analysis, market news, and a Buy/Hold/Sell recommendation.")

ticker = st.text_input("Enter Stock Ticker (e.g., NVDA)", "").strip().upper()

if st.button("Analyze Stock"):

    if not ticker:
        st.warning("Please enter a stock ticker.")
    else:
        with st.spinner("Running multi-agent analysis..."):

            try:
                # Run crew
                result = run_financial_crew(ticker)
                final_report = str(result)

                # Save locally
                filename = f"investment_report_{ticker}.md"
                with open(filename, "w", encoding="utf-8") as f:
                    f.write(final_report)

                # Upload to Azure Blob
                storage = StorageService()
                blob_url = storage.upload_file(filename, filename)

                # Save to PostgreSQL
                db = DatabaseService()
                db.save_reports(ticker=ticker, content=final_report)

                st.success("Analysis Complete ")

                # Display Results
                st.subheader(" Final Investment Recommendation")
                st.markdown(final_report)

                if blob_url:
                    st.markdown(f" [Download Full Report]({blob_url})")

            except Exception as e:
                st.error(f"Error: {str(e)}")
