"""
Main Entry Point
Handles:
1. Crew Execution
2. Local File Save
3. Azure Blob Upload
4. Azure PostgreSQL Logging
"""

import os
import sys
from dotenv import load_dotenv

load_dotenv(override=True)

# Validate required environment variables
required_env = ["OPENAI_API_KEY", "FIRECRAWL_API_KEY", "DATABASE_URL"]
for var in required_env:
    if not os.getenv(var):
        print(f" Missing environment variable: {var}")
        sys.exit(1)

try:
    from src.agent.crew import run_financial_crew
    from src.shared.storage import StorageService
    from src.shared.database import DatabaseService
except ImportError as e:
    print(f" Import Error: {e}")
    sys.exit(1)


def main():
    print("===================================")
    print(" Multi-Agent Quantitative System")
    print("===================================")

    ticker = input("\nEnter stock ticker (e.g. NVDA): ").strip().upper()
    if not ticker:
        print(" No ticker provided.")
        return

    try:
        # 1️⃣ Run Crew
        print("\nRunning financial crew...")
        result_object = run_financial_crew(ticker)
        final_report_text = str(result_object)

        print("\n Analysis Complete\n")

        # 2️⃣ Save file locally FIRST
        filename = f"investment_report_{ticker}.md"

        with open(filename, "w", encoding="utf-8") as f:
            f.write(final_report_text)

        print(f" Local file saved: {filename}")

        # 3️⃣ Upload to Azure Blob
        storage = StorageService()
        print(" Uploading to Azure Blob Storage...")
        url = storage.upload_file(filename, filename)

        if url:
            print(f" Blob URL: {url}")
        else:
            print(" Blob upload failed.")

        # 4️⃣ Save to Azure PostgreSQL
        print(" Saving to Azure PostgreSQL...")
        db = DatabaseService()
        db.save_reports(ticker=ticker, content=final_report_text)

        print("\n Pipeline executed successfully!")

    except Exception as e:
        print(f"\n Pipeline Failed: {str(e)}")


# Correct Python entry check
if __name__ == "__main__":
    main()
