---
type: source
title: "RealSec-bench: A Benchmark for Evaluating Secure Code Generation in Real-World Repositories"
authors: [Yanlin Wang, Ziyao Zhang, Chong Wang, Xinyi Xu, Mingwei Liu, Yong Wang, Jiachi Chen, Zibin Zheng]
year: 2026
venue:
source_type: preprint
interest: independent
doi:
url: https://arxiv.org/abs/2601.22706v1
pdf: "[[references/pdfs/sprint2/red_sec_bench.pdf]]"
snapshot:
status: summarised
summarised_by: claude-sonnet-5-5
reviewed_by:
tags: [topic/ai-code-security, topic/security-benchmarks, topic/secure-coding-standards, method/benchmark-evaluation, method/static-analysis-scoring, method/execution-based-evaluation]
---

## Stated by the source

### What it is about

The paper introduces RealSec-bench, a benchmark of 105 function-level secure code generation tasks drawn from real, high-risk, Maven-based Java repositories and covering 19 CWE types (p. 1, p. 4). It targets researchers who evaluate LLM code generation and asks whether models can produce code that is both functionally correct and free of the vulnerability CodeQL flagged in the original function, once repository context is available. It also tests two common mitigations, retrieval-augmented generation (RAG) and security guidelines placed in the prompt (p. 2).

### Argument

The authors start from a criticism of existing secure-code benchmarks: they rely on synthetic examples or isolated snippets, which the paper calls the **context-isolated phenomenon**. In their account this oversimplifies a problem where vulnerabilities arise from inter-procedural dataflows, and it inflates the perceived competence of models (p. 1). Prior work is also said to evaluate functionality and security separately (p. 8). The benchmark is built to close both gaps.

Construction runs in two phases (p. 2–3). Phase 1 selects repositories. The authors take the top 4,000 most-starred Java repositories, keep Maven projects, sample by topic, audit them with CodeQL, rank them by vulnerability count, and curate manually for CWE diversity, which gives 532 high-risk repositories. A high-recall CodeQL suite then yields over 20,000 candidate findings. Phase 2 refines the candidates. Following SWE-bench, only functions that build and are executed by at least one unit test are kept. GPT-4.1 filters false positives and assigns CWE labels, and two security engineers validate the output. LLMs then rewrite each docstring into a security-neutral Javadoc, which programmers and experts check so that it does not hint at the flaw.

Evaluation uses three metrics (p. 5). Pass@k measures unit-test success. **Secure@k** is the paper's own metric: a sample is secure if CodeQL reports nothing, or if a panel of voter LLMs and a final-judge LLM reclassify the alert as a false positive (confidence above 0.5). **SecurePass@k** counts a sample only if it is both functionally correct and secure. The paper validates the adjudication on 89 manually reviewed alerts, where it lifts precision from 44.9% to 81.7% at 98.0% recall (p. 6).

Five LLMs are run under a baseline one-shot prompt, three RAG variants (BM25, the dense RLCoder retriever, and a CodeQL dataflow retriever) and a five-directive OWASP-derived security guideline (p. 4–5). The paper reports that models handle the tasks poorly. SecurePass@1 stays below 6% for every model, and functional correctness alone is modest (p. 2, p. 6). Success is concentrated in a small "Code Quality & Security" category and absent in cryptography, where models pass functionally but not securely (p. 6). Performance varies non-monotonically with the number of dataflow hops: 1-hop tasks are the hardest, and 3-hop-plus tasks tend to decline (p. 6).

