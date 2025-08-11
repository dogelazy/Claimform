from flask import Flask, request, send_file
import xlsxwriter
import io
from flask_cors import CORS
import datetime
from itertools import zip_longest
from collections import defaultdict

app = Flask(__name__)
CORS(app)

@app.route('/process', methods=['POST'])
def process_data():
    now = datetime.datetime.now()
    data = request.json
    statements = data['statements']

    revenue_summary = defaultdict(float)
    expense_summary = defaultdict(float)

    output = io.BytesIO()
    workbook = xlsxwriter.Workbook(output, {'in_memory': True})
    sheet = workbook.add_worksheet("Income Statement")
    cashbook = workbook.add_worksheet("Cash Book")

    # Formats
    bold = workbook.add_format({'bold': True})
    bold_single = workbook.add_format({'bold': True, 'underline': 1})
    bold_double = workbook.add_format({'bold': True, 'underline': 2})
    currency = workbook.add_format({'align': 'center', 'bold': True})
    single = workbook.add_format({'underline': 1})

    # Group entries
    total_revenue = 0
    total_expense = 0

    # Income Statement Header
    sheet.write(0, 2, "Income Statement", currency)
    sheet.write(1, 2, f"For the Period Ended {now.strftime('%B %d, %Y')}", currency)

    # Revenue Section
    row = 2
    sheet.write(row, 0, "Revenue", bold)
    sheet.write(row, 1, "$", currency)
    sheet.write(row, 3, "$", currency)
    row += 1

    revenue_entries = defaultdict(list)
    for stmt in statements:
        if "credit" in stmt:
            key = stmt["account_name"]
            revenue_entries[key].append(stmt)
            revenue_summary[key] += stmt["credit"]

    for account, entries in revenue_entries.items():
        total_account = revenue_summary[account]

        if len(entries) == 1:
            entry = entries[0]
            sheet.write(row, 0, account)
            sheet.write(row, 1, entry["credit"])
            row += 1
        else:
            sheet.write(row, 0, f"{account} (Total)", bold)
            sheet.write(row, 1, total_account, bold)
            row += 1

            unit_groups = defaultdict(float)
            for entry in entries:
                unit = entry.get("unit_name", "General")
                unit_groups[unit] += entry["credit"]

            for unit, amount in unit_groups.items():
                label = f"  ↳ {unit}" if unit != "General" else "  ↳ Entry"
                sheet.write(row, 0, label)
                sheet.write(row, 1, amount)
                row += 1

        total_revenue += total_account

    row -= 1
    sheet.write(row, 3, total_revenue, bold_single)
    row += 3

    # Expense Section
    sheet.write(row, 0, "Expenses", bold)
    row += 1

    expense_entries = defaultdict(list)
    for stmt in statements:
        if "debit" in stmt:
            key = stmt["account_name"]
            amount = stmt.get("final_amount", stmt["debit"])
            expense_entries[key].append(stmt)
            expense_summary[key] += amount

    for account, entries in expense_entries.items():
        total_account = expense_summary[account]

        if len(entries) == 1:
            entry = entries[0]
            entry_amount = entry.get("final_amount", entry["debit"])
            sheet.write(row, 0, account)
            sheet.write(row, 1, entry_amount)
            row += 1
        else:
            sheet.write(row, 0, f"{account} (Total)", bold)
            sheet.write(row, 1, total_account, bold)
            row += 1
            for entry in entries:
                entry_amount = entry.get("final_amount", entry["debit"])
                source = entry.get("source", "N/A")
                sheet.write(row, 0, f"  ↳ {source}")
                sheet.write(row, 1, entry_amount)
                row += 1

        total_expense += total_account

    row -= 1
    sheet.write(row, 3, total_expense, bold_single)
    row += 3

    # Net Result
    net = total_revenue - total_expense
    if net > 0:
        sheet.write(row, 0, "Net Surplus", bold)
        sheet.write(row, 3, net, bold_double)
    elif net < 0:
        sheet.write(row, 0, "Net Deficit", bold)
        sheet.write(row, 3, abs(net), bold_double)
    else:
        sheet.write(row, 0, "Break-even", bold)
        sheet.write(row, 3, net, bold_double)

    sheet.set_column(0, 3, 30)

    # Cash Book Header
    cashbook.write(0, 4, "Cash Book", currency)
    cashbook.write(1, 4, f"For the Period Ended {now.strftime('%Y-%m-%d')}", currency)

    headers = ["", "Date", "Transaction details", "Amount", "", "Date", "Transaction details", "Amount"]
    for col, header in enumerate(headers):
        cashbook.write(3, col, header, bold)

    debits = []
    credits = []

    for stmt in statements:
        entry_type = "Revenue" if "credit" in stmt else "Expense"
        date = stmt.get("date", now.strftime('%Y-%m-%d'))
        account = stmt["account_name"]
        amount = stmt.get("final_amount", stmt.get("credit", stmt.get("debit", 0)))

        if entry_type == "Revenue":
            detail = account
            if stmt.get("unit_name"):
                detail += f" – {stmt['unit_name']}"
        else:
            source = stmt.get("source", "N/A")
            detail = f"{account} – {source}"

        if entry_type == "Expense":
            debits.append((date, detail, amount))
        else:
            credits.append((date, detail, amount))

    total_debit = sum(d[2] for d in debits)
    total_credit = sum(c[2] for c in credits)
    if total_debit != total_credit:
        diff = abs(total_debit - total_credit)
        if total_debit > total_credit:
            credits.append((now.strftime('%Y-%m-%d'), "Balancing c/d", diff))
            total_revenue += diff
        else:
            debits.append((now.strftime('%Y-%m-%d'), "Balancing c/d", diff))
            total_expense += diff

    cash_row = 4
    last_debit_row = None
    last_credit_row = None

    for debit, credit in zip_longest(debits, credits, fillvalue=("", "", "")):
        cashbook.write(cash_row, 1, debit[0])
        cashbook.write(cash_row, 2, debit[1])
        cashbook.write(cash_row, 3, debit[2])
        if debit[2]:
            last_debit_row = cash_row

        cashbook.write(cash_row, 5, credit[0])
        cashbook.write(cash_row, 6, credit[1])
        cashbook.write(cash_row, 7, credit[2])
        if credit[2]:
            last_credit_row = cash_row

        cash_row += 1

    if last_debit_row is not None:
        cashbook.write(last_debit_row + 1, 3, "", single)
    if last_credit_row is not None:
        cashbook.write(last_credit_row + 1, 7, "", single)

    cashbook.write(cash_row, 2, "Total", bold)
    cashbook.write(cash_row, 3, total_expense, bold_double)
    cashbook.write(cash_row, 6, "Total", bold)
    cashbook.write(cash_row, 7, total_revenue, bold_double)

    cashbook.set_column(0, 7, 18)

    workbook.close()
    output.seek(0)

    return send_file(
        output,
        download_name="Income_Statement_and_Cash_Book.xlsx",
        as_attachment=True,
        mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )

if __name__ == '__main__':
    app.run(debug=True, port=5000)