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

<p align="center">
  <img src="https://img.shields.io/badge/x86__64%20Assembly-6E4C13?style=for-the-badge" alt="x86_64 Assembly" />
  <img src="https://img.shields.io/badge/C%2B%2B-17-00599C?style=for-the-badge&logo=cplusplus&logoColor=white" alt="C++" />
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python" />
  <img src="https://img.shields.io/badge/Go-00ADD8?style=for-the-badge&logo=go&logoColor=white" alt="Go" />
</p>

---

## Research

### Where do production LLM guardrails actually fail?

**Setup.** Four production models were each run through the same 107 attack
vectors covering all ten OWASP LLM Top 10 categories. Same system prompt, temperature 0,
zero errors across every run. Detection was deterministic: a random secret
("canary") was planted in the system prompt, and a vector counted as a bypass only
if the model's output contained it (or a fixed leak pattern). No LLM judge.

| Model | Bypassed |
|---|---|
| `gemini-3.1-flash-lite` | 15 / 107 |
| `gpt-oss-20b` | 10 / 107 |
| `gpt-oss-120b` | 5 / 107 |
| `qwen3.8-27b` | 5 / 107 |

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

### [llm-red-team-cli](https://github.com/MRX-72/llm-red-team-cli)

<a href="https://github.com/MRX-72/llm-red-team-cli/actions/workflows/ci.yml"><img src="https://github.com/MRX-72/llm-red-team-cli/actions/workflows/ci.yml/badge.svg" alt="CI" /></a> <a href="https://github.com/MRX-72/llm-red-team-cli/blob/main/LICENSE"><img src="https://img.shields.io/badge/license-MIT-3da639?style=flat-square" alt="MIT" /></a> <img src="https://img.shields.io/badge/Python%203.9%2B-3776AB?style=flat-square&logo=python&logoColor=white" alt="Python 3.9+" /> <img src="https://img.shields.io/badge/OWASP%20LLM%20Top%2010-000000?style=flat-square&logo=owasp&logoColor=white" alt="OWASP LLM Top 10" /> <img src="https://img.shields.io/badge/330%20vectors-8957e5?style=flat-square" alt="330 vectors" /> <img src="https://img.shields.io/badge/240%2B%20tests-2ea043?style=flat-square&logo=pytest&logoColor=white" alt="240+ tests" /> <img src="https://img.shields.io/badge/multi--provider-0b7285?style=flat-square" alt="multi-provider" /> <img src="https://img.shields.io/badge/multi--turn-0b7285?style=flat-square" alt="multi-turn" />

**A CLI that red-teams LLM applications against the OWASP LLM Top 10 and reports exactly which attacks got through.**

**How it works:** each scan generates a random canary token and plants it in the
system prompt with an instruction never to reveal it. Then 330 attack vectors
(prompt injection, jailbreaks, encoding tricks, RAG poisoning, tool abuse, PII
leakage) all try to extract it. A finding is just a string match, so it is
reproducible, costs one API call per vector, and needs no second LLM to judge the
result. For risks a canary can't capture, dedicated detectors take over: `regex`
for SSNs and key formats, `repetition` for unbounded output, `absent` for missing
hedges. 15 vectors are multi-turn crescendo attacks, since guardrails that hold
for one message often give way over five. Works with any provider through LiteLLM
(OpenAI, Anthropic, Gemini, Groq, Ollama), and `diff` lets you check for regressions in CI.

```bash
lrtf scan gpt-4o --tui               # live view as each vector lands
lrtf scan gpt-4o --system mine.txt   # test your own prompt, not a toy one
lrtf compare gpt-4o claude-sonnet-4-5 ollama/llama3
lrtf diff base.json current.json     # did your fix actually work?
```

### [QFcli](https://github.com/MRX-72/QFcli)

