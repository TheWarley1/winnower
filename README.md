# Job-Sift

AI agent (Strands Agents SDK) that runs the repetitive end of a job hunt end to end:
scan job boards, filter to your fit rules, shortlist with reasons, draft tailored
cover letters, track applications, and ping follow-ups. Built for the
[Agents for Humans](https://agentsforhumans.devpost.com/) hackathon (Professional Agents track).

The author runs a version of this pipeline every day as his own job-hunt copilot,
powered by Strands Agents inside Hermes. This repo is the productized agent.

## What it does

```
job boards -> scan tool -> fit filter -> shortlist (LLM ranked, with reasons)
           -> approval (human in the loop) -> cover letter draft -> tracker write -> follow-up nudge
```

Three Strands agents, one pipeline:

1. **Scout agent** - deterministic tools fetch and normalize rows from public
   job APIs (arbeitnow, etc). No LLM guesses in the data layer.
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
python -m src.jobsift.agent --demo
```

## Model

Default: DeepSeek via LiteLLM (`deepseek/deepseek-chat`), falls back to
OpenRouter. No AWS account required. Amazon Bedrock + AgentCore deployment is
a drop-in swap for the demo-day bonus points.

## License

MIT
