---
type: source
title: "The Range Shrinks, the Threat Remains: Re-evaluating LLM Package Hallucinations on the 2026 Frontier-Model Cohort"
authors: [Aleksandr Churilov]
year: 2026
venue:
source_type:
interest: independent
doi:
url:
pdf: "[[references/pdfs/sprint1/threat_remains.pdf]]"
snapshot:
status: summarised
summarised_by: claude-sonnet-5-5
reviewed_by:
tags:
  - topic/package-hallucination
  - topic/supply-chain-security
  - method/replication
  - method/benchmark-evaluation
---

## Stated by the source

### What it is about

The paper is a temporal replication of Spracklen et al. (USENIX Security '25) on package hallucination by code-generating LLMs: models that name packages absent from PyPI or npm, which an attacker can then register ("slopsquatting") (p. 1). It re-runs the same prompts and validation lists on five frontier models released between October 2025 and March 2026, and asks whether the phenomenon has moved with the frontier (p. 1). It adds a cross-model analysis of names that all five models invent, and a coordinated disclosure to the registries (p. 1, p. 7). The author is an independent researcher; the audience is security and software-supply-chain researchers.

### Argument

The paper starts from the supply-chain premise. When a developer trusts an LLM's `pip install` or `import` suggestion, an attacker who registered the invented name wins without touching the developer or the provider (p. 1). It adopts Spracklen's six-stage attack chain and an unprivileged adversary whose only capability is registering packages, at zero upload cost (pp. 2–3). Spracklen's 2024 cohort showed 5.2% to 21.7% hallucinated-package rates; the paper's question is whether newer models have closed this (p. 1).

Its first move is replication. Using Spracklen's prompt datasets, master lists and heuristic extractor unchanged, it measures overall rates of 4.62% (Claude Haiku 4.5) to 6.10% (GPT-5.4-mini), an 11-fold narrowing of the spread (p. 1, p. 4). It attributes the compression to three causes: the open-weight/commercial gap closing at the frontier, near-saturated pretraining curation of package references, and converging RLHF recipes (p. 8). These are proposed explanations, not tested ones. It insists the threat persists, since at 4–7% the attack stays economically viable and "the threat is not contingent on high rates" (p. 8).

The second move is the paper's central finding, the **universal-hallucination set**: the intersection of the per-model hallucinated-name sets, after noise filtering. It has 127 names (109 PyPI, 18 npm) (p. 7). Disclosure to PyPI Security and Socket.dev narrowed this to 53 registrable names (41 PyPI, 12 npm), because prohibited-name rules and existing or scope-controlled registrations remove the rest (p. 7). The paper argues that one registration of such a name reaches users of all five providers, so per-model attack cost does not scale with model count. Single-model studies therefore understate the attack surface, and cross-cohort intersection should be a standard reported quantity (pp. 7–8). It suggests two mechanisms for convergence: shared training-data substrings (such as `rest_framework` versus `djangorestframework`) and overgeneralised npm namespace conventions (p. 8).

Further observations follow. Python rates exceed JavaScript rates for every model, inverting Spracklen's finding, and the paper speculates this reflects Python's looser naming conventions (p. 5, p. 8). Claude Haiku 4.5 hallucinates less than Claude Sonnet 4.6, against the expectation that smaller models hallucinate more, and the paper offers thinking-mode and post-training explanations it cannot disentangle (p. 6). Synthetic prompts yield higher rates than Stack Overflow prompts, so curated-corpus rates are read as lower bounds (p. 5, p. 8). It closes by restricting its own scope: the compression is conditional on the five-model selection and says nothing about smaller open-weight tiers (p. 8).

### Interlocutors

- Spracklen et al. 2025: the baseline whose method, prompts, master lists and extractor are re-used verbatim; foundation and comparison target (p. 2).
- Krishna et al. 2025 (Importing Phantoms): a contemporaneous measurement reporting comparable rates; counterpoint or concurrent work (p. 2).
- Pearce et al. 2022 (Asleep at the Keyboard): cited as the underlying pattern of vulnerable code generation by Copilot; foundation (p. 2).
- Neupane et al. 2023 and Birsan 2021: typosquatting and dependency-confusion work from which slopsquatting is distinguished; foundation (p. 2).
- Aboukhadijeh 2025 (Socket blog): source of the term slopsquatting and of industry monitoring consistent with the compression (p. 2).

### Methodology

The study is an empirical replication. Each model is queried once per prompt with default settings, except GPT-5.4-mini at `reasoning_effort=minimal` (p. 4). A regex extractor pulls install and import references; a name counts as hallucinated if it is absent from Spracklen's PyPI or npm master lists and from the known-false-positive list, after a noise filter (p. 4). Rates are hallucinated references over extracted references with 95% Wilson intervals, pairwise Pearson chi-squared tests with Holm–Bonferroni correction, a permutation-test robustness check, and Jaccard overlap of unique names (p. 4). The registrable subset comes from two different assessments: PyPI's automated rules and Socket.dev's manual review (p. 9).

### Empirical base

- Five models: Claude Sonnet 4.6, Claude Haiku 4.5, GPT-5.4-mini, Gemini 2.5 Pro, DeepSeek V3.2 (p. 3).
- 199,845 generations, about 39,969 per model, on Spracklen's 20,163 Stack Overflow and 19,806 LLM-synthesised prompts, split evenly between Python and JavaScript (pp. 3–4).
- Run between April 22 and 28, 2026; validation date April 28, 2026 (p. 4, p. 9).

### Findings

- Overall rates range from 4.62% (Haiku 4.5) to 6.10% (GPT-5.4-mini); five of ten pairs differ significantly after correction (p. 4, p. 5).
- Python rates exceed JavaScript rates for all five models, by +2.73 to +4.13 percentage points (p. 5).
- The universal set has 127 names, of which 53 are registrable (p. 7).
- Mean pairwise Jaccard is 0.222, highest for DeepSeek V3.2 and GPT-5.4-mini (0.343) and lowest for Sonnet 4.6 and Haiku 4.5 (0.179) (p. 6).
- Eight of the top-10 Python hallucinations per model are within edit distance 2 of an existing PyPI package (p. 7).

### What the source offers

- A 2026 comparison point for the Spracklen 2024 baseline, on the identical prompt corpus.
- A definition of the universal-hallucination set and the 127-to-53 registrability figures, with the registries' filtering criteria.
- A reproducible artifact (code, validation logs, analysis scripts) on Zenodo, with the raw response database under verified-researcher access (p. 2, p. 10).
- An API cost figure for a comparable sweep: $860.90 (p. 3, p. 12).

### Stated gaps and limitations

The paper lists eight limitations (p. 9). The ones it presses hardest are:

- Possible training-data leakage of the January 2025 Spracklen corpus, which would bias rates downward; no held-out post-cutoff prompt subset was collected.
- Asymmetric denominators from refusal rates (1.27% to 32.14%), especially for GPT-5.4-mini at minimal reasoning effort.
- DeepSeek's unpinned alias, whose metadata returned `deepseek-v4-flash` in the same window.
- No agentic configurations, where retrieval might eliminate hallucinations.
- Validation against the older Spracklen master lists rather than an April 2026 registry snapshot (p. 10).
- The 53-name figure is a point-in-time estimate (p. 9).

### Key claims

- The inter-model range of package-hallucination rates across five 2026 frontier models is 4.62%–6.10%, against 5.2%–21.7% in Spracklen's 2024 cohort (p. 1, p. 4).
- Five of the ten pairwise model differences are significant after Holm–Bonferroni correction; the paper describes the four non-Haiku models as a statistically indistinguishable cluster between 5.4% and 6.1%, although its Table 3 also marks Sonnet 4.6 vs GPT-5.4-mini as significant (p. 4, p. 6).
- Python hallucination rates exceed JavaScript rates for all five models, inverting Spracklen's 2024 pattern (p. 5).
- Claude Haiku 4.5 (4.62%) hallucinates significantly less than Claude Sonnet 4.6 (5.41%); the paper cannot separate thinking mode from post-training as the cause (p. 6).
- 127 package names are invented identically by all five models, of which 53 remain registrable after PyPI and Socket.dev review (p. 7).
- Because one registration can target users of all five providers, the paper argues single-model measurements understate the slopsquatting attack surface (p. 3, p. 8).
- The paper suggests, without testing, that shared training-data substrings and namespace-convention overgeneralisation make names universal (p. 8).
- The compression holds for the five sampled frontier models; smaller open-weight models may still show Spracklen-like rates (p. 8).

## Extracted facts

- Hallucination rate is defined as hallucinated references over all extracted package references, computed over valid and hallucinated generations only; refusals are reported separately (p. 4).
- A generation counts as refused if it was declined or returned a degenerate output (length below 20 characters, plus manual sampling) (p. 4).
- Overall and per-language rates in percent, as Python / JavaScript / overall (p. 5):
  - Haiku 4.5: 5.49 / 2.76 / 4.62
  - Sonnet 4.6: 6.63 / 2.62 / 5.41
  - Gemini 2.5 Pro: 6.75 / 3.61 / 5.80
  - DeepSeek V3.2: 6.69 / 3.78 / 5.89
  - GPT-5.4-mini: 7.27 / 3.14 / 6.10
- Refusal rates: Sonnet 4.6 18.79%, Haiku 4.5 1.27%, GPT-5.4-mini 32.14%, Gemini 2.5 Pro 8.14%, DeepSeek V3.2 2.08% (p. 3).
- Largest pair: Haiku 4.5 vs GPT-5.4-mini, Δ = 1.48 pp, χ² = 52.49, Holm-corrected p = 4.32 × 10⁻¹²; smallest non-significant pair DeepSeek V3.2 vs Gemini 2.5 Pro, Δ = 0.08 pp (p. 4).
- Spracklen's best 2024 commercial result is given as 3.6% (GPT-4 Turbo); the paper notes no 2026 model has surpassed it (p. 5).
- Spracklen baseline as described: 16 models, 576,000 generations, 205,474 unique hallucinated names (p. 1, p. 2).
- Master lists: PyPI 500,565 names, npm about 3,000,000 names (p. 4).
- Most frequent universal hallucinations: `aws-cdk` (429), `objc` (375), `opentelemetry` (374), `rest-framework` (315) on PyPI; `@ember/service` (55) and `@ember/object` (53) on npm. All top-10 entries are hallucinated by all five models (p. 7).
- Six of the 18 npm universal names were removed as non-exploitable: four `@ember/*` virtual modules, the published `ssh-keys`, and the security-hold `metro-evaluator` (p. 7). Examples of registrable npm names: `css-color-stop`, `dns-sd`, `dom-ains` (p. 7).
- Disclosure was sent on April 29, 2026 with a window of at least 30 days. The full list was nonetheless publicly accessible in an earlier artifact revision from April 30, 2026 (p. 9, p. 10).
- Spend by provider: Anthropic $375.26 (79,933 generations), OpenAI $93.54, Google $380.99, DeepSeek $11.11; total $860.90 (p. 12).
- Funding: personal accounts plus a one-time Google Cloud credit; no institutional or industry funding; no declared conflicts (p. 10).
- The abstract and §5.4 describe the DeepSeek–GPT-5.4-mini overlap (J = 0.343) as suggestive of shared training-data origins or convergent patterns; §5.4 states it cannot disentangle them, and §6 draws no inference on data-sharing direction (p. 1, p. 6, p. 8).
- Table 4 note on text: the paper says eight per model of the top-10 Python names (40 entries) are within edit distance 2 of an existing package, while the Table 4 "NEAR" flag appears on four of its eight PyPI rows (p. 7).
- Absence: the Haiku/Sonnet explanation relies on Haiku being queried with thinking enabled and Sonnet without; no ablation is run (p. 6).

## Quotes

- "an order-of-magnitude compression of the inter-model spread observed by Spracklen, but not a retirement of the threat" (p. 1)
- "A single registrable PyPI or npm name is therefore not, in general, a single-model attack." (p. 3)
- "We do not have ground truth for the underlying training corpora and cannot disentangle these explanations." (p. 6)
- "The threat is not contingent on high rates." (p. 8)
- "Cross-cohort intersection should be a standard reported quantity, and we publish ours as part of the artifact." (p. 8)
- "the frontier has compressed, not that the threat surface has narrowed at all capability tiers" (p. 8)
- "We did not collect a held-out subset of post-cutoff 2026 prompts to test for training-data leakage" (p. 9)
- "the 53-name figure should be read as a point-in-time estimate of the registrable subset rather than a fixed property of the 127-name set" (p. 9)

## Reading

## Connections

## Disagreements
