"use client";
import { useEffect, useState, useCallback } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { toast } from "sonner";
import { FlaskConical, CheckCircle2, XCircle, Clock, Plus, RefreshCw, Play, FileText, FileSpreadsheet, BarChart3, LogOut, Eye, Download, X, Loader2 } from "lucide-react";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Avatar, AvatarFallback } from "@/components/ui/avatar";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table"
import { ReportsTable } from "@/components/reports-table";
import { Separator } from "@/components/ui/separator";
interface Stats { total: number; passed: number; failed: number; running: number; avg_duration: number; pass_rate: number; }
interface TestRun { id: number; test_type: string; status: string; duration_seconds: number | null; started_at: string; finished_at: string | null; }
interface Report { filename: string; size: number; modified: number; type: string; }
interface DashboardViewProps { onSignOut: () => void; }
const fadeInUp = { initial: { opacity: 0, y: 16 }, animate: { opacity: 1, y: 0 }, transition: { duration: 0.4, ease: "easeOut" as const } };
const stagger = { animate: { transition: { staggerChildren: 0.07 } } };
function fmtDur(s: number | null) { if (!s) return "-"; const m = Math.floor(s / 60); const sec = Math.round(s % 60); return m > 0 ? m + "m " + sec + "s" : sec + "s"; }
function fmtSize(b: number) { if (b < 1024) return b + " B"; if (b < 1048576) return (b / 1024).toFixed(1) + " KB"; return (b / 1048576).toFixed(1) + " MB"; }
function fmtDate(d: string) { return new Date(d).toLocaleDateString("en-US", { month: "short", day: "numeric", year: "numeric" }); }
export function DashboardView({ onSignOut }: DashboardViewProps) {
  const [stats, setStats] = useState<Stats>({ total: 0, passed: 0, failed: 0, running: 0, avg_duration: 0, pass_rate: 0 });
  const [runs, setRuns] = useState<TestRun[]>([]);
  const [reports, setReports] = useState<Report[]>([]);
  const [user, setUser] = useState<{ displayName: string; username: string } | null>(null);
  const [loading, setLoading] = useState(false);
  const [showModal, setShowModal] = useState(false);
  const [selectedTest, setSelectedTest] = useState("creation");
  const [companyCount, setCompanyCount] = useState(1);
  const loadData = useCallback(async () => {
    try {
      const [s, r, rp] = await Promise.all([fetch("/api/stats"), fetch("/api/runs"), fetch("/api/reports")]);
      setStats(await s.json());
      setRuns(await r.json());
      setReports(await rp.json());
    } catch (e) { console.error(e); }
  }, []);
  useEffect(() => {
    const stored = localStorage.getItem("pacs_user");
    if (!stored) { onSignOut(); return; }
    setUser(JSON.parse(stored));
    loadData();
    const iv = setInterval(loadData, 5000);
    return () => clearInterval(iv);
  }, [loadData, onSignOut]);
  async function handleRun() {
    setLoading(true); setShowModal(false);
    try {
      const res = await fetch("/api/runs", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ testType: selectedTest, companyCount }) });
      const data = await res.json();
      if (data.success) { toast.success(data.message); setTimeout(loadData, 2000); } else { toast.error(data.error || "Failed"); }
    } catch { toast.error("Failed to start test"); } finally { setLoading(false); }
  }
  const cards = [
    { title: "Total Tests", value: String(stats.total), sub: stats.running + " running", icon: FlaskConical, ic: "text-primary", ib: "bg-primary/10" },
    { title: "Passed", value: String(stats.passed), sub: stats.pass_rate + "% rate", icon: CheckCircle2, ic: "text-emerald-600", ib: "bg-emerald-50" },
    { title: "Failed", value: String(stats.failed), sub: "Needs attention", icon: XCircle, ic: "text-red-600", ib: "bg-red-50" },
    { title: "Avg Duration", value: fmtDur(stats.avg_duration), sub: "Per test", icon: Clock, ic: "text-amber-600", ib: "bg-amber-50" },
  ];
  const actions = [
    { label: "Run Creation Test", sub: "Create new company records", icon: Plus, v: "bg-emerald-600 hover:bg-emerald-700 text-white shadow-sm shadow-emerald-600/25" },
    { label: "Run Update Test", sub: "Update existing company data", icon: RefreshCw, v: "bg-amber-600 hover:bg-amber-700 text-white shadow-sm shadow-amber-600/25" },
    { label: "Run Full Suite", sub: "Complete end-to-end test", icon: Play, v: "" },
  ];
  const initials = user?.displayName?.split(" ").map((n: string) => n[0]).join("").toUpperCase() || "U";
  return (
    <div className="min-h-screen flex flex-col bg-muted/30">
      <motion.header initial={{ opacity: 0, y: -8 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.35 }} className="sticky top-0 z-40 w-full border-b bg-background/95 backdrop-blur">
        <div className="flex h-16 items-center justify-between px-4 sm:px-6 lg:px-8 max-w-7xl mx-auto">
          <div className="flex items-center gap-3">
            <div className="flex items-center justify-center size-9 rounded-xl bg-primary text-primary-foreground font-bold text-sm shadow-sm"><FlaskConical className="size-5" /></div>
            <div className="flex flex-col"><span className="text-sm font-bold text-foreground leading-none">PACS</span><span className="text-xs text-muted-foreground leading-none mt-0.5">Test Automation Portal</span></div>
          </div>
          <div className="flex items-center gap-3">
            <div className="hidden sm:flex items-center gap-2.5">
              <Avatar className="size-8"><AvatarFallback className="bg-primary/10 text-primary text-xs font-semibold">{initials}</AvatarFallback></Avatar>
              <span className="text-sm font-medium text-foreground">{user?.displayName || "User"}</span>
            </div>
            <Separator orientation="vertical" className="hidden sm:block h-6" />
            <Button variant="ghost" size="sm" onClick={onSignOut} className="text-muted-foreground hover:text-foreground gap-1.5"><LogOut className="size-4" /><span className="hidden sm:inline">Sign Out</span></Button>
          </div>
        </div>
      </motion.header>
      <main className="flex-1 w-full max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6 sm:py-8 space-y-8">
        <motion.div variants={stagger} initial="initial" animate="animate" className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 sm:gap-6">
          {cards.map((c) => { const Icon = c.icon; return (
            <motion.div key={c.title} variants={fadeInUp}>
              <Card className="hover:shadow-md transition-shadow duration-200">
                <CardContent className="p-5">
                  <div className="flex items-start justify-between">
                    <div className="space-y-1">
                      <p className="text-sm font-medium text-muted-foreground">{c.title}</p>
                      <p className="text-3xl font-bold tracking-tight text-foreground">{c.value}</p>
                      <p className="text-xs text-muted-foreground">{c.sub}</p>
                    </div>
                    <div className={"size-10 rounded-xl flex items-center justify-center " + c.ib}><Icon className={"size-5 " + c.ic} /></div>
                  </div>
                </CardContent>
              </Card>
            </motion.div>
          ); })}
        </motion.div>
        <motion.div {...fadeInUp} transition={{ duration: 0.4, delay: 0.28 }}>
          <Card>
            <CardHeader className="pb-2">
              <CardTitle className="text-lg">Quick Actions</CardTitle>
              <CardDescription>Launch a test run for the Company Onboarding module</CardDescription>
            </CardHeader>
            <CardContent className="pt-2">
              <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
                {actions.map((a) => { const Icon = a.icon; const isCustom = a.v !== ""; return (
                  <button key={a.label} onClick={() => { setSelectedTest(a.label.toLowerCase().includes("creation") ? "creation" : a.label.toLowerCase().includes("update") ? "update" : "full"); setShowModal(true); }}
                    className={"group flex flex-col items-start gap-2 rounded-xl border p-4 text-left transition-all duration-200 hover:shadow-md hover:-translate-y-0.5 " + (isCustom ? a.v + " border-transparent" : "bg-primary hover:bg-primary/90 text-primary-foreground border-primary shadow-sm shadow-primary/25")}>
                    <div className="flex items-center gap-2 w-full">
                      <div className="flex items-center justify-center size-8 rounded-lg bg-white/20"><Icon className="size-4" /></div>
                      <span className="text-sm font-semibold">{a.label}</span>
                    </div>
                    <p className={"text-xs leading-relaxed " + (isCustom ? "text-white/80" : "text-primary-foreground/80")}>{a.sub}</p>
                  </button>
                ); })}
              </div>
            </CardContent>
          </Card>
        </motion.div>
        <motion.div {...fadeInUp} transition={{ duration: 0.4, delay: 0.36 }}>
          <Card>
            <CardHeader className="pb-2">
              <CardTitle className="text-lg">Recent Test Runs</CardTitle>
              <CardDescription>Latest automation results for Company Onboarding</CardDescription>
            </CardHeader>
            <CardContent className="pt-2">
              <div className="max-h-96 overflow-y-auto custom-scrollbar">
                <Table>
                  <TableHeader>
                    <TableRow className="hover:bg-transparent">
                      <TableHead className="w-12 text-xs font-semibold">#</TableHead>
                      <TableHead className="text-xs font-semibold">Test Type</TableHead>
                      <TableHead className="text-xs font-semibold">Status</TableHead>
                      <TableHead className="text-xs font-semibold">Duration</TableHead>
                      <TableHead className="text-xs font-semibold">Started</TableHead>
                    </TableRow>
                  </TableHeader>
                  <TableBody>
                    {runs.length === 0 ? (
                      <TableRow><TableCell colSpan={5} className="text-center text-muted-foreground py-8">No test runs yet. Click a button above to start!</TableCell></TableRow>
                    ) : runs.slice(0, 20).map((r) => (
                      <TableRow key={r.id}>
                        <TableCell className="text-muted-foreground font-mono text-xs">{r.id}</TableCell>
                        <TableCell className="font-medium text-sm">{r.test_type.charAt(0).toUpperCase() + r.test_type.slice(1)}</TableCell>
                        <TableCell>
                          <Badge variant={r.status === "PASSED" ? "default" : r.status === "FAILED" ? "destructive" : "secondary"} className={r.status === "PASSED" ? "bg-emerald-100 text-emerald-700 border-emerald-200" : r.status === "RUNNING" ? "bg-blue-100 text-blue-700 border-blue-200" : ""}>{r.status}</Badge>
                        </TableCell>
                        <TableCell className="text-sm text-muted-foreground font-mono">{fmtDur(r.duration_seconds)}</TableCell>
                        <TableCell className="text-sm text-muted-foreground">{fmtDate(r.started_at)}</TableCell>
                      </TableRow>
                    ))}
                  </TableBody>
                </Table>
              </div>
            </CardContent>
          </Card>
        </motion.div>
        <motion.div {...fadeInUp} transition={{ duration: 0.4, delay: 0.44 }}>
          <ReportsTable reports={reports} />

        </motion.div>
      </main>
      <motion.footer initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ duration: 0.4, delay: 0.5 }} className="border-t bg-background mt-auto">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4 flex items-center justify-center">
          <p className="text-xs text-muted-foreground">PACS Automation Portal · v1.0 · 2026</p>
        </div>
      </motion.footer>
      <AnimatePresence>
        {showModal && (
          <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }} className="fixed inset-0 z-50 bg-black/50 flex items-center justify-center p-4">
            <motion.div initial={{ scale: 0.95, opacity: 0 }} animate={{ scale: 1, opacity: 1 }} exit={{ scale: 0.95, opacity: 0 }}>
              <Card className="w-full max-w-sm">
                <CardContent className="p-6">
                  <div className="flex items-center justify-between mb-4">
                    <h3 className="text-lg font-semibold">Run {selectedTest.charAt(0).toUpperCase() + selectedTest.slice(1)} Test</h3>
                    <button onClick={() => setShowModal(false)} className="text-muted-foreground hover:text-foreground"><X className="size-4" /></button>
                  </div>
                  {selectedTest === "creation" && (
                    <div className="mb-4">
                      <label className="text-sm font-medium mb-2 block">Number of Companies</label>
                      <select value={companyCount} onChange={(e) => setCompanyCount(Number(e.target.value))} className="w-full h-9 rounded-md border border-input bg-transparent px-3 text-sm">
                        {[1, 2, 3, 5, 10, 20].map((n) => <option key={n} value={n}>{n}</option>)}
                      </select>
                    </div>
                  )}
                  <p className="text-sm text-muted-foreground mb-4">This will start the test in the background. Results will appear in the test history.</p>
                  <div className="flex gap-3 justify-end">
                    <Button variant="outline" size="sm" onClick={() => setShowModal(false)}>Cancel</Button>
                    <Button size="sm" onClick={handleRun} disabled={loading}>{loading ? <Loader2 className="size-4 animate-spin" /> : null}{loading ? "Starting..." : "Start Test"}</Button>
                  </div>
                </CardContent>
              </Card>
            </motion.div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}