On mitigations, RAG raises functional correctness but gives no substantial security gain. The high-precision dataflow retriever is inconsistent, which the authors explain by its omission of utility functions and class hierarchies needed to compile (p. 7). The security guideline helps some models (Deepseek-V3, GPT-4.1) and hurts others (Claude-3.7-Sonnet's Pass@1 falls from 16.2% to 9.5%), so the authors conclude that prompt-based security engineering is not universally effective (p. 7). The conclusion is that a gap persists between functional and secure generation (p. 1).

### Interlocutors

- SWE-bench (Jimenez et al., 2023): foundation; its reproducibility standard (build plus executable tests, fail-to-pass) is adopted for instance selection (p. 2, p. 3).
- BaxBench (Vero et al., 2025): foundation for the Pass@k / Secure@k / SecurePass@k metric family, and target of critique as a simplified scenario benchmark (p. 2, p. 8).
- CWEval (Peng et al., 2025a): target of critique for synthetic data in security benchmarks (p. 1, p. 8).
- SecRepoBench (Dilgren et al., 2025): counterpoint, cited with BaxBench for simplified scenarios lacking cross-file dependencies (p. 8).
- Wen et al. (2024) and Cheng et al. (2024): data sources for method, respectively the hybrid LLM-plus-expert false-positive workflow and CodeQL-based dataflow retrieval (p. 3, p. 5).

### Methodology

Benchmark construction plus an empirical evaluation. Code is generated for each task by five LLMs at temperature 0.7, top-p 1.0 and a 4096-token context window. Functional correctness is judged by the repository's unit tests, and security by CodeQL followed by multi-LLM adjudication (p. 4–5). The task is to write a single function body from a rewritten docstring, with a one-shot example, no helper methods and no explanation (p. 16). RAG and prompting variants are compared against a baseline prompt (p. 5).

### Empirical base

105 task instances from 30 Java repositories, 19 CWE types, hop counts from 0 to 34 (p. 1, p. 4). Five models: gpt-4.1-mini, gpt-4.1, Claude-3.7-Sonnet, Deepseek-V3, Qwen3-235B (p. 4). Results are reported at k = 1, 3, 5 for the baseline and at k = 1 for RAG and guideline variants (p. 7, p. 16).

### Findings

- SecurePass@1 stays at or below 5.71% for every model under the baseline prompt, against a Pass@1 of 8.57–16.19% (p. 7).
- Models do best on the five-task "Code Quality & Security" category, with GPT-4.1 at 80% SecurePass@1, and obtain 0.00% in the cryptography and web security category except for isolated cases at k = 3 and 5 (p. 6, p. 7).
- The Concurrency & System category (4 tasks) is 0% for four of five models at every k (p. 7).
- The benchmark's largest category, Injection & Traversal (64 tasks), gives averages of 4.06% SecurePass@1 (p. 7).
- RAG raises average Pass@1 (12.95% baseline to 19.05% with BM25) but average SecurePass@1 moves only from 5.14% to between 4.76% and 6.28% (p. 16).
- The security guideline moves average SecurePass@1 from 5.14% to 5.71% and average Pass@1 from 12.95% to 12.38%, with opposing effects across models (p. 16).
- Combining RAG with the guideline ("security-guided rag") gives an average SecurePass@1 of 4.38% (p. 16).

### What the source offers

- A repository-level Java benchmark in which each instance bundles the function, tests, a CodeQL vulnerability report and a security-neutral rewritten docstring (p. 4).
- A reusable two-stage procedure for adjudicating SAST alerts with LLM voters and a judge, with reported precision and recall against 89 manually reviewed alerts (p. 5, p. 6, p. 15–17).
- Baseline Pass@k, Secure@k and SecurePass@k figures for five models, broken down by vulnerability category and dataflow hops (p. 7, p. 15).

### Stated gaps and limitations

Internal validity: dependence on SAST tools brings false positives, and the multi-LLM adjudication, although it helps, remains limited by LLM accuracy and falls short of manual expert annotation. External validity: the benchmark covers only open-source Maven-based Java repositories, which limits generalisation to other languages and proprietary software (p. 9).

### Key claims

- Existing secure-code benchmarks rely on synthetic examples or isolated snippets, a limitation the authors call the context-isolated phenomenon (p. 1).
- On RealSec-bench, SecurePass@1 stays below 6% for all five evaluated models in the baseline setting, and no model exceeds 8% on SecurePass@k as reported in the main text (p. 2, p. 6).
- Models solve few cryptography tasks securely: SecurePass@1 is 0.00% in the Crypto & Web Security category on average, even where Pass@1 is up to 38.89% (p. 6, p. 7).
- RAG significantly improves functional correctness but offers no substantial improvement in security on this benchmark (p. 7).
- The dataflow retriever underperforms broader text-based retrieval, which the authors attribute to missing functional context (p. 7).
- A five-directive security guideline in the prompt has no significant overall effect; it helps Deepseek-V3 and GPT-4.1 but lowers Claude-3.7-Sonnet's Pass@1 from 16.2% to 9.5% (p. 7, p. 14).
- The two-stage voter-plus-judge adjudication lifts precision on 89 reviewed alerts from 44.9% to 81.7% while recall is 98.0% (p. 6).
- Dataflow complexity does not relate monotonically to success: 1-hop tasks are hardest for several models, and tasks with three or more hops tend to decline (p. 6).

## Extracted facts

- Pipeline counts: top 4,000 starred Java repositories, 532 high-risk repositories, over 20,000 raw CodeQL findings, 105 final instances from 30 repositories (p. 2, p. 3, p. 4).
- CWE mix: Log Injection 56.2%; broken cryptographic algorithms 6.7%; CSRF-unprotected HTTP requests 6.7%; user-controlled data in arithmetic 5.7%; implicit narrowing conversion 4.8%; unreleased locks 2.9%; sensitive information disclosure 1.9%; XXE, deserialisation, path traversal and command injection 0.9% each (p. 4).
- Hops: 37 zero-hop (35.2%), 25 one-hop (23.8%), 14 two-hop (13.3%), 7 three-hop (6.7%), 22 above three hops (21.0%), maximum 34 (p. 13). The percentages as printed sum to 100.0%.
- Category sizes in Table 2: Injection & Traversal 64, Crypto & Web Security 18, Data Processing & Validation 14, Code Quality & Security 5, Concurrency & System 4 (p. 7).
- Baseline at k = 1 (P / S / SP): Claude-3.7-Sonnet 16.19 / 4.76 / 4.76; Deepseek-V3 8.57 / 5.71 / 3.81; GPT-4.1 15.24 / 8.57 / 5.71; GPT-4.1-mini 13.33 / 5.71 / 5.71; Qwen3-235B 11.43 / 6.67 / 5.71; average 12.95 / 6.28 / 5.14 (p. 7).
- Baseline averages at k = 5: Pass 15.62%, Secure 8.76%, SecurePass 6.86% (p. 7).
- Average SecurePass@1 by hops: 0 hops 8.65%, 1 hop 2.40%, 2 hops 5.71%, three or more hops 2.76% (p. 15).
- RAG, average P / S / SP at k = 1: BM25 19.05 / 6.67 / 6.28; dense 17.91 / 5.90 / 5.52; dataflow 14.29 / 6.28 / 4.76 (p. 16).
- Prompting, average P / S / SP at k = 1: security-guideline 12.38 / 7.05 / 5.71; security-guided rag 13.91 / 5.33 / 4.38. Security-guideline SecurePass@1: Deepseek-V3 3.81% to 6.67%, GPT-4.1 5.71% to 8.57%, Claude-3.7-Sonnet 4.76% to 2.86% (p. 16). The appendix text states SecurePass@1 going from 4.76% to 8.57% for Deepseek-V3 and from 6.67% to 9.52% for GPT-4.1 (p. 14), which do not match Table 7 (p. 16).
- Adjudication ablation on 89 manually reviewed alerts (precision / recall / F1): SAST alone 44.9 / 100.0 / 62.0; three voters 63.0 / 85.0 / 72.3; voters plus judge 81.7 / 98.0 / 89.1 (p. 6).
- Judge reclassifies an alert as a false positive at confidence above 0.5 (p. 5). The voters' model identities and the number of generated samples per task are not stated.
- Guideline directives: input/output, authentication/access control, cryptography, error handling/logging, configuration/dependencies, derived from OWASP (p. 12).
- Internal inconsistencies between text and tables: the main text says GPT-4.1's best SecurePass@1 across hops is 5.7% at 0 hops (p. 6), while Table 5 gives 13.51% (p. 15); the main text gives Qwen3-235B's 2-hop SecurePass@1 as 1.9% (p. 6), while Table 5 gives 14.29% (p. 15); the appendix text gives Claude-3.7-Sonnet's 0-hop SecurePass@1 as 16.22% and a 2-hop peak of 21.43% for Qwen3-235B and Claude-3.7-Sonnet (p. 14), while Table 5 gives 8.11% and 14.29% / 7.14% at k = 1 (p. 15). The appendix text gives the dense retriever's best SecurePass@1 for Claude-3.7-Sonnet as 10.48% and BM25's for GPT-4.1-mini as 8.57% (p. 14), while Table 6 gives 7.62% and 6.67% (p. 16). The main text puts these at 7.6% for Claude and Qwen3-235B (p. 7). The intro's "below 6%" (p. 2) and the results section's "no model exceeding 8%" (p. 6) refer to different values of k.

## Quotes

- "Existing benchmarks often fall short by relying on synthetic vulnerabilities or evaluating functional correctness in isolation" (p. 1)
- "an issue we term the context-isolated phenomenon" (p. 1)
- "the composite SecurePass@1 metric remaining below 6% across all subjects" (p. 2)
- "they fail to secure the code, resulting in a near 0.00% SecurePass@1" (p. 6)
- "This configuration reduces false positives by 77.6% raising precision to 81.7% and restores recall to 98.0%." (p. 6)
- "results indicate that while RAG significantly bolsters functional correctness, it offers no substantial improvement in security" (p. 7)
- "Conversely, for models like Claude-3.7-Sonnet, the same guidelines induce a performance degradation." (p. 7)
- "guidance lacks uniformity and fails to reliably enhance composite performance on average" (p. 8)
- "our reliance on SAST tools introduces the risk of false positives, which can affect the accuracy of the security assessment." (p. 9)

## Reading

## Connections

## Disagreements
