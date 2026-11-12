---
type: source
title: "SecureForge: Finding and Preventing Vulnerabilities in LLM-Generated Code via Prompt Optimization"
authors: [Houjun Liu, Lisa Einstein, John Yang, Joachim Baumann, Duncan Eddy, Christopher D. Manning, Mykel Kochenderfer, Diyi Yang]
year: 2026
venue: arXiv preprint (cs.CR)
source_type: preprint
interest: independent
doi:
url: https://arxiv.org/abs/2605.08382v1
pdf: "[[references/pdfs/sprint2/secure_forge.pdf]]"
snapshot:
status: summarised
summarised_by: claude-sonnet-5-5
reviewed_by:
tags: [topic/ai-code-security, topic/automated-red-teaming, topic/coding-agents, topic/secure-coding-standards, method/static-analysis-scoring, method/execution-based-evaluation, method/system-proposal]
---

## Stated by the source

### What it is about

The paper presents SecureForge, an automated pipeline that audits frontier and open code models for statically detectable vulnerabilities triggered by benign prompts, and then uses the failures it finds to optimise a system prompt that lowers the vulnerability rate at inference time (p. 1). The scope is single-turn generation of new Python code, scored with Semgrep against the CWE Top-25 and with model-written unit tests (p. 6, p. 9). The intended audience is developers who reach closed-weight models only through an API and cannot fine-tune them (p. 2). The question it pursues is whether benign failures can be found and amplified automatically and then prevented without weight updates and without losing functional correctness.

### Argument

The paper starts from a gap it sees in prior work. Adversarial threat models do not match what ordinary users do, hand-written CWE scenarios cannot cover the space of benign prompts that yield vulnerable code, and fine-tuning defences need white-box access and risk distribution shift that degrades coding ability (p. 2). The dangerous case, it argues, is code that is functionally correct but insecure, because it passes tests, looks right and ships (pp. 1–2). It therefore measures the joint event of passing tests and being vulnerable, not vulnerability alone.

The method has three stages (p. 3, p. 4). First, **single-shot falsification**: for each CWE, an LLM writes a realistic coding task from the MITRE description, few-shot bootstrapped from Pearce et al.; a second pass strips mentions of attacks, vulnerabilities and CWE hotwords and adds production-quality wording; the target model is then sampled at temperature 1.0 and only prompts whose output triggers a Semgrep finding are kept as seeds (p. 4). Second, **MCMC amplification**: since single seeds are sparse and repeated paraphrase is not diverse, the paper samples from the failure distribution with a Metropolis-Hastings chain. The unnormalised target is the product of the probability that a prompt yields vulnerable code and the probability that a user writes it; the second factor is assumed uniform over fluent prompts, and an LLM rephrasing prompt serves as a symmetric proposal kernel (pp. 4–5). The failure probability of each prompt is estimated with a Beta posterior over repeated rollouts until its variance falls under a threshold (p. 5). The paper claims the chain keeps diversity because each prompt is derived from the previous one rather than from a fixed seed (p. 5).

Third, **hardening by prompt optimisation**: the resulting corpus of benign, high-failure prompts is used as hard negatives for GEPA, a reflective genetic-Pareto prompt optimiser. Starting from a generic system prompt, GEPA scores rollouts +1 or -1 on Semgrep and feeds back the CWE-labelled findings and line numbers, and it searches for the single system prompt that minimises aggregate failure probability across all weaknesses (p. 5, pp. 6–7, p. 20).

The evidence is laid out in this order. Asking a model to be secure, even naming the CWEs under test, leaves double-digit vulnerability rates, so prompting alone is not enough (p. 7, p. 9). The optimised prompt reduces weakness rates by up to 48% while test passage is essentially unchanged, and for the frontier models it moves joint security-and-test-pass upward without moving left on the capability axis, which the authors call a Pareto improvement (p. 8). The prompt, optimised only on synthetic CWE scenarios, also improves the joint rate on 203 real SWE-chat tasks (pp. 8–9). Ablations support the design: MCMC finds vulnerable prompts up to 2 times more successfully than plain rephrasing, and GEPA beats MIPRO at reducing vulnerabilities (p. 7, p. 13).

