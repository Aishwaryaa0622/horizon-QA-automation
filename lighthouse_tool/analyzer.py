"""
analyzer.py
-----------
The PageSpeed response is a very large JSON document (often > 1 MB).
This module reduces it to a small, easy to render summary:

    {
      "url": ...,
      "strategy": "mobile",
      "fetched_at": "2026-09-11 11:04 UTC",
      "scores": {"Performance": 63, ...},
      "metrics": [{"name": "Largest Contentful Paint", "value": "4.1 s", ...}],
      "issues": [{"title": ..., "impact": ..., "fix": ...}],
      "passed_count": 42
    }
"""

from datetime import datetime, timezone

from .recommendations import get_fix

# The six Core Web Vitals / lab metrics we show at the top of the report.
KEY_METRICS = [
    "first-contentful-paint",
    "largest-contentful-paint",
    "total-blocking-time",
    "cumulative-layout-shift",
    "speed-index",
    "interactive",
]

# Lighthouse category ids -> the label we display.
CATEGORY_LABELS = {
    "performance": "Performance",
    "accessibility": "Accessibility",
    "best-practices": "Best Practices",
    "seo": "SEO",
}


def summarise(raw: dict) -> dict:
    """Turn a raw PageSpeed API response into a small summary dictionary."""
    lighthouse = raw.get("lighthouseResult", {})
    audits = lighthouse.get("audits", {})
    categories = lighthouse.get("categories", {})

    return {
        "url": lighthouse.get("finalUrl") or raw.get("id", ""),
        "strategy": lighthouse.get("configSettings", {}).get("formFactor", "mobile"),
        "fetched_at": datetime.now(timezone.utc).strftime("%d %b %Y, %H:%M UTC"),
        "scores": _collect_scores(categories),
        "metrics": _collect_metrics(audits),
        "issues": _collect_issues(audits),
        "passed_count": _count_passed(audits),
        "verdict": _verdict(_collect_scores(categories).get("Performance")),
    }


def _collect_scores(categories: dict) -> dict:
    """Category scores as whole numbers out of 100."""
    scores = {}
    for key, label in CATEGORY_LABELS.items():
        category = categories.get(key)
        if category and category.get("score") is not None:
            scores[label] = round(category["score"] * 100)
    return scores


def _collect_metrics(audits: dict) -> list:
    """The headline timing metrics, already formatted as display strings."""
    metrics = []
    for audit_id in KEY_METRICS:
        audit = audits.get(audit_id)
        if not audit:
            continue
        metrics.append(
            {
                "name": audit.get("title", audit_id),
                "value": audit.get("displayValue", "-"),
                "status": _status_from_score(audit.get("score")),
            }
        )
    return metrics


def _collect_issues(audits: dict) -> list:
    """
    Every audit Lighthouse marked as failing, paired with a fix recommendation.

    An audit is considered a problem when its score is below 0.9. Audits with a
    score of `None` are informative only, so we skip them.
    """
    issues = []
    for audit_id, audit in audits.items():
        score = audit.get("score")
        if score is None or score >= 0.9:
            continue

        issues.append(
            {
                "id": audit_id,
                "title": audit.get("title", audit_id),
                "detail": audit.get("description", "").split("[Learn")[0].strip(),
                "impact": audit.get("displayValue", ""),
                "savings_ms": _savings_ms(audit),
                "status": _status_from_score(score),
                "fix": get_fix(audit_id, audit.get("description", "")),
            }
        )

    # Biggest time saving first, so the most useful fix is at the top.
    issues.sort(key=lambda issue: issue["savings_ms"], reverse=True)
    return issues


def _savings_ms(audit: dict) -> float:
    """How many milliseconds this fix could save (0 when Lighthouse says nothing)."""
    details = audit.get("details") or {}
    return float(details.get("overallSavingsMs") or 0)


def _count_passed(audits: dict) -> int:
    """How many audits passed - nice to show so the report is not all bad news."""
    return sum(1 for audit in audits.values() if (audit.get("score") or 0) >= 0.9)


def _status_from_score(score) -> str:
    """Traffic-light status used for colour coding in the UI."""
    if score is None:
        return "info"
    if score >= 0.9:
        return "good"
    if score >= 0.5:
        return "average"
    return "poor"


def _verdict(performance_score) -> str:
    """One sentence summary of the overall performance score."""
    if performance_score is None:
        return "No performance score was returned for this page."
    if performance_score >= 90:
        return "Great - this page is fast for most visitors."
    if performance_score >= 50:
        return "Average - a few fixes below will make a noticeable difference."
    return "Slow - the issues listed below are costing real visitors."
