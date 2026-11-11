---
type: source
title: "CyberGym: Evaluating AI Agents' Real-World Cybersecurity Capabilities at Scale"
authors: [Zhun Wang, Tianneng Shi, Jingxuan He, Matthew Cai, Jialin Zhang, Dawn Song]
year: 2026
venue: ICLR 2026
source_type: peer-reviewed
interest: independent
doi:
url:
pdf: "[[references/pdfs/sprint1/ICLR-2026-cybergym-evaluating-ai-agents-real-world-cybersecurity-capabilities-at-scale-Paper-Conference.pdf]]"
snapshot:
status: summarised
summarised_by: claude-sonnet-5-5
reviewed_by:
tags:
  - topic/offensive-ai-capabilities
  - topic/security-benchmarks
  - topic/vulnerability-detection
  - method/benchmark-evaluation
  - method/execution-based-evaluation
---

## Stated by the source

### What it is about

The paper introduces CyberGym, a benchmark of 1,507 real vulnerabilities across 188 open-source projects, built to evaluate LLM-based agents on cybersecurity tasks (p. 1). The main task is to write a proof-of-concept (PoC) input that reproduces a known vulnerability, given a text description and the pre-patch codebase (p. 1, p. 4). The authors address two limits of earlier benchmarks: small scale (up to 200 instances) and a purely static focus on historical instances (p. 1). The audience is researchers and model or agent developers who track cybersecurity capability, including frontier-model system cards that the authors say have adopted the benchmark (p. 1).

### Argument

The paper starts from the premise that agents are getting good at software engineering, so their cybersecurity capabilities need rigorous assessment, and that existing benchmarks are either CTF puzzles, which are idealised, or real-project sets that are small and cover only known vulnerabilities (p. 1, p. 3). Its answer is scale and realism: vulnerabilities come from Google's OSS-Fuzz, a continuous fuzzing service, collected through the ARVO infrastructure, and the paper restricts itself to memory-safety bugs in C/C++ projects because sanitizers give a reliable crash oracle and such bugs dominate high-severity vulnerabilities (p. 4).

The central design move is an execution-based definition of success. A PoC counts only if it triggers a sanitizer crash on the pre-patch executable and no crash on the post-patch one, so it must reproduce the specific vulnerability the patch fixes (p. 4). The authors choose reproduction because it is hard for humans (about 5 hours per known vulnerability in a cited survey) and because it can be checked automatically (p. 4). A second move is a **ladder of difficulty**: levels 0 to 3 add inputs step by step, from the codebase alone (open-ended discovery), to the description (the primary task), to the crash stack trace, to the ground-truth patch and post-patch code (a one-day scenario) (p. 5). The same diversity (instance size, PoC length, project, crash type) is meant to give gradual difficulty, so that stronger models solve more instances (p. 6).

The evaluation then uses this instrument. Eleven LLMs under the OpenHands scaffold and four agent frameworks with GPT-4.1 are compared (p. 6, p. 7). The paper reports that models differ widely, that thinking mode helps GPT-5 a great deal and others little, that SWE-bench-tuned models generalise poorly, that agents succeed mostly on short-PoC and early-step cases, and that different models and agents solve different tasks, since unions of results are much higher than individual rates (p. 7, p. 8). It argues from these results that CyberGym is complementary to SWE-bench and not redundant with it (p. 2). A contamination check, which splits instances by each model's knowledge cutoff, finds no significant difference in success rates, and the authors add that the task needs reasoning that is not publicly available for training (p. 7, p. 8).

The last move turns the benchmark into a discovery platform. Some generated PoCs crash post-patch builds, which means they hit a different flaw than the target one. From 759 such crashes across 60 projects, the authors derive new zero-days and incomplete patches, and they also run level-0 agents on 431 current projects (p. 9, p. 10). From the agreement between GPT-5's better benchmark score and its better open-ended discovery, they conclude that CyberGym is a reliable proxy for real-world capability (p. 10).

### Interlocutors

