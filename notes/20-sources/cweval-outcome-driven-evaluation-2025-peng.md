---
type: source
title: "CWEval: Outcome-driven Evaluation on Functionality and Security of LLM Code Generation"
authors: [Jinjun Peng, Leyi Cui, Kele Huang, Junfeng Yang, Baishakhi Ray]
year: 2025
venue:
source_type: preprint
interest: independent
doi:
url: https://arxiv.org/abs/2501.08200v1
pdf: "[[references/pdfs/sprint2/CWEval.pdf]]"
snapshot:
status: summarised
summarised_by: claude-sonnet-5-5
reviewed_by:
tags: [topic/ai-code-security, topic/security-benchmarks, topic/secure-coding-standards, method/benchmark-evaluation, method/execution-based-evaluation, method/static-analysis-scoring]
---

## Stated by the source

### What it is about

The paper introduces CWEval, an evaluation framework for the security of LLM-generated code, and CWEval-Bench, a multilingual benchmark built on it (pp. 1–3). It targets researchers who benchmark or train models for secure code generation. The question it pursues is how to measure functional correctness and security at the same time, on the same tasks, without relying on static analysers (p. 2, p. 5). It then uses the benchmark to ask how large the gap is between functional and functional-and-secure code, whether larger models close it, and whether security prompting or security fine-tuning helps (p. 6).

### Argument

The paper starts from an asymmetry: functionally wrong LLM code is easily spotted and discarded, whereas vulnerabilities inside functionally correct code often go unnoticed, especially for non-security experts (p. 1). Existing security benchmarks, it argues, cannot measure this well because of three limitations: poorly defined specifications, infeasibility of rigorous functionality evaluation, and instability of static-analysis-based security evaluation (pp. 1–2).

On specifications, CyberSecEval gives only preceding lines or an LLM-written summary, and SecurityEval gives one-sentence comments; vague specs can underestimate risk because a model may return a no-op that is "secure" but useless (p. 1, p. 2). On functionality, benchmarks lack tests, so prior secure-coding work evaluates functionality and security on separate benchmarks. The paper argues this hides the **alignment tax**: a model can score well on both while having merely learned to avoid security-sensitive code (p. 2). On stability, static analysers miss semantically equivalent variants and flag secure ones, as the CodeQL redirect example in Fig. 1 shows (p. 2).

The response is the **outcome-driven test oracle**. Each task has a specification P, implementations I, and two oracle sets, one for functionality and one for security, giving four cells (f+/f−, s+/s−) (p. 3). Security oracles go beyond return values: timeouts detect DoS, address sanitizer detects out-of-bounds access in C, and data integrity checks detect SQL injection (p. 5). Because oracles observe execution outcomes rather than code patterns, the paper says they cope with diverse implementations and are language-agnostic (p. 5). Specifications must contain security-relevant semantics, must not leak security awareness, and must be unambiguous enough that a model passes the functionality tests before any security training (pp. 4–5). Each task ships a secure and at least one insecure reference implementation to cross-check the oracles (p. 5).

The evaluation reports two metrics adapted from pass@k: func@k and func-sec@k (p. 6). The paper reports that all models lose around 30 points from func@10 to func-sec@10, that larger models do almost always better on func-sec@k, that a one-line security instruction raises func-sec@k, and that a security-fine-tuned model collapses on the joint metric (pp. 6–8). It concludes that evaluating the two properties jointly separates learning secure coding from learning to avoid security-related coding (p. 8).

### Interlocutors

- SecurityEval (Siddiq and Santos, 2022): a dataset of vulnerable-code scenarios over 40 CWE categories, scored with CodeQL; target of critique for one-line specs, no functionality tests and static analysis (p. 1, p. 2).
- CyberSecEval and CyberSecEval 2 (Bhatt et al., 2023, 2024): mined, non-self-contained vulnerable snippets; target of critique, with a reproduction rate of 562/1916 under its own analyser (p. 2, p. 3).
- HumanEval (Chen et al., 2021): foundation for the specification format, the test-oracle style and the unbiased pass@k estimator (p. 1, p. 5, p. 6).
- EvalPlus (Liu et al., 2024): foundation for future differential testing and oracle augmentation using the reference implementations (p. 5).
- SVEN (He and Vechev, 2023) and SafeCoder (cited as Su et al., 2024): security fine-tuning work whose evaluation relies on separate benchmarks; counterpoint, and SafeCoder is evaluated directly (p. 3, p. 7).

