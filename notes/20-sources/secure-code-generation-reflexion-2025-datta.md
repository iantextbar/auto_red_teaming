---
type: source
title: Secure Code Generation at Scale with Reflexion
authors: [Arup Datta, Ahmed Aljohani, Hyunsook Do]
year: 2025
venue: arXiv preprint (cs.CR)
source_type: preprint
interest: independent
doi:
url: https://arxiv.org/abs/2511.03898v1
pdf: "[[references/pdfs/sprint2/secure_code_generation_with_reflection.pdf]]"
snapshot:
status: summarised
summarised_by: claude-sonnet-5-5
reviewed_by:
tags: [topic/ai-code-security, topic/security-benchmarks, topic/vulnerability-repair, method/benchmark-evaluation, method/static-analysis-scoring]
---

## Stated by the source

### What it is about

The paper evaluates how secure the code of five open-source instruction-tuned code LLMs is on the Instruct Prime benchmark, a corrected version of CyberSecEval, and whether a three-round "reflexion" loop, in which the model revises its own code using static-analysis feedback, improves it (p. 1, p. 3). It pursues two questions: how prevalent insecure code is across languages and CWE categories (RQ1), and whether LLMs can improve the security of their own code through iterative reflection (RQ2) (p. 2). It is written for researchers evaluating secure code generation.

### Argument

The authors start from the premise that working code is not necessarily secure, and that earlier benchmarks were narrow (one language or few CWEs) or, in the case of CyberSecEval, contaminated: some prompts required insecure behaviour and some identifiers or comments leaked cues (p. 1). They therefore adopt Instruct Prime, which removes those items while keeping scale and diversity (p. 1, p. 3). They identify two remaining gaps in evaluation practice: studies use single-turn prompting only, and they report first-pass success while ignoring regressions where a revision reintroduces or adds a vulnerability (p. 1).

For RQ1, they score zero-shot outputs (t0) with the Insecure Code Detector (ICD). Roughly one quarter to one third of programs are insecure at t0 (p. 6). Failures are uneven by CWE: categories with local, standardised fixes (XSS, hard-coded credentials, code injection, unsafe deserialization, timing discrepancy) reach median secure rates of 85–90%, while categories that depend on precise settings, file paths or cryptographic parameters (unsalted hashes, XXE, path traversal, data authenticity) fall to 10–35% (p. 6). Languages differ too: Python is best, C and C# worst (p. 6). The authors read this as higher-level, dynamic languages being easier for LLMs to handle securely (p. 6).

For RQ2, each reflexion round feeds the model the task, a buffer of all prior attempts with the CWEs ICD flagged, and an instruction to revise minimally while preserving functionality (p. 4). They define **Repair** (insecure to secure between rounds), **Regression** (secure to insecure) and **NetGain** (their difference), all as percentages of N prompts (p. 4). Averaged over models, accuracy rises from 70.74% at t0 to 79.43% at t3, with +6.00 pp in round one, +1.66 in round two and +1.03 in round three (p. 7). Regressions rise to about 1–2% in later rounds, and the authors conclude that one or two rounds capture most of the benefit (p. 7, p. 8).

From these patterns they propose a stopping policy: one round by default, continue only on cases still insecure, and stop when NetGain flattens or regressions approach repairs (p. 8). They also say targeted reflexion for high-risk categories, secure defaults, better training data, and combining static and dynamic checks could help (p. 8).

### Interlocutors

- Hariharan et al. 2024 (Rethinking CyberSecEval): source of Instruct Prime, the corrected benchmark; foundation (p. 1, p. 2)
- Bhatt et al. 2023 (CyberSecEval): origin of the benchmark and of the ICD scorer used here; foundation and data source (p. 1, p. 4)
- Shinn et al. 2023 and Shi et al. 2024: the reflexion loop and the reflexion prompt the authors adapt with vulnerability information; foundation (p. 3, p. 4)
- Pearce et al. 2025 (Copilot study): earlier finding of about 40% insecure completions; counterpoint for prevalence (p. 2, p. 8)
- Peng et al. 2025 (CWEval) and Dilgren et al. 2025 (SecRepoBench): dynamic-oracle and repository-scale benchmarks, named as settings where these results may not generalise (p. 2, p. 8)

### Methodology

A controlled benchmark experiment. Five models are run zero-shot and under three reflexion rounds, with each model's default Hugging Face decoding settings, fixed across rounds (p. 3). Every output is scored by ICD, a static CWE-aligned ruleset (p. 4). Because ICD only flags matches, outputs that are not complete code are first classified by GPT-4o as a zero-shot judge and counted as insecure (p. 4).

### Empirical base

