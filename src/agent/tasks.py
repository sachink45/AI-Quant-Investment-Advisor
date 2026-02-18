"""
Task defination
Task that our agents will executes.
It acts as a prompt engineering layer for our application/ agentic system

key feature:
context injection : strategist's task explicitly waits for and receives the output from quant agent's tasks to ensure data driven reasoning
"""

from crewai import Task, Agent

def create_tasks(quant_agent : Agent, strategist_agent : Agent, ticker :str) -> list[Task]:
    """
    Args:
    quant_agent : financial metrics
    strat_Agent : news and synthesis
    ticker : stock symbol
    """

    quant_task = Task(
        description = (
            f"Perform a comprehensive quantitative financial analysis of the stock '{ticker}'.\n\n"

            "You must:\n"
            "1. Use the fundamental analysis tool to retrieve key financial metrics.\n"
            "2. Use the stock comparison tool if necessary to evaluate historical performance.\n"
            "3. Focus strictly on numerical and financial data.\n"
            "4. Do NOT consider news, public sentiment, or speculation.\n\n"

            "Analyze the following:\n"
            "- Valuation (P/E, Forward P/E, PEG ratio)\n"
            "- Earnings strength (EPS)\n"
            "- Market capitalization\n"
            "- Volatility (Beta)\n"
            "- 52-week trading range\n"
            "- 1-year price performance\n\n"

            "Provide a structured financial assessment."
        ),
        expected_output = (
            "Structured quantitative report in the following format:\n\n"
            "1. Company Overview (Ticker + Current Price + Market Cap)\n"
            "2. Valuation Analysis\n"
            "3. Profitability & Earnings Review\n"
            "4. Volatility & Risk Assessment\n"
            "5. Historical Performance Summary\n\n"
            "Do NOT provide a Buy/Sell/Hold recommendation."
        ),
        agent = quant_agent

    )

    strategist_task = Task(
        description=(
            f"Using the quantitative analysis of '{ticker}' and recent market news, "
            "develop a strategic investment recommendation.\n\n"

            "You must:\n"
            "1. Review the quantitative report provided by the Quantitative Analyst.\n"
            "2. Use the web search tool to gather recent news and analyst opinions.\n"
            "3. Identify prevailing market sentiment and narrative trends.\n"
            "4. Evaluate potential risks and catalysts.\n\n"

            "Synthesize numerical insights with qualitative signals "
            "to form a final investment view."
        ),

        expected_output=(
            "Final structured report in the following format:\n\n"
            "1. Quantitative Summary (Key strengths & weaknesses)\n"
            "2. Market Sentiment Summary\n"
            "3. Key Risks & Catalysts\n"
            "4. Final Recommendation: Buy / Hold / Sell\n\n"
            "Justify the recommendation using both financial data and sentiment insights."
        ),

        agent=strategist_agent,
        context = [quant_task],
        output_file = f"investment_report_{ticker}.md"
    )

    return [quant_task, strategist_task]
