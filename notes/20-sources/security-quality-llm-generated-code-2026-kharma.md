---
type: source
title: "Security and Quality in LLM-Generated Code: A Multi-Language, Multi-Model Analysis"
authors: [Mohammed F. Kharma, Soohyeon Choi, Mohammad Alkhanafseh, David Mohaisen]
year: 2026
venue: arXiv (version 2 stamped 9 Mar 2026; running header reads IEEE Transactions on Dependable and Secure Computing)
source_type: preprint
interest: independent
doi:
url: https://arxiv.org/abs/2502.01853v2
pdf: "[[references/pdfs/sprint2/security_and_quality_of_llm_generated_code.pdf]]"
snapshot:
status: summarised
summarised_by: claude-sonnet-5-5
reviewed_by:
tags: [topic/ai-code-security, topic/security-benchmarks, topic/secure-coding-standards, method/benchmark-evaluation, method/static-analysis-scoring, method/execution-based-evaluation]
---

## Stated by the source

### What it is about

The paper is a measurement study of the quality and security of code produced by five LLMs (claude-3.5, gemini-1.5, codestral, GPT-4o, llama-3) in four languages (Python, Java, C++, C), written for researchers evaluating AI code generation (p. 1). It builds a dataset of 200 language-neutral programming tasks in seven categories and scores every task-language-model combination for compilation, semantic correctness, complexity, static-analysis findings and "clean code" attributes (p. 1, p. 4). It pursues three questions: how the choice of language affects the security of generated code (RQ1), how the models compare on syntactic validity and semantic correctness (RQ2), and which vulnerabilities are most prevalent and how they vary by model and language (RQ3) (pp. 1–2).

### Argument

The paper starts from the claim that LLMs can produce both secure and vulnerable code, that the factors behind this are not identified, and that security may differ with the chosen language (p. 1). It positions itself against prior work that mostly used one model, one language or constrained prompts, and says its contribution is a unified setup that allows direct cross-language and cross-model comparison (p. 2, p. 13). It treats quality and security as complementary, on the premise that low-quality code often correlates with vulnerabilities (p. 2).

The method is deliberately realistic. Tasks come from coding-challenge sites, vulnerability databases and SecurityEval, are rewritten in neutral language, and are sent to the models as-is, with no prompt engineering and no fixed function signatures (pp. 4, 7). Because signatures then vary, the authors write a per-sample unit test for each of the 4,000 programs from a shared language-agnostic specification (p. 5). Static analysis uses SonarQube for reliability, maintainability and security hotspots and CodeQL for query-based vulnerability validation, with manual review (p. 5).

The results are then reported in layers. Python compiles best (three models at 100%) and C++ worst (77.0–89.0%) (p. 8). Semantic correctness follows the same ordering, with C lowest (72.9–84.2%) (p. 9, p. 10). Static analysis finds more vulnerabilities and many more security hotspots in C and C++ than in Python, and the CWE profile differs by language: buffer and memory issues in C and C++, cryptographic and XML issues in Java and Python (pp. 11–12). The authors attribute the language gaps to strict typing, manual memory management and training data, though they give no test of these explanations (pp. 8–10).

The paper concludes that models underuse modern language and compiler features and favour outdated practices, for example legacy random number generation despite Java 17 improvements (p. 14). It describes the study as a time-stamped baseline, and says it measures local code-level properties of self-contained programs rather than system-level security (pp. 13–14).

### Interlocutors

- Pearce et al. 2022 (Copilot, 89 scenarios): foundation; showed Copilot often produces insecure code, but was limited to a single model (p. 13).
- Siddiq and Santos 2022 (SecurityEval): data source and counterpoint; Python-only, 130 prompts with predefined signatures, from which some tasks were adapted and rewritten language-neutrally (p. 7, p. 13).
- Tony et al. 2023 (LLMSecEval): counterpoint; language-agnostic security prompts, but secure-only outputs and a limited language set (p. 13).
- Lenarduzzi et al. 2023 (six static analysers): foundation for the manual-validation step; reports inconsistency across tools (p. 13).
- Perry et al. 2023 and Sandoval et al. 2023 (user studies): background; report more flaws than human-written code and a 10% increase in vulnerabilities in C (p. 2).

### Methodology

The source is a quantitative measurement study that, in its own words, introduces no new vulnerability classes or analysis techniques (p. 3). It generates one sample per task, language and model at temperature 0.9, top-p 0.9 and 4,096 max tokens (p. 4, p. 13), compiles and tests each, and runs static analysis. Compilation outcomes sit in a 200 by 20 binary matrix (p. 5). Two engineers with four and ten years of experience validated the tests, a process the authors put at over 800 person-hours across five months (p. 4). Manual review covered all reported vulnerabilities, and a stratified 20% sample was validated against false positives (p. 5).

