# AI Red Teamer | Systems Engineer

Adversarial testing, low-level optimization, automation, and quantitative research.

[![GitHub Followers](https://img.shields.io/github/followers/MRX-72)](https://github.com/MRX-72) [![Public Repos](https://img.shields.io/github/repos/MRX-72)](https://github.com/MRX-72?tab=repositories) [![Total Forks](https://img.shields.io/github/forks/MRX-72)](https://github.com/MRX-72)

<p align="center">
  <a href="https://github.com/MRX-72">
    <img height="170" src="https://github-readme-stats-one-bice.vercel.app/api?username=MRX-72&show_icons=true&include_all_commits=true&theme=react&hide_border=true&hide=stars,prs" />
  </a>
  <img height="170" src="https://github-readme-stats-one-bice.vercel.app/api/top-langs/?username=MRX-72&layout=compact&theme=react&hide_border=true" />
</p>

---

## Featured

### [llm-red-team-cli](https://github.com/MRX-72/llm-red-team-cli)

[![CI](https://github.com/MRX-72/llm-red-team-cli/actions/workflows/ci.yml/badge.svg)](https://github.com/MRX-72/llm-red-team-cli/actions/workflows/ci.yml) [![License: MIT](https://img.shields.io/badge/License-MIT-brightgreen.svg)](https://github.com/MRX-72/llm-red-team-cli/blob/main/LICENSE) [![Last Commit](https://img.shields.io/github/last-commit/MRX-72/llm-red-team-cli)](https://github.com/MRX-72/llm-red-team-cli/commits) [![Open Issues](https://img.shields.io/github/issues/MRX-72/llm-red-team-cli)](https://github.com/MRX-72/llm-red-team-cli/issues) [![Python 3.9+](https://img.shields.io/badge/Python-3.9%2B-blue.svg)](https://github.com/MRX-72/llm-red-team-cli) [![Code Size](https://img.shields.io/github/languages/code-size/MRX-72/llm-red-team-cli)](https://github.com/MRX-72/llm-red-team-cli) [![Repo Size](https://img.shields.io/github/repo-size/MRX-72/llm-red-team-cli)](https://github.com/MRX-72/llm-red-team-cli)

*Pinpoint where an LLM's guardrails crack — deterministically, not by judge-model opinion.*

Adversarial test harness for LLM applications. **107 vectors across 10 categories**
mapped to the OWASP LLM Top 10 — prompt injection, jailbreaks, encoding bypass,
indirect injection, system-prompt leakage, PII disclosure, improper output
handling, excessive agency, unbounded consumption, misinformation.

Deeper terms: detection is **canary-based, not LLM-judged** — a fresh random token
is planted in the system prompt at scan time, so a finding is a deterministic
string match: reproducible, one API call per vector, no judge model. 12 vectors
run as real **multi-turn conversations**, because a guardrail that holds against
one message often erodes across five.

Live results are published in the README, including a reproduced persona-split
bypass where a model refuses and complies in the same reply.

```bash
lrtf scan gpt-4o --tui              # live view
lrtf scan gpt-4o --system mine.txt  # test your own prompt
lrtf diff base.json current.json    # did the fix work?
```

### [QFcli](https://github.com/MRX-72/QFcli)

[![CI](https://github.com/MRX-72/QFcli/actions/workflows/ci.yml/badge.svg)](https://github.com/MRX-72/QFcli/actions/workflows/ci.yml) [![License: MIT](https://img.shields.io/badge/License-MIT-brightgreen.svg)](https://github.com/MRX-72/QFcli/blob/main/LICENSE) [![Last Commit](https://img.shields.io/github/last-commit/MRX-72/QFcli)](https://github.com/MRX-72/QFcli/commits) [![Open Issues](https://img.shields.io/github/issues/MRX-72/QFcli)](https://github.com/MRX-72/QFcli/issues) [![Python 3.9+](https://img.shields.io/badge/Python-3.9%2B-blue.svg)](https://github.com/MRX-72/QFcli) [![Code Size](https://img.shields.io/github/languages/code-size/MRX-72/QFcli)](https://github.com/MRX-72/QFcli) [![Repo Size](https://img.shields.io/github/repo-size/MRX-72/QFcli)](https://github.com/MRX-72/QFcli)

A command-line quantitative research workbench for stock analysis, strategy backtesting, and portfolio optimization. Signals are shifted one bar (**no lookahead**), realistic cost/slippage is charged against turnover, and every run reports alpha / active return / information ratio against buy-and-hold — so a strategy that doesn't add value says so.

Deeper terms: **walk-forward** out-of-sample validation with parameter grids and **ensemble blending** (`equal` / `rank` / `topk`), a **paper-trading harness** with a **hysteresis stability filter** (`--stable-days`), **target-vol and fractional-Kelly position sizing** with a **slow-vol, Moreira–Muir style overlay** (`--slow-vol-window`), and portfolio math built on **shrinkage covariance**, **PCA factor risk models**, **Black-Litterman** with absolute views and a **Fama-French factor prior**, plus **Monte Carlo / bootstrap / Jobson–Korkie** significance tests. Pure **numpy/pandas**, no scipy, offline test suite, deterministic `--json` output.

```bash
qfcli AAPL --period 5y              # single-stock analysis: metrics, stats, regime
qfcli --backtest AAPL --walk-forward --ensemble rank --grid "fast=10,20;slow=40,60"
qfcli --portfolio AAPL MSFT NVDA --bl --view NVDA=0.18 --ff   # Black-Litterman + factor overlay
qfcli --paper-trade AAPL --stable-days 5                      # monitor — it does not place orders
```

### [zapscan](https://github.com/MRX-72/zapscan)

[![CI](https://github.com/MRX-72/zapscan/actions/workflows/ci.yml/badge.svg)](https://github.com/MRX-72/zapscan/actions/workflows/ci.yml) [![License: MIT](https://img.shields.io/badge/License-MIT-brightgreen.svg)](https://github.com/MRX-72/zapscan/blob/main/LICENSE) [![Last Commit](https://img.shields.io/github/last-commit/MRX-72/zapscan)](https://github.com/MRX-72/zapscan/commits) [![Open Issues](https://img.shields.io/github/issues/MRX-72/zapscan)](https://github.com/MRX-72/zapscan/issues) [![C++17](https://img.shields.io/badge/C%2B%2B-17-blue.svg)](https://github.com/MRX-72/zapscan) [![Code Size](https://img.shields.io/github/languages/code-size/MRX-72/zapscan)](https://github.com/MRX-72/zapscan) [![Repo Size](https://img.shields.io/github/repo-size/MRX-72/zapscan)](https://github.com/MRX-72/zapscan)

*The no-dependency way to see what is listening on a network.*

Native parallel TCP port scanner in **C++17** — no `nmap` underneath. Connections
are made with non-blocking `connect()` and awaited through `poll()`, from a
bounded worker pool with deterministic concurrency, so scanning the same range
twice behaves the same twice.

Deeper terms: targets parse as **IPs, hostnames, CIDR blocks, and ranges**,
ports as `80`, `1-1000`, or `22,80,443-900` with deduplication, and everything
is validated up front — invalid input aborts before a single packet is sent.
Open ports get a **banner grab** reconnecting and reading up to 2 KB. Output is
either text or machine-parsable **JSON**, with banners sanitized to printable
characters.

Verified by a **CTest** suite that spins up real listening sockets on loopback,
**ASan/UBSan** runs in CI on macOS and Linux, and there are no dependencies to
pin or shell out to.

```bash
zapscan -p 1-1024 -c 256 scanme.nmap.org   # sweep the default range fast
zapscan 10.0.0.0/24                        # subnet via CIDR
zapscan -j -o report.json -p 22,80,443 db.prod.corp
```

---

## Technical Stack

* **Languages:** C++, Go, Python, x86_64 Assembly
* **Focus:** AI Red Teaming, LLM Security, Offensive Security, Vulnerability Analysis
* **LLM Red Teaming:** prompt injection, jailbreak & encoding-bypass vectors, system-prompt extraction, OWASP LLM Top 10 mapping, canary-based deterministic detection, multi-turn attack chains
* **Agentic AI Security:** memory-poisoning surfaces (LangChain / ChromaDB / Mem0), RAG & retrieval security, tool-use and excessive-agency attacks
* **Offensive Security:** network recon & port scanning (C++17, [`zapscan`](https://github.com/MRX-72/zapscan)), dependency vulnerability analysis & CVE identification (invited maintainer, [`OWASP/cve-lite-cli`](https://github.com/OWASP/cve-lite-cli)), low-level socket programming and request pacing for adversarial tooling
* **Quantitative Finance:** parameterized backtesting with no-lookahead signals and cost/slippage modeling, walk-forward validation with ensemble parameter blending, target-vol / Kelly / vol-managed position sizing, mean-variance & **Black-Litterman** allocation with **shrinkage and PCA-factor covariance**, **Fama-French** factor overlay, paper-trading harness ([`QFcli`](https://github.com/MRX-72/QFcli))
* **Systems & Automation:** Linux internals, socket programming, n8n orchestration

---

## Open Source

* **Invited maintainer** — [OWASP/cve-lite-cli](https://github.com/OWASP/cve-lite-cli), a JS/TS dependency vulnerability scanner
* [llm-red-team-cli](https://github.com/MRX-72/llm-red-team-cli) — LLM adversarial test harness
* [zapscan](https://github.com/MRX-72/zapscan) — C++17 port scanner and recon tool

---

## Current Work

* **AI Red Teaming** — building tooling against the OWASP LLM Top 10, with an emphasis on detection that is deterministic rather than model-judged
* **Agentic AI Security** — mapping memory-poisoning and agent-manipulation surfaces, and building runtime defense against them
* **Systems Programming** — low-level Linux utilities and automated infrastructure workflows in Go, C++, and n8n
* **Quantitative Finance** — honest backtesting and portfolio tooling: no-lookahead signals, walk-forward validation, Black-Litterman allocation

---

## Contact

* Email: theaiguy369@gmail.com