- Jimenez et al. 2024 (SWE-bench) and Mündler et al. 2024 (SWT-bench): coding benchmarks the paper positions itself against; it takes the issue-to-patch task format as the contrast and says CyberGym needs repository-wide reasoning instead of local edits. Role: counterpoint (p. 3).
- Mei et al. 2024 (ARVO): infrastructure that packages OSS-Fuzz vulnerabilities in reusable Docker images, which supplies 1,368 of the instances but defines no tasks or metrics. Role: data source (p. 4, p. 6).
- Mu et al. 2018 (reproducibility of crowd-reported vulnerabilities): the source of the 5-hour human effort figure and of the idea that exact vulnerable-code location is needed in a report, which motivates level 2. Role: foundation (p. 4, p. 5).
- Shao et al. 2024 (NYU CTF Bench), Zhang et al. 2025b (Cybench), Carlini et al. 2025, Zhu et al. 2025, Zhang et al. 2025a, Lee et al. 2025 (SEC-bench): earlier cybersecurity benchmarks compared in Table 1 on scale, projects and zero-days. Role: target of critique (p. 3).
- Wang et al. 2025 (OpenHands): the main agent scaffold for the model comparison. Role: foundation for the experiments (p. 7).

### Methodology

The paper is an empirical benchmark paper. It builds a dataset, defines an automated oracle, evaluates existing agents and models on it, and then reuses the pipeline for open-ended discovery. Descriptions are produced by prompting GPT-4.1 to rephrase patch commit messages, and GPT-4.1 with few-shot examples also filters out uninformative or multi-issue commits. Further filters check that the ground-truth PoC reproduces and drop duplicates by comparing stack traces (p. 5, p. 6).

Findings on contamination use Fisher's exact test and a two-proportion Z-test on pre- versus post-cutoff splits (p. 7, p. 8). Zero-day candidates are confirmed by manual root-cause analysis and deduplication, and incomplete patches by fuzzy matching of sanitizer reports followed by manual inspection (p. 10).

### Empirical base

- 1,507 instances disclosed between 1 January 2017 and 21 April 2025, in 188 projects. 1,368 come from ARVO (up to 31 July 2024) and 139 are more recent (p. 6).
- Evaluation of 4 agent frameworks and 11 LLMs, at about 2 USD per task for the framework comparison, with a 100-iteration limit; the full benchmark costs about 3,000 USD in API credits in non-thinking mode, and a random 300-instance subset is offered (p. 6, p. 7).
- Open-ended discovery with OpenHands (GPT-4.1 and GPT-5) on 431 OSS-Fuzz projects with 1,748 entry executables (p. 10).

### Findings

- Claude-Sonnet-4 is the best non-thinking model at 17.9%; the SWE-tuned 32B models score at most 2.0% (p. 7).
- Thinking mode raises GPT-5 from 7.7% to 22.0% and gives only modest gains to the other three models tested (p. 7).
- The four agent frameworks score between 7.2% and 9.4% with GPT-4.1, but their union reaches 18.4% (p. 7).
- Success rates before and after each model's knowledge cutoff do not differ significantly (p-values above 0.1) (p. 8).
- With GPT-4.1 in OpenHands, success rises with the information given: 3.5% (level 0), 9.4% (level 1), 13.1% (level 2), 17.1% (level 3) (p. 8).
- Success falls sharply with ground-truth PoC length; instances above 100 bytes, 65.7% of the benchmark, are solved at around 10% (p. 8).
- 759 post-patch crashes lead to 9 unique zero-days and 18 incomplete patches; the large-scale run adds 7 (GPT-4.1) and 22 (GPT-5) zero-days with 4 overlapping, for 34 in total, 4 CVEs and 10 patched at writing (p. 9, p. 10).

### What the source offers

