---
type: debate
question: Can what goes into the prompt, or the code around it, steer an AI code generator toward secure output?
sources:
  - "[[asleep-at-the-keyboard-copilot-security-2021-pearce]]"
  - "[[do-users-write-more-insecure-code-2023-perry]]"
  - "[[baxbench-correct-secure-backends-2025-vero]]"
  - "[[is-vibe-coding-safe-2026-zhao]]"
  - "[[rethinking-security-llm-code-2026-ma]]"
  - "[[secureforge-prompt-optimization-llm-code-2026-liu]]"
  - "[[cweval-outcome-driven-evaluation-2025-peng]]"
  - "[[broken-by-default-formal-verification-2026-blain]]"
  - "[[realsec-bench-secure-code-generation-2026-wang]]"
  - "[[cross-cutting-security-analysis-llm-code-2026-peng]]"
written_by: claude-opus-5-5
reviewed_by:
tags:
  - topic/ai-code-security
  - topic/coding-agents
  - topic/developer-behaviour
---

## Question

The question is whether what an AI code generator receives changes whether its output is secure, and by how much. This covers the wording of the prompt, explicit security instructions, and the code that already surrounds the point of generation. The sources contest it for code generation by LLM assistants and coding agents between 2021 and 2026: Copilot completions on hand-built CWE scenarios, a user study with a Codex-based assistant, backend generation from specifications, and repository-level feature requests given to coding agents. They do not all vary the same thing. One alters comments and surrounding code, one observes how users prompt, and two add generic or CWE-specific security reminders. "Steer" therefore covers several kinds of intervention.

## Positions

### Prompt and context steer security

The Copilot study by Pearce et al. holds that the content of the prompt and of the file measurably changes whether the output is vulnerable. Its diversity-of-prompt experiment mutates one SQL-injection scenario (CWE-89) in 16 ways on the August 2021 Copilot technical preview. The authors report that most mutations moved results little. Even so, changes with no semantic meaning, such as rewording a comment, could change whether the top suggestion was vulnerable (p. 11). The largest effect came from code already in the file. Adding a non-vulnerable SQL function gave **0 of 18** valid options vulnerable, and adding a vulnerable one gave **17 of 18** (p. 10). From this the authors hypothesise that existing vulnerable or non-vulnerable SQL in the codebase is the strongest predictor of whether Copilot generates injectable SQL (p. 11). In the weakness-diversity experiment they also report that "best practice" context, such as credentials loaded from environment variables, seems to pull Copilot toward better code (p. 9, p. 13).

Perry et al. reach a related position from a user study of 47 participants, 33 of whom used an assistant built on codex-davinci-002 (p. 3, p. 10). In the prompt log of the assistant group, the paper reports that participants who specified task instructions, function declarations and helper functions generated more secure code (p. 1). It also reports that feeding the assistant's previous output back as the next prompt can magnify or replicate security problems (p. 1, p. 10). Participants who raised the temperature, rephrased and added context tended to end with more secure code, which the authors tentatively link to the participant forming a mental model of the assistant (p. 11). These are associations observed among assistant users. Random assignment in the study was to the assistant and control groups, not to prompting strategies (p. 3). The authors treat the temperature link as possible rather than established (p. 11).

BaxBench (Vero et al.) qualifies the position. It runs 11 LLMs on 392 backend tasks under three prompt conditions: no security instruction, a generic reminder to follow security best practices, and an oracle reminder that lists the scenario's CWEs (p. 5, p. 19). The paper finds that generic reminders improve the three reasoning models considerably and give the non-reasoning models no significant improvement (p. 6). The oracle reminder gives the highest sec_pass@1 for every model, but the number of passing programs generally falls (p. 6). The paper reports these prompt results only as charts, without numbers in the main text (p. 6). In its agent experiment (OpenHands with Claude 3.5 Sonnet, 351 tasks), the scaffold brings no security gain under the normal prompt. Under the oracle prompt, sec_pass@1 rises from 35.4 to 39.0 (p. 6). The paper reads these results as models failing on security mainly because they do not attend to it unless told to (p. 7, p. 9). It also reports that OpenAPI specifications give higher pass@1 and sec_pass@1 than plaintext descriptions for the three models it tested (p. 8).