### Empirical base

200 tasks (123 custom, 64 from challenge sites, 13 from security datasets; only 20 labelled Easy) (p. 7). Five models by four languages gave 4,000 code files and 4,000 unit test files; the static analysis spans 97,412 lines of code (pp. 4–5). Task tags put 102 tasks in Secure Coding, covering 86 unique CWE identifiers (p. 8). Environment: Debian 12, OpenJDK 17.0.8, Python 3.11.9, C++17 via CMake 3.28.6 (p. 4). Model versions are fixed, for example GPT-4o-202407 and claude-3-5-sonnet-20240620 (p. 3).

### Findings

- Compilation success is highest in Python (99.5–100%) and lowest in C++ (77.0–89.0%); Java ranges 88.0–95.0% and C 88.0–96.0% (p. 8).
- Semantic correctness (share of unit tests passed) ranges 88.5–92.1% in Python, 79.3–91.2% in C++ and 72.9–84.2% in C; claude-3.5 is highest in all four languages (p. 8, p. 10).
- Summed over the five models, SonarQube flags 69 vulnerabilities in Java, 40 in Python, 53 in C++ and 122 in C, and 237, 196, 109 and 762 security hotspots respectively (p. 12).
- The most frequent CWEs are CWE-780 (RSA without OAEP) and CWE-259 (hard-coded password) in Java and Python, CWE-295/326/327 (certificate validation and weak cryptography) in C and C++, and CWE-120 (unchecked buffer copy) in C (pp. 11–12).
- gemini-1.5 shows the most vulnerabilities overall (p. 12); claude-3.5 produces the most lines and the highest cognitive complexity in C and C++, while codestral and GPT-4o produce simpler code (pp. 10–11).
- Clean-code issues, particularly intentionality, are prominent in Java, C++ and C (p. 12, p. 13).
- Frequent compile errors are missing imports or includes, undeclared variables and exception handling (p. 9, p. 10).

### What the source offers

- A released dataset of 200 language-neutral tasks with difficulty labels, CWE tags, unit tests and model outputs (p. 8).
- A per-language, per-model breakdown of CWE categories from SonarQube and CodeQL on one task set (p. 12).
- A documented procedure for testing programs whose function signatures differ, with a shared test specification (p. 5, p. 20).

### Stated gaps and limitations

- Tasks are self-contained single-file programs and may not represent complex or domain-specific systems; system-level security is not captured (pp. 13–14).
- Single-turn generation without prompt engineering, interactive refinement or IDE assistance (p. 14).
- SonarQube can produce false positives; unit tests may miss behavioural defects; manual adaptation of tests adds subjectivity (p. 13).
- Non-deterministic decoding adds stochasticity, and model versions will change, so rankings are a snapshot (p. 13, p. 14).
- Planned future work: Semgrep, dynamic analysis and fuzzing, expert reviewers (p. 14).

### Key claims

- Python and Java reach higher compilation and semantic-correctness rates and produce fewer security findings than C and C++ on the study's 200 tasks and five models (p. 1).
- C and C++ outputs show more memory-safety issues, hard-coded secrets and cryptographic misuse than Python and Java outputs (p. 1).
- Compilation success ranged from 77.0% (llama-3, C++) to 100% (Python for three models) (p. 8).
- Semantic correctness was lowest in C, between 72.9% and 84.2% across models (p. 9, p. 10).
- Vulnerabilities in C and C++ skew toward memory management, while those in Java and Python skew toward cryptographic and XML-related issues (p. 12).
- RSA without OAEP padding (CWE-780) was the most frequently flagged CWE in the Java outputs (p. 11).
- The authors state that models "underutilize" modern language and compiler features and often favour outdated practices, citing legacy random number generation in Java despite Java 17 (p. 14).
- The rankings are described as a time-stamped snapshot, while the language gaps and recurring cryptographic misuse are expected to be stable (p. 14).

## Extracted facts

