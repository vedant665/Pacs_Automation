"use client"
import { useState, useEffect, useCallback, useMemo } from "react"
import { motion, AnimatePresence } from "framer-motion"
import { X, ChevronLeft, ChevronRight, FileSpreadsheet, Download, Loader2, CheckCircle2, XCircle, Minus } from "lucide-react"
import { Button } from "@/components/ui/button"
import * as XLSX from "xlsx"

const PER_PAGE = 25

type RowType = "title" | "subtitle" | "stats_label" | "stats_value" | "header" | "data" | "empty"

interface ParsedSheet {
  rows: string[][]
  rowTypes: RowType[]
  headerIdx: number
  maxCol: number
}

function parseSheet(ws: any): ParsedSheet {
  const merges = ws["!merges"] || []
  const raw = XLSX.utils.sheet_to_json(ws, { header: 1, defval: "" }) as string[][]

  // Fill merged cells
  for (const m of merges) {
    const val = raw[m.s.r]?.[m.s.c] ?? ""
    for (let r = m.s.r; r <= m.e.r; r++) {
      for (let c = m.s.c; c <= m.e.c; c++) {
        if (!raw[r]) raw[r] = []
        raw[r][c] = val
      }
    }
  }

  // Normalize row lengths
  const maxCol = raw.reduce((m: number, row: string[]) => Math.max(m, row.length), 0)
  for (const row of raw) {
    while (row.length < maxCol) row.push("")
  }

  // Detect row types
  const rowTypes: RowType[] = []
  let headerIdx = -1

  for (let i = 0; i < raw.length; i++) {
    const row = raw[i]
    const nonEmpty = row.filter(c => c !== "" && c !== undefined)
    const first = String(row[0] || "").trim()

    if (nonEmpty.length === 0) {
      rowTypes.push("empty")
      continue
    }

    // Check if all non-empty cells have the same value (merged title row)
    const uniqueVals = [...new Set(nonEmpty.map(v => String(v).trim()))]
    if (uniqueVals.length === 1 && nonEmpty.length >= maxCol * 0.5) {
      if (i === 0) { rowTypes.push("title"); continue }
      if (i <= 2) { rowTypes.push("subtitle"); continue }
    }

    // Check for # as first cell (header row)
    if (first === "#" && nonEmpty.length >= 3) {
      rowTypes.push("header")
      if (headerIdx === -1) headerIdx = i
      continue
    }

    // Check for summary stats labels (Total, Passed, Failed, Pass Rate)
    if (["Total", "Total Companies", "Total Fields", "Total Fields Updated"].includes(first) && nonEmpty.length >= 2) {
      rowTypes.push("stats_label")
      continue
    }

    // After header, everything is data
    if (headerIdx !== -1 && i > headerIdx) {
      rowTypes.push("data")
      continue
    }

    // Row with all numeric values after stats_label → stats_value
    if (rowTypes.length > 0 && rowTypes[rowTypes.length - 1] === "stats_label") {
      rowTypes.push("stats_value")
      continue
    }

    // Default
    rowTypes.push("data")
    if (headerIdx === -1 && first === "#" && nonEmpty.length >= 2) {
      headerIdx = i
      rowTypes[rowTypes.length - 1] = "header"
    }
  }

  // Remove leading empty rows
  let startIdx = 0
  while (startIdx < rowTypes.length && rowTypes[startIdx] === "empty") startIdx++

  return {
    rows: raw.slice(startIdx),
    rowTypes: rowTypes.slice(startIdx),
    headerIdx: headerIdx >= startIdx ? headerIdx - startIdx : -1,
    maxCol
  }
}

function isBadgeValue(val: string): "pass" | "fail" | "neutral" | null {
  const v = val.trim().toUpperCase()
  if (v === "PASS" || v === "PASSED" || v === "YES" || v === "ACTIVE" || v === "OK") return "pass"
  if (v === "FAIL" || v === "FAILED" || v === "NO" || v === "INACTIVE" || v === "ERROR") return "fail"
  return null
}

function BadgeCell({ value }: { value: string }) {
  const type = isBadgeValue(value)
  if (!type) return <span>{value}</span>
  if (type === "pass") return <span className="inline-flex items-center gap-1 px-2 py-0.5 rounded-full text-[10px] font-semibold bg-emerald-100 text-emerald-700"><CheckCircle2 className="size-3" />{value}</span>
  return <span className="inline-flex items-center gap-1 px-2 py-0.5 rounded-full text-[10px] font-semibold bg-red-100 text-red-700"><XCircle className="size-3" />{value}</span>
}