<a href="https://github.com/MRX-72/QFcli/actions/workflows/ci.yml"><img src="https://github.com/MRX-72/QFcli/actions/workflows/ci.yml/badge.svg" alt="CI" /></a> <a href="https://github.com/MRX-72/QFcli/blob/main/LICENSE"><img src="https://img.shields.io/badge/license-MIT-3da639?style=flat-square" alt="MIT" /></a> <img src="https://img.shields.io/badge/Python%203.9%2B-3776AB?style=flat-square&logo=python&logoColor=white" alt="Python 3.9+" /> <img src="https://img.shields.io/badge/numpy-013243?style=flat-square&logo=numpy&logoColor=white" alt="numpy" /> <img src="https://img.shields.io/badge/pandas-150458?style=flat-square&logo=pandas&logoColor=white" alt="pandas" /> <img src="https://img.shields.io/badge/walk--forward-8957e5?style=flat-square" alt="walk-forward" /> <img src="https://img.shields.io/badge/Black--Litterman-8957e5?style=flat-square" alt="Black-Litterman" /> <img src="https://img.shields.io/badge/no%20lookahead-2ea043?style=flat-square" alt="no lookahead" />

**A quantitative research CLI for backtesting trading strategies and building portfolios, with the statistical checks to flag when a result is overfit or just noise.**

**How it works:** it pulls OHLCV data from Yahoo Finance and runs strategies such as
SMA cross, momentum and RSI reversion (or your own). Signals are shifted one bar
to rule out lookahead bias, costs and slippage are charged on turnover, and
every result is compared with buy-and-hold (alpha, information ratio, hit rate).
Parameters are chosen with **walk-forward validation**: tune in-sample, evaluate on
unseen windows, and optionally blend the grid as an ensemble to cut selection
variance. Positions can be sized by target volatility or fractional Kelly. For
allocation it offers min-variance, tangency and Black-Litterman portfolios
over Ledoit-Wolf shrinkage or PCA-factor covariance, plus a Fama-French factor
overlay. Bootstrap and Jobson-Korkie tests show whether a Sharpe ratio is real.
Built on numpy and pandas only.

```bash
qfcli --backtest AAPL --walk-forward --ensemble rank --grid "fast=10,20;slow=40,60"
qfcli --portfolio AAPL MSFT NVDA --bl --view NVDA=0.18 --ff
```

### [zapscan](https://github.com/MRX-72/zapscan)

<a href="https://github.com/MRX-72/zapscan/actions/workflows/ci.yml"><img src="https://github.com/MRX-72/zapscan/actions/workflows/ci.yml/badge.svg" alt="CI" /></a> <a href="https://github.com/MRX-72/zapscan/blob/main/LICENSE"><img src="https://img.shields.io/badge/license-MIT-3da639?style=flat-square" alt="MIT" /></a> <img src="https://img.shields.io/badge/C%2B%2B17-00599C?style=flat-square&logo=cplusplus&logoColor=white" alt="C++17" /> <img src="https://img.shields.io/badge/CMake-064F8C?style=flat-square&logo=cmake&logoColor=white" alt="CMake" /> <img src="https://img.shields.io/badge/zero%20deps-2ea043?style=flat-square" alt="zero deps" /> <img src="https://img.shields.io/badge/ASan%20/%20UBSan-d1242f?style=flat-square" alt="ASan / UBSan" /> <img src="https://img.shields.io/badge/CTest-8957e5?style=flat-square" alt="CTest" /> <img src="https://img.shields.io/badge/JSON%20output-0b7285?style=flat-square" alt="JSON output" />

**A fast, dependency-free TCP port scanner written from scratch in C++17, directly on BSD sockets. It never shells out to `nmap`.**

**How it works:** targets (IPs, hostnames, CIDR, ranges) and port specs are fully
parsed and validated before any socket opens. A fixed pool of worker threads pulls
`(host, port)` pairs from a shared atomic index, interleaved across hosts so one
slow host can't stall the rest. Each probe runs a non-blocking `connect()` with a
`poll()` timeout, and open ports get a banner grabbed on the same connection.
Results are sorted before output, so reports are stable no matter what order
probes finish in. Output as text, JSON or CSV (CSV is escaped against formula injection).
Integration tests bind real loopback listeners with no network mocking, and CI
runs ASan/UBSan on macOS and Linux.

