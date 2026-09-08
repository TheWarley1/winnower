"""Deterministic job-board scan tools.

No LLM in the data layer: these fetch and normalize rows from public APIs.
A tool returns plain data; the agent decides what to do with it.

NOTE (Sep 2026): arbeitnow's public API now 301s to the homepage and is
effectively dead; Remotive is the primary source.
"""
from __future__ import annotations

import re
from typing import Any

import requests

REMOTIVE_API = "https://remotive.com/api/remote-jobs"

STUDENT_MARKERS = re.compile(
    r"\b(werkstudent|working student|studentische|pflichtpraktikum|"
    r"hiwi|thesis|apprenticeship)\b",
    re.I,
)
SENIOR_MARKERS = re.compile(
    r"\b(senior|lead|head|director|principal|staff|architect)\b", re.I
)


def scan_remotive() -> list[dict[str, Any]]:
    """Fetch the newest remote postings from the Remotive public API.

    Returns normalized rows:
      {title, company, location, url, category, tags, remote, posted}
    """
    resp = requests.get(REMOTIVE_API, timeout=30)
    resp.raise_for_status()
    data = resp.json()
    rows = []
    for item in data.get("jobs", []):
        rows.append(
            {
                "title": item.get("title", ""),
                "company": item.get("company_name", ""),
                "location": item.get("candidate_required_location", ""),
                "url": item.get("url", ""),
                "category": item.get("category", ""),
                "tags": item.get("tags", []) or [],
                "remote": True,
                "posted": item.get("publication_date", ""),
            }
        )
    return rows


def normalize_rows(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Drop rows that are clearly out of scope and annotate the rest."""
    kept = []
    for r in rows:
        title = r["title"]
        if STUDENT_MARKERS.search(title):
            continue
        if SENIOR_MARKERS.search(title):
            continue
        r["fit_flags"] = {
            "student_role": bool(STUDENT_MARKERS.search(title)),
            "senior_role": bool(SENIOR_MARKERS.search(title)),
        }
        kept.append(r)
    return kept


def rank_by_keywords(rows: list[dict[str, Any]], keywords: list[str]) -> list[dict[str, Any]]:
    """Cheap deterministic pre-rank: count keyword hits in title+tags+category.

    The Strands agent re-ranks with reasoning; this gives it a signal.
    """
    scored = []
    for r in rows:
        hay = (
            r["title"] + " " + " ".join(r["tags"]) + " " + r["category"]
        ).lower()
        score = sum(1 for k in keywords if k.lower() in hay)
        scored.append({**r, "keyword_score": score})
    scored.sort(key=lambda x: x["keyword_score"], reverse=True)
    return scored