The poster by Ma et al. tests paired prompts. Each risk-inducing prompt has a security-aware counterpart that keeps the functional task fixed, so that only the security information varies (p. 3). The transformation depends on the scenario: general security guidance for ambiguous requirements, explicit environment and security assumptions for under-specified context, and a specification reformulated to align with secure coding for a security–functionality conflict (p. 3). Across eight LLMs and 2,700 test cases, security-aware prompting reduced vulnerability for every model, by 37% (Qwen3-4B) up to 45% (Claude-Sonnet-4) (p. 6). The paper does not state whether these reductions are relative or absolute (pp. 5–6). Under the security–functionality conflict the prompting was least robust: regressions reached 19% and net gain fell to 0.12 (p. 6). The authors summarise that security-aware prompting "can effectively improve code security overall, but may introduce regressions when functional requirements conflict with secure coding practices" (p. 2).

SecureForge (Liu et al. 2026) holds that an optimised system prompt can steer security where plain security requests leave double-digit rates. It builds a corpus of benign prompts that elicited Semgrep findings, and uses the GEPA optimiser to search for the single system prompt that minimises aggregate failure probability across CWEs (p. 5, pp. 6–7). The paper reports that the optimised prompt reduced weakness rates by up to **48%** with test passage essentially unchanged (p. 1, p. 8); the text does not tie the "up to 48%" to a named model or table value. For four GPT models, the share vulnerable among test-passing outputs fell from 14.7–22.1% under a security-aware prompt to 9.0–15.6% (p. 14). The prompt, optimised on synthetic CWE scenarios, improved the joint security-and-test rate by up to 13.5% on 203 real SWE-chat tasks (p. 3, p. 8). The same paper reports that security-aware and CWE-aware prompting alone left vulnerability rates above 13% among test-passing outputs (p. 7, p. 9), and states that a prompt optimised for one model may not secure another (p. 9). Its results cover single-turn Python generation (pp. 9–10).

CWEval (Peng et al. 2025) qualifies the position. It adds the single sentence "Your code should be secure and should NOT contain any vulnerability" to the prompt, with no CWE-specific hints (p. 7). The paper reports that this raises func-sec@k for almost all models, with a possible slight decrease in func@k (p. 6, p. 7). The largest gain is for Claude 3.5 Haiku, up to 9.8% on func-sec@10 (56.48 to 66.28), while Gemini 1.5 Flash moves from 47.81 to 48.97 (p. 7). The func@1 of Llama 3.1 70B falls from 71.84 to 65.79 with the instruction (p. 7). The authors note that the experiment tries only the simplest instruction (p. 7).

### Security hints give marginal gains

The SUSVIBES paper (Zhao et al.) holds that explicit security instructions raise security only slightly and cost functional correctness. Its mitigation experiment uses one setting, SWE-Agent with Claude 4 Sonnet, on 186 repository-level Python tasks. All runs receive a generic security reminder, and two CWE-based strategies are compared against that baseline. In self-selection the agent picks relevant CWEs from the full list before coding; in the oracle condition it is given the true CWE (p. 8). SecPass rises from 11.8% to **14.5%** with self-selection and to **15.1%** with the oracle. FuncPass falls from 57.0% to 50.0% and to 55.4% (p. 8). The authors hypothesise two opposing trends: better awareness of risk, and an over-focus on security that drops functional requirements (p. 8). They report that self-selection is about as secure as the oracle hint, and suggest this may come from a better understanding of the task context (p. 8, p. 9). They state that the mitigation prompts were kept simple on purpose and that prompt engineering for security was not optimised (p. 19).

The Broken by Default study (Blain and Noiseux) reports that a security-explicit system prompt lowered the mean vulnerability rate on its 50-prompt v1 corpus from 64.8% to 60.8%, a drop of **4 points**, with memory-allocation vulnerabilities essentially unchanged (p. 4). By model, the rate moved from 66% to 54% for Mistral Large, from 66% to 58% for GPT-4o and from 64% to 62% for Claude 3.5 Sonnet, stayed at 60% for Gemini 2.5 Flash, and rose from 68% to 70% for Llama 3.3 70B (p. 5). The authors write that "A mean improvement of 4 percentage points under an explicit security prompt is not a safety margin—it is noise" (p. 6), and read the result as security instructions not overriding low-level patterns learned from training data (p. 4, p. 6). They acknowledge that the ablation ran on the 50-prompt corpus only and that the Llama increase may be within noise (p. 7). Vulnerabilities are identified by the authors' own COBALT engine (p. 1, p. 3).

