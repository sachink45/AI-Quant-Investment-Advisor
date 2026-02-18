"""
Building the api endpoints.
Consider it as a controller. It receives the request adn calls the ai agents, and it returns the json result. 
"""

from fastapi import APIRouter, HTTPException
from src.api.module import AnalysisRequest, AnalysisResponse
from src.agent.crew import run_financial_crew
from src.shared.storage import StorageService
from src.shared.database import DatabaseService


# router to orgnize our endpoints
router = APIRouter()

@router.post("/analyze", response_model = AnalysisResponse)
async def analyze_stock(request:AnalysisRequest):
    """
    Triggers the financial analysis for the given ticker symbol, ex; MSFT
    Runs the agents, uploads the report to blob, Saves the record tp Azure postgres
    """

    ticker = request.ticker.upper()
    try:
        print(f"API Request received for : {ticker}")
        result_object = run_financial_crew(ticker)
        # convert the crew output to string
        report_text = str(result_object)
        # /upload to blob StorageService
        filename = f"investment_report_{ticker}.md"
        storage = StorageService()
        blob_url = storage.upload_file(filename, filename)
        # save this to db
        db = DatabaseService()
        db.save_reports(ticker=ticker, content=report_text)
        return AnalysisResponse(
            status = "Success",
            ticker = ticker,
            report_content = report_text,
            report_url = blob_url,
            message = "Analysis is now complete and saved to the cloud to the cloud successfully"
        )
    except Exception as e:
        print(f"API Error : {e}")
        raise HTTPException(status_code=500, detail=str(e))


