"""
app.py
------
The Flask web page. Start it with:

    python app.py

Then open http://127.0.0.1:5000 , paste a website address and press Scan.

The app has only two routes:
  GET  /       -> the form
  POST /scan   -> runs the audit and renders the report
"""

from dotenv import load_dotenv
from flask import Flask, render_template, request

from lighthouse_tool.analyzer import summarise
from lighthouse_tool.pagespeed import PageSpeedError, run_audit

# Load PAGESPEED_API_KEY from a local .env file (if there is one).
load_dotenv()

app = Flask(__name__)


@app.route("/")
def home():
    """Show the empty form."""
    return render_template("index.html")


@app.route("/scan", methods=["POST"])
def scan():
    """Run a Lighthouse audit for the submitted URL and show the summary."""
    url = request.form.get("url", "")
    strategy = request.form.get("strategy", "mobile")

    try:
        raw_report = run_audit(url, strategy)
        report = summarise(raw_report)
    except PageSpeedError as error:
        # Show the problem on the form instead of crashing.
        return render_template("index.html", error=str(error), url=url), 400

    return render_template("report.html", report=report)


if __name__ == "__main__":
    # debug=True reloads the server automatically while you edit the code.
    app.run(debug=True, port=5000)
