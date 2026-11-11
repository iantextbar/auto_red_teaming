# Taxonomy

The controlled tag vocabulary of the vault. Only contributors declare tags here (CLAUDE.md §4.9). Claude applies tags that already exist and proposes new ones in conversation, as a line in the format below, ready to paste.

Line format: `- #facet/name — what the tag covers`. Names are English, lowercase, hyphenated.

## Topic

What the source is about. Applied by Claude (factual facet).

- #topic/ai-code-security — vulnerabilities in code written by or with AI models, assistants or agents
- #topic/coding-agents — autonomous or repository-level coding agents, as opposed to completion assistants
- #topic/vibe-coding — building software mainly by prompting, with little reading of the generated code
- #topic/developer-behaviour — how developers use, trust and review AI output, and what that does to security
- #topic/package-hallucination — models suggesting dependencies that do not exist, and the slopsquatting attacks this enables
- #topic/supply-chain-security — attacks through dependencies, package registries and build pipelines
- #topic/vulnerability-detection — finding vulnerabilities automatically: static analysis, LLM-based review, fuzzing
- #topic/automated-red-teaming — automated or agent-driven adversarial probing of software or models for exploitable flaws
- #topic/offensive-ai-capabilities — AI agents reproducing, discovering or exploiting vulnerabilities
- #topic/vulnerability-repair — automatic fixing of detected vulnerabilities
- #topic/security-benchmarks — benchmarks and datasets that measure code security or agents' security capabilities
- #topic/secure-coding-standards — CWE, OWASP, CERT and similar taxonomies and guidelines
- #topic/compliance-checking — checking code against standards, regulation or organisational policy

## Method

How the source supports what it claims. Applied by Claude (factual facet).

- #method/benchmark-evaluation — builds or uses a fixed task set and scores models or agents on it
- #method/user-study — controlled experiment with human participants
- #method/static-analysis-scoring — generated code scored by static analysers (e.g. CodeQL)
- #method/execution-based-evaluation — generated code run against functional tests and exploits
- #method/replication — re-runs a published study on new models or a new cohort
- #method/system-proposal — proposes a tool or technique and evaluates it
- #method/literature-review — survey or systematic review of other work

## Source

What kind of publication the source is; mirrors the `source_type` field. Applied by Claude (factual facet).

## Evidence

What the evidence is worth. Judgement: applied by contributors only.

## State

Reading and review state. Who applies it is not yet settled in CLAUDE.md §7.
