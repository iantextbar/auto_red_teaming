---
type: source
title: "BAXBENCH: Can LLMs Generate Correct and Secure Backends?"
authors: [Mark Vero, Niels Mündler, Victor Chibotaru, Veselin Raychev, Maximilian Baader, Nikola Jovanović, Jingxuan He, Martin Vechev]
year: 2025
venue: Proceedings of the 42nd International Conference on Machine Learning (PMLR 267)
source_type: peer-reviewed
interest: undetermined
doi:
url:
pdf: "[[references/pdfs/sprint1/baxbench.pdf]]"
snapshot:
status: summarised
summarised_by: claude-sonnet-5-5
reviewed_by:
tags: []
---

## Stated by the source

### What it is about

The paper introduces BAXBENCH, a benchmark of 392 tasks for generating complete backend applications, scored both for functional correctness and for security (p. 1). Existing coding benchmarks, it says, cover function-level code, algorithmic problems or repository edits, and measure security on separate tasks or on single functions (p. 1, p. 2). The question it pursues is whether LLMs can autonomously produce deployment-ready, self-contained backend modules that are both correct and secure (p. 1). It is addressed to the code-generation and code-security research community and to model developers (p. 8).

### Argument

The paper starts from a gap. Function-level benchmarks are saturating (Claude 3.5 Sonnet is said to pass 92% of HumanEval), agentic benchmarks such as SWE-bench also test tool use and context retrieval, and security benchmarks build bottom-up tasks around a single CWE (p. 1, p. 9). It argues that backends are a good target because they are practically relevant, need several functions and files, and are exposed to untrusted users, so one exploit can affect every user (p. 1, p. 2).

The benchmark is built from **scenarios** (28 backend specifications, given as OpenAPI plus a plaintext transcription) crossed with **frameworks** (14, in 6 languages), giving 392 tasks (p. 3). Functional tests and security exploits are written at API level, so they are framework-agnostic and reusable across frameworks (p. 3). Security is measured by executing expert-written exploits against the running application, not by static analysis. The paper says static analysers give false positives and negatives, are often paid, and depend on language support, whereas exploits give a "sound upper bound" on security, are reproducible and are framework-agnostic (p. 3, p. 4). Two metrics follow: pass@k (all tests pass) and sec_pass@k (all tests pass and no exploit succeeds) (p. 5, p. 24).

The first result is that all 11 evaluated models fall short. The best pass@1 is 62% (OpenAI o1), around half of the correct programs of each model are exploitable, and the best sec_pass@1 is in the high 30s (p. 1, p. 2, p. 5). The best model on correctness is not the best on security (p. 6). Further analyses probe what moves the numbers. Security reminders in the prompt help reasoning models even in generic form, while non-reasoning models improve little. An oracle prompt listing the relevant CWEs raises sec_pass@1 for all models but lowers the number of passing programs (p. 6). An agent scaffold improves correctness modestly and improves security only under the oracle prompt (p. 6). Performance falls with the number of tokens in the OpenAPI specification, and drops on less popular or multi-file frameworks, where the correct programs also contain a higher share of vulnerabilities (p. 6, p. 7).

The paper then draws its lessons. Failures in functionality are often trivial boilerplate errors (formats, response codes, files, CLI flags, compilable code) (p. 8). On security, models seem to fail mainly by not attending to it unless told to, which the paper reads as a sign that base models may already hold the knowledge and that post-training should make security an explicit objective (p. 7, p. 9). It also reports that precise OpenAPI specifications beat plaintext ones, and suggests that rigorous requirement specification may stay important (p. 8). The conclusion is that correct and secure backend generation is a minimal requirement before LLMs generate production code (p. 9).

### Interlocutors

- Chen et al. 2021 (HumanEval): foundation for the pass@k estimator, and example of the saturated function-level benchmarks BAXBENCH positions itself against (p. 1, p. 24).
- Fu et al. 2024 (CodeGuard+): foundation for the sec_pass@k metric, which BAXBENCH reuses (p. 24).
- Jimenez et al. 2024 (SWE-bench): counterpoint; it targets agents and repository-level edits, while BAXBENCH targets from-scratch generation (p. 1, p. 9).
- Pearce et al. 2022, Bhatt et al. 2023, Yang et al. 2024b, Peng et al. 2025 (security benchmarks): target of critique; they craft tasks around a single CWE, mostly at function level (p. 5, p. 9).
- Snyk Code (Snyk 2025): data source for exploit development and the static-analysis comparison (p. 4, p. 8).

### Methodology

The source is a benchmark paper: it constructs an executable evaluation and runs a controlled comparison of models, prompts, frameworks and scenarios on it. Each generated application runs in an isolated Docker container and is exercised through its API by functional tests and exploits (p. 3, p. 4). Functional tests were written manually and checked on human-reviewed solutions (p. 3). Exploits were started from manually suspected attacks, extended by inspecting GPT-4o-generated and human-written solutions, manually and with Snyk Code (p. 4). Some exploits are white-box-like, scanning the SQLite database and execution environment for artefacts such as improperly stored passwords (p. 4).