A secondary observation runs through the appendix. Benign prompts elicited vulnerabilities at least as often as prompts built straight from CWE descriptions, which the authors read as safety training having reduced malicious misuse but not the unintentional-harm case (p. 15).

### Interlocutors

- Pearce et al. 2025, "Asleep at the keyboard?": hand-crafted CWE scenarios using Copilot; source of the human-written prompts used for few-shot bootstrapping, and an example of the hand-crafted approach judged insufficient (p. 2, p. 4).
- Xu et al. 2025, ProSec: closest prior work, synthetic CWE scenarios plus iterative prompting and fine-tuning; target of critique for its cost and risk of pushing the model out of distribution (p. 3).
- He and Vechev 2023 and He et al. 2024: white-box prefix tuning and instruction tuning for secure code; counterpoint requiring weight access (p. 3).
- Agrawal et al. 2026, GEPA, and Opsahl-Ong et al. 2024, MIPRO: prompt optimisers; GEPA is the foundation of the hardening stage and MIPRO the compared alternative (p. 6, p. 13).
- Baumann et al. 2026, SWE-chat: dataset of real human-agent coding sessions, the data source for the out-of-distribution evaluation (p. 7).

### Methodology

The paper is a system proposal evaluated empirically. Vulnerability is operationalised as any Semgrep Community Python rule firing on the extracted code file, mapped to CWEs by Semgrep's per-rule mapping (p. 6). The vulnerability rate of a prompt is the expected value of a Beta posterior over repeated rollouts at temperature 1.0, resampled until its variance is below 0.015, and results carry 95% Beta-posterior credible intervals (p. 6). Functionality is checked with pytest files that an LLM generates for each task and that stay fixed across rollouts; 50 were checked by hand, and the authors state that the tests do not exhaustively measure implementation quality (p. 6).

Baselines are three user-side prompts: plain "write code", a "secure/production code" prompt, and the same with CWE information added (p. 6). Optimised prompts are compared with these on held-out scenarios built from non-overlapping seed examples, then on the SWE-chat tasks (p. 7).

### Empirical base

- Models: open (Qwen 2.5 Coder 7B and 14B, Qwen3 30B-A3B, CodeLlama 7B, Kimi K2) and closed (GPT 5.4 nano, mini and full, GPT 5.3-codex, Claude Sonnet 4.6), sampled at temperature 1.0 with a 32,768-token budget (p. 5).
- Seeds: 20 scenarios for each CWE Top-25 entry, 10 for MCMC and tuning and 10 held out, giving 500 prompts and 5,000 seed rollouts; MCMC uses three burn-in steps and 32 sampling steps per prompt and yields 80,000 prompts (p. 6).
- In-distribution evaluation: 25 CWEs by 10 scenarios by 10 rollouts, 2,500 samples (p. 7).
- Out-of-distribution evaluation: 203 Python-related tasks from SWE-chat, multi-turn sessions collapsed into single prompts by Claude Sonnet 4.6 and validated manually (p. 7).

### Findings

- Across the audit, models produced statically verifiable weaknesses on average 23% of the time even when asked to write secure production code with the relevant CWEs in context, and 12.7% of outputs were both vulnerable and passing tests (p. 2).
- Under security-aware and CWE-aware prompting, models stayed vulnerable more than 13% of the time on test-passing cases (p. 7, p. 9).
- The optimised system prompt cut weakness rates by up to 48% across models with test passage essentially unchanged (p. 8).
- For frontier models, the joint rate of secure-and-passing rose significantly against 95% Beta credible intervals, which the authors describe as a Pareto improvement (p. 8).
- On SWE-chat tasks the joint rate improved by up to 13.5%, with the strongest effect on the strongest GPT models (p. 3, p. 8).
- The reduction is near uniform across CWEs except CWE-94 and CWE-306 (p. 15).

