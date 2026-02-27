# 🚀 Slack AI SQL Bot

Convert natural language questions into real SQL queries directly inside Slack using AI.

**[🔗 GitHub Repository](https://github.com/somyajangir/Slack-AI-SQL-Bot)** | **[🎥 Live Demo](https://drive.google.com/file/d/1G8MsKU7WH42bmsvQhdHAJh8pg7X6gHIe/view?usp=sharing)**

---

## 🧠 What This Project Does

Slack AI SQL Bot allows non-technical users to query a PostgreSQL database using plain English directly inside Slack.

Instead of writing SQL manually, users can simply type:

```
/ask-data show revenue by region
```

The system:

- Converts natural language → SQL using Groq LLM
- Validates the query for safety (SELECT-only)
- Executes it securely on PostgreSQL
- Returns formatted results back in Slack

This makes internal analytics accessible to business teams without SQL knowledge, reducing dependency on engineering teams while maintaining security and performance.

---

## ✨ Features

- **Slash Command**: `/ask-data "your question"`
- **Natural Language → SQL**: Uses Groq LLM (free API)
- **Secure PostgreSQL Execution**: Direct, safe database queries
- **SELECT-Only SQL Validation**: Automatic security enforcement
- **Dangerous Keyword Blocking**: DROP, DELETE, and more blocked
- **Connection Pooling**: 6x faster queries
- **Async Slack Responses**: No timeout issues
- **Clean Table Formatting**: Professional results display
- **Professional Error Handling**: User-friendly messages

---

## 🏗 Architecture Overview

```
Slack User
    ↓
Slack Slash Command
    ↓
FastAPI Backend (Signature Verification)
    ↓
Groq LLM (Natural Language → SQL)
    ↓
PostgreSQL (Safe Execution with Pooling)
    ↓
Formatted Slack Response
```

---

## 🎯 Why This Project Matters

Most companies store valuable data in databases, but business teams cannot easily access it without SQL knowledge.

This project enables:

- Business teams to query data independently
- Faster internal reporting
- Reduced engineering workload
- Secure AI-powered analytics within Slack
- Scalable architecture for enterprise use

This system design can be extended to multi-table databases, enterprise warehouses, or internal BI tools.

---

## 🚀 Quick Start

### Prerequisites

- Python 3.9+
- PostgreSQL 12+
- Slack workspace
- Groq API key (free from [console.groq.com](https://console.groq.com))

### 1️⃣ Clone & Setup

```bash
git clone https://github.com/somyajangir/Slack-AI-SQL-Bot.git
cd Slack-AI-SQL-Bot
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2️⃣ Database Setup

```bash
psql -U postgres
CREATE DATABASE analytics;
\c analytics

CREATE TABLE sales_daily (
    date DATE NOT NULL,
    region TEXT NOT NULL,
    category TEXT NOT NULL,
    revenue NUMERIC(12,2) NOT NULL,
    orders INTEGER NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    PRIMARY KEY (date, region, category)
);

INSERT INTO sales_daily VALUES
('2025-09-01','North','Electronics',125000.50,310),
('2025-09-01','South','Grocery',54000.00,820),
('2025-09-01','West','Fashion',40500.00,190),
('2025-09-02','North','Electronics',132500.00,332),
('2025-09-02','West','Fashion',45500.00,210),
('2025-09-02','East','Grocery',62000.00,870);
```

### 3️⃣ Environment Configuration

Create a `.env` file in the root directory:

```
SLACK_BOT_TOKEN=xoxb-your-bot-token
SLACK_SIGNING_SECRET=your-signing-secret
GROQ_API_KEY=your-groq-api-key
DATABASE_URL=postgresql://postgres:password@localhost:5432/analytics
```

### 4️⃣ Run the Application

```bash
python main.py
```

Server will run at:

```
http://localhost:8000
```

### 5️⃣ Local Testing with ngrok

```bash
ngrok http 8000
```

Copy the HTTPS URL and update your Slack App Slash Command Request URL:

```
https://your-ngrok-url/slack/slash-command
```

---

## 💬 Usage Examples

Inside Slack:

```
/ask-data show total revenue
/ask-data revenue by region
/ask-data how many orders in North?
/ask-data electronics revenue by date
/ask-data total orders on 2025-09-01
```

---

## 🔐 Security

- Slack signature verification
- SELECT-only SQL enforcement
- Dangerous keyword blocking (DROP, DELETE, INSERT, etc.)
- Query timeout protection (30 seconds)
- Connection pooling
- No raw SQL execution from users

---

## ⚡ Performance

- **Typical Response Time**: 1–3 seconds
- **Connection Pooling**: Improves query speed ~6x
- **Concurrent Support**: Handles concurrent Slack requests
- **Async Processing**: Prevents Slack timeouts

---

## 🧪 Testing

```bash
python test_db_connection.py
python test_db_executor.py
python test_langchain.py
```

---

## 📁 Project Structure

```
Slack-AI-SQL-Bot/
├── main.py
├── llm.py
├── db.py
├── slack_handler.py
├── config.py
├── error_handlers.py
├── utils.py
├── requirements.txt
├── .gitignore
├── test_db_connection.py
├── test_db_executor.py
├── test_langchain.py
└── README.md
```

---

## 🚀 Deployment (Production)

For production deployment:

- Deploy backend on Render / Railway / AWS / GCP
- Use managed PostgreSQL
- Store secrets securely as environment variables
- Replace ngrok with public HTTPS domain

---

## 🛠 Tech Stack

FastAPI • LangChain • Groq • PostgreSQL • Slack SDK • Python

---

## 📡 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Service info |
| `/health` | GET | Health check |
| `/slack/slash-command` | POST | Slack slash command handler |

---

## ❓ Troubleshooting

### Bot not responding?

- Check: `http://localhost:8000/health`
- Ensure ngrok is running
- Verify Slack Request URL

### Database error?

- Ensure PostgreSQL is running
- Verify `DATABASE_URL`
- Run `python test_db_connection.py`

### Groq API error?

- Verify `GROQ_API_KEY`
- Check rate limits at [console.groq.com](https://console.groq.com)

---

## 📜 License

MIT License

---

## 🤝 Contributing

Pull requests are welcome.

If you find this project useful, consider starring the repository ⭐
