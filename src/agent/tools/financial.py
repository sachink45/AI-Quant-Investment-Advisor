# tool kit


# define the input schema
from typing import TypedDict, Dict, Any, List, Optional, Annotated, Type
from pydantic import BaseModel, Field
from crewai.tools import BaseTool
import yfinance as yf


class StockAnalysisInput(BaseModel):

    """Input schema for the fundamental analysis tool.
    Enforce that a ticker symbol which is provided as a string
    ... -> Ellipsis. """

    ticker : str =Field(..., description = "The stock ticker symbol (e.g. 'AAPL', 'NVDA')")

class CompareStocksInput(BaseModel):

    """
    This is input schema for the compare stock tool, requires two distinct ticker : ticker_a and ticker_b
    """

    ticker_a : str = Field(..., description = "the first stock ticker to analyze")
    ticker_b : str = Field(..., description = "the second stock ticker to analyze")

# building tools (Tool Defination)

class FundamentalAnalysisTool(BaseTool):

    """
    Crewai tool that extract the fundamental metrics for a stock. This tool will act as a screening analyst, providing the raw data determine - stock
    is undervalued, OV, volatile.
    """

    name : str = "Fetch fundametal metrics"
    description : str = ("Fetches key metrics for a specific stock ticker.\
                         Useful for quantitative analysis, and returns a json formatted\
                         data includes - P/E ratio, Beta, Market Cap, EPS, 52- Week high and Low")
    args_schema : Type[BaseModel] = StockAnalysisInput

    def _run(self, ticker:str) -> str:

        """
        Executes the data fetching from yahoo finance.
        Args : ticker(str) :
        returns : string json dict contains metrics or error message if it fails
        """

        try:
            stock = yf.Ticker(ticker)
            info : Dict[str, Any] = stock.info

            # select the robust mertics to avoid context window bloat
            metrics = {
                "Ticker" : ticker.upper(),
                "Current Price" : info.get("currentPrice", "N/A"),
                "Market Cap" : info.get("marketCap", "N/A"),
                "P/E Ratio (trailing)" : info.get("trailingPE", "N/A"),
                "Forward P/E" : info.get("forwardPE", "N/A"),
                "PEG Ratio" : info.get("pegRatio", "N/A"),
                "Beta (Volatility)" : info.get("beta", "N/A"),
                "EPS (traling)" : info.get("eps", "N/A"),
                "52 Week High" : info.get("fiftyTwoWeekHigh", "N/A"),
                "52 Week Low" : info.get("fiftyTwoWeekLow", "N/A"),
                "Analyst Recommendation" : info.get("recommendation", "none")
            }

            return str(metrics)
        
        except Exception as e:
            return f"Error fetching fundamental data for '{ticker} : {str(e)}"


class CompareStocks(BaseTool):

    """
    Tool that calculates the performance between stocks and answer the question. 
    """

    name : str = "Compare stock performance"
    description : str = ("Compares the historical performance of 2 stocks over the last 365 days."
                        "retruns the percnbtage gain or loss for both assets")
    args_schema : Type[BaseModel] = CompareStocksInput

    def _run(self, ticker_a : str, ticker_b : str) -> str:

        """
        Fetch the historical data and calculate the percentage return.
        formula : (last price - first price) / (first price) *100
        """

        try:
            tickers = f"{ticker_a} {ticker_b}"
            data = yf.download(tickers, period = "1y", progress = False)['Close']

            # helper function to calculate return
            def calculate_return(symbol:str) -> float:
                start_price = data[symbol].iloc[0]
                end_price = data[symbol].iloc[-1]

                return ((end_price - start_price) / start_price)*100
            
            perf_a = calculate_return(ticker_a)
            perf_b = calculate_return(ticker_b)

            better = ticker_a if perf_a > perf_b else ticker_b

            return (
                f"Performance Comparison (Last 1 Year):\n"
                f"{ticker_a}: {perf_a:.2f}%\n"
                f"{ticker_b}: {perf_b:.2f}%\n"
                f"Better Performer: {better}"
            )
        
        except Exception as e:
            return f"Error comparing stocks '{ticker_a}' and '{ticker_b} : {str(e)}"

