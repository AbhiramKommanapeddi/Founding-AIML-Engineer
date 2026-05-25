import sqlite3
import datetime
import os
import pandas as pd

DB_FILE = "observability.db"

def init_db(db_path: str = DB_FILE):
    """Initializes the SQLite database for telemetry and logs if it does not exist."""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Create interactions table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS interactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            model_type TEXT NOT NULL,
            prompt TEXT NOT NULL,
            response TEXT NOT NULL,
            latency_ms REAL NOT NULL,
            tokens_input INTEGER,
            tokens_output INTEGER,
            cost_usd REAL,
            guardrail_tripped INTEGER DEFAULT 0,
            guardrail_reason TEXT,
            eval_category TEXT,
            judge_score REAL,
            judge_reason TEXT,
            timestamp TEXT NOT NULL
        )
    """)
    
    conn.commit()
    conn.close()

class TelemetryLogger:
    """Logs and tracks AI assistant performance, latency, costs, and safety metrics."""
    def __init__(self, db_path: str = DB_FILE):
        self.db_path = db_path
        init_db(self.db_path)

    def log_interaction(
        self,
        model_type: str,
        prompt: str,
        response: str,
        latency_ms: float,
        tokens_input: int = 0,
        tokens_output: int = 0,
        cost_usd: float = 0.0,
        guardrail_tripped: int = 0,
        guardrail_reason: str = None,
        eval_category: str = None,
        judge_score: float = None,
        judge_reason: str = None
    ):
        """Saves a single conversation or evaluation turn into the observability database."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        timestamp = datetime.datetime.now().isoformat()
        
        cursor.execute("""
            INSERT INTO interactions (
                model_type, prompt, response, latency_ms, tokens_input, tokens_output, 
                cost_usd, guardrail_tripped, guardrail_reason, eval_category, 
                judge_score, judge_reason, timestamp
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            model_type, prompt, response, latency_ms, tokens_input, tokens_output,
            cost_usd, guardrail_tripped, guardrail_reason, eval_category,
            judge_score, judge_reason, timestamp
        ))
        
        conn.commit()
        conn.close()

    def get_all_logs(self) -> pd.DataFrame:
        """Retrieves all logged interactions as a Pandas DataFrame."""
        conn = sqlite3.connect(self.db_path)
        df = pd.read_sql_query("SELECT * FROM interactions ORDER BY timestamp DESC", conn)
        conn.close()
        return df

    def get_summary_stats(self) -> pd.DataFrame:
        """Computes aggregate performance statistics grouped by model type."""
        conn = sqlite3.connect(self.db_path)
        query = """
            SELECT 
                model_type,
                COUNT(*) as total_calls,
                AVG(latency_ms) as avg_latency_ms,
                SUM(cost_usd) as total_cost_usd,
                SUM(guardrail_tripped) as total_guardrail_violations,
                AVG(judge_score) as avg_judge_score
            FROM interactions
            GROUP BY model_type
        """
        df = pd.read_sql_query(query, conn)
        conn.close()
        return df

    def clear_logs(self):
        """Clears all records from the interactions table."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM interactions")
        conn.commit()
        conn.close()
