import sqlite3
import os
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(__file__), "pacs_portal.db")

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS test_runs (id INTEGER PRIMARY KEY AUTOINCREMENT, test_type TEXT NOT NULL, company_name TEXT, status TEXT NOT NULL DEFAULT 'RUNNING', duration_seconds REAL, error_message TEXT, report_path TEXT, started_at TEXT NOT NULL, finished_at TEXT, log_output TEXT)""")
    cursor.execute("""CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT UNIQUE NOT NULL, password_hash TEXT NOT NULL, display_name TEXT, role TEXT DEFAULT 'admin', created_at TEXT NOT NULL)""")
    cursor.execute("SELECT COUNT(*) FROM users")
    if cursor.fetchone()[0] == 0:
        cursor.execute("INSERT INTO users (username, password_hash, display_name, role, created_at) VALUES (?, ?, ?, ?, ?)", ("admin", "admin123", "Admin User", "admin", datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    conn.commit()
    conn.close()

def create_test_run(test_type, company_name=None):
    conn = get_connection()
    cursor = conn.cursor()
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("INSERT INTO test_runs (test_type, company_name, status, started_at) VALUES (?, ?, 'RUNNING', ?)", (test_type, company_name, now))
    run_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return run_id

def update_test_run(run_id, status, duration=None, error_message=None, report_path=None, log_output=None):
    conn = get_connection()
    cursor = conn.cursor()
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("UPDATE test_runs SET status=?, duration_seconds=?, error_message=?, report_path=?, finished_at=?, log_output=? WHERE id=?", (status, duration, error_message, report_path, now, log_output, run_id))
    conn.commit()
    conn.close()

def get_all_runs():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, test_type, company_name, status, duration_seconds, error_message, report_path, started_at, finished_at FROM test_runs ORDER BY id DESC")
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

def get_run(run_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM test_runs WHERE id=?", (run_id,))
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None

def get_stats():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM test_runs")
    total = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM test_runs WHERE status='PASSED'")
    passed = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM test_runs WHERE status='FAILED'")
    failed = cursor.fetchone()[0]
    cursor.execute("SELECT AVG(duration_seconds) FROM test_runs WHERE status IN ('PASSED','FAILED') AND duration_seconds IS NOT NULL")
    avg_row = cursor.fetchone()[0]
    avg_duration = round(avg_row, 1) if avg_row else 0
    conn.close()
    return {"total": total, "passed": passed, "failed": failed, "running": total - passed - failed, "avg_duration": avg_duration, "pass_rate": round((passed / total * 100), 1) if total > 0 else 0}

def verify_user(username, password):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, username, display_name, role FROM users WHERE username=? AND password_hash=?", (username, password))
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None