### What the source offers

- An open-source toolkit (`secureforge`, CLI `rcg`) with generate, amplify, rollout and propose commands, and the exact DSPy prompt signatures for falsification, rephrasing, baselines, test generation and SWE-chat rewriting (pp. 17–24).
- A formulation of vulnerability rate as the failure probability of a prompt set per weakness, estimated with a Beta posterior, plus a recipe for scaling failures with a Metropolis-Hastings chain (pp. 3–5).
- Per-model numbers for baseline versus optimised prompts, and a per-CWE vulnerability breakdown (p. 8, p. 16).

### Stated gaps and limitations

- A prompt optimised for one model may not secure another; the authors propose re-running the open-source procedure per model (p. 9).
- The method has a one-time search cost, put at on average $150 with 50M tokens (p. 9).
- Only single-turn generation of new Python code is evaluated; Python eliminates classes such as memory bugs, so results are described as a lower bound on failure rates (pp. 9–10).
- The unit tests are not claimed to be exhaustive (p. 6).
- The two exceptions, CWE-94 and CWE-306, are put down tentatively to GEPA adopting a test-focused strategy and to authentication needing design decisions beyond a single file (p. 15).

### Key claims

- Frontier models asked to write secure production code, with the CWEs under test named, still produced verifiable vulnerabilities on average 23% of the time across 250 benign prompts (p. 1, p. 2).
- 12.7% of outputs were both vulnerable and passed the generated unit tests (p. 2).
- Security-aware and CWE-aware prompting left vulnerability rates above 13% among test-passing outputs in the GPT-family comparison (p. 7, p. 9).
- The SecureForge system prompt reduced output vulnerabilities by up to 48% on frontier models while maintaining unit test performance (p. 1, p. 8).
- MCMC amplification found new vulnerable prompts up to 2 times more successfully than simply rephrasing the original seed (p. 7).
- Static-analysis-enriched GEPA improved output security more than MIPRO in the paper's comparison on the GPT models (p. 8, p. 13).
- The optimised prompts transferred zero-shot to 203 in-the-wild SWE-chat tasks, improving the joint security-and-test rate by up to 13.5% (p. 3, p. 8).
- Benign prompts elicited vulnerabilities more often than non-benign CWE-derived prompts in the paper's comparison on two GPT models (p. 15, p. 17).
- The paper's results are limited to single-turn Python generation and may be a lower bound on failure rates for such models (pp. 9–10).

## Extracted facts

