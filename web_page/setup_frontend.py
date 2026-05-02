import os

FRONTEND_DIR = os.path.join(os.path.dirname(__file__), "frontend")

def write_file(rel_path, content):
    full_path = os.path.join(FRONTEND_DIR, rel_path)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"  Created: {rel_path}")

print("Building PACS Test Portal frontend...")
print()

write_file("next.config.ts", """import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  async rewrites() {
    return [
      {
        source: "/api/:path*",
        destination: "http://localhost:5000/api/:path*",
      },
    ];
  },
};

export default nextConfig;
""")

write_file("app/globals.css", """@import "tailwindcss";

:root {
  --primary: #2563eb;
  --primary-dark: #1d4ed8;
  --success: #16a34a;
  --danger: #dc2626;
  --warning: #f59e0b;
  --gray-50: #f9fafb;
  --gray-100: #f3f4f6;
  --gray-200: #e5e7eb;
  --gray-300: #d1d5db;
  --gray-400: #9ca3af;
  --gray-500: #6b7280;
  --gray-600: #4b5563;
  --gray-700: #374151;
  --gray-800: #1f2937;
  --gray-900: #111827;
}

body {
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
  background: var(--gray-50);
  color: var(--gray-900);
}

.card {
  background: white;
  border-radius: 12px;
  border: 1px solid var(--gray-200);
  padding: 24px;
  box-shadow: 0 1px 3px rgba(0,0,0,0.05);
}

.btn {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 10px 20px;
  border-radius: 8px;
  font-weight: 600;
  font-size: 14px;
  cursor: pointer;
  border: none;
  transition: all 0.2s;
}

.btn:hover { transform: translateY(-1px); box-shadow: 0 4px 12px rgba(0,0,0,0.15); }
.btn-primary { background: var(--primary); color: white; }
.btn-primary:hover { background: var(--primary-dark); }
.btn-success { background: var(--success); color: white; }
.btn-danger { background: var(--danger); color: white; }
.btn-outline { background: white; color: var(--gray-700); border: 1px solid var(--gray-300); }
.btn-sm { padding: 6px 14px; font-size: 13px; }

input, select {
  width: 100%;
  padding: 10px 14px;
  border: 1px solid var(--gray-300);
  border-radius: 8px;
  font-size: 14px;
  outline: none;
  transition: border-color 0.2s;
  box-sizing: border-box;
}

input:focus, select:focus {
  border-color: var(--primary);
  box-shadow: 0 0 0 3px rgba(37,99,235,0.1);
}

.badge {
  display: inline-block;
  padding: 3px 10px;
  border-radius: 20px;
  font-size: 12px;
  font-weight: 600;
}

.badge-passed { background: #dcfce7; color: #15803d; }
.badge-failed { background: #fee2e2; color: #b91c1c; }
.badge-running { background: #dbeafe; color: #1d4ed8; }

table {
  width: 100%;
  border-collapse: collapse;
}

th {
  text-align: left;
  padding: 12px 16px;
  font-size: 12px;
  font-weight: 600;
  color: var(--gray-500);
  text-transform: uppercase;
  letter-spacing: 0.05em;
  border-bottom: 2px solid var(--gray-200);
}

td {
  padding: 12px 16px;
  font-size: 14px;
  border-bottom: 1px solid var(--gray-100);
}

tr:hover td { background: var(--gray-50); }
""")

write_file("app/layout.tsx", """import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "PACS Test Portal",
  description: "Test Automation Portal for RhythmERP",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
""")

write_file("app/page.tsx", """"use client";
import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";

export default function Home() {
  const router = useRouter();
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const user = localStorage.getItem("pacs_user");
    if (user) {
      router.push("/dashboard");
    } else {
      router.push("/login");
    }
    setLoading(false);
  }, [router]);

  if (loading) {
    return (
      <div style={{ display: "flex", justifyContent: "center", alignItems: "center", height: "100vh" }}>
        <p style={{ color: "#6b7280", fontSize: "18px" }}>Loading...</p>
      </div>
    );
  }

  return null;
}
""")

