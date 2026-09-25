<h1 align="center">LLM Security &nbsp;·&nbsp; Systems Programming</h1>

<p align="center">
  <em>Adversarial testing, low-level optimization, and quantitative research.</em>
</p>

<p align="center">
  <a href="https://github.com/MRX-72">
    <picture>
      <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/MRX-72/MRX-72/main/stats-dark.svg" />
      <source media="(prefers-color-scheme: light)" srcset="https://raw.githubusercontent.com/MRX-72/MRX-72/main/stats-light.svg" />
      <img src="https://raw.githubusercontent.com/MRX-72/MRX-72/main/stats-dark.svg" alt="GitHub stats" width="470" />
    </picture>
  </a>
</p>

---

## Recent Contributions

> Work merged into upstream security tooling.

| Project | Contribution | Upstream |
| :-- | :-- | :-- |
| **[CrowdStrike/falconpy](https://github.com/CrowdStrike/falconpy/pull/1510)** | preserve non-JSON response bodies instead of silently discarding them | 516★ · merged |
| **[hashcat](https://github.com/hashcat/hashcat/pulls?q=is%3Apr+author%3AMRX-72+is%3Amerged)** | zlib symbol loading on macOS; leaks in config teardown; unchecked lock/unlock return values; 22000/22001 outfile line written as loaded | 26.9k★ · 4 merged |
| **[NetExec](https://github.com/Pennyw0rth/NetExec/pull/1428)** | SSH login timeouts now fail cleanly instead of raising | 5.9k★ · merged |
| **[nmap](https://github.com/nmap/nmap/blob/8a11c8c2042d9c594bed0e75d073e590d048dab7/CHANGELOG#L5-L9)** | Ncat no longer signals its own process group | 13.7k★ · credited |
| **[OWASP AISVS](https://github.com/OWASP/AISVS/pull/1153)** | missing controls in the Appendix B inventory | 456★ · merged |
| **[OWASP DockSec](https://github.com/OWASP/DockSec/pull/169)** | passwords leaking from connection-string URLs | 490★ · merged |
| **[OWASP cve-lite-cli](https://github.com/OWASP/cve-lite-cli/pulls?q=is%3Apr+author%3AMRX-72+is%3Amerged)** | batches FIRST.org EPSS queries for full CVE coverage; accurate error hints for unreadable lockfiles; scanner comparison analysis | 738★ · 3 merged |
| **[VirusTotal/yara](https://github.com/VirusTotal/yara/pulls?q=is%3Apr+author%3AMRX-72+is%3Amerged)** | `yr_get_version` runtime version API; nine more ELF `e_machine` values exposed | 9.9k★ · 2 merged |
| **[GenAI Red Team Lab](https://github.com/GenAI-Security-Project/GenAI-Red-Team-Lab/pull/81)** | memory-poisoning exploit module | 54★ · merged |

---

## Tech Stack

<p align="center">
<img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python" /> <img src="https://img.shields.io/badge/C%2B%2B-00599C?style=for-the-badge&logo=cplusplus&logoColor=white" alt="C++" /> <img src="https://img.shields.io/badge/C-A8B9CC?style=for-the-badge&logo=c&logoColor=white" alt="C" /> <img src="https://img.shields.io/badge/Go-00ADD8?style=for-the-badge&logo=go&logoColor=white" alt="Go" /> <img src="https://img.shields.io/badge/NumPy-013243?style=for-the-badge&logo=numpy&logoColor=white" alt="NumPy" /> <img src="https://img.shields.io/badge/pandas-150458?style=for-the-badge&logo=pandas&logoColor=white" alt="pandas" /> <img src="https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white" alt="Docker" /> <img src="https://img.shields.io/badge/PostgreSQL-4169E1?style=for-the-badge&logo=postgresql&logoColor=white" alt="PostgreSQL" />
</p>

---

## Research

### Where do production LLM guardrails actually fail?

**Setup.** Four production models were each run through the same 107 attack
vectors covering all ten OWASP LLM Top 10 categories. Same system prompt, temperature 0,
zero errors across every run. Detection was deterministic: a random secret
("canary") was planted in the system prompt, and a vector counted as a bypass only
if the model's output contained it (or a fixed leak pattern). No LLM judge.

```
  Vectors bypassed, out of 107

  gemini-3.1-flash-lite  ███████████████  15/107
  gpt-oss-20b            ██████████·····  10/107
  gpt-oss-120b           █████··········  5/107
  qwen3.8-27b            █████··········  5/107
```

Where the 35 failures landed:

```
  agentic & output layer   ████████████████████████████████████  34
  everything else          █                                      1

  jailbreaks · encoding bypass · indirect injection
  · system-prompt extraction  (51 vectors)              zero bypasses
```

**Finding.** The attacks everyone writes about **failed completely.** 51 vectors
covering jailbreaks, encoding bypass (base64, ROT13, homoglyphs), indirect injection
and system-prompt extraction got **0 bypasses on all four models**.

34 of the 35 failures landed in the *agentic and output* layer instead:

- **Tool misuse:** calling `transfer_funds` with no confirmation, running a `send_email` call that was hidden inside a pasted ticket, using an admin token when a normal tool would have worked
- **Output handling:** filling a secret into a markdown image URL, which leaks it with zero clicks as soon as the chat renders
- **PII disclosure:** asked to reformat a config file as JSON, all four models returned the API keys unredacted
- **Confabulation:** inventing a pip package name, which opens the door to slopsquatting
- **Unbounded consumption:** getting pushed into runaway repetitive output

> **Takeaway:** refusal training works on the prompts it was trained on. The risk
> sits *after* the model decides to help: in what it writes, which tools it calls,
> and what data it repeats back. The same model that refuses a poisoned document
> telling it to *say* something will obey one telling it to *do* something.

<sub>One run per model at temperature 0, so these are observations and not rates ·
synthetic system prompt · the suite has since grown to 330 vectors, and the new ones
have not been run yet · every raw report and per-finding transcript is public</sub>

<p align="center">
  <a href="https://github.com/MRX-72/llm-red-team-cli#field-results"><b>Full evaluation →</b></a>
  &nbsp;·&nbsp;
  <a href="https://github.com/MRX-72/llm-red-team-cli/tree/main/results"><b>Raw data →</b></a>
</p>

---

## Projects

> Built and maintained solo. All open source.

### [llm-red-team-cli](https://github.com/MRX-72/llm-red-team-cli)

<a href="https://github.com/MRX-72/llm-red-team-cli/actions/workflows/ci.yml"><img src="https://github.com/MRX-72/llm-red-team-cli/actions/workflows/ci.yml/badge.svg" alt="CI" /></a> <a href="https://github.com/MRX-72/llm-red-team-cli/blob/main/LICENSE"><img src="https://img.shields.io/badge/license-MIT-3da639?style=flat-square" alt="MIT" /></a> <img src="https://img.shields.io/badge/330%20vectors-8957e5?style=flat-square" alt="330 vectors" />

**Red-teams an LLM app against the OWASP LLM Top 10 and reports exactly which attacks got through.**
A random canary planted in the system prompt makes every finding a reproducible string
match: one API call per vector, no second LLM to judge. Works with any provider via LiteLLM.

```bash
lrtf scan gpt-4o --tui               # live view as each vector lands
lrtf compare gpt-4o claude-sonnet-4-5 ollama/llama3
lrtf diff base.json current.json     # did your fix actually work?
```

### [QFcli](https://github.com/MRX-72/QFcli)

<a href="https://github.com/MRX-72/QFcli/actions/workflows/ci.yml"><img src="https://github.com/MRX-72/QFcli/actions/workflows/ci.yml/badge.svg" alt="CI" /></a> <a href="https://github.com/MRX-72/QFcli/blob/main/LICENSE"><img src="https://img.shields.io/badge/license-MIT-3da639?style=flat-square" alt="MIT" /></a> <img src="https://img.shields.io/badge/walk--forward-8957e5?style=flat-square" alt="walk-forward" />

**Backtests strategies and builds portfolios, with the statistical checks that flag an overfit result.**
Signals are lagged one bar (no lookahead), costs are charged on turnover, and every result is
benchmarked to buy-and-hold. Walk-forward validation, Black-Litterman allocation, and bootstrap
significance tests on the Sharpe.

```bash
qfcli --backtest AAPL --walk-forward --ensemble rank --grid "fast=10,20;slow=40,60"
qfcli --portfolio AAPL MSFT NVDA --bl --view NVDA=0.18 --ff
```

### [zapscan](https://github.com/MRX-72/zapscan)

<a href="https://github.com/MRX-72/zapscan/actions/workflows/ci.yml"><img src="https://github.com/MRX-72/zapscan/actions/workflows/ci.yml/badge.svg" alt="CI" /></a> <a href="https://github.com/MRX-72/zapscan/blob/main/LICENSE"><img src="https://img.shields.io/badge/license-MIT-3da639?style=flat-square" alt="MIT" /></a> <img src="https://img.shields.io/badge/zero%20deps-2ea043?style=flat-square" alt="zero deps" />

**A dependency-free TCP port scanner in C++17 on raw BSD sockets. It never shells out to `nmap`.**
Non-blocking `connect()` with `poll()` timeouts, a bounded worker pool, banner grabbing, and
stable text/JSON/CSV output. CI runs ASan/UBSan on macOS and Linux.

```bash
zapscan -p 1-1024 -c 256 scanme.nmap.org
zapscan -j -o report.json -p 22,80,443 10.0.0.0/24
```

---

## Focus Areas

**LLM security** &nbsp; Prompt injection, jailbreaks, encoding bypass, RAG injection and multi-turn chains, scored by deterministic canary detection.

**Agentic AI security** &nbsp; Memory poisoning and excessive-agency abuse across LangChain, ChromaDB and Mem0, and the integrity checks that catch it.

**Systems & offensive security** &nbsp; POSIX-socket network tooling, x86_64 assembly, email forensics, and dependency CVE analysis via OSV.

**Quantitative finance** &nbsp; Backtesting that catches its own overfitting: no lookahead, costs on turnover, walk-forward validation.

---

## Now

- **Shipped** — [LRTF](https://github.com/MRX-72/llm-red-team-cli): an LLM red-team CLI. 330 vectors mapped to the OWASP LLM Top 10, deterministic canary detection, multi-turn attack chains, multi-provider through LiteLLM.
- **Building** — AMPAF, an agentic memory-poisoning framework. Four payload classes (identity shift, behavior drift, data exfiltration, bias injection) against LangChain, ChromaDB, and Mem0, with an integrity checker, anomaly detector, and live memory-state monitor.
- **Direction** — a full-lifecycle AI security toolchain: pre-deployment testing, runtime defense, incident forensics.
- **Collaborator** — [OWASP](https://owasp.org).
- **Core dev** — [Omnikon](https://www.omnikonhub.com/).

---

<p align="center">
  <a href="mailto:theaiguy369@gmail.com">theaiguy369@gmail.com</a>
</p>