- Metric definitions: vulnerability means any Semgrep Community Python rule triggered on the code extracted from a rollout; code is analysed as a standalone file; CWE mapping uses Semgrep's per-rule mapping (p. 6).
- Test passing: pytest files generated by an LLM from the task and given to the coding model so that failures do not come from name or signature mismatches; 50 checked by hand (p. 6).
- Estimation: Beta(failures, successes) per prompt, resampled until posterior variance is below 0.015; 95% Beta-posterior credible intervals reported (p. 6).
- GEPA settings: light preset (n=6), Pareto selection, reflection minibatch 3, merge enabled; reflection model gpt-5.4 at temperature 1.0; reward of plus or minus 1 from Semgrep with CWE-labelled critique (pp. 6–7).
- Figure 1, GPT 5.4, "vulnerable and passing tests": 18.3%, 12.0%, 11.7% and 7.9% for "Write Code", "Write Secure Code", "...without CWEs" and SecureForge, in the order the figure labels them (p. 2).
- Figure 6 and Figure 4, P(vulnerable | tests pass), security-aware prompt to SecureForge: GPT 5.3 Codex 14.7% to 9.0%, GPT 5.4 15.8% to 10.1%, GPT 5.4 Mini 21.4% to 12.4%, GPT 5.4 Nano 22.1% to 15.6% (p. 14).
- Same models, P(secure and tests pass): 66.9% to 71.9%, 63.9% to 70.0%, 57.3% to 60.7%, 50.8% to 54.3% (p. 14).
- MIPRO on the same four models: P(vulnerable | tests pass) 14.3%, 13.2%, 19.7%, 18.9%; P(secure and tests pass) 66.6%, 68.3%, 56.6%, 52.4% (p. 14).
- Aggregate over all models and rollouts, security-aware prompt: 63% tests pass, 77% secure, 50.2% secure and passing, 12.7% vulnerable and passing, 26.9% secure and failing, 10.3% vulnerable and failing. After SecureForge: 62% pass, 85% secure, 54.7% secure and passing, 7.3% vulnerable and passing, 30.3% secure and failing, 7.8% vulnerable and failing (p. 15).
- The paper states that the marginal rate of test failure increased slightly for vulnerable cases after intervention, and suspects that some approaches are harder to implement securely (p. 14); vulnerability among test-failing rollouts also decreased (p. 15).
- Commit-time hardening: static analysis findings fed back for regeneration up to 36 retries; AUC of the share of scenarios still vulnerable by number of resamples: baseline 0.30, secure 0.28, CWE 0.16, SecureForge 0.03; the paper says SecureForge after a few resamples beats baselines at 30 resamples (p. 14).
- Diversity: Self-BLEU of generated code rises only marginally and does not exceed 20% for any model (p. 16).
- Severity: the ratio of severe to medium vulnerabilities stays roughly equivalent after GEPA (p. 16).
- SWE-chat table over 203 tasks: 177 findings in changed files before and 209 after; 53 introduced, 21 fixed, 156 persistent; 22 tasks (11%) with at least one introduced finding, 4 (2%) with a fixed finding, 43 (21%) with a persistent finding, 146 (72%) clean (p. 17).
- Cost: one-time search, $150 on average at $15 per MTok with 50M tokens (p. 9).
- Inconsistencies in the text. The $150 cost is stated alongside 50M tokens at $15 per MTok, which would multiply to $750 (p. 9). Models are named Qwen3 30B-A3B and Kimi K2 in the setup (p. 5) and Qwen 35B and K2.6 in the figures (p. 8). The audit cites 250 benign prompts in the abstract (p. 1), while the setup describes 500 prompts of which 250 are held out for evaluation (p. 6).- Absence relevant to a claim: the "up to 48%" reduction (p. 1, p. 8) and the "up to 13.5%" in-the-wild improvement (p. 3) are not tied in the text to a named model or a table value.

## Quotes

- "Even when specifically asked to write production, secure code, and prompted with the CWEs on which they will be tested, language models often fail to do so, producing statically-verifiable weaknesses 23% of the time; 12.7% of the time, outputs are both vulnerable and yet still pass unit tests." (p. 2)
- "Single falsification examples alone are sparse and cannot cover the set of potential variations of diverse failure scenarios." (p. 2)
- "this procedure maintains diversity better than simply rephrasing the original prompt, because the sequentiality of MCMC enables continuous exploration: each new prompt is sampled from the previous one rather than from a fixed seed." (p. 5)
- "Notably, we do not guarantee that the tests exhaustively test implementation quality, and only claim that they measure a facet of instruction following and coding ability." (p. 6)
- "simply prompting frontier language models to write secure code, even when providing them with the static analysis guidelines, still leaves >13% vulnerability rates." (p. 9)
- "A system prompt optimized for the security of one model may not make another model secure." (p. 9)
- "Python structurally eliminates certain classes of weaknesses such as memory bugs, and our results therefore represent a lower bound on the failure rates of such models." (p. 10)
- "benign prompts are in fact more likely to elicit successful attacks." (p. 15)

## Reading

## Connections

## Disagreements