function StatCards({ labels, values }: { labels: string[]; values: string[] }) {
  const cards: { label: string; value: string; color: string }[] = []
  for (let i = 0; i < values.length; i++) {
    const label = labels[i] || ""
    const value = String(values[i] || "")
    if (value === "") continue
    let color = "bg-gray-50 text-gray-700"
    if (label.toLowerCase().includes("pass rate")) color = value === "100.0%" || value === "100%" ? "bg-emerald-50 text-emerald-700" : "bg-yellow-50 text-yellow-700"
    else if (label.toLowerCase().includes("passed")) color = "bg-emerald-50 text-emerald-700"
    else if (label.toLowerCase().includes("failed")) color = "bg-red-50 text-red-700"
    else if (label.toLowerCase().includes("total")) color = "bg-violet-50 text-violet-700"
    cards.push({ label, value, color })
  }
  if (cards.length === 0) return null
  return (
    <div className="flex gap-3 flex-wrap mb-4">
      {cards.map((c, i) => (
        <div key={i} className={"flex-1 min-w-[100px] rounded-xl p-3 text-center " + c.color}>
          <p className="text-xl font-bold">{c.value}</p>
          <p className="text-[10px] uppercase tracking-wider opacity-70">{c.label}</p>
        </div>
      ))}
    </div>
  )
}

interface ExcelViewerProps { filename: string; onClose: () => void }

