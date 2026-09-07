<h1 align="center">AI Red Teamer &nbsp;·&nbsp; Systems Engineer</h1>

<p align="center">
  <em>Adversarial testing, low-level optimization, and quantitative research.</em>
</p>

<p align="center">
  <a href="https://github.com/MRX-72"><img src="https://raw.githubusercontent.com/MRX-72/MRX-72/main/stats.svg" alt="GitHub stats" width="470" /></a>
</p>

<p align="center">
  <a href="https://github.com/OWASP/cve-lite-cli"><img src="https://img.shields.io/badge/OWASP-invited%20maintainer-000000?style=for-the-badge&logo=owasp&logoColor=white" alt="OWASP" /></a>
  <img src="https://img.shields.io/badge/C%2B%2B-17-00599C?style=for-the-badge&logo=cplusplus&logoColor=white" alt="C++" />
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python" />
  <img src="https://img.shields.io/badge/Go-00ADD8?style=for-the-badge&logo=go&logoColor=white" alt="Go" />
</p>

---

## What I found

I built an adversarial test harness and pointed it at four production LLMs —
**300 vectors, 10 OWASP categories, one canary-based deterministic detector.**

| | |
|---|---|
| **51 vectors** of jailbreaks, encoding bypass, poisoned RAG and prompt extraction | got through **0 times**, on any model |
| **All 35 failures** | were in tool use, output handling, PII and confabulation |
| **1 vector** — credential passthrough in a reformatting task | failed on **every model tested** |

The attacks people write about are the ones these models are trained hardest to
refuse — and they do refuse them. The holes are *downstream of the refusal*: what
the model emits, what it does, and what it repeats back.

One model went from a clean pass to the worst score of the four, without
changing — the suite grew to cover tool use, and that is where it broke.

<p align="center">
  <a href="https://github.com/MRX-72/llm-red-team-cli#field-results"><b>Full results, raw reports and reproduction steps →</b></a>
</p>

---

## Projects

### [llm-red-team-cli](https://github.com/MRX-72/llm-red-team-cli) &nbsp;<a href="https://github.com/MRX-72/llm-red-team-cli/actions/workflows/ci.yml"><img src="https://github.com/MRX-72/llm-red-team-cli/actions/workflows/ci.yml/badge.svg" alt="CI" /></a>

> *Find where an LLM's guardrails crack — deterministically, not by judge-model opinion.*

A fresh random **canary** is planted in the system prompt at scan time, so a
finding is a string match: reproducible, one API call per vector, no second model
grading the first. 12 vectors run as real **multi-turn conversations**, because a
guardrail that holds against one message often erodes across five.

```bash
lrtf scan gpt-4o --tui               # live view as each vector lands
lrtf scan gpt-4o --system mine.txt   # test your own prompt, not a toy one
lrtf compare gpt-4o claude-sonnet-4-5 ollama/llama3
lrtf diff base.json current.json     # did your fix actually work?
```

### [QFcli](https://github.com/MRX-72/QFcli) &nbsp;<a href="https://github.com/MRX-72/QFcli/actions/workflows/ci.yml"><img src="https://github.com/MRX-72/QFcli/actions/workflows/ci.yml/badge.svg" alt="CI" /></a>

> *A backtester that tells you when your strategy adds nothing.*

Signals shift one bar — **no lookahead**. Cost and slippage are charged against
turnover. Every run reports alpha and information ratio **against buy-and-hold**,
so a strategy with no edge says so out loud.

Walk-forward validation, ensemble blending, target-vol and fractional-Kelly
sizing, **Black-Litterman** allocation over shrinkage and PCA-factor covariance,
Fama-French overlay, bootstrap and Jobson-Korkie significance tests. Pure
numpy/pandas.

```bash
qfcli --backtest AAPL --walk-forward --ensemble rank --grid "fast=10,20;slow=40,60"
qfcli --portfolio AAPL MSFT NVDA --bl --view NVDA=0.18 --ff
```

### [zapscan](https://github.com/MRX-72/zapscan) &nbsp;<a href="https://github.com/MRX-72/zapscan/actions/workflows/ci.yml"><img src="https://github.com/MRX-72/zapscan/actions/workflows/ci.yml/badge.svg" alt="CI" /></a>

> *See what's listening on a network. No dependencies, no `nmap` underneath.*

Native parallel TCP scanner in **C++17**. Non-blocking `connect()` awaited through
`poll()`, from a bounded worker pool with deterministic concurrency — scan the same
range twice, get the same behaviour twice. Banner grabs on open ports, JSON output,
input validated before a single packet is sent.

Verified by a **CTest** suite that spins up real listening sockets, with
**ASan/UBSan** in CI on macOS and Linux.

```bash
zapscan -p 1-1024 -c 256 scanme.nmap.org
zapscan -j -o report.json -p 22,80,443 10.0.0.0/24
```

---

## Stack

**Languages** &nbsp;C++ · Go · Python · x86_64 Assembly

**LLM security** &nbsp;prompt injection · jailbreak and encoding-bypass vectors ·
system-prompt extraction · multi-turn attack chains · canary-based deterministic
detection · OWASP LLM Top 10

**Agentic AI** &nbsp;memory poisoning (LangChain / ChromaDB / Mem0) · RAG and
retrieval security · tool-use and excessive-agency attacks

**Offensive security** &nbsp;network recon and port scanning · dependency
vulnerability analysis and CVE identification · low-level socket programming

**Quant** &nbsp;no-lookahead backtesting · walk-forward validation ·
Black-Litterman · shrinkage and PCA-factor covariance · vol-managed sizing

---

## Now

- **AI red teaming** — tooling against the OWASP LLM Top 10, with detection that is deterministic rather than model-judged
- **Agentic AI security** — mapping memory-poisoning and agent-manipulation surfaces, and building runtime defense against them
- **Invited maintainer** — [OWASP/cve-lite-cli](https://github.com/OWASP/cve-lite-cli)

---

<p align="center">
  <a href="mailto:theaiguy369@gmail.com"><img src="https://img.shields.io/badge/theaiguy369@gmail.com-EA4335?style=for-the-badge&logo=gmail&logoColor=white" alt="Email" /></a>
</p>
