# Winnower

> It keeps the grain. It blows away the chaff.

Winnower is an AI agent (Strands Agents SDK) that separates the real job fits
from the chaff. It runs the repetitive end of a job hunt end to end: scans
boards, filters against your fit rules, shortlists with reasons, drafts
tailored cover letters, tracks applications, and pings follow-ups. Quiet in
the background, present only when a decision matters.

Built for the [Agents for Humans](https://agentsforhumans.devpost.com/)
hackathon (Professional Agents track). The author runs a version of this
pipeline every day as his own job-hunt copilot; this repo is the productized
agent.

## Why "Winnower"

Winnowing is the old craft of tossing grain into the wind so the breeze
carries away the chaff and the good grain falls back to the winnower's hand.
That is exactly what a job-hunt copilot does: the listings are the harvest,
the ghost postings and wrong-fit roles are the chaff, and the shortlist is
the grain worth keeping.

## What it does

```
job boards -> scan tool -> fit filter -> shortlist (LLM ranked, with reasons)
           -> approval (human in the loop) -> cover letter draft -> tracker write -> follow-up nudge
```

Three Strands agents, one pipeline:

1. **Scout agent** - deterministic tools fetch and normalize rows from public
   job APIs (Remotive, arbeitnow is dead). No LLM guesses in the data layer.
2. **Sifter agent** - applies fit rules (entry level, remote first, no
   enrollment gates, English) and ranks candidates with reasons.
3. **Drafter agent** - writes tailored cover letters from a template and
   verified CV facts, then appends the application to the tracker.

Human approval is a first-class step (Strands interrupts): nothing is sent
until the user confirms. No apply-spam bots here.

## Architecture

```
[public job APIs] --scan tool--> [normalized rows] --sifter--> [shortlist]
                                                                  |
                                                     [user approves] (interrupt)
                                                                  |
                                     [drafter] -> [letter md] -> [tracker csv]
```

- Strands Agents SDK: agent loop, tools, interrupts, structured output
- LiteLLM provider: any model (DeepSeek / OpenRouter / Bedrock)
- Data layer: plain deterministic Python (requests + parsing), testable

## Setup

```bash
python -m venv .venv && source .venv/bin/activate
pip install 'strands-agents[litellm]' strands-agents-tools requests
cp .env.example .env   # set DEEPSEEK_API_KEY or OPENROUTER_API_KEY
python -m src.winnower.agent --demo
```

## Model

Default: DeepSeek via LiteLLM (`deepseek/deepseek-chat`), falls back to
OpenRouter. No AWS account required. Amazon Bedrock + AgentCore deployment is
a drop-in swap for the demo-day bonus points.

## License

MIT