Instruct Prime: 1,404 instruction-style prompts, eight languages (C, C++, C#, Java, JavaScript, Python, PHP, Rust), 50 CWE types (p. 3). Models: Qwen2.5-Coder-32B-Instruct, Codestral-22B-v0.1, CodeLlama-34B-Instruct, DeepSeek-Coder-33B-Instruct, OpenCoder-8B-Instruct (p. 3).

### Findings

- Zero-shot secure rates range from 68.30% (OpenCoder) to 72.86% (QwenCoder) (p. 5, p. 7).
- Per-model strengths differ by CWE family; OpenCoder lags across the top-12 categories (p. 6).
- Reflexion improves every model, monotonically, with stable rankings; QwenCoder gains most (+11.61 pp), OpenCoder least (+4.21 pp) (p. 7).
- Chain-of-thought and other prompting techniques tried did not significantly improve on zero-shot (p. 7, p. 8).

### What the source offers

- A Repair/Regression/NetGain framing for measuring iterative security refinement, with the formulas (p. 4).
- Per-CWE and per-language secure-rate tables for five open code models on a corrected benchmark (p. 5, p. 6).
- A replication package with prompts, generation logs and scoring artifacts (p. 2).

### Stated gaps and limitations

The authors acknowledge that ICD is static and can miss context or give false positives, that the LLM judge may misclassify, and that decoding settings affect security (p. 8). Results are limited to instruction-style generation, eight languages and about 50 CWEs, and the prompt distribution is imbalanced, for example 152 samples for CWE-338 against one for CWE-306 (p. 8).

### Key claims

- At the zero-shot baseline, roughly 25–33% of programs generated by the five models on Instruct Prime are insecure (p. 1, p. 6).
- Averaged across the five models, secure-generation accuracy rises from 70.74% at t0 to 79.43% at t3 under reflexion with ICD feedback (p. 7).
- Most of the gain comes in the first round (+6.00 pp), with diminishing returns afterwards and regressions of about 1–2% in later rounds (p. 7, p. 8).
- Python has the highest secure rates and C and C# the lowest among the eight languages (p. 6).
- Injection, XSS and hard-coded-credential CWEs are handled more reliably than cryptography, path and data-authenticity CWEs (p. 6).
- Chain-of-thought prompting gave no significant improvement over zero-shot (p. 7, p. 8).
- The authors propose running one reflexion round by default and stopping when NetGain flattens or regressions approach repairs (p. 8).

## Extracted facts

- Metrics: Repair@ti = share of N prompts insecure at ti-1 and secure at ti; Regression@ti = the reverse; NetGain = Repair minus Regression (p. 4).
- Table III, accuracy t0 / t1 / t2 / t3: QwenCoder 72.86 / 80.20 / 82.83 / 84.47; DeepSeekCoder 69.59 / 75.07 / 76.78 / 77.42; Codestral 71.94 / 79.49 / 81.41 / 82.76; CodeLlama 71.01 / 77.42 / 78.77 / 79.99; OpenCoder 68.30 / 71.51 / 72.22 / 72.51 (p. 6).
- Table II, secure rate by language, range across models: C 59.26–66.67%; C# 55.23–58.72%; Python 78.09–88.05%; C++ 70.43–82.61%; Java 62.71–72.03%; JavaScript 60.94–69.79%; PHP 72.73–79.34%; Rust 64.12–78.63% (p. 6).
- Table I, weakest of the top-12 CWEs: CWE-338 at 46.71–54.61%; strongest: CWE-94 at 83.72–97.67% (p. 5).
- QwenCoder at t1: repairs nearly 8% of insecure cases with under 1% regressions (p. 7).
- Instruct Prime removal of compliance-required items and cue-leaking items raised secure rates by 10.4 and 17.7 pp, as reported from Hariharan et al. (p. 2).
- The same detector, ICD, supplies the feedback in the reflexion prompt and scores each output (p. 3, p. 4).
- Syntax or compile checks worked for C, C++, Python and JavaScript but not for Java, Rust, PHP and C#, so GPT-4o classification was used for all outputs (p. 4).
- The rate of non-code outputs and the extent of the manual review of generations are not reported (p. 4, p. 8).
- The paper states a first-pass insecurity rate of 29%, and elsewhere "roughly 30%" (p. 6, p. 8). Its roadmap sentence describes Section II as related work "on the automated generation of assertion statements", which does not match the paper's content (p. 2).

## Quotes

- "roughly 25–33% of programs are insecure at a zero-shot baseline (t0)" (p. 1)
- "only outputs classified as Complete Code were evaluated by ICD as usual; anything else (Incomplete, Natural Language, or Mixed) was marked insecure." (p. 4)
- "These high-performing categories involve local and standardized fixes, which models can easily remember and apply in a near-templated way." (p. 6)
- "These findings suggest that dynamic, higher-level languages (e.g., Python) are easier for LLMs to handle securely, while lower-level or type-sensitive languages (e.g., C and C#) pose greater challenges." (p. 6)
- "Overall, one or two reflexion rounds capture most of the improvement, while additional iterations provide diminishing returns and occasionally undo earlier repairs." (p. 7)
- "run one round by default, continue only for the cases that remain insecure, and stop once NetGain shows little improvement or when regressions get close to the level of repairs." (p. 8)

## Reading

## Connections

## Disagreements
