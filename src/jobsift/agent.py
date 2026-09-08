"""Job-Sift agent: wire Strands agents to the job-hunt pipeline.

Usage:
    python -m src.jobsift.agent --demo        # run the scout + sifter once
    python -m src.jobsift.agent --scan-only   # just fetch and normalize rows

Model: DeepSeek via LiteLLM by default (DEEPSEEK_API_KEY), falls back to
OpenRouter (OPENROUTER_API_KEY). Override with JOB_SIFT_MODEL.
"""
from __future__ import annotations

import os
import sys

from strands import Agent, tool
from strands.models.litellm import LiteLLMModel

from jobsift.rules import CV_FACTS, FIT_RULES
from jobsift.tools.scan import normalize_rows, rank_by_keywords, scan_remotive


def _load_key(name: str) -> str | None:
    # read from env, including the Hermes .env convention
    v = os.environ.get(name)
    if v:
        return v
    env_path = os.path.expanduser("~/.hermes/.env")
    if os.path.exists(env_path):
        for line in open(env_path):
            line = line.strip()
            if line.startswith(name + "="):
                return line.partition("=")[2].strip().strip('"\'')
    return None


def build_model() -> LiteLLMModel:
    """DeepSeek direct (free tier) or OpenRouter, via LiteLLM."""
    deepseek_key = _load_key("DEEPSEEK_API_KEY")
    openrouter_key = _load_key("OPENROUTER_API_KEY")

    if deepseek_key:
        return LiteLLMModel(
            client_args={"api_key": deepseek_key},
            model_id=os.environ.get("JOB_SIFT_MODEL", "deepseek/deepseek-chat"),
            params={"max_tokens": 2000, "temperature": 0.3},
        )
    if openrouter_key:
        return LiteLLMModel(
            client_args={
                "api_key": openrouter_key,
                "api_base": "https://openrouter.ai/api/v1",
            },
            model_id=os.environ.get(
                "JOB_SIFT_MODEL", "openrouter/deepseek/deepseek-v4-flash-0731"
            ),
            params={"max_tokens": 2000, "temperature": 0.3},
        )
    raise RuntimeError(
        "No model key found. Set DEEPSEEK_API_KEY or OPENROUTER_API_KEY "
        "(e.g. in ~/.hermes/.env)."
    )


def build_scout_agent() -> Agent:
    """Scout: fetch + normalize. Pure deterministic tools."""
    return Agent(
        model=build_model(),
        tools=[scan_remotive, normalize_rows, rank_by_keywords],
    )


def build_sifter_agent() -> Agent:
    """Sifter: rank the normalized pool against the fit rules.

    The rules and CV facts are injected as context; the agent's reasoning
    produces the ranked shortlist with reasons (structured output in v0.2).
    """
    return Agent(
        model=build_model(),
        system_prompt=(
            "You are Job-Sift, a job-hunt copilot. You turn raw job rows into "
            "a shortlist a human can act on. Follow the fit rules exactly. "
            "Be honest: if a row fails a rule, say why. Never invent roles "
            "that are not in the input data.\n\n"
            f"FIT RULES:\n{FIT_RULES}\n\n"
            f"CANDIDATE FACTS:\n{CV_FACTS}"
        ),
    )


def demo() -> None:
    """Scout -> normalize -> deterministic pre-rank, print the pool."""
    print("Scanning Remotive...")
    rows = scan_remotive()
    print(f"Fetched {len(rows)} rows")
    kept = normalize_rows(rows)
    print(f"After fit normalization: {len(kept)} rows")
    top = rank_by_keywords(kept, ["product", "marketing", "analyst", "operations", "data"])
    for r in top[:10]:
        print(f"  [{r['keyword_score']}] {r['title']} @ {r['company']} - {r['location']}")
        print(f"      {r['url']}")


if __name__ == "__main__":
    if "--scan-only" in sys.argv:
        rows = scan_remotive()
        print(f"{len(rows)} rows fetched")
        for r in rows[:15]:
            print(f"  {r['title']} @ {r['company']} - {r['location']}")
    else:
        demo()
