# Horizon QA Automation — Web Lighthouse Performance Monitor

A simple, beginner-friendly Python tool that scans any public web page with
Google Lighthouse, summarises the report, and gives plain-English fix
recommendations.

---

## 1. Project overview

Paste a website address into a small web page, press **Scan**, and the tool:

1. sends the URL to the Google PageSpeed Insights API (which runs Lighthouse),
2. reduces the very large JSON response to a short summary,
3. shows the category scores, the key timing metrics and every failing audit,
4. attaches a recommended fix to each failing audit.

No Node.js, Chrome or Lighthouse install is required — Google runs the audit.

---

## 2. Features implemented

- Scan any public URL (a missing `https://` is added automatically)
- Mobile or Desktop audit
- Scores out of 100 for Performance, Accessibility, Best Practices and SEO
- Key metrics: FCP, LCP, Total Blocking Time, CLS, Speed Index, Time to Interactive
- Colour-coded good / average / poor status
- Failing audits sorted by biggest estimated time saving
- Plain-English fix recommendation for every issue
- One-sentence overall verdict and count of passing audits
- Friendly error messages for bad URLs, timeouts and API quota errors

---

## 3. Technology stack

| Layer     | Technology                          |
| --------- | ----------------------------------- |
| Language  | Python 3.9+                         |
| Web       | Flask + Jinja2 templates            |
| Styling   | Plain CSS (no framework)            |
| Audit     | Google PageSpeed Insights API v5    |
| HTTP      | requests                            |
| Config    | python-dotenv                       |

---

## 4. Architecture

A simple three-layer design; each module has one job.

```text
Browser
   |  POST /scan  (url, strategy)
   v
app.py                  Flask routes: form + report page
   |
   v
lighthouse_tool/pagespeed.py     calls Google PageSpeed Insights -> raw JSON
   |
   v
lighthouse_tool/analyzer.py      raw JSON -> small summary dict
   |
   v
lighthouse_tool/recommendations.py   audit id -> "how to fix" text
   |
   v
templates/report.html            renders the summary
```

Folder layout:

```text
horizon-QA-automation/
├── app.py                      Flask application (routes only)
├── lighthouse_tool/
│   ├── __init__.py
│   ├── pagespeed.py            API client
│   ├── analyzer.py             report summarising logic
│   └── recommendations.py      fix knowledge base
├── templates/                  base.html, index.html, report.html
├── static/style.css
├── requirements.txt
├── .env.example
└── README.md
```

---

## 5. Libraries / frameworks used

- **Flask** — tiny web framework serving the two pages
- **Jinja2** — HTML templating (ships with Flask)
- **requests** — HTTP calls to the PageSpeed API
- **python-dotenv** — reads the optional API key from a `.env` file

---

## 6. Setup instructions

```bash
# 1. Clone the repository
git clone https://github.com/<your-account>/horizon-QA-automation.git
cd horizon-QA-automation

# 2. Create and activate a virtual environment
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate

# 3. Install the dependencies
pip install -r requirements.txt

# 4. (Optional) add a free API key for a higher daily quota
cp .env.example .env
#   then edit .env and set PAGESPEED_API_KEY=your_key

# 5. Run the app
python app.py
```

Open <http://127.0.0.1:5000>, paste a URL and press **Scan**.
A scan normally takes 20–40 seconds.

### Getting an API key (optional)

Free key: <https://developers.google.com/speed/docs/insights/v5/get-started>.
Without a key Google still works, but limits how many scans you can run per day.

---

## 7. Troubleshooting

| Message                              | What it means                                       |
| ------------------------------------ | --------------------------------------------------- |
| "Please enter a website address."    | The form was submitted empty                         |
| "The scan took too long."            | The site was slow to respond — try again             |
| "Unable to process request" (Google) | The URL is not publicly reachable (localhost/login)  |
| Quota / rate limit error             | Add a `PAGESPEED_API_KEY` to `.env`                  |
