import os
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import database
import test_runner

app = Flask(__name__)
CORS(app)
database.init_db()

REPORTS_DIR = os.path.join(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")), "pages", "company_onboarding", "reports")

@app.route("/api/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data.get("username", "")
    password = data.get("password", "")
    user = database.verify_user(username, password)
    if user:
        return jsonify({"success": True, "user": {"id": user["id"], "username": user["username"], "displayName": user["display_name"], "role": user["role"]}})
    return jsonify({"success": False, "error": "Invalid credentials"}), 401

@app.route("/api/runs", methods=["GET"])
def get_runs():
    return jsonify(database.get_all_runs())

@app.route("/api/runs/<int:run_id>", methods=["GET"])
def get_run(run_id):
    run = database.get_run(run_id)
    if not run:
        return jsonify({"error": "Run not found"}), 404
    return jsonify(run)

@app.route("/api/runs", methods=["POST"])
def start_run():
    data = request.get_json()
    test_type = data.get("testType", "creation")
    company_count = data.get("companyCount", 1)
    if test_type not in ("creation", "update", "full"):
        return jsonify({"error": "Invalid test type"}), 400
    run_id = test_runner.start_test(test_type, company_count)
    return jsonify({"success": True, "runId": run_id, "message": f"Test run started (ID: {run_id})"})

@app.route("/api/stats", methods=["GET"])
def get_stats():
    return jsonify(database.get_stats())

@app.route("/api/reports", methods=["GET"])
def list_reports():
    if not os.path.exists(REPORTS_DIR):
        return jsonify([])
    reports = []
    for filename in os.listdir(REPORTS_DIR):
        if filename.endswith((".xlsx", ".xls")):
            filepath = os.path.join(REPORTS_DIR, filename)
            stat = os.stat(filepath)
            reports.append({"filename": filename, "size": stat.st_size, "modified": stat.st_mtime, "type": "Update" if "Update" in filename else "Creation"})
    reports.sort(key=lambda r: r["modified"], reverse=True)
    return jsonify(reports)

@app.route("/api/reports/<filename>", methods=["GET"])
def download_report(filename):
    filepath = os.path.join(REPORTS_DIR, filename)
    if not os.path.exists(filepath):
        return jsonify({"error": "File not found"}), 404
    return send_file(filepath, as_attachment=True)

@app.route("/api/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"})

if __name__ == "__main__":
    print("=" * 50)
    print("  PACS Test Automation Portal - API Server")
    print("  Running on http://localhost:5000")
    print("=" * 50)
    app.run(host="0.0.0.0", port=5000, debug=True)