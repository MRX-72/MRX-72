# AI Red Teamer | Systems Engineer

Adversarial testing, low-level optimization, and automation.

---

## Featured

### [llm-red-team-cli](https://github.com/MRX-72/llm-red-team-cli) · `pip install llm-red-team-cli`

Adversarial test harness for LLM applications. **107 vectors across 10 categories**
mapped to the OWASP LLM Top 10 — prompt injection, jailbreaks, encoding bypass,
indirect injection, system-prompt leakage, PII disclosure, improper output
handling, excessive agency, unbounded consumption, misinformation.

Detection is **canary-based, not LLM-judged**: a fresh random token is planted in
the system prompt at scan time, so a finding is a deterministic string match —
reproducible, one API call per vector, no judge model. 12 vectors run as real
multi-turn conversations, because a guardrail that holds against one message
often erodes across five.

Live results are published in the README, including a reproduced persona-split
bypass where a model refuses and complies in the same reply.

```bash
lrtf scan gpt-4o --tui              # live view
lrtf scan gpt-4o --system mine.txt  # test your own prompt
lrtf diff base.json current.json    # did the fix work?
```

---

## Technical Stack

* **Languages:** C++, Go, Python, x86_64 Assembly
* **Focus:** AI Red Teaming, Offensive Security, Vulnerability Analysis
* **LLM Systems & Compute:** Inference optimization (vLLM, llama.cpp), custom CUDA kernels, custom RAG architectures
* **Systems & Automation:** Linux internals, low-level networking, socket programming, n8n orchestration

---

## Open Source

* **Invited maintainer** — [OWASP/cve-lite-cli](https://github.com/OWASP/cve-lite-cli), a JS/TS dependency vulnerability scanner
* [llm-red-team-cli](https://github.com/MRX-72/llm-red-team-cli) — LLM adversarial test harness
* [zapscan](https://github.com/MRX-72/zapscan) — C++17 port scanner and recon tool
* [QFcli](https://github.com/MRX-72/QFcli) — quantitative stock analysis CLI

---

## Current Work

* **AI Red Teaming** — building tooling against the OWASP LLM Top 10, with an emphasis on detection that is deterministic rather than model-judged
* **Inference Engineering** — minimizing latency and preserving output quality in local LLMs via custom CUDA kernels and C++ inference engines
* **Systems Programming** — low-level Linux utilities and automated infrastructure workflows in Go, C++, and n8n

---

## Contact

* Email: theaiguy369@gmail.com