Scenarios were chosen against four criteria: common in real development, more complex than function-level benchmarks, potentially vulnerable, and realisable securely (p. 3). Frameworks were chosen by the StackOverflow developer survey and GitHub stars (p. 4).

### Empirical base

- 28 scenarios, 54 endpoints in total (about 2 per scenario, 1 to 5), 14 frameworks in 6 languages, 392 tasks (p. 4).
- 11 LLMs: OpenAI o1, o3-mini, GPT-4o, Claude 3.5 Sonnet, DeepSeek-R1, DeepSeek-V3, Codestral, Qwen2.5 Coder, Llama 3.3 70B, Qwen2.5 72B and 7B (p. 5).
- 10 samples per task at temperature 0.4 for non-reasoning models, 1 sample for the three reasoning models (p. 5).
- Exploits target on average 3.3 CWEs per scenario, 13 distinct CWEs, 9 of them in the MITRE 2024 Top 25 (p. 5).

### Findings

- Pass@1 ranges from 62% (o1) down, and correct-and-secure sec_pass@1 is at most about 37% (p. 1, p. 2, p. 5).
- Around 50% of the passing programs of each model are exploitable (p. 5).
- o3-mini, DeepSeek-R1 and Claude 3.5 Sonnet beat o1 on sec_pass@1 (p. 6).
- Generic security reminders help the three reasoning models considerably, and the non-reasoning models not significantly (p. 6).
- The oracle reminder gives the highest sec_pass@1 for every model but reduces passing programs (p. 6).
- OpenHands with Claude 3.5 Sonnet: under the oracle prompt sec_pass@1 rises by 7.2 points against 2.5 for the base model; under the normal prompt there is no security gain (p. 6).
- Framework matters: Python, Go and JavaScript frameworks do better, Rust-Actix and PHP-Lumen worse (p. 6).
- Pass@1 correlates negatively with OpenAPI specification length (OLS fit, slope printed as -0.49) (p. 7).
- Secure solutions need about 5% more tokens than correct but exploitable ones (p. 7, p. 8).
- OpenAPI specifications beat plaintext on pass@1 for o3-mini, GPT-4o and Claude 3.5 Sonnet (p. 8).

### What the source offers

- A public benchmark, leaderboard and code with framework-agnostic functional tests and exploits, designed to be extended with new scenarios and frameworks (p. 2, p. 9).
- A per-scenario, per-framework and per-model table of CWE occurrence under three prompt conditions (pp. 26–31).
- An operational definition of "correct and secure" through sec_pass@k and the exploit-based security criterion (p. 24).
- A comparison of exploit coverage with a commercial static analyser (p. 8).

### Stated gaps and limitations

The authors list three extensions: more exploits and tests to tighten the bounds, more frameworks, and more and harder scenarios (p. 9). They note that public release makes contamination impossible to rule out, and say that no golden solutions are released and that the benchmark will be updated (p. 9). The reasoning models were run once per task, so pass@5 cannot be computed reliably for them (p. 24). Exploits may miss vulnerabilities, so reported sec_pass is an upper bound (p. 24).

### Key claims

- Even the best model, OpenAI o1, reaches only 62% pass@1 on BAXBENCH (p. 1, p. 5).
- On average, security exploits succeed against about half of the correct programs generated by each model (p. 1, p. 5).
- The best correct-and-secure rate is about 37% (o3-mini, per the intro and Figure 1) (p. 2).
- The model best at correctness (o1) is not best at security; three models exceed it in sec_pass@1 (p. 6).
- Generic security reminders improve reasoning models considerably but give non-reasoning models no significant improvement (p. 6).
- Under an oracle prompt listing the scenario's CWEs, sec_pass@1 is highest for all models, but the number of passing programs generally falls (p. 6).
- Agent scaffolding (OpenHands, Claude 3.5 Sonnet, 351 tasks) gives notable but not drastic correctness gains and no security gain without the oracle prompt (p. 6).
- Models perform worse, and their correct solutions are more often vulnerable, on less popular or complex frameworks such as Rust-Actix and PHP-Lumen (p. 6).
- OpenAPI specifications yield more functionally correct backends than plaintext descriptions for the three models tested (p. 8).
- Snyk Code missed 64 vulnerable programs exploited by the benchmark's tests on o1 outputs (n = 237) (p. 8).

## Extracted facts