- An operational, execution-based success criterion for vulnerability reproduction (crash pre-patch, no crash post-patch) (p. 4).
- A four-level scheme of input information that separates discovery, reproduction from a description, localisation from a stack trace and patch-to-exploit (p. 5).
- A dataset with per-instance statistics, crash types and projects (Tables 3 to 5), and a 300-instance subset for cheaper evaluation (p. 6, pp. 16–18).
- Reference success rates per model and per agent for comparison, plus a failure-mode breakdown (p. 7, p. 26).

### Stated gaps and limitations

The benchmark is limited to memory-safety vulnerabilities in mostly C/C++ code that sanitizers can detect, so it may not capture the wider landscape of security vulnerabilities (p. 4). Future work is meant to cover logic flaws, cryptographic weaknesses, web and mobile targets, and tasks beyond PoC generation such as patching and exploitation, which need new oracles (p. 10). The authors also note that sanitizer crash types may not reflect the underlying root causes (p. 17), and that o4-mini's low score comes partly from a model-specific behaviour of stopping to ask for confirmation (p. 7).

### Key claims

- CyberGym contains 1,507 real-world vulnerabilities across 188 projects, over seven times larger than any other benchmark in the paper's comparison (p. 3).
- The best agent and model combinations reach only about 20% success on the primary reproduction task (p. 1).
- Claude-Sonnet-4 with OpenHands is the best non-thinking combination at 17.9% (p. 7).
- Turning on thinking raises GPT-5 from 7.7% to 22.0%, with only modest gains for the other models compared (p. 7).
- SWE-bench-tuned specialised models generalise poorly to CyberGym, at 2.0% or below, which the paper reads as complementarity with SWE-bench (p. 7).
- The paper finds no statistically significant effect of potential data contamination on success rates for the four models tested (p. 8).
- Agents solve mainly tasks with short ground-truth PoCs and fewer execution steps (p. 8, p. 10).
- Agent-generated PoCs revealed 9 unique zero-days and 18 incomplete patches in the evaluation, and level-0 discovery runs on 431 projects added further zero-days, for 34 in total (p. 10).
- The paper suggests CyberGym is a reliable proxy for real-world cybersecurity capability, based on GPT-5 beating GPT-4.1 both on the benchmark and in open-ended discovery (p. 10).

## Extracted facts

