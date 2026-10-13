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

**LLM security** &nbsp; Prompt injection, jailbreaks, encoding bypass, RAG injection and multi-turn chains, scored by deterministic canary detection.

**Agentic AI security** &nbsp; Memory poisoning and excessive-agency abuse across LangChain, ChromaDB and Mem0, and the integrity checks that catch it.

**Systems & offensive security** &nbsp; POSIX-socket network tooling, x86_64 assembly, email forensics, and dependency CVE analysis via OSV.

**Quantitative finance** &nbsp; Backtesting that catches its own overfitting: no lookahead, costs on turnover, walk-forward validation.

---

## Tech Stack

<p align="center">
<b>Languages</b><br/>
<img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python" /> <img src="https://img.shields.io/badge/C%2B%2B-00599C?style=for-the-badge&logo=cplusplus&logoColor=white" alt="C++" /> <img src="https://img.shields.io/badge/C-A8B9CC?style=for-the-badge&logo=c&logoColor=white" alt="C" /> <img src="https://img.shields.io/badge/Go-00ADD8?style=for-the-badge&logo=go&logoColor=white" alt="Go" /> <img src="https://img.shields.io/badge/Crystal-000000?style=for-the-badge&logo=crystal&logoColor=white" alt="Crystal" /> <img src="https://img.shields.io/badge/Bash-4EAA25?style=for-the-badge&logo=gnubash&logoColor=white" alt="Bash" />
</p>

<p align="center">
<b>Low-Level &amp; RE</b><br/>
<img src="https://img.shields.io/badge/x86--64%20Asm-6E4C13?style=for-the-badge" alt="x86-64 Asm" /> <img src="https://img.shields.io/badge/Ghidra-C00000?style=for-the-badge" alt="Ghidra" /> <img src="https://img.shields.io/badge/GDB-A42E2B?style=for-the-badge&logo=gnu&logoColor=white" alt="GDB" /> <img src="https://img.shields.io/badge/pwndbg-2B2B2B?style=for-the-badge" alt="pwndbg" /> <img src="https://img.shields.io/badge/pwntools-2B2B2B?style=for-the-badge" alt="pwntools" /> <img src="https://img.shields.io/badge/radare2-4B3A86?style=for-the-badge" alt="radare2" /> <img src="https://img.shields.io/badge/Cutter-2B2B2B?style=for-the-badge" alt="Cutter" />
</p>

<p align="center">
<b>Network Security</b><br/>
<img src="https://img.shields.io/badge/Nmap-0E83CD?style=for-the-badge" alt="Nmap" /> <img src="https://img.shields.io/badge/Wireshark-1679A7?style=for-the-badge&logo=wireshark&logoColor=white" alt="Wireshark" /> <img src="https://img.shields.io/badge/tcpdump-2B2B2B?style=for-the-badge" alt="tcpdump" /> <img src="https://img.shields.io/badge/Scapy-2B2B2B?style=for-the-badge" alt="Scapy" /> <img src="https://img.shields.io/badge/NetExec-2B2B2B?style=for-the-badge" alt="NetExec" /> <img src="https://img.shields.io/badge/aircrack--ng-2B2B2B?style=for-the-badge" alt="aircrack-ng" /> <img src="https://img.shields.io/badge/Kali%20Linux-557C94?style=for-the-badge&logo=kalilinux&logoColor=white" alt="Kali Linux" />
</p>

<p align="center">
<b>Offensive Tooling</b><br/>
<img src="https://img.shields.io/badge/Metasploit-2596CD?style=for-the-badge&logo=metasploit&logoColor=white" alt="Metasploit" /> <img src="https://img.shields.io/badge/sqlmap-2B2B2B?style=for-the-badge" alt="sqlmap" /> <img src="https://img.shields.io/badge/hashcat-2B2B2B?style=for-the-badge" alt="hashcat" /> <img src="https://img.shields.io/badge/Nuclei-2B2B2B?style=for-the-badge" alt="Nuclei" /> <img src="https://img.shields.io/badge/YARA-2B2B2B?style=for-the-badge" alt="YARA" /> <img src="https://img.shields.io/badge/garak-76B900?style=for-the-badge" alt="garak" /> <img src="https://img.shields.io/badge/Nikto-2B2B2B?style=for-the-badge" alt="Nikto" />
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
