---
type: debate
question: Does feeding detector feedback back to the model remove the vulnerabilities in its code?
sources:
  - "[[assessing-quality-code-generation-chatgpt-2024-liu]]"
  - "[[ai-generated-code-considered-harmful-2024-chong]]"
  - "[[secure-code-generation-reflexion-2025-datta]]"
written_by: claude-opus-5-5
reviewed_by:
tags:
  - topic/ai-code-security
  - topic/vulnerability-repair
---

## Question

The question is whether a model that is shown what a vulnerability detector found in its own generated code, and asked to revise it, removes those vulnerabilities, and at what cost in new ones. The sources contest it for single-model repair loops on generated code in 2024–2025: GPT-3.5 given CodeQL's CWE messages, GPT-4o given Clang-detected issue categories on C code, and five open code models given the findings of the Insecure Code Detector (ICD) over three reflexion rounds. In all three the feedback comes from a static detector, and the sources report removal in the terms of that detector's findings.

## Positions

### Feedback repair removes most flagged flaws

Liu et al. test multi-round fixing on ChatGPT (gpt-3.5-turbo-0301), feeding CodeQL's messages back as the next prompt for at most five rounds (p. 4, p. 10). On the CWE scenarios taken from Pearce et al., the paper reports that this fixed 143 of 160 sampled vulnerable snippets, **89.4%** (p. 25, p. 27). On code generated for LeetCode problems in C, C++ and Java, with 15 snippets sampled per CodeQL query, fixing succeeded for all sampled snippets (p. 22, p. 25, p. 27). Fixing was weak for the Input Validation and Information Leakage groups (p. 25, p. 26). The paper takes these results to suggest that combining ChatGPT with vulnerability detection tools can mitigate vulnerabilities in the generated code (p. 25, p. 27). It acknowledges that CodeQL may report secure code as vulnerable (p. 32). Its non-determinism study finds that temperature 0 made one-round generation consistent across trials but not multi-round fixing (p. 27, p. 29).

### Feedback repair is partial and can regress

Chong et al. run three feedback loops on 60 of GPT-4o's C solutions to LeetCode problems, 30 with Clang-reported issues and 30 without, one loop per issue category: malloc overflow, array index out of bounds and null dereference (p. 9). Each loop adds to the original prompt an instruction not to have the named issue (p. 9, p. 10, p. 11). On the files with issues, the total fell from 58 to 44: malloc overflow from 40 to 24 and null dereference from 3 to 2, while array-index-out-of-bounds issues rose from 15 to 18 (p. 10, p. 11). On the files without issues, the regenerated code had 4 malloc overflows where there had been none (p. 10, p. 12). The authors conclude that the LLM "so far is not capable of consistently removing security issues even though the prompt has explicitly asked it to do so" (p. 11). The study uses one model, GPT-4o, and small independent tasks, which the authors contrast with large software projects (p. 13).

Datta, Aljohani and Do qualify the position. They run a three-round reflexion loop with five open code models on the 1,404 prompts of Instruct Prime, in eight languages (p. 3). Each round gives the model the task, a buffer of all prior attempts with the CWEs flagged by ICD, and an instruction to revise minimally while preserving functionality (p. 4). Averaged over models, secure-generation accuracy rises from **70.74%** at the zero-shot baseline to **79.43%** after three rounds, by +6.00 pp in round one, +1.66 in round two and +1.03 in round three (p. 7). Every model improves, QwenCoder most (+11.61 pp) and OpenCoder least (+4.21 pp) (p. 7), and accuracy after three rounds ranges from 72.51% (OpenCoder) to 84.47% (QwenCoder) (p. 6). Regressions, outputs going from secure to insecure, rise to about 1–2% in later rounds (p. 7, p. 8). The authors conclude that "one or two reflexion rounds capture most of the improvement, while additional iterations provide diminishing returns and occasionally undo earlier repairs" (p. 7). The same detector, ICD, supplies the feedback and scores each output (p. 3, p. 4), and the authors acknowledge that ICD is static and can miss context or give false positives (p. 8).

## Why they differ

The feedback differs. Liu feeds back CodeQL's CWE messages (p. 4, p. 10), Chong names a Clang issue category in the prompt (p. 9), and Datta passes the CWEs ICD flagged together with a buffer of all prior attempts (p. 4). The models differ: GPT-3.5 (Liu, p. 4), GPT-4o (Chong, p. 13) and five open code models (Datta, p. 3). So do the languages: C and Python scenarios plus C, C++ and Java LeetCode code (Liu, p. 22), C only (Chong, p. 2), and eight languages (Datta, p. 3). The samples differ in size and selection: 160 sampled vulnerable snippets and 15 per LeetCode query (Liu, p. 22, p. 25), 60 files of which half had no issues (Chong, p. 9), and the full 1,404-prompt benchmark (Datta, p. 3). What is counted also differs. Liu counts sampled vulnerable snippets that were fixed (p. 25). Chong counts issue totals, including in files that had none, so newly introduced issues are visible (p. 11, p. 12). Datta counts repairs and regressions between rounds as shares of all prompts (p. 4), and uses the same detector for feedback and scoring (p. 3, p. 4).

## Stances

- [[assessing-quality-code-generation-chatgpt-2024-liu]] · Feedback repair removes most flagged flaws · supports · (p. 25, p. 27)
- [[ai-generated-code-considered-harmful-2024-chong]] · Feedback repair is partial and can regress · supports · (p. 10, p. 11, p. 12)
- [[secure-code-generation-reflexion-2025-datta]] · Feedback repair is partial and can regress · qualifies · (p. 7, p. 8)

## Reading
