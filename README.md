<h1 align="center">MRX-72 &nbsp;·&nbsp; Offsec</h1>

<p align="center">
  <em>llms, exploits, and low-level stuff.</em>
</p>

<p align="center">
  <a href="https://github.com/MRX-72">
    <picture>
      <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/MRX-72/MRX-72/main/stats-dark.svg" />
      <source media="(prefers-color-scheme: light)" srcset="https://raw.githubusercontent.com/MRX-72/MRX-72/main/stats-light.svg" />
      <img src="https://raw.githubusercontent.com/MRX-72/MRX-72/main/stats-dark.svg" alt="MRX-72 — GitHub stats" width="470" />
    </picture>
  </a>
</p>

<p align="center">
  <a href="#research">Research</a> &nbsp;·&nbsp;
  <a href="#projects">Projects</a> &nbsp;·&nbsp;
  <a href="#recent-contributions"><b>Recent Contributions</b></a> &nbsp;·&nbsp;
  <a href="#now">Now</a>
</p>

---

## Research

### Where do production LLM guardrails actually fail?

Four production models, 107 attack vectors across the full OWASP LLM Top 10, temperature 0.
A vector counts as a bypass only if a canary planted in the system prompt shows up in the
output. Deterministic string match, no LLM judge.

```
  gemini-3.1-flash-lite  ███████████████  15/107
  gpt-oss-20b            ██████████·····  10/107
  gpt-oss-120b           █████··········  5/107
  qwen3.8-27b            █████··········  5/107
```

**Finding.** Jailbreaks, encoding bypass, indirect injection and system-prompt extraction
(51 vectors) got **0 bypasses on all four models**. 34 of the 35 failures were in the
*agentic and output* layer: unconfirmed tool calls, secrets leaked through markdown image
URLs, unredacted API keys, hallucinated package names, runaway output.

> Refusal training holds on the prompts it was trained on. The risk is in what the model
> *does* after it decides to help.

<sub>One run per model at temperature 0: observations, not rates · <a href="https://github.com/MRX-72/llm-red-team-cli#field-results">full evaluation</a> · <a href="https://github.com/MRX-72/llm-red-team-cli/tree/main/results">raw data</a></sub>

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

## Recent Contributions

> Work merged into upstream security tooling.

