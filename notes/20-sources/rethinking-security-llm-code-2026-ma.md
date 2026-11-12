---
type: source
title: "Poster: Rethinking Security in LLM Code Generation through Real-World Risk Scenarios"
authors: [Lixun Ma, Ruolong Ma, Bei Wang, Feng Wei, Zhenguang Liu, Lorenzo Cavallaro, Wentao Chen]
year: 2026
venue: arXiv
source_type: preprint
interest: independent
doi:
url: https://arxiv.org/abs/2607.23088v1
pdf: "[[references/pdfs/sprint2/Rethinking Security in LLM Code.pdf]]"
snapshot:
status: summarised
summarised_by: claude-sonnet-5-5
reviewed_by:
tags: [topic/ai-code-security, topic/security-benchmarks, method/benchmark-evaluation, method/static-analysis-scoring]
---

## Stated by the source

### What it is about

A six-page poster paper on the security of code produced by LLMs when the prompt resembles what developers actually write: vague, incomplete, or at odds with security practice (p. 1). It builds a benchmark of 2,700 test cases and evaluates eight LLMs on it. The two research questions are how secure the generated code is under realistic risk scenarios (RQ1) and how far security-aware prompting improves it (RQ2) (p. 2).

### Argument

The paper starts from a gap. Existing evaluations rely on CWE-based benchmarks that assess whether models write secure code when security requirements or vulnerabilities are explicitly specified, whereas real developer prompts are often ambiguous, incomplete or optimised for functionality (p. 1). The authors therefore take a **developer-centric perspective** and name three prompt-side risk scenarios, drawn from CWE categories, prior empirical studies and anonymized internal logs of developer interactions (p. 2).

The scenarios are **Ambiguous Requirements** (SC1: a functional request with no security constraints, which implicitly delegates security decisions to the model), **Under-Specified Operational Context** (SC2: deployment or runtime details omitted, so the model may default to outdated or insecure configurations) and **Security–Functionality Conflict** (SC3: the user asks for something that conflicts with best practice, such as disabling certificate validation) (pp. 2–3).

Each test case is a prompt pair: a risk-inducing prompt and a security-aware counterpart, produced by a scenario-specific transformation that keeps the functional task fixed. This allows a controlled comparison in which only the security information varies (p. 3). Models are run on both prompts in a baseline round and a mitigation round, and outputs are labelled secure or vulnerable and paired by sample (p. 4).

The results are reported at model and scenario level. Every model has a baseline vulnerability rate above 56%, and SC1 is the worst scenario at 66%. SC3 has the lowest baseline rate, 52%, which the authors suggest may reflect more cautious generation when the trade-off is explicit (p. 5). Security-aware prompting reduces vulnerability for all models, but in SC3 it also produces regressions (p. 6). The authors conclude that security of generated code depends on prompt-side risk conditions as well as model capability (p. 2).

### Interlocutors

- Pearce et al. 2022 and Chen et al. 2021, with SWE-bench (Jimenez et al. 2024): representative of the CWE-style and general code benchmarks the paper positions itself against (target of critique) (pp. 1, 6).
- Perry et al. 2023: user study of AI assistants; cited as source for the ambiguous-requirement scenario (data source) (pp. 2, 6).
- Jallow et al. 2024: Stack Overflow snippet evolution; cited for outdated or insecure configurations in SC2 (foundation) (pp. 2, 6).
- Oltrogge et al. 2021: TLS insecurity in Android apps; cited for developers' limited awareness behind SC3 (foundation) (pp. 3, 6).

### Methodology

Benchmark evaluation with paired prompts. Prompts come from GitHub issues, Stack Overflow posts and anonymized internal developer logs, supplemented by manually designed prompts guided by CWE categories to cover under-represented cases (p. 3). Generated code is checked with static analysis (Clang Static Analyzer, CodeQL) and expert review assisted by GPT-5. The final binary label is set by expert review (p. 4).

### Empirical base