write_file("app/login/page.tsx", """"use client";
import { useState } from "react";
import { useRouter } from "next/navigation";

export default function LoginPage() {
  const router = useRouter();
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  async function handleLogin(e: React.FormEvent) {
    e.preventDefault();
    setLoading(true);
    setError("");

    try {
      const res = await fetch("/api/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username, password }),
      });

      const data = await res.json();

      if (data.success) {
        localStorage.setItem("pacs_user", JSON.stringify(data.user));
        router.push("/dashboard");
      } else {
        setError(data.error || "Login failed");
      }
    } catch {
      setError("Cannot connect to server. Is the Flask server running?");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div style={{
      minHeight: "100vh",
      display: "flex",
      alignItems: "center",
      justifyContent: "center",
      background: "linear-gradient(135deg, #1e3a5f 0%, #2563eb 50%, #7c3aed 100%)"
    }}>
      <div className="card" style={{ width: "400px", padding: "40px" }}>
        <div style={{ textAlign: "center", marginBottom: "32px" }}>
          <div style={{
            width: "60px", height: "60px", borderRadius: "12px",
            background: "linear-gradient(135deg, #2563eb, #7c3aed)",
            display: "inline-flex", alignItems: "center", justifyContent: "center",
            marginBottom: "16px"
          }}>
            <span style={{ color: "white", fontSize: "24px", fontWeight: "bold" }}>P</span>
          </div>
          <h1 style={{ fontSize: "24px", fontWeight: "bold", marginBottom: "8px" }}>PACS Test Portal</h1>
          <p style={{ color: "#6b7280", fontSize: "14px" }}>Sign in to continue</p>
        </div>

        <form onSubmit={handleLogin}>
          <div style={{ marginBottom: "16px" }}>
            <label style={{ display: "block", fontSize: "14px", fontWeight: "600", marginBottom: "6px", color: "#374151" }}>
              Username
            </label>
            <input
              type="text"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              placeholder="Enter username"
              required
            />
          </div>

          <div style={{ marginBottom: "24px" }}>
            <label style={{ display: "block", fontSize: "14px", fontWeight: "600", marginBottom: "6px", color: "#374151" }}>
              Password
            </label>
            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="Enter password"
              required
            />
          </div>

          {error && (
            <div style={{ background: "#fee2e2", color: "#b91c1c", padding: "10px 14px", borderRadius: "8px", marginBottom: "16px", fontSize: "14px" }}>
              {error}
            </div>
          )}

          <button type="submit" className="btn btn-primary" disabled={loading} style={{ width: "100%", justifyContent: "center", padding: "12px" }}>
            {loading ? "Signing in..." : "Sign In"}
          </button>
        </form>

        <p style={{ textAlign: "center", marginTop: "24px", fontSize: "12px", color: "#9ca3af" }}>
          Default: admin / admin123
        </p>
      </div>
    </div>
  );
}
""")

