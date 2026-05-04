"use client"
import { useState, useMemo } from "react"
import { motion } from "framer-motion"
import { FileSpreadsheet, BarChart3, FileText, Download, ArrowUpDown, Building2, LogIn, Shield } from "lucide-react"
import { Card, CardContent } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { ExcelViewer } from "@/components/excel-viewer"
import { Eye } from "lucide-react"

function getModuleInfo(filename: string) {
  const f = filename.toLowerCase()
  if (f.includes("company") || f.includes("onboarding") || f.includes("bulk")) {
    return { name: "Company Onboarding", icon: Building2, color: "blue" }
  }
  if (f.includes("login") || f.includes("forgot")) {
    return { name: "Login Screens", icon: LogIn, color: "green" }
  }
  if (f.includes("access") || f.includes("role") || f.includes("entity")) {
    return { name: "Access Screens", icon: Shield, color: "purple" }
  }
  return { name: "Other", icon: FileText, color: "gray" }
}

function fmtSize(bytes: number) {
  if (bytes < 1024) return bytes + " B"
  if (bytes < 1048576) return (bytes / 1024).toFixed(1) + " KB"
  return (bytes / 1048576).toFixed(1) + " MB"
}

function fmtDate(iso: string) {
  try { return new Date(iso).toLocaleDateString("en-US", { month: "short", day: "numeric", year: "numeric" }) }
  catch { return iso }
}

const MODULES = ["All", "Company Onboarding", "Login Screens", "Access Screens"]
const PER_PAGE = 10

interface Report { filename: string; type: string; size: number; modified: number }

