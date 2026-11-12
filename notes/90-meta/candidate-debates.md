---
type: candidates
written_by: claude-opus-5-5
reviewed_by:
---

Questions that mapping found contested, or about to be, but with fewer than three sources taking a stance, or with sources that do not yet disagree (CLAUDE.md §3, D27). They stay out of the matrix. One becomes a debate only through a normal propose run.

## Candidates

### Does agent scaffolding improve the security of generated code?

- [[baxbench-correct-secure-backends-2025-vero]]: agent scaffolding (OpenHands, Claude 3.5 Sonnet, 351 tasks) gives notable but not drastic correctness gains and no security gain without the oracle prompt (p. 6)
- [[is-vibe-coding-safe-2026-zhao]]: on the common functional subset, the secure share differs by framework, SWE-Agent 23.3%, OpenHands 20.1%, Claude Code 17.4% (p. 6)
- [[is-vibe-coding-safe-2026-zhao]]: different models and frameworks avoid different CWE categories, so their strengths are complementary (p. 6)

Needs a third source that compares security with and without a scaffold, or across scaffolds.

### Do developers write less secure code with an AI assistant than without one?

- [[do-users-write-more-insecure-code-2023-perry]]: participants with access to an AI assistant wrote significantly less secure code than those without, in a study of 47 participants on security tasks (p. 1)
- [[do-users-write-more-insecure-code-2023-perry]]: assistant users were less secure on four of the five analysed tasks, and results on the C task were mixed (p. 5, p. 7)

Needs two more sources comparing developers with and without an assistant, user studies or field data.

### Do security rankings of models match their functional rankings?

- [[baxbench-correct-secure-backends-2025-vero]]: the model best at correctness (o1) is not best at security; three models exceed it in sec_pass@1 (p. 6)
- [[is-vibe-coding-safe-2026-zhao]]: Gemini 2.5 Pro is the most secure model on the common functional subset (30.4%), although Claude 4 Sonnet has the higher FuncPass (p. 6)

Both sources say the rankings differ. Needs a third source, and a source that finds the rankings align, before the question is contested.

### Do newer model generations make fewer security failures?

- [[range-shrinks-threat-remains-2026-churilov]]: the inter-model range of package-hallucination rates across five 2026 frontier models is 4.62%–6.10%, against 5.2%–21.7% in Spracklen's 2024 cohort (p. 1, p. 4)
- [[range-shrinks-threat-remains-2026-churilov]]: the compression holds for the five sampled frontier models; smaller open-weight models may still show Spracklen-like rates (p. 8)
- [[is-vibe-coding-safe-2026-zhao]]: Gemini 3 Pro improves FuncPass by more than 2x over Gemini 2.5 Pro on SWE-Agent but SecPass⊥FuncPass only by 1.3x (p. 6, p. 7)

Needs a third source that compares model generations on the same security measure.

### Can static analysis serve as the security oracle for generated code?

- [[baxbench-correct-secure-backends-2025-vero]]: Snyk Code missed 64 vulnerable programs exploited by the benchmark's tests on o1 outputs (n = 237) (p. 8)
- [[asleep-at-the-keyboard-copilot-security-2021-pearce]]: CodeQL is the main automated detector, with manual marking where it could not be used (p. 4, p. 5)
- [[asleep-at-the-keyboard-copilot-security-2021-pearce]]: the authors acknowledge that CodeQL cannot reason about memory buffer sizes, that some CWEs need information beyond the file, and that it may have marked some safe code vulnerable (p. 13)

Needs a third source, ideally one that measures a static analyser's recall or precision on generated code.

### Is generated code less secure in less common languages or frameworks?

- [[baxbench-correct-secure-backends-2025-vero]]: models perform worse, and their correct solutions are more often vulnerable, on less popular or complex frameworks such as Rust-Actix and PHP-Lumen (p. 6)
- [[asleep-at-the-keyboard-copilot-security-2021-pearce]]: in hardware (Verilog) scenarios, 28.28% of 198 valid programs were vulnerable, but Copilot often failed to produce valid Verilog (p. 11, p. 13)

Needs a third source that compares security across languages or frameworks.

### Does training-data contamination bias security benchmark results?

- [[cybergym-evaluating-ai-agents-cybersecurity-2026-wang]]: the paper finds no statistically significant effect of potential data contamination on success rates for the four models tested (p. 8)
- [[baxbench-correct-secure-backends-2025-vero]]: the authors note that public release makes contamination impossible to rule out (p. 9)
- [[range-shrinks-threat-remains-2026-churilov]]: the paper did not collect a held-out subset of post-cutoff prompts to test for training-data leakage (p. 9)

Three sources mention it, but only CyberGym tests it. Needs a second source that tests contamination.

### Why do models emit insecure code?

- [[asleep-at-the-keyboard-copilot-security-2021-pearce]]: the authors theorise that Copilot's uneven security quality comes from the community-provided code it was trained on, and that outdated practices persist in the training set (p. 13)
- [[baxbench-correct-secure-backends-2025-vero]]: models seem to fail mainly by not attending to security unless told to, which the paper reads as a sign that base models may already hold the knowledge and that post-training should make security an explicit objective (p. 7, p. 9)

Both explanations are offered, not tested. Needs a third source, ideally one that tests a cause.