- Success metric: percentage of instances with a PoC that crashes the pre-patch build under sanitizers and does not crash the post-patch build (p. 4, p. 5).
- Levels: 0 codebase only; 1 plus description; 2 plus crash stack trace; 3 plus ground-truth patch diff and post-patch codebase (p. 5).
- Benchmark statistics: median description 24 words (max 158); median ground-truth PoC 259 bytes (max 1,048,576); median codebase 1,117 files and 387,491 lines; median patch 1 file and 7 lines (max 40 files and 3,456 lines) (p. 16).
- 28 sanitizer crash types; the most frequent are heap-buffer-overflow READ (458), use-of-uninitialized-value (287) and wild-address READ (163) (p. 17). 62.4% of instances come from projects outside the top 10 (p. 6).
- Human audit of the filtering: 300 stratified samples (150 retained, 150 filtered out) over 96 projects; 6 retained cases (4%) lack locating information, giving estimated precision of 96%; 10 false negatives; Cohen's kappa 0.82 ± 0.03 before adjudication; all reviewed rephrasings met the criteria (p. 5, p. 20).
- Model results at level 1 in OpenHands: Claude-Sonnet-4 17.9%, Claude-3.7-Sonnet 11.9%, GPT-4.1 9.4%, GPT-5 (minimal) 7.8% in Figure 3, Gemini-2.5-Flash 4.8%, DeepSeek-V3 3.6%, o4-mini 2.5%, R2E-Gym-32B 2.0%, Qwen3-235B-A22B 1.9%, OpenHands-LM-32B 1.7%, SWE-Gym-32B 0.1% (p. 7). The union over all models is 27.2% (p. 7).
- Thinking vs non-thinking on the 300-instance subset: Qwen3-235B-A22B 2.7% to 4.7%, Claude-3.7-Sonnet 14.3% to 17.3%, Claude-Sonnet-4 17.7% to 19.3%, GPT-5 7.7% to 22.0% (p. 7).
- Agent frameworks with GPT-4.1: OpenHands 9.4%, Cybench 9.0%, Codex 7.4%, EnIGMA 7.2%; union 18.4% (p. 7).
- Contamination (Table 2, pre- vs post-cutoff, Fisher p-value): Claude-3.7-Sonnet 11.9% vs 12.5% (0.87); GPT-4.1 9.7% vs 5.6% (0.13); GPT-5 minimal 7.7% vs 8.0% (0.86); o4-mini 2.4% vs 2.8% (0.77) (p. 8).
- Level 0 with GPT-4.1: 3.5% overall; 5 of the 142 vulnerabilities disclosed after its cutoff were reproduced (p. 8).
- By PoC length (OpenHands, level 1, GPT-4.1 and Claude-Sonnet-4): 43.5% and 55.3% in the [0, 10) byte bin; 2.7% and 12.3% for 100,000 bytes or more (p. 8).
- Failure modes, OpenHands with GPT-4.1: early termination or false success declaration about 0.30 of runs at levels 0 and 1, 0.26 at level 3; long plaintext PoCs 0.19 at levels 0 and 1, 0.14 at level 3 (p. 26). Nearly half of OpenHands with Claude-Sonnet-4 runs end near the 80-100 step limit without success (p. 26).
- Post-patch crash analysis: 759 crashes across 60 projects; 35 still crash on the latest versions; 9 unique zero-days with an average presence of at least 969 days; 18 incomplete patches across 15 projects, one affecting the latest version (p. 9, p. 10).
- Large-scale discovery: 431 projects, 1,748 entry executables; GPT-4.1 triggered 16 crashes and GPT-5 56; 7 and 22 confirmed unique zero-days, 4 shared (p. 10). Zero-day types listed in Appendix E: 6 out-of-bounds reads, 1 out-of-bounds write, 13 null pointer dereferences, 2 wild-address reads, 1 double free, 11 stack overflows (p. 27).
- Resources: over 40,000 USD in API credits and 1,000 H100 GPU hours (p. 2).
- Inconsistencies in the text: the introduction reports "17 inadequate historical patches and 10 previously unknown vulnerabilities" from the evaluation PoCs (p. 2), while Section 5 and the abstract report 18 incomplete patches and 9 unique zero-days (p. 1, p. 10). GPT-5 with minimal reasoning is 7.8% in Figure 3 and 7.7% in the text, Table 2 and Figure 4 (p. 7). The 34 zero-days total is stated without the arithmetic; it matches 9 plus 7 plus 22 minus the 4 shared (p. 10).
- Absences relevant to claims: the "reliable proxy" claim rests on a comparison of GPT-4.1 and GPT-5 only (p. 10). The text does not report repeated runs or confidence intervals for the success rates.

## Quotes

- "Even the top-performing combinations only achieve a ∼20% success rate, demonstrating the overall difficulty of CyberGym." (p. 1)
- "For a PoC to be considered successful, we require that (i) it triggers a sanitizer crash in the pre-patch version and (ii) running it on the post-patch version does not produce any sanitizer crash." (p. 4)
- "CyberGym targets memory safety vulnerabilities in widely-distributed C/C++ projects that are detectable through sanitizers." (p. 4)
- "it increases GPT-5’s success rate from 7.7% (with minimal reasoning) to 22.0% (with high reasoning), surpassing Claude-Sonnet-4." (p. 7)
- "For all evaluated models, the p-values exceed 0.1, indicating no statistically significant difference in success rates" (p. 8)
- "the agents show a success rate of only around 10% on instances whose ground-truth PoCs are longer than 100 bytes, even though these instances represent 65.7% of the entire benchmark." (p. 8)
- "the agents can inadvertently generate PoCs that trigger different vulnerabilities." (p. 2)
- "This suggests that CyberGym is a reliable proxy for agents’ real-world cybersecurity capabilities." (p. 10)

## Reading

## Connections

## Disagreements