export function ExcelViewer({ filename, onClose }: ExcelViewerProps) {
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState("")
  const [sheets, setSheets] = useState<string[]>([])
  const [activeSheet, setActiveSheet] = useState(0)
  const [parsed, setParsed] = useState<ParsedSheet | null>(null)
  const [page, setPage] = useState(1)

  const loadSheet = useCallback(async (sheetIdx: number) => {
    try {
      setLoading(true)
      const url = "/api/reports/" + encodeURIComponent(filename)
      const res = await fetch(url)
      if (!res.ok) throw new Error("Failed to fetch file")
      const data = await res.arrayBuffer()
      const wb = XLSX.read(data, { type: "array" })
      setSheets(wb.SheetNames)
      if (wb.SheetNames[sheetIdx]) {
        const ws = wb.Sheets[wb.SheetNames[sheetIdx]]
        setParsed(parseSheet(ws))
      }
      setPage(1)
    } catch (e: any) {
      setError(e.message || "Failed to load")
    } finally {
      setLoading(false)
    }
  }, [filename])

  useEffect(() => { loadSheet(activeSheet) }, [loadSheet, activeSheet])

  const dataRows = useMemo(() => {
    if (!parsed) return []
    return parsed.rows.filter((_, i) => parsed.rowTypes[i] === "data")
  }, [parsed])

  const totalPages = Math.ceil(dataRows.length / PER_PAGE)
  const paged = dataRows.slice((page - 1) * PER_PAGE, page * PER_PAGE)

  // Extract stats
  const statsLabels = useMemo(() => {
    if (!parsed) return []
    const idx = parsed.rowTypes.indexOf("stats_label")
    if (idx === -1) return []
    return parsed.rows[idx]
  }, [parsed])

  const statsValues = useMemo(() => {
    if (!parsed) return []
    const idx = parsed.rowTypes.indexOf("stats_value")
    if (idx === -1) return []
    return parsed.rows[idx]
  }, [parsed])

  // Get header row
  const headerRow = useMemo(() => {
    if (!parsed || parsed.headerIdx === -1) return []
    return parsed.rows[parsed.headerIdx]
  }, [parsed])

  // Title and subtitle
  const title = useMemo(() => {
    if (!parsed) return filename
    const idx = parsed.rowTypes.indexOf("title")
    return idx !== -1 ? parsed.rows[idx][0] : filename
  }, [parsed, filename])

  const subtitle = useMemo(() => {
    if (!parsed) return ""
    const idx = parsed.rowTypes.indexOf("subtitle")
    return idx !== -1 ? parsed.rows[idx][0] : ""
  }, [parsed])

  return (
    <AnimatePresence>
      <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }}
        className="fixed inset-0 z-50 flex items-center justify-center bg-black/50 backdrop-blur-sm"
        onClick={onClose}>
        <motion.div initial={{ opacity: 0, scale: 0.95, y: 20 }} animate={{ opacity: 1, scale: 1, y: 0 }}
          exit={{ opacity: 0, scale: 0.95, y: 20 }}
          className="bg-background rounded-2xl shadow-2xl w-[95vw] max-w-6xl max-h-[85vh] flex flex-col border"
          onClick={e => e.stopPropagation()}>

          {/* Header */}
          <div className="flex items-center justify-between p-5 border-b shrink-0">
            <div className="flex items-center gap-3">
              <div className="p-2 rounded-xl bg-violet-100"><FileSpreadsheet className="size-5 text-violet-600" /></div>
              <div>
                <h2 className="text-sm font-semibold text-foreground">{title}</h2>
                {subtitle && <p className="text-xs text-muted-foreground mt-0.5">{subtitle}</p>}
                <p className="text-[10px] text-muted-foreground">{dataRows.length} data rows · {headerRow.length} columns</p>
              </div>
            </div>
            <div className="flex items-center gap-2">
              <a href={"/api/reports/" + encodeURIComponent(filename)}>
                <Button variant="outline" size="sm" className="gap-1"><Download className="size-3.5" />Download</Button>
              </a>
              <Button variant="ghost" size="icon" onClick={onClose}><X className="size-4" /></Button>
            </div>
          </div>

          {/* Sheet Tabs */}
          {sheets.length > 1 && (
            <div className="flex gap-1 px-5 pt-3 border-b shrink-0">
              {sheets.map((s, i) => (
                <button key={s} onClick={() => setActiveSheet(i)}
                  className={"px-3 py-1.5 text-xs font-medium rounded-t-lg transition-colors " +
                    (i === activeSheet ? "bg-muted text-foreground" : "text-muted-foreground hover:text-foreground hover:bg-muted/50")}>
                  {s}
                </button>
              ))}
            </div>
          )}

          {/* Content */}
          <div className="overflow-auto flex-1 p-5">
            {loading ? (
              <div className="flex items-center justify-center py-20"><Loader2 className="size-6 animate-spin text-muted-foreground" /></div>
            ) : error ? (
              <div className="flex items-center justify-center py-20 text-destructive"><p>{error}</p></div>
            ) : !parsed ? null : (
              <div>
                {/* Stats Cards */}
                {statsLabels.length > 0 && <StatCards labels={statsLabels} values={statsValues} />}

                {/* Data Table */}
                <div className="rounded-xl border overflow-hidden">
                  <table className="w-full text-sm">
                    <thead>
                      <tr className="bg-muted/50 sticky top-0">
                        {headerRow.length > 0 ? headerRow.map((h, i) => (
                          <th key={i} className="py-2.5 px-3 text-left text-xs font-semibold text-muted-foreground whitespace-nowrap">{h || "Col " + (i + 1)}</th>
                        )) : (
                          <th className="py-2.5 px-3 text-left text-xs font-semibold text-muted-foreground">#</th>
                        )}
                      </tr>
                    </thead>
                    <tbody>
                      {paged.map((row, ri) => (
                        <tr key={ri} className="border-t hover:bg-muted/20 transition-colors">
                          {row.map((cell, ci) => {
                            const badge = isBadgeValue(String(cell))
                            return (
                              <td key={ci} className={"py-2 px-3 text-xs whitespace-nowrap max-w-[220px] truncate " + (badge === "pass" ? "text-emerald-600" : badge === "fail" ? "text-red-600" : "text-foreground")}
                                title={String(cell || "")}>
                                {badge ? <BadgeCell value={String(cell)} /> : (cell !== undefined && cell !== "" ? String(cell) : <span className="text-muted-foreground/30">—</span>)}
                              </td>
                            )
                          })}
                        </tr>
                      ))}
                      {paged.length === 0 && (
                        <tr><td colSpan={headerRow.length || 1} className="py-10 text-center text-sm text-muted-foreground">No data rows found</td></tr>
                      )}
                    </tbody>
                  </table>
                </div>
              </div>
            )}
          </div>

          {/* Pagination */}
          {totalPages > 1 && !loading && (
            <div className="flex items-center justify-between px-5 py-3 border-t shrink-0">
              <span className="text-xs text-muted-foreground">Showing {(page - 1) * PER_PAGE + 1}–{Math.min(page * PER_PAGE, dataRows.length)} of {dataRows.length}</span>
              <div className="flex gap-2">
                <Button variant="outline" size="sm" disabled={page <= 1} onClick={() => setPage(p => p - 1)}><ChevronLeft className="size-3.5" />Prev</Button>
                <span className="text-xs text-muted-foreground self-center">Page {page} of {totalPages}</span>
                <Button variant="outline" size="sm" disabled={page >= totalPages} onClick={() => setPage(p => p + 1)}>Next<ChevronRight className="size-3.5" /></Button>
              </div>
            </div>
          )}
        </motion.div>
      </motion.div>
    </AnimatePresence>
  )
}