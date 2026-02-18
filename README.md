# 🚀 AI-Quant Investment Advisor

A cloud-integrated, multi-agent AI system that combines quantitative financial analysis and real-time market sentiment to generate intelligent investment reports.

---

## 📌 Overview

AI-Quant Investment Advisor is designed to simulate how institutional research teams operate — combining:

- 📊 Structured financial fundamentals
- 📰 Real-time qualitative news sentiment
- 🤖 Multi-agent AI collaboration
- ☁️ Cloud-based report storage and metadata persistence

The system leverages **CrewAI multi-agent orchestration**, integrates with **Yahoo Finance**, scrapes live market news using **Firecrawl**, and persists results using **Azure Blob Storage** and **Azure PostgreSQL**.

---

## 🎯 Problem Statement

Retail investors often rely on either:

- Purely quantitative metrics (P/E, EPS, growth ratios)
- Purely news-based sentiment
- Manual research workflows

This fragmented approach results in inconsistent decision-making.

This project solves that problem by:

✔ Combining structured financial metrics  
✔ Integrating unstructured real-time news sentiment  
✔ Using AI agents to generate consolidated investment reports  
✔ Storing outputs in scalable cloud infrastructure  

---

## 🧠 System Architecture
<img width="1001" height="661" alt="image" src="https://github.com/user-attachments/assets/4be6d344-f067-400d-be04-fbd964d260ec" />



---

## 🤖 Multi-Agent Design (CrewAI)

### 1️⃣ Quant Analyst Agent

Responsible for:

- Fetching financial metrics from Yahoo Finance
- Analyzing valuation ratios
- Evaluating profitability
- Reviewing growth indicators
- Producing structured financial insight

Focus: **Fundamentals**

---

### 2️⃣ Strategy Analyst Agent

Responsible for:

- Scraping real-time news using Firecrawl
- Extracting relevant articles
- Limiting content for efficient processing
- Performing sentiment analysis
- Identifying analyst signals and market narratives

Focus: **Market Sentiment**

---

### 🧠 Why Multi-Agent?

Instead of using a single large prompt:

- Improves reasoning clarity
- Enables task specialization
- Mimics real financial research teams
- Enhances modularity and scalability

---

## 🔄 Report Generation Workflow

1. User selects a stock symbol
2. Quant agent retrieves financial metrics
3. Strategy agent scrapes and analyzes market news
4. CrewAI orchestrates collaborative reasoning
5. Final investment report is generated
6. Report is stored in Azure Blob Storage
7. Metadata is stored in Azure PostgreSQL

---

## ☁️ Cloud Architecture

### Azure Blob Storage

Used for:

- Storing generated investment reports
- Scalable and durable file storage
- Secure cloud persistence

### Azure PostgreSQL (Flexible Server)

Used for:

- Storing metadata:
  - Stock symbol
  - Generation timestamp
  - Report URL
  - Sentiment summary
- Secure relational database storage

### Why Cloud?

- Scalability
- High availability
- Managed infrastructure
- Secure SSL connections
- Production-ready architecture

---

## 🔌 Interfaces

The system supports multiple execution modes:

### 🔹 FastAPI (Backend API)
- REST endpoints
- Production deployment ready
- Integrates with other systems

### 🔹 Streamlit (Interactive UI)
- User-friendly dashboard
- Live stock selection
- Report viewing interface

### 🔹 CLI
- Developer testing
- Automation workflows
- Local debugging

---

## 🛠 Tech Stack

- **Python**
- **CrewAI** (Multi-Agent Orchestration)
- **FastAPI** (Backend API)
- **Streamlit** (Frontend UI)
- **Firecrawl** (Web Scraping)
- **Yahoo Finance API**
- **Azure Blob Storage**
- **Azure PostgreSQL**
- **SQLAlchemy**
- **Pydantic**

---

## 🚀 How to Run Locally

### 1️⃣ Clone Repository

```bash
git clone https://github.com/sachink45/AI-Quant-Investment-Advisor.git
cd AI-Quant-Investment-Advisor
python -m venv .venv
source .venv/bin/activate  # Mac/Linux
.venv\Scripts\activate     # Windows
pip install -r requirements.txt
OPENAI_API_KEY=your_key
FIRECRAWL_API_KEY=your_key
AZURE_STORAGE_CONNECTION_STRING=your_string
DATABASE_URL=your_postgres_url
uvicorn main:app --reload     # for api testing
streamlit run app.py          # for UI tesing
```