```bash
zapscan -p 1-1024 -c 256 scanme.nmap.org
zapscan -j -o report.json -p 22,80,443 10.0.0.0/24
```

---

## Tech Stack

**Languages**

<img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python" /> <img src="https://img.shields.io/badge/C%2B%2B-00599C?style=for-the-badge&logo=cplusplus&logoColor=white" alt="C++" /> <img src="https://img.shields.io/badge/Go-00ADD8?style=for-the-badge&logo=go&logoColor=white" alt="Go" /> <img src="https://img.shields.io/badge/Crystal-000000?style=for-the-badge&logo=crystal&logoColor=white" alt="Crystal" /> <img src="https://img.shields.io/badge/x86__64%20Assembly-6E4C13?style=for-the-badge" alt="x86_64 Assembly" /> <img src="https://img.shields.io/badge/ARM%20Assembly-0091BD?style=for-the-badge&logo=arm&logoColor=white" alt="ARM Assembly" /> <img src="https://img.shields.io/badge/SQL-4169E1?style=for-the-badge&logo=postgresql&logoColor=white" alt="SQL" />

**AI / ML**

<img src="https://img.shields.io/badge/PyTorch-EE4C2C?style=for-the-badge&logo=pytorch&logoColor=white" alt="PyTorch" /> <img src="https://img.shields.io/badge/Hugging%20Face%20Transformers-FFD21E?style=for-the-badge&logo=huggingface&logoColor=black" alt="Hugging Face Transformers" />

**Backend, Data & Cloud**

<img src="https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white" alt="FastAPI" /> <img src="https://img.shields.io/badge/REST%20APIs-6BA539?style=for-the-badge&logo=openapiinitiative&logoColor=white" alt="REST APIs" /> <img src="https://img.shields.io/badge/Supabase-3FCF8E?style=for-the-badge&logo=supabase&logoColor=white" alt="Supabase" /> <img src="https://img.shields.io/badge/Vercel-000000?style=for-the-badge&logo=vercel&logoColor=white" alt="Vercel" /> <img src="https://img.shields.io/badge/NumPy-013243?style=for-the-badge&logo=numpy&logoColor=white" alt="NumPy" /> <img src="https://img.shields.io/badge/pandas-150458?style=for-the-badge&logo=pandas&logoColor=white" alt="pandas" /> <img src="https://img.shields.io/badge/yfinance-7B0099?style=for-the-badge" alt="yfinance" />

**CLI, TUI & Systems**

<img src="https://img.shields.io/badge/CLI-4EAA25?style=for-the-badge&logo=gnubash&logoColor=white" alt="CLI" /> <img src="https://img.shields.io/badge/TUI-241F31?style=for-the-badge&logo=gnometerminal&logoColor=white" alt="TUI" /> <img src="https://img.shields.io/badge/POSIX%20Sockets-555555?style=for-the-badge" alt="POSIX Sockets" />

**Security**

<img src="https://img.shields.io/badge/OWASP%20LLM%20Top%2010-000000?style=for-the-badge&logo=owasp&logoColor=white" alt="OWASP LLM Top 10" /> <img src="https://img.shields.io/badge/Penetration%20Testing-557C94?style=for-the-badge&logo=kalilinux&logoColor=white" alt="Penetration Testing" /> <img src="https://img.shields.io/badge/OSINT-2F3E46?style=for-the-badge" alt="OSINT" /> <img src="https://img.shields.io/badge/Networking%20%26%20Network%20Security-1679A7?style=for-the-badge&logo=wireshark&logoColor=white" alt="Networking & Network Security" /> <img src="https://img.shields.io/badge/Fuzzing-B22222?style=for-the-badge" alt="Fuzzing" />

