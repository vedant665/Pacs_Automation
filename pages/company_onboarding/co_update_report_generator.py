"""
co_update_report_generator.py
-------------------------------
Excel report generator for Company Onboarding UPDATE tests.

3 Sheets:
  1. Summary         - Overall pass/fail + field counts
  2. Field Verification - Per-field before/after/expected/match status
  3. All Fields Before vs After - Complete before/after snapshot
"""

import os
from datetime import datetime
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter


# -- Color Palette --
FILL_DARK  = PatternFill("solid", fgColor="1F3864")
FILL_MED   = PatternFill("solid", fgColor="2E75B6")
FILL_LIGHT = PatternFill("solid", fgColor="D6E4F0")
FILL_ALT   = PatternFill("solid", fgColor="F5F5F5")
FILL_WHITE = PatternFill("solid", fgColor="FFFFFF")
FILL_GREEN = PatternFill("solid", fgColor="C6EFCE")
FILL_RED   = PatternFill("solid", fgColor="FFC7CE")
FILL_GOLD  = PatternFill("solid", fgColor="FFEB9C")

FONT_TITLE    = Font(name="Calibri", bold=True, color="FFFFFF", size=16)
FONT_SUBTITLE = Font(name="Calibri", italic=True, color="FFFFFF", size=11)
FONT_HEADER   = Font(name="Calibri", bold=True, color="FFFFFF", size=10)
FONT_NORMAL   = Font(name="Calibri", size=10)
FONT_BOLD     = Font(name="Calibri", bold=True, size=10)
FONT_KPI_VAL  = Font(name="Calibri", bold=True, size=18, color="1F3864")
FONT_PASS     = Font(name="Calibri", bold=True, size=10, color="006100")
FONT_FAIL     = Font(name="Calibri", bold=True, size=10, color="9C0006")

BORDER = Border(
    left=Side("thin", color="D9D9D9"),
    right=Side("thin", color="D9D9D9"),
    top=Side("thin", color="D9D9D9"),
    bottom=Side("thin", color="D9D9D9"),
)

A_C = Alignment(horizontal="center", vertical="center", wrap_text=True)
A_L = Alignment(horizontal="left", vertical="center", wrap_text=True)


def _sc(cell, font=None, fill=None, align=None, border=None):
    if font:   cell.font = font
    if fill:   cell.fill = fill
    if align:  cell.alignment = align
    if border: cell.border = border


def _title_banner(ws, title, subtitle, cols=8):
    ws.merge_cells(start_row=1, start_column=1, end_row=1, end_column=cols)
    c = ws.cell(row=1, column=1, value=title)
    _sc(c, FONT_TITLE, FILL_DARK, A_C)
    ws.row_dimensions[1].height = 36
    ws.merge_cells(start_row=2, start_column=1, end_row=2, end_column=cols)
    c = ws.cell(row=2, column=1, value=subtitle)
    _sc(c, FONT_SUBTITLE, FILL_MED, A_C)
    ws.row_dimensions[2].height = 22
    ws.row_dimensions[3].height = 8


def _headers(ws, row, heads, start=1):
    for i, h in enumerate(heads, start):
        c = ws.cell(row=row, column=i, value=h)
        _sc(c, FONT_HEADER, FILL_MED, A_C, BORDER)
    ws.row_dimensions[row].height = 24
    return row + 1


def _row(ws, row, vals, start=1, alt=False):
    fill = FILL_ALT if alt else FILL_WHITE
    for i, v in enumerate(vals, start):
        c = ws.cell(row=row, column=i, value=v)
        _sc(c, FONT_NORMAL, fill, A_L, BORDER)
    return row + 1


def _match_cell(ws, row, col, matched):
    c = ws.cell(row=row, column=col, value="PASS" if matched else "FAIL")
    if matched:
        _sc(c, FONT_PASS, FILL_GREEN, A_C, BORDER)
    else:
        _sc(c, FONT_FAIL, FILL_RED, A_C, BORDER)


def _widths(ws, spec, mn=10, mx=45):
    for col, w in spec.items():
        ws.column_dimensions[get_column_letter(col)].width = min(max(w, mn), mx)


# ================================================================
# MAIN: generate_update_report()
# ================================================================
def generate_update_report(before_values, after_values, expected_updates, company_name, output_dir):
    """
    Generate Excel report for update test results.

    Args:
        before_values:    dict {step_num: {field: value}} - values before update
        after_values:     dict {step_num: {field: value}} - values after update
        expected_updates: dict {step_num: {field: value}} - what we expected
        company_name:     str - name of the company updated
        output_dir:       str - directory to save the report
    """
    os.makedirs(output_dir, exist_ok=True)
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    fp = os.path.join(output_dir, f"CompanyOnboarding_UpdateReport_{ts}.xlsx")
    wb = Workbook()

    _build_summary(wb, before_values, after_values, expected_updates, company_name)
    _build_field_verification(wb, before_values, after_values, expected_updates)
    _build_before_after(wb, before_values, after_values)

    wb.save(fp)
    return fp


