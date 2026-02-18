"""
Act as a contract for the api. it defines what data it accepts as an input and returns as an output. 
"""

from pydantic import BaseModel, Field

class AnalysisRequest(BaseModel):
    ticker : str = Field(..., desciption = "The stock ticker symbol (e.g. MSFT, NVDA, TSLA)")

class AnalysisResponse(BaseModel):
    status : str
    ticker : str
    report_content : str
    report_url : str
    message : str   