write_file("app/dashboard/page.tsx", """"use client";
import { useEffect, useState, useCallback } from "react";
import { useRouter } from "next/navigation";

interface Stats {
  total: number;
  passed: number;
  failed: number;
  running: number;
  avg_duration: number;
  pass_rate: number;
}

interface TestRun {
  id: number;
  test_type: string;
  status: string;
  duration_seconds: number | null;
  started_at: string;
  finished_at: string | null;
  error_message: string | null;
}

interface Report {
  filename: string;
  size: number;
  modified: number;
  type: string;
}

export default function DashboardPage() {
  const router = useRouter();
  const [stats, setStats] = useState<Stats>({ total: 0, passed: 0, failed: 0, running: 0, avg_duration: 0, pass_rate: 0 });
  const [runs, setRuns] = useState<TestRun[]>([]);
  const [reports, setReports] = useState<Report[]>([]);
  const [loading, setLoading] = useState(false);
  const [showModal, setShowModal] = useState(false);
  const [selectedTest, setSelectedTest] = useState("creation");
  const [companyCount, setCompanyCount] = useState(1);
  const [user, setUser] = useState<{ displayName: string } | null>(null);

  const loadData = useCallback(async () => {
    try {
      const [statsRes, runsRes, reportsRes] = await Promise.all([
        fetch("/api/stats"),
        fetch("/api/runs"),
        fetch("/api/reports"),
      ]);
      setStats(await statsRes.json());
      setRuns(await runsRes.json());
      setReports(await reportsRes.json());
    } catch (err) {
      console.error("Failed to load data:", err);
    }
  }, []);

  useEffect(() => {
    const stored = localStorage.getItem("pacs_user");
    if (!stored) {
      router.push("/login");
      return;
    }
    setUser(JSON.parse(stored));
    loadData();
    const interval = setInterval(loadData, 5000);
    return () => clearInterval(interval);
  }, [router, loadData]);

  async function handleRunTest() {
    setLoading(true);
    setShowModal(false);
    try {
      await fetch("/api/runs", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ testType: selectedTest, companyCount: companyCount }),
      });
      setTimeout(loadData, 2000);
    } catch (err) {
      console.error("Failed to start test:", err);
    } finally {
      setLoading(false);
    }
  }

  function logout() {
    localStorage.removeItem("pacs_user");
    router.push("/login");
  }

  function formatDuration(seconds: number | null) {
    if (!seconds) return "-";
    const mins = Math.floor(seconds / 60);
    const secs = Math.round(seconds % 60);
    return mins > 0 ? `${mins}m ${secs}s` : `${secs}s`;
  }

  function formatTime(dateStr: string) {
    return new Date(dateStr).toLocaleString();
  }

  function formatSize(bytes: number) {
    if (bytes < 1024) return bytes + " B";
    if (bytes < 1048576) return (bytes / 1024).toFixed(1) + " KB";
    return (bytes / 1048576).toFixed(1) + " MB";
  }

  const statCards = [
    { label: "Total Runs", value: stats.total, color: "#2563eb", icon: ">" },
    { label: "Passed", value: stats.passed, color: "#16a34a", icon: "+" },
    { label: "Failed", value: stats.failed, color: "#dc2626", icon: "!" },
    { label: "Pass Rate", value: stats.pass_rate + "%", color: "#f59e0b", icon: "%" },
    { label: "Avg Duration", value: formatDuration(stats.avg_duration), color: "#7c3aed", icon: "~" },
  ];

  return (
    <div style={{ minHeight: "100vh", background: "#f9fafb" }}>
      {/* Header */}
      <header style={{ background: "white", borderBottom: "1px solid #e5e7eb", padding: "0 24px", height: "64px", display: "flex", alignItems: "center", justifyContent: "space-between" }}>
        <div style={{ display: "flex", alignItems: "center", gap: "12px" }}>
          <div style={{ width: "36px", height: "36px", borderRadius: "8px", background: "linear-gradient(135deg, #2563eb, #7c3aed)", display: "flex", alignItems: "center", justifyContent: "center" }}>
            <span style={{ color: "white", fontWeight: "bold", fontSize: "16px" }}>P</span>
          </div>
          <span style={{ fontWeight: "bold", fontSize: "18px", color: "#111827" }}>PACS Test Portal</span>
        </div>
        <div style={{ display: "flex", alignItems: "center", gap: "16px" }}>
          <span style={{ color: "#6b7280", fontSize: "14px" }}>Hi, {user?.displayName || "User"}</span>
          <button onClick={logout} className="btn btn-outline btn-sm">Logout</button>
        </div>
      </header>

      <main style={{ maxWidth: "1200px", margin: "0 auto", padding: "24px" }}>
        {/* Stat Cards */}
        <div style={{ display: "grid", gridTemplateColumns: "repeat(5, 1fr)", gap: "16px", marginBottom: "24px" }}>
          {statCards.map((card) => (
            <div key={card.label} className="card" style={{ textAlign: "center", padding: "20px 12px" }}>
              <div style={{
                width: "40px", height: "40px", borderRadius: "10px", background: card.color + "15",
                display: "inline-flex", alignItems: "center", justifyContent: "center",
                color: card.color, fontWeight: "bold", fontSize: "18px", marginBottom: "8px"
              }}>{card.icon}</div>
              <div style={{ fontSize: "24px", fontWeight: "bold", color: "#111827" }}>{card.value}</div>
              <div style={{ fontSize: "13px", color: "#6b7280", marginTop: "4px" }}>{card.label}</div>
            </div>
          ))}
        </div>

        {/* Quick Actions */}
        <div className="card" style={{ marginBottom: "24px" }}>
          <h2 style={{ fontSize: "16px", fontWeight: "bold", marginBottom: "16px", color: "#111827" }}>Quick Actions</h2>
          <div style={{ display: "flex", gap: "12px", flexWrap: "wrap" }}>
            <button className="btn btn-primary" onClick={() => { setSelectedTest("creation"); setShowModal(true); }}>
              Run Creation Test
            </button>
            <button className="btn btn-success" onClick={() => { setSelectedTest("update"); setShowModal(true); }}>
              Run Update Test
            </button>
            <button className="btn btn-danger" onClick={() => { setSelectedTest("full"); setShowModal(true); }}>
              Run Full Suite
            </button>
          </div>
        </div>

        {/* Test History */}
        <div className="card" style={{ marginBottom: "24px" }}>
          <h2 style={{ fontSize: "16px", fontWeight: "bold", marginBottom: "16px", color: "#111827" }}>Test History</h2>
          {runs.length === 0 ? (
            <p style={{ color: "#9ca3af", textAlign: "center", padding: "24px" }}>No test runs yet. Click a button above to start!</p>
          ) : (
            <div style={{ overflowX: "auto" }}>
              <table>
                <thead>
                  <tr>
                    <th>ID</th>
                    <th>Test Type</th>
                    <th>Status</th>
                    <th>Duration</th>
                    <th>Started</th>
                    <th>Finished</th>
                  </tr>
                </thead>
                <tbody>
                  {runs.slice(0, 20).map((run) => (
                    <tr key={run.id}>
                      <td style={{ fontWeight: "600" }}>#{run.id}</td>
                      <td>{run.test_type.charAt(0).toUpperCase() + run.test_type.slice(1)}</td>
                      <td>
                        <span className={"badge badge-" + run.status.toLowerCase()}>
                          {run.status}
                        </span>
                      </td>
                      <td>{formatDuration(run.duration_seconds)}</td>
                      <td style={{ fontSize: "13px", color: "#6b7280" }}>{formatTime(run.started_at)}</td>
                      <td style={{ fontSize: "13px", color: "#6b7280" }}>{run.finished_at ? formatTime(run.finished_at) : "-"}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </div>

        {/* Reports */}
        <div className="card">
          <h2 style={{ fontSize: "16px", fontWeight: "bold", marginBottom: "16px", color: "#111827" }}>Reports</h2>
          {reports.length === 0 ? (
            <p style={{ color: "#9ca3af", textAlign: "center", padding: "24px" }}>No reports generated yet.</p>
          ) : (
            <div style={{ display: "grid", gap: "8px" }}>
              {reports.slice(0, 10).map((report) => (
                <div key={report.filename} style={{
                  display: "flex", alignItems: "center", justifyContent: "space-between",
                  padding: "12px 16px", background: "#f9fafb", borderRadius: "8px", border: "1px solid #e5e7eb"
                }}>
                  <div>
                    <div style={{ fontWeight: "600", fontSize: "14px" }}>{report.filename}</div>
                    <div style={{ fontSize: "12px", color: "#9ca3af" }}>
                      {report.type} - {formatSize(report.size)} - {new Date(report.modified * 1000).toLocaleDateString()}
                    </div>
                  </div>
                  <a href={"/api/reports/" + encodeURIComponent(report.filename)} className="btn btn-primary btn-sm" download>
                    Download
                  </a>
                </div>
              ))}
            </div>
          )}
        </div>
      </main>

      {/* Run Test Modal */}
      {showModal && (
        <div style={{ position: "fixed", inset: 0, background: "rgba(0,0,0,0.5)", display: "flex", alignItems: "center", justifyContent: "center", zIndex: 50 }}>
          <div className="card" style={{ width: "420px" }}>
            <h3 style={{ fontSize: "18px", fontWeight: "bold", marginBottom: "16px" }}>
              Run {selectedTest.charAt(0).toUpperCase() + selectedTest.slice(1)} Test
            </h3>

            {selectedTest === "creation" && (
              <div style={{ marginBottom: "16px" }}>
                <label style={{ display: "block", fontSize: "14px", fontWeight: "600", marginBottom: "6px" }}>Number of Companies</label>
                <select value={companyCount} onChange={(e) => setCompanyCount(Number(e.target.value))}>
                  {[1, 2, 3, 5, 10, 20].map((n) => (
                    <option key={n} value={n}>{n}</option>
                  ))}
                </select>
              </div>
            )}

            <div style={{ display: "flex", gap: "12px", justifyContent: "flex-end" }}>
              <button className="btn btn-outline" onClick={() => setShowModal(false)}>Cancel</button>
              <button className="btn btn-primary" onClick={handleRunTest} disabled={loading}>
                {loading ? "Starting..." : "Start Test"}
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
""")

print()
print("All frontend files created!")
print()
print("Next steps:")
print("  cd frontend")
print("  npm run dev")
print("  Open http://localhost:3000")