**Cryptography**

<img src="https://img.shields.io/badge/bcrypt-3D3D3D?style=for-the-badge" alt="bcrypt" /> <img src="https://img.shields.io/badge/pyAesCrypt-3D3D3D?style=for-the-badge" alt="pyAesCrypt" /> <img src="https://img.shields.io/badge/pyaes-3D3D3D?style=for-the-badge" alt="pyaes" />

**Testing**

<img src="https://img.shields.io/badge/pytest-0A9EDC?style=for-the-badge&logo=pytest&logoColor=white" alt="pytest" /> <img src="https://img.shields.io/badge/CTest-064F8C?style=for-the-badge&logo=cmake&logoColor=white" alt="CTest" /> <img src="https://img.shields.io/badge/Playwright-2EAD33?style=for-the-badge" alt="Playwright" />

**Tools & Platforms**

<img src="https://img.shields.io/badge/Git-F05032?style=for-the-badge&logo=git&logoColor=white" alt="Git" /> <img src="https://img.shields.io/badge/GitHub-181717?style=for-the-badge&logo=github&logoColor=white" alt="GitHub" /> <img src="https://img.shields.io/badge/macOS-000000?style=for-the-badge&logo=apple&logoColor=white" alt="macOS" /> <img src="https://img.shields.io/badge/Linux-FCC624?style=for-the-badge&logo=linux&logoColor=black" alt="Linux" />

---

## Focus Areas

**LLM security** &nbsp; Adversarial evaluation across the OWASP LLM Top 10:
prompt injection, jailbreaks, encoding bypass, indirect and RAG injection,
system-prompt extraction, and multi-turn crescendo chains. Detection is
canary-based and deterministic — a secret planted in the system prompt makes
every finding a reproducible string match, with no second model grading the first.

**Agentic AI security** &nbsp; The surface that opens once a model has persistent
memory and tools. Memory poisoning across LangChain, ChromaDB, and Mem0 (identity
shift, behavior drift, data exfiltration, bias injection), tool-use and
excessive-agency abuse, and the integrity hashing and embedding-anomaly detection
that catches it.

**Systems & offensive security** &nbsp; Low-level network tooling: non-blocking
TCP scanning over POSIX sockets with a bounded worker pool, banner grabbing, and
x86_64 assembly. Plus email forensics (SMTP relay-path reconstruction,
SPF/DKIM/DMARC, punycode detection, offline GeoIP) and dependency CVE analysis
via OSV.

**Quantitative finance** &nbsp; Backtesting with the checks that catch
overfitting: one-bar-lagged signals (no lookahead), costs charged on turnover,
and every result benchmarked to buy-and-hold. Walk-forward validation,
Black-Litterman allocation over Ledoit-Wolf and PCA-factor covariance, and
bootstrap and Jobson-Korkie significance tests.

---

## Now

- **Shipped** — [LRTF](https://github.com/MRX-72/llm-red-team-cli): an LLM red-team CLI. 330 vectors mapped to the OWASP LLM Top 10, deterministic canary detection, multi-turn attack chains, multi-provider through LiteLLM.
- **Building** — AMPAF, an agentic memory-poisoning framework. Four payload classes (identity shift, behavior drift, data exfiltration, bias injection) against LangChain, ChromaDB, and Mem0, with an integrity checker, anomaly detector, and live memory-state monitor.
- **Direction** — a full-lifecycle AI security toolchain: pre-deployment testing, runtime defense, incident forensics.
- **Maintainer** — invited to [OWASP/cve-lite-cli](https://github.com/OWASP/cve-lite-cli).

---

<p align="center">
  <a href="mailto:theaiguy369@gmail.com"><img src="https://img.shields.io/badge/theaiguy369@gmail.com-EA4335?style=for-the-badge&logo=gmail&logoColor=white" alt="Email" /></a>
</p>
