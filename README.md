# 🚀 Slack AI SQL Bot

Convert natural language questions to SQL queries instantly in Slack using AI.

**[👉 Watch Demo](https://drive.google.com/file/d/1G8MsKU7WH42bmsvQhdHAJh8pg7X6gHIe/view?usp=sharing)** 

---

## ✨ Features

- **Slash Command**: `/ask-data "your question"`
- **Natural Language → SQL**: Uses LangChain + Groq LLM (Free API)
- **PostgreSQL Execution**: Direct, secure database queries
- **SELECT-Only**: Automatic SQL validation for safety
- **Connection Pooling**: 6x faster query execution
- **Async Responses**: No Slack timeout issues
- **Professional Error Handling**: User-friendly error messages
- **Compact Results**: Clean table formatting

---

## 🏗 How It Works

```
/ask-data "question"
    ↓
FastAPI Backend (Verify Slack signature)
    ↓
LangChain + Groq LLM (Convert NL → SQL)
    ↓
PostgreSQL (Execute query with pooling)
    ↓
Formatted Slack response
```

---

## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- PostgreSQL 12+
- Slack workspace
- Groq API key (free from [console.groq.com](https://console.groq.com))

### Installation

**1. Clone & Setup**
```bash
git clone https://github.com/somyajangir/Slack-AI-SQL-Bot.git
cd slack-ai-sql-bot
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

**2. Database**
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

**3. Environment**
```bash
# Create .env file
SLACK_BOT_TOKEN=xoxb-your-token
SLACK_SIGNING_SECRET=your-secret
GROQ_API_KEY=your-groq-key
DATABASE_URL=postgresql://postgres:password@localhost:5432/analytics
```

**4. Run**
```bash
python main.py
```

**5. Expose (Local Testing)**
```bash
ngrok http 8000
# Update Slack app Request URL: https://your-ngrok-url/slack/slash-command
```

---

## 💬 Usage Examples

In Slack:
```
/ask-data show total revenue
/ask-data revenue by region
/ask-data how many orders in North?
/ask-data electronics revenue
```

---

## 🔐 Security

✅ Slack signature verification  
✅ SELECT-only query validation  
✅ Dangerous keyword blocking (DROP, DELETE, INSERT, etc.)  
✅ Query timeout protection (30 seconds)  
✅ Connection pooling  

---

## ⚡ Performance

- **Query Latency**: 1-3 seconds (typical)
- **Connection Pooling**: 6x faster than creating new connections
- **Concurrent Support**: 10+ simultaneous queries

---

## 🧪 Testing

```bash
python test_db_connection.py    # Test database
python test_db_executor.py      # Test queries
python test_langchain.py        # Test NL→SQL
```

---

## 📁 Project Structure

```
slack-ai-sql-bot/
├── main.py                      # FastAPI app
├── llm.py                       # LangChain + Groq
├── db.py                        # PostgreSQL + pooling
├── slack_handler.py             # Slack API
├── config.py                    # Configuration
├── error_handlers.py            # Error handling
├── utils.py                     # Utilities
├── requirements.txt             # Dependencies
├── .gitignore                   # Git ignore
└── test_*.py                    # Tests
```

---



## 🛠 Tech Stack

FastAPI • LangChain • Groq • PostgreSQL • Slack SDK • Python

---

## 📝 API Endpoints

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/` | GET | Service info |
| `/health` | GET | Health check |
| `/slack/slash-command` | POST | Slash command handler |

---

## ❓ Troubleshooting

**Bot not responding?**
- Check FastAPI: `curl http://localhost:8000/health`
- Verify ngrok is running
- Check `.env` variables

**Database error?**
- Ensure PostgreSQL is running
- Run: `python test_db_connection.py`
- Verify DATABASE_URL

**Groq API error?**
- Verify GROQ_API_KEY
- Check rate limits at [console.groq.com](https://console.groq.com)

---

## 📜 License

MIT License

---

## 🤝 Contributing

Pull requests welcome!

---

**Built with ❤️ • [Star if helpful!](https://github.com/yourusername/slack-ai-sql-bot)**
