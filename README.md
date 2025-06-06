# Ask SQL

## Overview
The SQL Assistant is a tool designed to help users generate SQL queries using AI. It utilizes PostgreSQL (with the pgvector extension) and OpenAI's GPT-4 for intelligent query generation and assistance.

---

## Installation & Setup

### 1. Install Required Libraries
Ensure you have all dependencies installed by running:
```bash
pip install -r requirements.txt
```

### 2. Run PgVector (PostgreSQL with Vector Extension)
The SQL Assistant uses PostgreSQL with pgvector for database storage and vector similarity search.

#### Install Docker Desktop
Ensure that Docker is installed on your system before proceeding.

#### OR Start PgVector Manually using Docker
```bash
docker run -d \
  -e POSTGRES_DB=ai \
  -e POSTGRES_USER=ai \
  -e POSTGRES_PASSWORD=ai \
  -e PGDATA=/var/lib/postgresql/data/pgdata \
  -v pgvolume:/var/lib/postgresql/data \
  -p 5532:5432 \
  --name pgvector \
  phidata/pgvector:16
```

---

## Data Preparation

### 3. Load F1 Data
Load sample F1 racing data into the database:
```bash
python load_f1_data.py
```


## Running the SQL Assistant

### 5. Export OpenAI API Key
The Assistant works best with GPT-4 but can be configured to use any LLM. Set up your API key:
```bash
export OPENAI_API_KEY="your-api-key-here"
```
(For Windows PowerShell, use `$env:OPENAI_API_KEY="your-api-key-here"`)

### 6. Start the SQL Assistant
Run the Streamlit app:
```bash
streamlit run app.py
```
Then, open [localhost:8501](http://localhost:8501) in your browser to use the SQL Assistant.

---