export function ReportsTable({ reports }: { reports: Report[] }) {
  const [filter, setFilter] = useState("All")
  const [sortKey, setSortKey] = useState<"name" | "module" | "date">("date")
  const [sortDir, setSortDir] = useState<"asc" | "desc">("desc")
  const [page, setPage] = useState(1)
  const [viewFile, setViewFile] = useState<string | null>(null)

  const toggleSort = (key: "name" | "module" | "date") => {
    if (sortKey === key) setSortDir(d => d === "asc" ? "desc" : "asc")
    else { setSortKey(key); setSortDir("asc") }
  }

  const filtered = useMemo(() => {
    let list = reports
    if (filter !== "All") list = list.filter(r => getModuleInfo(r.filename).name === filter)
    list = [...list].sort((a, b) => {
      let cmp = 0
      if (sortKey === "name") cmp = a.filename.localeCompare(b.filename)
      if (sortKey === "module") cmp = getModuleInfo(a.filename).name.localeCompare(getModuleInfo(b.filename).name)
      if (sortKey === "date") cmp = a.modified - b.modified
      return sortDir === "asc" ? cmp : -cmp
    })
    return list
  }, [reports, filter, sortKey, sortDir])

  const totalPages = Math.ceil(filtered.length / PER_PAGE)
  const paged = filtered.slice((page - 1) * PER_PAGE, page * PER_PAGE)

  const badgeColor = (c: string) => {
    if (c === "blue") return "bg-blue-100 text-blue-700"
    if (c === "green") return "bg-emerald-100 text-emerald-700"
    if (c === "purple") return "bg-purple-100 text-purple-700"
    return "bg-gray-100 text-gray-700"
  }

  return (
    <div>
      <div className="mb-4">
        <h2 className="text-lg font-semibold text-foreground">Latest Reports</h2>
        <p className="text-sm text-muted-foreground">Generated test execution reports</p>
      </div>

      {reports.length === 0 ? (
        <Card><CardContent className="py-8 text-center text-muted-foreground">No reports generated yet.</CardContent></Card>
      ) : (
        <motion.div initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.3 }}>
          {/* Filter Pills */}
          <div className="flex gap-2 mb-4 flex-wrap">
            {MODULES.map(m => (
              <button key={m} onClick={() => { setFilter(m); setPage(1) }}
                className={"px-3 py-1.5 rounded-full text-xs font-medium transition-colors " +
                  (filter === m ? "bg-primary text-primary-foreground" : "bg-muted text-muted-foreground hover:bg-muted/80")}>
                {m}
              </button>
            ))}
            <span className="ml-auto text-xs text-muted-foreground self-center">
              {filtered.length} report{filtered.length !== 1 ? "s" : ""}
            </span>
          </div>

          {/* Table */}
          <Card>
            <CardContent className="p-0">
              <div className="overflow-x-auto">
                <table className="w-full">
                  <thead>
                    <tr className="border-b">
                      <th className="py-3 px-4 text-left text-xs font-medium text-muted-foreground w-10">#</th>
                      <th className="py-3 px-4 text-left">
                        <button onClick={() => toggleSort("name")} className="inline-flex items-center gap-1 text-xs font-medium text-muted-foreground hover:text-foreground">
                          Report Name <ArrowUpDown className="size-3" />
                        </button>
                      </th>
                      <th className="py-3 px-4 text-left">
                        <button onClick={() => toggleSort("module")} className="inline-flex items-center gap-1 text-xs font-medium text-muted-foreground hover:text-foreground">
                          Module <ArrowUpDown className="size-3" />
                        </button>
                      </th>
                      <th className="py-3 px-4 text-left">
                        <button onClick={() => toggleSort("date")} className="inline-flex items-center gap-1 text-xs font-medium text-muted-foreground hover:text-foreground">
                          Date <ArrowUpDown className="size-3" />
                        </button>
                      </th>
                      <th className="py-3 px-4 text-center text-xs font-medium text-muted-foreground">Size</th>
                      <th className="py-3 px-4 text-center text-xs font-medium text-muted-foreground w-16"></th>
                    </tr>
                  </thead>
                  <tbody>
                    {paged.map((rp, i) => {
                      const mod = getModuleInfo(rp.filename)
                      const MIcon = mod.icon
                      return (
                        <motion.tr key={rp.filename} initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ delay: i * 0.03 }}
                          className="border-b last:border-0 hover:bg-muted/30 transition-colors">
                          <td className="py-3 px-4 text-xs text-muted-foreground">{(page - 1) * PER_PAGE + i + 1}</td>
                          <td className="py-3 px-4">
                            <div className="flex items-center gap-2">
                              {rp.type === "Update" ? <FileSpreadsheet className="size-4 text-emerald-500 shrink-0" /> :
                               rp.filename.includes("Bulk") ? <BarChart3 className="size-4 text-blue-500 shrink-0" /> :
                               <FileText className="size-4 text-muted-foreground shrink-0" />}
                              <span className="text-sm font-medium text-foreground truncate max-w-[250px]" title={rp.filename}>{rp.filename}</span>
                            </div>
                          </td>
                          <td className="py-3 px-4">
                            <Badge variant="secondary" className={"text-[10px] px-2 py-0.5 " + badgeColor(mod.color)}>
                              {mod.name}
                            </Badge>
                          </td>
                          <td className="py-3 px-4 text-xs text-muted-foreground">{fmtDate(new Date(rp.modified * 1000).toISOString())}</td>
                          <td className="py-3 px-4 text-xs text-muted-foreground text-center">{fmtSize(rp.size)}</td>
                          <td className="py-3 px-4 text-center">
                            <a href={"/api/reports/" + encodeURIComponent(rp.filename)}
                              className="inline-flex items-center justify-center p-1.5 rounded-lg hover:bg-muted transition-colors text-muted-foreground hover:text-primary">
                              <Download className="size-4" />
                            </a>
                            <button onClick={() => setViewFile(rp.filename)}
                              className="inline-flex items-center justify-center p-1.5 rounded-lg hover:bg-muted transition-colors text-muted-foreground hover:text-primary">
                              <Eye className="size-4" />
                            </button>
                          </td>
                        </motion.tr>
                      )
                    })}
                    {paged.length === 0 && (
                      <tr><td colSpan={6} className="py-8 text-center text-sm text-muted-foreground">No reports match this filter.</td></tr>
                    )}
                  </tbody>
                </table>
              </div>
            </CardContent>
          </Card>

          {/* Pagination */}
          {totalPages > 1 && (
            <div className="flex items-center justify-between mt-3">
              <button disabled={page <= 1} onClick={() => setPage(p => p - 1)}
                className="px-3 py-1 text-xs rounded-md bg-muted hover:bg-muted/80 disabled:opacity-40 disabled:cursor-not-allowed transition-colors">
                Previous
              </button>
              <span className="text-xs text-muted-foreground">Page {page} of {totalPages}</span>
              <button disabled={page >= totalPages} onClick={() => setPage(p => p + 1)}
                className="px-3 py-1 text-xs rounded-md bg-muted hover:bg-muted/80 disabled:opacity-40 disabled:cursor-not-allowed transition-colors">
                Next
              </button>
            </div>
          )}
        </motion.div>
      )}
      {viewFile && <ExcelViewer filename={viewFile} onClose={() => setViewFile(null)} />}
    </div>
  )
}