2,700 test cases: three scenarios, nine languages, 50 prompt pairs per scenario-language combination (p. 3). Eight models: six large (Qwen3-Max, Claude-Sonnet-4, DeepSeek-V3-0324, GPT-5, Grok-4, Gemini-2.5-Pro) and two small (Qwen3-4B, GLM-Z1-Air). Each prompt is sampled n = 5 times at temperature 1.0 through official APIs with default settings (p. 4).

### Findings

- Baseline vulnerability exceeds 56% for all eight models (p. 5).
- Vulnerability is highest for ambiguous requirements (66%) and lower for security–functionality conflict (52%) (p. 5).
- Security-aware prompting improves every model; the vulnerability-rate reduction runs from 37% (Qwen3-4B) to up to 45% (Claude-Sonnet-4) (p. 6).
- SC3 is the hardest scenario to mitigate: regression rate reaches 19% and net gain falls to 0.12 (p. 6).

### What the source offers

- A three-scenario taxonomy of prompt-side risk (ambiguous, under-specified context, security–functionality conflict).
- A paired-prompt design and metrics (Vul, Imp, Reg, NetG) that separate fixes from regressions under mitigation prompting.
- A 2,700-case benchmark in nine languages, to be released upon publication (p. 3).

### Stated gaps and limitations

The authors acknowledge limits in model coverage, in the enhancement techniques explored and in the scope of risk scenarios. Future work is to cover more LLMs and scenarios, test RAG, fine-tuning and skill-based augmentation, and collect more real developer interaction data (p. 6).

### Key claims

- All eight evaluated LLMs show baseline vulnerability rates above 56% on the benchmark's risk scenarios (p. 5).
- Vulnerability is highest under ambiguous requirements (SC1, 66%), which the authors read as models being especially vulnerable when security constraints are not specified (p. 5).
- Security–functionality conflict (SC3) has a lower baseline vulnerability rate (52%), which the authors suggest may reflect more cautious generation when trade-offs are explicit (p. 5).
- Security-aware prompting consistently improves security for all models, with vulnerability-rate reductions of 37% to up to 45% (p. 6).
- In SC3, security-aware prompting is least robust: regressions reach 19% and net gain drops to 0.12 (p. 6).
- The authors state that security of LLM-generated code is shaped by prompt-side risk conditions as well as model capability (p. 2).

## Extracted facts

- Outcome categories from paired labels (b1, b2), with 0 = vulnerable and 1 = secure: (0,0) persistently vulnerable, (0,1) improved, (1,0) regressed, (1,1) persistently secure (p. 4).
- Metrics: VulB and VulM are the share of vulnerable outputs in baseline and mitigation; Imp = share of outputs with b1 = 0 and b2 = 1; Reg = share with b1 = 1 and b2 = 0; NetG = Imp − Reg (pp. 4–5).
- Languages: Bash (scripting); HTML and JavaScript (front-end); C++, Java, PHP, Go and SQL (back-end); Python (AI development) (p. 4).
- Security-aware prompt transformations: general security guidance for SC1; explicit environment and security assumptions for SC2; reformulated specifications aligned with secure coding for SC3 (p. 3).
- The paper does not state how the "up to 45%" and "37%" reductions are computed (relative or absolute) or give per-model baseline values in text; these are in Fig. 3, not in the extracted text (pp. 5–6).
- Disclosure: the authors declare no competing interests (p. 6).

## Quotes

- "Existing benchmarks often rely on explicitly specified security requirements, failing to capture real-world scenarios where prompts are frequently ambiguous or incomplete." (p. 1)
- "all models exhibit average vulnerability rates exceeding 56% across risk scenarios" (p. 1)
- "This design preserves task semantics while varying only scenario-relevant security information, enabling controlled comparison of model behavior under identical functional requirements." (p. 3)
- "Security-aware prompting can effectively improve code security overall, but may introduce regressions when functional requirements conflict with secure coding practices." (p. 2)
- "indicating that LLMs are particularly vulnerable when security constraints are not explicitly specified" (p. 5)
- "This indicates limited robustness when explicit functional requirements conflict with secure coding practices." (p. 6)

## Reading

## Connections

## Disagreements
