<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Claim Form Tutorial</title>
  <style>
    body {
      font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
      background-color: #f4f6f8;
      margin: 0;
      padding: 0;
      line-height: 1.6;
    }
    header {
      background-color: #007bff;
      color: white;
      padding: 20px;
      text-align: center;
    }
    main {
      max-width: 900px;
      margin: 30px auto;
      padding: 20px;
      background-color: white;
      border-radius: 8px;
      box-shadow: 0 0 10px rgba(0,0,0,0.1);
    }
    h2 {
      color: #007bff;
      margin-top: 30px;
    }
    ul {
      padding-left: 20px;
    }
    li {
      margin-bottom: 10px;
    }
    .step {
      margin-bottom: 25px;
    }
    .highlight {
      background-color: #e9f5ff;
      padding: 10px;
      border-left: 4px solid #007bff;
      margin-top: 10px;
      border-radius: 4px;
    }
    footer {
      text-align: center;
      padding: 20px;
      color: #666;
    }
  </style>
</head>
<body>

<header>
  <h1>Claim Form System Tutorial</h1>
  <p>Learn how to input entries, export your report, and verify your Excel file</p>
</header>

<main>

  <div class="step">
    <h2>1. Input Revenue</h2>
    <ul>
      <li>Select <strong>Type: Revenue</strong> from the dropdown.</li>
      <li>Choose an account:
        <ul>
          <li><strong>Self Unit Funding</strong>: no extra input needed.</li>
          <li><strong>Other Unit Funding</strong>: a field will appear to enter the unit name.</li>
          <li><strong>Participation Fees</strong>: enter the amount received from participants.</li>
          <li><strong>Donations</strong>: enter the donation amount.</li>
        </ul>
      </li>
      <li>Pick the date and enter the amount.</li>
    </ul>
    <div class="highlight">💡 Tip: If you select "Other Unit Funding", make sure to enter the unit name for proper tracking.</div>
  </div>

  <div class="step">
    <h2>2. Input Expenses</h2>
    <ul>
      <li>Select <strong>Type: Expense</strong>.</li>
      <li>Choose the appropriate expense account (e.g., Rent, Stationery).</li>
      <li>Pick the date.</li>
      <li>Fill in the following:
        <ul>
          <li><strong>Source of Purchase</strong>: where the item/service was bought.</li>
          <li><strong>Original Price</strong>: full price before discount.</li>
          <li><strong>Discount</strong>: enter 0 if no discount.</li>
        </ul>
      </li>
      <li>The <strong>Final Amount</strong> will be calculated automatically.</li>
    </ul>
    <div class="highlight">💡 Tip: If there's no discount, just leave it as 0. The system will treat the original price as the final amount.</div>
  </div>

  <div class="step">
    <h2>3. Add New Entries</h2>
    <ul>
      <li>Click the <strong>➕ Add Entry</strong> button to create a new entry block.</li>
      <li>Repeat the steps above for each revenue or expense you want to record.</li>
    </ul>
    <div class="highlight">📌 You can add as many entries as needed. Use the ❌ Remove button to delete any unwanted entry.</div>
  </div>

  <div class="step">
    <h2>4. Export to Excel</h2>
    <ul>
      <li>Once all entries are filled, click the <strong>📤 Submit</strong> button.</li>
      <li>The system will generate and download an Excel file named <em>Income_Statement_and_Cash_Book.xlsx</em>.</li>
    </ul>
    <div class="highlight">✅ Make sure all required fields are filled before submitting. The system will alert you if anything is missing.</div>
  </div>

  <div class="step">
    <h2>5. Open and Verify Excel File</h2>
    <ul>
      <li>Open the downloaded Excel file using Microsoft Excel or any compatible spreadsheet software.</li>
      <li>Check the following sheets:
        <ul>
          <li><strong>Income Statement</strong>: shows grouped revenue and expenses, with subtotals if multiple sources exist.</li>
          <li><strong>Cash Book</strong>: shows all transactions side-by-side with dates and details.</li>
        </ul>
      </li>
      <li>Ensure all amounts and sources are correctly listed.</li>
    </ul>
    <div class="highlight">🔍 If you see only one entry for a revenue or expense account, it will appear without a subtotal or source breakdown—this is expected behavior.</div>
  </div>
</body>
</html>