### Methodology

The paper is a benchmark-construction and evaluation study. Tasks are designed from CWE and CodeQL documentation, written to be self-contained, tested against common LLMs for clarity and refined iteratively (p. 5). Oracles are written HumanEval-style for functionality and with tool-specific logic for security. Tasks were first translated across languages by LLMs and then reviewed manually (pp. 5–6). Security is measured by dynamic execution, not static analysis (p. 5).

Models are sampled at four temperatures with n = 100, plus greedy decoding, for RQ.1. RQ.2 and RQ.3 use only temperature 0.8 with n = 100, because of budget (p. 6).

### Empirical base

CWEval-Bench has 119 security-critical tasks covering 31 CWEs in 5 programming languages, including 11 C-specific memory tasks (p. 3, p. 6). Models: GPT-4o mini, Claude 3.5 Haiku, Gemini 1.5 Flash and Llama 3.1 70B Instruct as main models; GPT-4o, Claude 3.5 Sonnet, Gemini 1.5 Pro, Llama 3.1 8B and 405B for size comparison; CodeLlama-7b-hf and its SafeCoder checkpoint for fine-tuning (p. 6, p. 7).

### Findings

- For every model, func-sec@k is well below func@k; from func@10 to func-sec@10 the drop is around 30%, up to 35.79% for Gemini 1.5 Flash (p. 6).
- A higher func@k tends to go with a higher func-sec@k, but not always: Llama 3.1 70B beats Claude 3.5 Haiku on func@10, while Haiku wins on func-sec@10 (p. 6).
- Larger models almost always get higher func-sec@k; in the GPT-4o and Gemini families the func@k differences are small (the smaller model is sometimes slightly better) while func-sec@k differences are larger (p. 6).
- Adding "Your code should be secure and should NOT contain any vulnerability" improves func-sec@k for almost all models, with a possible slight decrease in func@k; the gain is largest for Claude 3.5 Haiku, up to 9.8% on func-sec@10 (p. 6, p. 7).
- SafeCoder-tuned CodeLlama-7b shows a significant functionality drop and much less functional-and-secure code than its base on CWEval-Bench, although SafeCoder's own evaluation reports more secure code without functionality loss (p. 7).

### What the source offers

- An open-source benchmark and pipeline (119 tasks, 31 CWEs, 5 languages) with specifications, functionality and security oracles, and secure and insecure reference implementations (p. 3).
- The func@k and func-sec@k metrics, a joint measure that penalises both non-functional and insecure output (p. 6).
- A documented design checklist for security-benchmark tasks: security-semantics existence, no security-awareness leakage, expectation unambiguity (p. 4).
- A worked example of static-analysis false negatives and false positives on CodeQL's incomplete URL sanitisation rule (p. 2).

### Stated gaps and limitations

The task count is limited by human resources (p. 6). The authors state that the benchmark could be expanded to more CWEs and languages manually or automatically, and name automating benchmark creation as future work (p. 6, p. 8). RQ.2 and RQ.3 use a single temperature because of budget (p. 6). The prompting experiment tries only the simplest instruction (p. 7). The explanation for SafeCoder's degradation (learning to avoid security-sensitive code) is given as "possibly" (p. 7).

### Key claims

- Existing secure-code benchmarks suffer from poorly defined specifications, no rigorous functionality evaluation and unstable static-analysis-based security evaluation (pp. 1–2).
- Only 562 of 1916 vulnerable CyberSecEval samples are still flagged by its associated static analyser (p. 2).
- CodeQL's incomplete-URL-sanitisation rule yields false negatives and a false positive on semantically similar redirect implementations (p. 2).
- Outcome-driven dynamic test oracles evaluate functionality and security together on the same tasks, which the authors say no earlier evaluation did (p. 3).
- On CWEval-Bench, all evaluated LLMs show a gap of around 30% between func@10 and func-sec@10, up to 35.79% for Gemini 1.5 Flash (p. 6).
- Larger models within a family almost always achieve higher func-sec@k (p. 6).
- A simple security instruction in the prompt improves func-sec@k for almost all evaluated models, up to 9.8% on func-sec@10 for Claude 3.5 Haiku (p. 6, p. 7).
- SafeCoder-fine-tuned CodeLlama-7b shows a significant functionality degradation and less functional-and-secure code than its base model on CWEval-Bench; the authors suggest this may be because it avoids security-sensitive code (p. 7).