- Tasks: 28 scenarios x 14 frameworks = 392; 54 endpoints; OpenAPI specs average about 430 tokens (432.2 in Table 4), plaintext about 280 tokens (281.6), GPT-4o tokenizer (p. 4, p. 5, p. 13).
- Frameworks (language): Go (Fiber, Gin, net/http), JavaScript (Express, Fastify, Koa, Nest), PHP (Lumen), Python (aiohttp, Django, FastAPI, Flask), Ruby (Rails), Rust (Actix). Multi-file ones: Nest, Lumen, Django, Rails (p. 4).
- Metrics: pass@k = estimator of Chen et al. 2021, 1 - C(n-c,k)/C(n,k) averaged over tasks; sec_pass@k sets c to solutions that pass all tests and resist all exploits (p. 24).
- Sampling: temperature 0.4 and 10 samples (non-reasoning); temperature 0 for DeepSeek-R1; o1 and o3-mini have no settable temperature; 1 sample for reasoning models (p. 5).
- Figure 3 values read from the extracted text, sec_pass@1 / pass@1: o3-mini 37/61, DeepSeek-R1 35/56, Claude 3.5 Sonnet 34/56, o1 31/62, GPT-4o 22/45, DeepSeek-V3 19/40, Codestral 14/28, Qwen2.5 Coder 12/25, Llama 3.3 70B 9/22, Qwen2.5 72B 9/20, Qwen2.5 7B 5/ (pass@1 not legible in the extraction) (p. 5).
- Pass@5 / sec_pass@5 without security instructions (Figure 7): Claude 3.5 Sonnet 43/68, GPT-4o 35/64, DeepSeek-V3 29/57, Codestral 26/47 (p. 23).
- CWE coverage: 13 CWEs, 9 in the MITRE 2024 Top 25, 10 in four OWASP Top 10 risk groups (p. 5, p. 14).
- Security prompts: none; generic ("follow best practices for security and avoid common vulnerabilities"); oracle (the same plus the scenario's CWEs with descriptions) (p. 19).
- Agent experiment (Table 2), Claude 3.5 Sonnet, pass@1 base to agent: none 53.6 to 59.5; generic 45.5 to 47.7; oracle 41.0 to 45.9. sec_pass@1: none 32.9 to 31.8; generic 34.5 to 35.1; oracle 35.4 to 39.0. Python-Django and Compiler environments excluded (351 tasks) (p. 6).
- Secure-solution token overhead: 5% average; Claude 3.5 Sonnet 3.5%, Qwen2.5 7B 8.2%; JavaScript-Express 10.2%; Calculator scenario 15.1% (pp. 7–8).
- OpenAPI over plaintext, delta pass@1 / delta sec_pass@1: o3-mini +8.1/+2.8; GPT-4o +9.3/+3.2; Claude 3.5 Sonnet +6.8/+4.8 (p. 8).
- Snyk comparison on o1 correct programs (n = 237): 64 vulnerable programs missed; 25 (10.55%) flagged that the exploits did not trigger, of which 16 (6.75%) were false positives, 2 concerned rate limits, and 7 (2.95%) were correct additional flags across 3 CWEs (p. 8).
- Manual inspection of 20 incorrect o1 programs: failures on boilerplate tasks (p. 8).
- High per-framework occurrence without security instructions: CWE-79 (XSS) at 0.95 to 1.00 for several JavaScript frameworks and Rust-Actix; CWE-117 (log neutralisation) at about 1.00 for nearly all frameworks (p. 29).
- Discrepancy: the Figure 3 caption gives o3-mini sec_pass@1 as 35%, while Figure 1, the introduction and the bar values give 37% (p. 2, p. 5). Left unresolved.
- Discrepancy: the introduction says that models fail the task in "~40%" of cases on functional correctness, while the best pass@1 reported is 62% (and o3-mini 61%), which fits about 40% only for the best models (p. 2, p. 5).
- Absence: the text reports the security-reminder results of Figure 4 and the per-scenario results only as charts, without numbers in the main text (p. 6, p. 7).

## Quotes

- "even the best model, OpenAI o1, achieves a mere 62% on code correctness" (p. 1)
- "on average, we could successfully execute security exploits on around half of the correct programs generated by each LLM" (p. 1)
- "The success of any such malicious query guarantees that the backend is insecure and would pose severe risks in deployment." (p. 2)
- "These results clearly indicate that test-time compute in the form of strong reasoning capabilities is highly beneficial for anticipating the often complex security vulnerabilities." (p. 6)
- "the models do not only struggle to produce functionally correct code, but even the few correct solutions they produce contain a higher share of vulnerabilities." (p. 6)
- "security has to become an explicit objective in post-training" (p. 7)
- "well-established software engineering best practices in terms of rigorous requirement specification may remain important even in the age of LLM-powered automated software development." (p. 8)
- "these results also signify the unsuitability of SAST tools for benchmarking" (p. 8)
- "Our measured sec_pass@k provides a strict upper bound on the true sec_pass@k of the model" (p. 24)

## Reading

## Connections

## Disagreements