| Project | Contribution | Stars | Status |
| :-- | :-- | --: | :-- |
| **[sqlmap](https://github.com/sqlmapproject/sqlmap/pull/6136)** | make `test_ssti` and `test_xpath` runnable standalone | 38.6k★ | merged |
| **[Nuclei](https://github.com/projectdiscovery/nuclei/pull/7766)** | zstd decoder goroutine leak that could OOM-kill long scans (dependency bump, closes #7749) | 31.5k★ | merged |
| **[hashcat](https://github.com/hashcat/hashcat/pulls?q=is%3Apr+author%3AMRX-72+is%3Amerged)** | zlib symbol loading on macOS; leaks in config teardown; unchecked lock/unlock return values; 22000/22001 outfile line written as loaded | 26.9k★ | 4 merged |
| **[nmap](https://github.com/nmap/nmap/blob/8a11c8c2042d9c594bed0e75d073e590d048dab7/CHANGELOG#L5-L9)** | Ncat no longer signals its own process group; Nping passes the correct sockaddr length (fixes `--tcp-connect` and unprivileged `--udp` on macOS/BSD) | 13.7k★ | 2 landed |
| **[Nikto](https://github.com/sullo/nikto/pull/916)** | preserve the root path when stripping a trailing slash for `-noslash` | 10.7k★ | merged |
| **[VirusTotal/yara](https://github.com/VirusTotal/yara/pulls?q=is%3Apr+author%3AMRX-72+is%3Amerged)** | `yr_get_version` runtime version API; nine more ELF `e_machine` values exposed | 9.9k★ | 2 merged |
| **[NVIDIA/garak](https://github.com/NVIDIA/garak/pull/2270)** | scope the ApiKey detector's safe-token check to each match, so one safe example no longer masks a real credential | 9.5k★ | merged |
| **[aircrack-ng](https://github.com/aircrack-ng/aircrack-ng/pull/2732)** | `hexToInt()` now strips the `0x`/`0X` prefix instead of returning `-1` for every prefixed input | 7.7k★ | merged |
| **[NetExec](https://github.com/Pennyw0rth/NetExec/pull/1428)** | SSH login timeouts now fail cleanly instead of raising | 5.9k★ | merged |
| **[microsoft/PyRIT](https://github.com/microsoft/PyRIT/pulls?q=is%3Apr+author%3AMRX-72+is%3Amerged)** | `ShellCommandOutputScorer` stops flagging `rsync` and checksum pipes as shells; `PathTraversalOutputScorer` catches Windows traversal written with either slash | 4.6k★ | 2 merged |
| **[rapid7/metasploit-payloads](https://github.com/rapid7/metasploit-payloads/pull/816)** | mask the 64-bit `st_dev` in the Python Meterpreter `stat` call so it fits the wire format | 2.1k★ | merged |
| **[OWASP cve-lite-cli](https://github.com/OWASP/cve-lite-cli/pulls?q=is%3Apr+author%3AMRX-72+is%3Amerged)** | batches FIRST.org EPSS queries for full CVE coverage; flags override floors that exceed every declaring package's range; accurate error hints for unreadable lockfiles; scanner comparison analysis | 758★ | 4 merged |
| **[CrowdStrike/falconpy](https://github.com/CrowdStrike/falconpy/pull/1510)** | preserve non-JSON response bodies instead of silently discarding them | 516★ | merged |
| **[OWASP DockSec](https://github.com/OWASP/DockSec/pull/169)** | passwords leaking from connection-string URLs | 490★ | merged |
| **[OWASP AISVS](https://github.com/OWASP/AISVS/pull/1153)** | missing controls in the Appendix B inventory | 456★ | merged |
| **[GenAI Red Team Lab](https://github.com/GenAI-Security-Project/GenAI-Red-Team-Lab/pull/81)** | memory-poisoning exploit module | 54★ | merged |

---

## Focus Areas

**AI security** &nbsp; Most of my time goes here. I test LLMs and agents for the failures that aren't jailbreaks, like a model handing over an API key because someone asked it to reformat a config file.

**Reverse engineering** &nbsp; I spend a lot of evenings in Ghidra and GDB, and pwntools when there's something to exploit.

**Network security** &nbsp; I like writing my own tools for this. zapscan started as a way to understand what nmap actually does under the hood.

**Open source** &nbsp; When a tool I use breaks, I try to fix it upstream. That's how I ended up with patches in Metasploit, sqlmap, hashcat and a few others.

---

## Tech Stack

<p>
<b>Languages</b><br/>
Python &nbsp;·&nbsp; C++ &nbsp;·&nbsp; C &nbsp;·&nbsp; Go &nbsp;·&nbsp; Crystal &nbsp;·&nbsp; Bash
</p>

<p>
<b>Low-Level &amp; RE</b><br/>
x86-64 Asm &nbsp;·&nbsp; Ghidra &nbsp;·&nbsp; GDB &nbsp;·&nbsp; pwndbg &nbsp;·&nbsp; pwntools &nbsp;·&nbsp; radare2 &nbsp;·&nbsp; Cutter
</p>

<p>
<b>Network Security</b><br/>
Nmap &nbsp;·&nbsp; Wireshark &nbsp;·&nbsp; tcpdump &nbsp;·&nbsp; Scapy &nbsp;·&nbsp; NetExec &nbsp;·&nbsp; aircrack-ng
</p>

<p>
<b>Offensive Tooling</b><br/>
Metasploit &nbsp;·&nbsp; sqlmap &nbsp;·&nbsp; hashcat &nbsp;·&nbsp; Nuclei &nbsp;·&nbsp; YARA &nbsp;·&nbsp; garak &nbsp;·&nbsp; Nikto
</p>

<p>
<b>OS</b><br/>
BlackArch &nbsp;·&nbsp; SamuraiWTF
</p>

---

## Now

- **Shipped** — [LRTF](https://github.com/MRX-72/llm-red-team-cli): an LLM red-team CLI. 330 vectors mapped to the OWASP LLM Top 10, deterministic canary detection, multi-turn attack chains, multi-provider through LiteLLM.
- **Building** — AMPAF, an agentic memory-poisoning framework. Four payload classes (identity shift, behavior drift, data exfiltration, bias injection) against LangChain, ChromaDB, and Mem0, with an integrity checker, anomaly detector, and live memory-state monitor.
- **Direction** — a full-lifecycle AI security toolchain: pre-deployment testing, runtime defense, incident forensics.
- **Collaborator** — [OWASP](https://owasp.org).
- **Core dev** — [Omnikon](https://www.omnikonhub.com/).

---

<p align="center">
  <a href="https://github.com/MRX-72"><b>@MRX-72</b></a> &nbsp;·&nbsp; reach me by opening an issue on any of my repositories
</p>