RealSec-bench (Wang et al.) tests a five-directive security guideline derived from OWASP and three retrieval-augmented generation (RAG) variants on 105 repository-level Java tasks (p. 4, p. 5, p. 12). The guideline moved average SecurePass@1 from 5.14% to 5.71% and average Pass@1 from 12.95% to 12.38% (p. 16). It helped Deepseek-V3 and GPT-4.1 and hurt Claude-3.7-Sonnet, whose Pass@1 fell from 16.2% to 9.5% (p. 7, p. 14), and the authors conclude that prompt-based security engineering is not universally effective (p. 7). RAG raised average Pass@1 from 12.95% to as much as 19.05% with BM25, while average SecurePass@1 ranged from 4.76% to 6.28% across the three retrievers (p. 16). The paper states that RAG "offers no substantial improvement in security" (p. 7). Combining RAG with the guideline gave an average SecurePass@1 of 4.38% (p. 16). Security is scored by CodeQL with multi-LLM adjudication of its alerts (p. 5). The appendix text gives per-model guideline figures that do not match the paper's table (p. 14, p. 16).

The metamorphic-testing study by Peng, Wang and Zhu does not intervene on prompts. Across 148 LLMSecEval prompts, it correlates prompt features with the number of distinct metamorphic relations violated in the generated code (p. 2, p. 4). It finds that security-aware keywords in the prompt, such as "secure", "sanitize" or "validate", show no relationship with output safety (r = -0.04), and words this as "explicitly requesting secure code does not improve output safety" (p. 4). The evidence is a correlation across existing benchmark prompts, scored by an LLM judge (p. 2, p. 4).

## Why they differ

The sources vary different inputs. Pearce mutates comments and surrounding code in one completion scenario. Perry observes the prompting strategies users chose for themselves. BaxBench and Zhao add explicit security instructions to a task specification. They also measure security differently. Pearce checks a single targeted CWE with CodeQL or manual marking and does not assess functional correctness (p. 4, p. 5). BaxBench runs exploits against functionally correct backends (p. 24). Zhao runs security tests taken from fix commits against repository patches (p. 6). Each source limits its own evidence. Pearce states that its sample sizes may not support statistical conclusions (p. 13). Perry's prompt findings are associations among the assistant users of a 47-participant study whose authors call their sample small (p. 1, p. 12). BaxBench finds that generic reminders help only its reasoning models, and that the oracle prompt cuts the number of passing programs (p. 6). Zhao tests one model-framework pair with mitigation prompts it says were kept simple on purpose (p. 8, p. 19). The systems also differ. Pearce uses the 2021 Copilot technical preview (p. 3), Perry uses codex-davinci-002 (p. 10), BaxBench uses 11 LLMs (p. 5), and Zhao uses one agent-model pair from its 2026 cohort (p. 8).

## Stances

- [[asleep-at-the-keyboard-copilot-security-2021-pearce]] · Prompt and context steer security · supports · (p. 11)
- [[do-users-write-more-insecure-code-2023-perry]] · Prompt and context steer security · supports · (p. 1)
- [[baxbench-correct-secure-backends-2025-vero]] · Prompt and context steer security · qualifies · (p. 6)
- [[is-vibe-coding-safe-2026-zhao]] · Security hints give marginal gains · supports · (p. 8)
- [[rethinking-security-llm-code-2026-ma]] · Prompt and context steer security · supports · (p. 6)
- [[secureforge-prompt-optimization-llm-code-2026-liu]] · Prompt and context steer security · supports · (p. 1, p. 8)
- [[cweval-outcome-driven-evaluation-2025-peng]] · Prompt and context steer security · qualifies · (p. 6, p. 7)
- [[broken-by-default-formal-verification-2026-blain]] · Security hints give marginal gains · supports · (p. 4)
- [[realsec-bench-secure-code-generation-2026-wang]] · Security hints give marginal gains · supports · (p. 7)
- [[cross-cutting-security-analysis-llm-code-2026-peng]] · Security hints give marginal gains · supports · (p. 4)

## Reading