## Extracted facts

- Definitions: func@k = probability that any of k generated implementations passes all functionality oracles (same as pass@k); func-sec@k = same, requiring both functionality and security oracles; unbiased estimator with n samples and c functional-and-secure ones (p. 6).
- Sampling: n = 100 per temperature in {0.2, 0.4, 0.6, 0.8}, best result reported for k = 1, 10, 50; greedy decoding reported as @1* (p. 6). RQ.2 and RQ.3: temperature 0.8 only (p. 6).
- Model versions: gpt-4o-mini-2024-07-18, claude-3-5-haiku-20241022, gemini-1.5-flash-002, gpt-4o-2024-08-06, claude-3-5-sonnet-20241022, gemini-1.5-pro-002, Llama 3.1 8B, 70B and 405B Instruct (p. 6).
- Table I (temperature 0.8), func@10 / func-sec@10: GPT-4o 90.71 / 65.33; GPT-4o mini 91.42 / 60.28; Gemini 1.5 Pro 83.25 / 53.08; Gemini 1.5 Flash 84.41 / 47.81; Claude 3.5 Sonnet 91.36 / 59.2; Claude 3.5 Haiku 85.33 / 56.48; Llama 3.1 405B 88.93 / 53.7; Llama 3.1 70B 85.21 / 52.07; Llama 3.1 8B 80.54 / 48.7 (p. 7).
- Table II, func-sec@10 without and with the security instruction: GPT-4o mini 60.28 / 64.12; Claude 3.5 Haiku 56.48 / 66.28; Gemini 1.5 Flash 47.81 / 48.97; Llama 3.1 70B 52.07 / 53.47 (p. 7). The func@1 of Llama 3.1 70B falls from 71.84 to 65.79 with the instruction (p. 7).
- Table II, CodeLlama-7b-hf versus SafeCoder: func@10 68.82 / 33.75; func-sec@10 40.74 / 18.26 (p. 7).
- The security instruction used is the single sentence "Your code should be secure and should NOT contain any vulnerability", with no CWE-specific hints (p. 7).
- Task coverage: 119 tasks, 31 CWEs, 5 languages, 11 C-specific memory tasks (p. 6).
- Inconsistencies in the text: the paper says it mainly studies four LLMs (p. 6) while Fig. 3 is described as showing five LLMs, with Llama 3.1 8B added (p. 6, p. 7). The reference given for SafeCoder, [23], is titled "Safecoder: A machine-learning-based encoding system to embed safety identification information into qr codes" (p. 8), whereas the text uses SafeCoder as a security fine-tuning method for code LLMs (p. 3, p. 7).

## Quotes

- "an LLM might produce a no-op solution to avoid vulnerabilities, which ensures security but does not follow the user intention" (p. 2)
- "only less than a third (562/1916) of the vulnerable samples included in CyberSecEval can be reproduced" (p. 2)
- "We intentionally avoid leaking any security-awareness to LLMs in the specification" (p. 4)
- "The key difference between our approach and previous security benchmarks is that we are outcome-driven and do not rely on any static analyzer." (p. 5)
- "From func@10 to func-sec@10, the performance drops around 30% across all models, with the maximum 35.79% observed on Gemini 1.5 Flash." (p. 6)
- "It shows that larger models almost always achieves higher func-sec@k." (p. 6)
- "the model may learn to avoid generating any security-sensitive code to be securer (though keeps its functionality on other tasks)" (p. 7)
- "which distinguishes learning secure coding practice from learning to avoid security-related coding at all" (p. 8)

## Reading

## Connections

## Disagreements
