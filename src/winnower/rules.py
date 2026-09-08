"""Fit rules for Job-Sift (author's real constraints, configurable).

These mirror the rules the author applies to his own daily job scan:
entry level, remote first, no enrollment gates, English-capable.
"""
from __future__ import annotations

FIT_RULES = """
- Entry level only: internships, graduate programs, junior roles. Skip senior,
  lead, head, director, principal, staff titles, and roles demanding 2+ years.
- Remote-first: remote or hybrid roles rank above on-site.
- Skip student-gated roles: werkstudent / working-student (German university
  enrollment required).
- Skip enrollment-window roles: 'must be enrolled', class of YYYY windows.
- Skip roles requiring a specific degree the candidate lacks (law, medicine,
  engineering degrees, CS-only requirements).
- English language preferred; German-only postings are out.
- Flag roles that offer visa sponsorship or relocation.
"""

CV_FACTS = """
- BSc Mass Communication, Lagos State University, 2023 (communication + marketing)
- Technical: Python, SQL, AI tooling, automation, Chrome extension dev
- Shipped TweetScrub: content moderation tool for web3 communities (live,
  integrated payments: Paystack, Stripe, Coinbase Commerce)
- Certifications: AI Fluency (Anthropic), Google Prompting Essentials,
  AWS AI Practitioner, Data Labeling & Annotation (DataLens Africa),
  EF SET C2 English
- Career goal: Product Management. Product marketing for technical products
  is the target intersection.
- Location: Lagos, Nigeria. Open to remote, hybrid, or relocation.
"""