# ================================================================
# SHEET 1: SUMMARY
# ================================================================
def _build_summary(wb, before, after, expected, company_name):
    ws = wb.active
    ws.title = "Summary"
    ws.sheet_properties.tabColor = "1F3864"

    _title_banner(ws, "COMPANY ONBOARDING - UPDATE REPORT",
                  f"Company: {company_name} | Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    # Count fields
    total_fields = 0
    matched_fields = 0
    for step_num, updates in expected.items():
        for field in updates:
            total_fields += 1
            before_val = before.get(step_num, {}).get(field, "")
            after_val = after.get(step_num, {}).get(field, "")
            if after_val == expected[step_num][field]:
                matched_fields += 1

    failed_fields = total_fields - matched_fields
    rate = (matched_fields / total_fields * 100) if total_fields else 0

    r = 4
    kpis = [
        ("Company", company_name, FILL_LIGHT),
        ("Total Fields", str(total_fields), FILL_LIGHT),
        ("Matched", str(matched_fields), FILL_GREEN),
        ("Failed", str(failed_fields), FILL_RED if failed_fields > 0 else FILL_GREEN),
        ("Match Rate", f"{rate:.1f}%", FILL_GREEN if rate == 100 else FILL_GOLD),
    ]
    for i, (label, val, fill) in enumerate(kpis):
        col = 1
        ws.merge_cells(start_row=r, start_column=col, end_row=r, end_column=col + 1)
        _sc(ws.cell(row=r, column=col, value=label), FONT_BOLD, FILL_MED, A_C, BORDER)
        ws.cell(row=r, column=col + 1).border = BORDER
        ws.merge_cells(start_row=r + 1, start_column=col, end_row=r + 1, end_column=col + 1)
        _sc(ws.cell(row=r + 1, column=col, value=val), FONT_KPI_VAL, fill, A_C, BORDER)
        ws.cell(row=r + 1, column=col + 1).border = BORDER
        ws.row_dimensions[r].height = 24
        ws.row_dimensions[r + 1].height = 36
        r += 3

    _widths(ws, {1: 20, 2: 30})


# ================================================================
# SHEET 2: FIELD VERIFICATION
# ================================================================
def _build_field_verification(wb, before, after, expected):
    ws = wb.create_sheet("Field Verification")
    ws.sheet_properties.tabColor = "2E75B6"

    _title_banner(ws, "FIELD VERIFICATION",
                  "Expected vs Actual after update")

    r = _headers(ws, 4, ["Step", "Field", "Before", "Expected", "After", "Match"])
    step_names = {1: "Step 1 - Details", 2: "Step 2 - Promoters",
                  3: "Step 3 - Address", 4: "Step 4 - Business", 5: "Step 5 - Infra"}
    idx = 1
    for step_num in sorted(expected.keys()):
        for field, exp_val in expected[step_num].items():
            before_val = before.get(step_num, {}).get(field, "")
            after_val = after.get(step_num, {}).get(field, "")
            matched = (after_val == exp_val)
            alt = idx % 2 == 0
            r = _row(ws, r, [step_names.get(step_num, f"Step {step_num}"),
                            field, before_val, exp_val, after_val], alt=alt)
            _match_cell(ws, r - 1, 6, matched)
            idx += 1

    _widths(ws, {1: 22, 2: 22, 3: 30, 4: 30, 5: 30, 6: 10})


# ================================================================
# SHEET 3: ALL FIELDS BEFORE vs AFTER
# ================================================================
def _build_before_after(wb, before, after):
    ws = wb.create_sheet("Before vs After")
    ws.sheet_properties.tabColor = "548235"

    _title_banner(ws, "ALL FIELDS - BEFORE vs AFTER",
                  "Complete snapshot of all form values")

    r = _headers(ws, 4, ["Step", "Field", "Before Update", "After Update", "Changed"])
    step_names = {1: "Step 1 - Details", 2: "Step 2 - Promoters",
                  3: "Step 3 - Address", 4: "Step 4 - Business", 5: "Step 5 - Infra"}
    idx = 1
    for step_num in sorted(before.keys()):
        all_fields = set(before.get(step_num, {}).keys()) | set(after.get(step_num, {}).keys())
        for field in sorted(all_fields):
            b = before.get(step_num, {}).get(field, "")
            a = after.get(step_num, {}).get(field, "")
            changed = "Yes" if b != a else "No"
            alt = idx % 2 == 0
            r = _row(ws, r, [step_names.get(step_num, f"Step {step_num}"),
                            field, b, a, changed], alt=alt)
            if changed == "Yes":
                c = ws.cell(row=r - 1, column=5)
                _sc(c, FONT_BOLD, FILL_GOLD, A_C, BORDER)
            idx += 1

    _widths(ws, {1: 22, 2: 22, 3: 35, 4: 35, 5: 12})