---
type: debate
question: Is the security of AI-generated code driven more by the task or prompt than by which model writes it?
sources:
  - "[[cross-cutting-security-analysis-llm-code-2026-peng]]"
  - "[[security-vulnerability-patterns-ai-generated-code-2026-kahn]]"
  - "[[assessing-quality-security-ai-generated-code-2025-sabra]]"
  - "[[rethinking-security-llm-code-2026-ma]]"
  - "[[cweval-outcome-driven-evaluation-2025-peng]]"
written_by: claude-opus-5-5
reviewed_by:
tags:
  - topic/ai-code-security
  - topic/security-benchmarks
---

## Question

The question is whether the vulnerabilities in LLM-generated code follow mainly from the task or prompt the model is given, or whether the choice of model makes a systematic difference. The sources contest it for code generated from benchmark or task prompts in 2025–2026: five open models of 4.5B to 30B on LLMSecEval prompts, three commercial chatbots on three automation tasks, five LLMs on Java benchmark tasks, eight LLMs on prompts built around risk scenarios, and model families of several sizes on CWEval-Bench. The sources isolate different factors. Some hold the prompt fixed and compare models; one varies the prompt within pairs; one varies model size within families.

## Positions

### Task and prompt drive vulnerability

The metamorphic-testing study by Peng, Wang and Zhu holds that vulnerability is largely prompt-driven. On 3,700 snippets (148 LLMSecEval prompts, five open models, five runs each), all five models agree on violation status for **65.5%** of prompts, with a mean agreement score of 0.846 (p. 5). Of the prompts, 94 (63.5%) were violated by all models and 3 (2.0%) were consistently secure (p. 5). The authors read this as vulnerability being largely prompt-driven rather than model-dependent: "the prompt itself, not the model architecture, is the primary driver of insecure code" (p. 5). Prompt keywords correlate with the number of violations, database keywords at r = 0.52 and authentication keywords at r = 0.43 (p. 4). The paper also reports model violation rates from 65.1% (Gemma4:e4b) to 73.8% (DeepSeek-Coder 6.7B), and notes that the largest model, Qwen3-Coder 30B, is not the safest (p. 3). On the 51 prompts where models disagree, DeepSeek-Coder violates 76.5% and Qwen3-Coder 49.0% (p. 5). Violations are judged by an LLM (p. 2), and the authors state that results are specific to LLMSecEval prompts and five open models of 4.5B to 30B (p. 5).

Kahn and Hastings reach a similar conclusion for routine Python automation scripts. Three tasks (web scraping, email and document automation, file and workflow automation) were each given once, with identical prompts, to ChatGPT, Microsoft Copilot and Google Gemini, giving nine scripts (p. 3). Nine of the 17 deduplicated vulnerability classes appeared in code from all three models and 14 in at least two, and weighted CVSS totals differed by less than 10% across models (p. 4). The same classes recur in the same task contexts, such as template injection in each email sender and SSRF in each scraper (p. 5). The authors conclude that the risk "is not tied to any particular model but rather to the task category" (p. 1). Their evidence is one generation per model and task, reviewed by Claude Code with a cap of five findings per file, with no manual confirmation and no exploitation (p. 3, p. 8).

The Sonar study by Sabra, Schmitt and Tyler qualifies the position. With identical prompts across five LLMs on 4,442 Java tasks (p. 5), each model produced a comparable mix of about 90–93% code smells, 5–8% bugs and around 2% vulnerabilities (p. 9), and hard-coded credentials appeared in code from all five (p. 17). The paper reads the similarity as a systemic pattern of current code generation rather than a model-specific flaw (p. 9). It attributes the consistency of vulnerabilities across models to training data, "the most plausible origin" (p. 16), not to the prompt. It also reports model differences in issue density, from 19.48 to 32.45 issues per KLOC (p. 8), and in vulnerabilities per KLOC, from 0.38 to 0.62 (p. 9). The paper's explanations are framed as possible rather than established (pp. 11–15).

The poster by Ma et al. also qualifies it. Its 2,700 test cases are prompt pairs in three risk scenarios across nine languages, given to eight LLMs (p. 3, p. 4). Every model has a baseline vulnerability rate above 56%, and the rate differs by scenario, 66% under ambiguous requirements against 52% under a security–functionality conflict (p. 5). The authors state that the security of generated code is shaped by prompt-side risk conditions as well as by model capability (p. 2).

### Model choice matters

CWEval (Peng et al. 2025) finds that model size makes a systematic difference within families. On 119 tasks over 31 CWEs in five languages, scored by dynamic functionality and security oracles (p. 3, p. 5, p. 6), it reports that "larger models almost always achieves higher func-sec@k" (p. 6). In the GPT-4o and Gemini families the func@k differences are small, with the smaller model sometimes slightly ahead, while the func-sec@k differences are larger (p. 6). At func-sec@10, GPT-4o scores 65.33 against 60.28 for GPT-4o mini, Gemini 1.5 Pro 53.08 against 47.81 for Gemini 1.5 Flash, and Llama 3.1 405B, 70B and 8B score 53.7, 52.07 and 48.7 (p. 7). Across families, Claude 3.5 Haiku beats Llama 3.1 70B on func-sec@10 despite a lower func@10 (p. 6). All models drop around 30% from func@10 to func-sec@10 (p. 6). The size comparison uses a single sampling temperature, 0.8, because of budget (p. 6).

## Why they differ

The sources isolate different factors. Peng (2026) holds the prompt set fixed and measures agreement on violation status across five open models, as judged by an LLM (p. 2, p. 5). Kahn holds one prompt fixed per task and compares three commercial assistants, with one generation each and one capped LLM review (p. 3, p. 8). Sabra holds prompts fixed and finds a similar issue profile across models, but explains it by shared training data rather than by the prompt (p. 16). Ma varies the security information in the prompt while keeping the functional task fixed (p. 3), and attributes security to both prompt and model (p. 2). CWEval varies model size within families on fixed tasks (p. 6). The quantities reported differ: agreement on violation status (Peng), overlap of vulnerability classes and CVSS totals (Kahn), proportions of issue types (Sabra), vulnerability rates by scenario (Ma) and functional-and-secure pass rates (CWEval). So do the models: open models of 4.5B to 30B (Peng, p. 5), consumer chatbots (Kahn, p. 3), five LLMs including two Claude generations (Sabra, p. 5), six large and two small models (Ma, p. 4), and three families at several sizes (CWEval, p. 6).

## Stances

- [[cross-cutting-security-analysis-llm-code-2026-peng]] · Task and prompt drive vulnerability · supports · (p. 5)
- [[security-vulnerability-patterns-ai-generated-code-2026-kahn]] · Task and prompt drive vulnerability · supports · (p. 4, p. 5)
- [[assessing-quality-security-ai-generated-code-2025-sabra]] · Task and prompt drive vulnerability · qualifies · (p. 9, p. 16)
- [[rethinking-security-llm-code-2026-ma]] · Task and prompt drive vulnerability · qualifies · (p. 2)
- [[cweval-outcome-driven-evaluation-2025-peng]] · Model choice matters · supports · (p. 6)

## Reading
