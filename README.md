# playwright-so-cookie-consent

This repository contains an automated test suite for verifying cookie consent behavior on [https://www.ing.pl](https://www.ing.pl). It uses **Playwright** in Python with the **Page Object Model (POM)** pattern and supports multi-browser testing through **GitHub Actions**.

---

## 📁 Project Structure

```
ing_cookie_project/
├── pages/
│   └── homepage.py              # Page Object for ING homepage
├── tests/
│   └── test_cookie_consent.py   # Single test for full cookie consent flow
├── .github/
│   └── workflows/
│       └── playwright-multibrowser.yml   # Manual CI trigger
├── requirements.txt             # Python dependencies
└── README.md                    # This file
```

---

## 🧩 Requirements

- Python 3.8+
- pip (Python package manager)

Install dependencies and Playwright browsers:

```bash
pip install -r requirements.txt
python -m playwright install
```

---

## 🧪 Running Tests Locally

By default, tests run in **headless** mode (no browser UI, PowerShell):

```bash
python -m pytest tests/test_cookie_consent.py
```

To run tests in **headed** mode (see the browser window):

### On Windows (PowerShell):

```powershell
$env:HEADED="true"
python -m pytest tests/test_cookie_consent.py
```
### On macOS/Linux:

```bash
HEADED=true pytest tests/test_cookie_consent.py
```

You can also choose the browser using the `BROWSER` environment variable:

```powershell
$env:BROWSER="firefox"
python -m pytest tests/test_cookie_consent.py
```

---

## ✅ What the Test Does

### `test_cookie_consent_flow`
This single test performs the full cookie consent verification:

- Navigates to https://www.ing.pl
- Skips the test if a CAPTCHA or access block is detected
- Verifies that expected cookies are **not** present before consent
- Opens cookie settings and enables **only analytics cookies**
- Accepts the selection
- Verifies that expected cookies are **present** after consent

**Expected cookies:**
- `cookiePolicyGDPR`
- `cookiePolicyGDPR__details`
- `cookiePolicyINCPS`

---

## 🚀 CI: Running Tests in GitHub Actions

This project includes a GitHub Actions workflow that:
- Runs tests in **Chromium**, **Firefox**, and **Edge**
- Only runs **manually**, not on push or pull requests

### To run the workflow:
1. Go to the **Actions** tab in your GitHub repository
2. Select the **Playwright Multi-Browser Tests** workflow
3. Click the **"Run workflow"** button in the top-right

Workflow file location:
```
.github/workflows/playwright-multibrowser.yml
```

**⚠️ Note:** In CI environments (e.g., GitHub Actions), the ING website may trigger a CAPTCHA or block automated access.  
If detected, the test is **automatically skipped** (not failed), and this will be visible in the test report.

---

## 🛠️ Notes

- All browsers run in **headless mode** in CI
- Local test visibility can be controlled using the `HEADED=true` environment variable
- Tests are parallelized across multiple browsers in GitHub Actions using matrix strategy
- Tracing and HTML reports are automatically generated per browser

---

## 📄 requirements.txt

```
playwright==1.52.0
pytest==8.4.0
pytest-html==4.1.1
```


---

## 📊 Test Results and Trace Files

After each CI run, the following artifacts are generated and uploaded **per browser**:

- ✅ **HTML test report**: A visual summary of passed/failed/skipped tests
- 🎯 **Playwright trace file**: A full trace of browser actions, useful for debugging (screenshots, steps, sources)

You can download them from the **"Artifacts"** section of a completed GitHub Actions run:
- `html-report-chromium.html`
- `trace-chromium.zip`
- `html-report-firefox.html`
- `trace-firefox.zip`
- `html-report-edge.html`
- `trace-edge.zip`

Use the trace viewer by running locally (PowerShell):
```bash
python -m playwright show-trace trace-<browser>.zip
```
or upload it to the [Playwright Trace Viewer](https://trace.playwright.dev).