- Models and settings: GPT-4o-202407, llama-3-sonar-large-32k-chat (Perplexity), claude-3-5-sonnet-20240620, codestral-2405, gemini-1.5-pro-001; all at temperature 0.9, top-p 0.9, 4,096 max tokens (p. 3, p. 4).
- Dataset: 200 tasks; sources Manual 123 (E 3, M 117, H 3), code challenge sites 64 (E 14, M 43, H 7), security datasets 13 (all M) (p. 7).
- Category counts (multi-label): Secure Coding 102, Data Structures and Algorithms 86, Parsing and Validation 54, Networking 48, Mathematics and Logic 26, Programming Systems and Utilities 18, Concurrency and Synchronization 6 (p. 8). 86 unique CWE identifiers (p. 8).
- Compilation error-free, Java / Python / C++ / C: claude-3.5 95.0 / 99.5 / 81.5 / 96.0; gemini-1.5 88.5 / 100 / 77.5 / 90.5; codestral 88.5 / 100 / 80.0 / 91.5; GPT-4o 94.0 / 100 / 89.0 / 91.5; llama-3 88.0 / 100 / 77.0 / 88.0 (p. 8).
- Semantic error-free, same order of models and languages: claude-3.5 91.8 / 92.1 / 91.2 / 84.2; gemini-1.5 89.5 / 90.5 / 81.0 / 77.0; codestral 82.9 / 88.6 / 83.7 / 73.7; GPT-4o 88.3 / 90.9 / 88.0 / 81.1; llama-3 81.6 / 88.5 / 79.3 / 72.9 (p. 8).
- Lines of code analysed, per language: Java 26,550; Python 14,154; C++ 27,180; C 29,528; total 97,412 (pp. 5, 12).
- Table 11 totals (vulnerabilities S, reliability R, maintainability M, hotspots SH): Java 69 / 232 / 3,896 / 237; Python 40 / 3 / 353 / 196; C++ 53 / 35 / 2,671 / 109; C 122 / 240 / 1,817 / 762 (p. 12).
- Vulnerabilities per model (Java / Python / C++ / C): claude-3.5 15 / 5 / 9 / 19; gemini-1.5 16 / 9 / 17 / 33; codestral 12 / 9 / 10 / 21; GPT-4o 13 / 8 / 7 / 27; llama-3 13 / 9 / 10 / 22 (p. 12).
- CWE counts summed over the five models (computed from Table 12): CWE-780 Java 29, Python 18; CWE-259 Java 11, Python 11; CWE-295/326/327 grouped C++ 35, C 32; CWE-120 C 66, C++ 0 (p. 12).
- Complexity metrics: LoC, cyclomatic complexity, cyclomatic complexity density, cognitive complexity; summary CCD Java 0.17, Python 0.25, C++ 0.18, C 0.19 (p. 5, p. 12).
- Clean-code issue totals (consistency / intentionality / adaptability / responsibility): Java 69 / 976 / 1,853 / 43; Python 234 / 116 / 16 / 30; C++ 583 / 1,936 / 194 / 46; C 862 / 1,119 / 151 / 44 (p. 13).
- Test coverage: up to 10 unit tests per task; average line coverage above 75% on a sampled subset of tasks (p. 5).
- Internal inconsistencies, left unresolved. The related-work section says the study evaluates "four LLMs" while the rest of the paper uses five (p. 2). The conclusion says Java shows stronger intentionality (p. 14), while section 5.4 reports intentionality issues as prominent in Java (p. 12). The abstract says "4,000 per program unit test files" (p. 1), the body says 4,000 unit test files, 200 per language per model (p. 5). Manual validation is described as covering a stratified 20% sample of vulnerabilities (p. 5), then as about 20% of tasks (p. 13).
- Absences that bear on stated claims. The abstract and conclusion claim that models miss Java 17 security features (p. 1, p. 14), but the results sections report no per-feature analysis of Java 17 usage. Each cell is a single generation at temperature 0.9, with no repeated runs or variance reported (p. 13). The paper reports no per-vulnerability false-positive rate from the manual review, and Table 12 lists CWE counts only for those categories shown.

## Quotes

- "Python and Java achieve higher compilation and semantic correctness rates and produce fewer security findings than C and C++," (p. 1)
- "This study is a quantitative measurement study: it introduces no new vulnerability classes or analysis techniques, but systematically compares the behavior of existing LLMs across languages and tasks under a unified setup." (p. 3)
- "All inputs used the original task descriptions without prompt engineering." (p. 4)
- "Vulnerabilities in languages like C and C++ are more skewed towards memory management issues (i.e., buffer overflows, incorrect buffer size calculations) compared to Java and Python, where cryptographic and XML-related vulnerabilities are more common." (p. 12)
- "These examples show that LLMs may default to insecure practices when safer alternatives exist, indicating limited contextual security awareness." (p. 12)
- "We used non-deterministic decoding (temperature = 0.9) to reflect typical developer interactions with LLMs." (p. 13)
- "These tasks may not represent complex or domain-specific systems." (p. 13)
- "The results therefore represent a time-stamped snapshot of the evaluated model generation rather than a fixed ordering." (p. 14)
- "High semantic correctness alone does not imply task simplicity; persistent weaknesses in security and robustness underscore the need for evaluations that extend beyond correctness to capture real-world trustworthiness." (p. 14)

## Reading

## Connections

## Disagreements
