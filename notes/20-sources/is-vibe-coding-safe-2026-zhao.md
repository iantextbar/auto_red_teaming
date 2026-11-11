---
type: source
title: "Is Vibe Coding Safe? Benchmarking Vulnerability of Agent-Generated Code in Real-World Tasks"
authors: [Songwen Zhao, Danqing Wang, Kexun Zhang, Jiaxuan Luo, Zhuo Li, Lei Li]
year: 2026
venue: Proceedings of the 43rd International Conference on Machine Learning (PMLR 306, 2026); arXiv:2512.03262v4
source_type: preprint
interest: undetermined
doi:
url: https://arxiv.org/abs/2512.03262
pdf: "[[references/pdfs/sprint1/is_vibe_coding_safe.pdf]]"
snapshot:
status: summarised
summarised_by: claude-sonnet-5-5
reviewed_by:
tags: []
---

## Stated by the source

### What it is about

The paper introduces SUSVIBES, a benchmark of 186 repository-level, security-sensitive feature-request tasks drawn from real open-source Python projects, to test whether code written by coding agents in "vibe coding" is secure as well as functionally correct (p. 1, p. 2). Vibe coding is defined as producing software by describing goals in natural language with minimal review of the generated code (p. 1). The question pursued is whether code that passes functional tests is safe to deploy, and whether simple prompting strategies close the gap (p. 1). The audience is the benchmark and agent-security community, and organisations deploying coding agents (p. 9).

### Argument

The paper starts from a gap in the evaluation landscape. Function-level benchmarks such as HumanEval and MBPP, and the SWE-bench series, measure functionality and ignore implicit security concerns, while vibe coding users usually know which feature they want but not how to avoid security risks (p. 1, p. 2). Earlier security benchmarks work on a single file or function, and the repository-level ones (BaxBench, ASE, SecureAgentBench) cover fewer CWE types and smaller edits (p. 3).

The construction move is to take each feature that a human developer once implemented in a vulnerable way and later patched. The authors mine vulnerability-fix commits, keep the human-written tests the fix added as security tests, take the preceding vulnerable commit and its functional tests, and have an LLM agent mask the feature code and write an issue-style request that omits security considerations (p. 3, p. 4). The agent under test must therefore infer the implicit security need (p. 2). An adaptive verification loop checks that every line of the secure canonical implementation is justified by the request, and enlarges the mask otherwise (p. 4, p. 15).

Two metrics follow. FuncPass is pass@1 on functional tests. SecPass is pass@1 on functional and security tests jointly, because a solution that implements nothing would trivially be secure (p. 6). SecPass⊥FuncPass is the share of secure solutions on the intersection of tasks that all compared settings solve correctly, which separates security from functional ability (p. 6).

The results are that functional success does not carry security. Across three frameworks (SWE-Agent, OpenHands, Claude Code) and four models, average SecPass is around 10%. The best system, SWE-Agent with Claude 4 Sonnet, solves 57.0% of tasks functionally, but 79.3% of those solutions are insecure (p. 6, p. 7). Models and frameworks differ by CWE category and application domain, with complementary strengths (p. 6). Gemini 3 Pro gains more than 2x in FuncPass over Gemini 2.5 Pro on SWE-Agent but only 1.3x on SecPass⊥FuncPass, which the authors read as reasoning-oriented post-training being insufficient for security (p. 6, p. 7). A qualitative case, a Django password check that returns early and so leaks a timing difference between existing and non-existing users, illustrates a vulnerability that functional tests do not catch (p. 7).

The mitigation experiments (SWE-Agent with Claude 4 Sonnet only) add a generic security reminder to all runs, then compare self-selection (the agent picks relevant CWEs from the full list before coding) and oracle (the true CWE is given). Both raise SecPass slightly and lower FuncPass, so the net gain is small (p. 8). The authors hypothesise two opposing trends: better risk awareness, and over-focus on security that drops functional requirements (p. 8). Self-selection performs about as securely as the oracle, which they attribute to a better understanding of the risk in context (p. 9). They conclude that casual adoption of vibe coding in security-sensitive contexts is cautioned against and that better security strategies are needed (p. 9).

### Interlocutors

- Vero et al. 2025 (BaxBench): repository-free backend benchmark with functional tests and exploits; counterpoint, covers 13 CWEs against 79 (p. 3).
- Chen et al. 2025 (SecureAgentBench) and Lian et al. 2025 (ASE): repository-level benchmarks built from vulnerability-fixing commits; closest counterpoints, smaller edits and fewer CWEs (p. 3).
- Jimenez et al. (SWE-bench) and Yang et al. 2024a (SWE-Agent): foundation; the task format and the agent used both for the pipeline and for evaluation (p. 2, p. 4).
- Wang et al. 2024 (ReposVul) and Akhoundali et al. 2024 (MoreFixes): data source for the vulnerability-fix commits (p. 3).
- Pearce et al. 2025 (Asleep at the keyboard): earlier file-level security benchmark, 18 CWEs, no functional evaluation (p. 3).

### Methodology

The source is an empirical benchmark paper. Tasks are built by an automatic pipeline in which SWE-Agent masks the feature, writes the request, verifies it against the secure patch and builds a Docker environment (p. 4, p. 5). Validity is checked by running the commits C0, C−1 and the masked C−1 against the functional and functional-plus-security suites, requiring the masked version to fail both, the vulnerable version to pass only functional tests, and the fixed version to pass both (p. 5). Five software engineering experts then rated the security tests of the 200 surviving tasks and revised those coupled to the reference implementation (p. 19).

Agents run with default system prompts and a 200-step limit, and results are single-attempt pass@1 (p. 6).

### Empirical base

186 tasks from 100 Python GitHub repositories in 10 application domains, covering 79 CWE types (p. 5, p. 13). Evaluation covers 3 agent frameworks x 4 LLMs (12 settings) (p. 6). Mitigation experiments use one setting (p. 7).

### Findings

- Average SecPass is about 10%, against much higher FuncPass (p. 6).
- 79.3% of functionally correct SWE-Agent plus Claude 4 Sonnet solutions, and 77.8% for OpenHands plus Claude 4 Sonnet, are insecure (p. 6).
- Secure share on the common functional subset, by model: Claude 4 Sonnet 18.3%, Kimi K2 22.0%, Gemini 2.5 Pro 30.4%, Gemini 3 Pro 21.4%; by framework: SWE-Agent 23.3%, OpenHands 20.1%, Claude Code 17.4% (p. 6).
- Strengths vary by CWE category and by application domain (p. 6).
- Tasks that need edits in more files are solved less often, functionally and securely (p. 14).
- Self-selection and oracle CWE hints raise SecPass by 2.7 and 3.3 points and lower FuncPass by 7.0 and 1.6 points (p. 8).

### What the source offers

- A repository-level benchmark of 186 tasks with executable environments, human-written functional and security tests, and a public leaderboard (p. 1).
- An automatic, extensible curation pipeline from vulnerability-fix commits to tasks, with prompts in the appendix (p. 5, pp. 15–19).
- The FuncPass, SecPass and SecPass⊥FuncPass metrics (p. 6).
- Worked case studies of functionally correct but vulnerable agent patches (django, buildbot, wagtail, aiohttp-session) (pp. 20–24).

### Stated gaps and limitations

The benchmark emphasises Python and uses test outcomes as a proxy for security. CWE annotations and tests may be insufficient, and the authors do not claim coverage of all exploit modalities (p. 24). Security tests taken from fix commits may be coupled to the reference implementation, so alternative secure implementations can fail them (p. 4). The prompts for the mitigation strategies were kept simple on purpose, and prompt engineering for security was not optimised (p. 19). The authors list property-based and adversarial test synthesis, static analysis, security-aware training rewards and tool use as future work (p. 24).

### Key claims

- Among 12 coding-agent settings on SUSVIBES, all perform poorly on security; average SecPass is only around 10% (p. 6).
- SWE-Agent with Claude 4 Sonnet solves 57.0% of tasks functionally, but only 11.8% are also secure, so 79.3% of its functionally correct solutions are insecure (p. 6, p. 7).
- Rankings by security differ from rankings by function: Gemini 2.5 Pro is the most secure model on the common functional subset (30.4%), although Claude 4 Sonnet has the higher FuncPass (p. 6).
- Different models and frameworks avoid different CWE categories, so their strengths are complementary (p. 6).
- Gemini 3 Pro improves FuncPass by more than 2x over Gemini 2.5 Pro on SWE-Agent but SecPass⊥FuncPass only by 1.3x, which the authors take to show that reasoning-oriented post-training is insufficient for security (p. 6, p. 7).
- Self-selection and oracle CWE prompting raise SecPass only slightly (to 14.5% and 15.1% from 11.8%) and lower FuncPass, on SWE-Agent with Claude 4 Sonnet only (p. 8).
- Self-selection is about as secure as the oracle hint, and the authors suggest this may come from its better understanding of the task context (p. 8, p. 9).
- The authors conclude that the results caution against casual adoption of vibe coding in security-sensitive contexts (p. 9).

## Extracted facts

- Construction: more than 20,000 vulnerability-fix commits from ReposVul and MoreFixes, Python 3.7 or later, only commits that modify tests (p. 3, p. 4). Yield: about 20,000 records, about 2,000 Python, about 450 candidate commits, about 420 after task verification, 200 after environment and execution validation, 186 after human test review (p. 14).
- MoreFixes commits are kept only with a Prospector relevance score of 65 or more (p. 15).
- Task statistics (mean, max): context 236K lines (4,312K), 1,186 files (14,119); target patch 175.0 lines (1,247), 1.8 files (11); security fix 29.9 lines (263), 1.6 files (10); functional tests 66.9 (644), security tests 3.5 (59) (p. 5).
- Files in the target patch: 130 tasks one file, 23 two files, 33 more than two (p. 14).
- CWE labels: 1.08 per task; 91.9% of tasks have one label, 8.1% two; 2.2% are CWE-noinfo or CWE-Other (p. 13).
- Table 3, FuncPass / SecPass (%), SWE-Agent, OpenHands, Claude Code: Claude 4 Sonnet 57.0/11.8, 53.2/11.8, 41.4/5.9; Kimi K2 21.5/5.4, 36.0/9.1, 40.3/8.6; Gemini 2.5 Pro 18.3/6.5, 19.9/8.1, 12.9/3.8; Gemini 3 Pro 37.1/12.9, 50.5/10.8, 34.9/6.5 (p. 7).
- Agent settings: default recommended system prompt per framework, 200 steps maximum, pass@1; Claude 4 Sonnet, Kimi K2, Gemini 2.5 Pro, Gemini 3 Pro as backbones (p. 6).
- Table 5 (SWE-Agent, Claude 4 Sonnet), FuncPass / SecPass: generic 57.0/11.8; self-selection 50.0/14.5; oracle 55.4/15.1 (p. 8).
- Self-selection selects 7.2 CWE types per task on average, against 1.1 ground-truth types; recall 0.571 (incorrect), 0.561 (correct but insecure), 0.667 (correct and secure); precision 0.086, 0.092, 0.114 (p. 8, p. 9).
- Transition generic to self-selection, per cent of all tasks: incorrect to incorrect 38.7, correct-secure to correct-secure 8.1 (Figure 5; the extracted cell layout is not fully legible) (p. 8).
- Tasks by edited files, SWE-Agent with Claude 4 Sonnet: single file 66.9% FuncPass and 15.4% SecPass; two files 39.1% and 4.3%; more than two files 30.3% and 3.0% (p. 14).
- Human review: five software engineering experts reviewed the security tests of 200 tasks; 6.5% were coupled to the ground-truth implementation; 93.5% verify the security property, of which 49.5% fully cover alternative implementations and 44.0% may miss edge cases; 92.1% of the latter could be refined to full coverage (p. 19).
- Environment construction used SWE-Agent with Claude 4 Sonnet and log parsers synthesised by OpenAI o3; the .git history was removed to avoid reward hacking (p. 17, p. 18). The authors report that the building agent sometimes started database containers with overly permissive network exposure (p. 18).
- Intro surveys cited for adoption: 75% of respondents vibe coding, 90% of them satisfied (Perry 2025, The Information) (p. 1).
- Inconsistencies: the main text describes a three-step pipeline (p. 2) and the appendix five stages (p. 14). The introduction says the mitigation strategies "reduce functional correctness by 7 points" (p. 2), but Table 5 gives -7.0 for self-selection and -1.6 for oracle (p. 8).- Absence: the mitigation experiments cover one model-framework pair and no repeated runs or variance are reported for any result.

## Quotes

- "Although 57% of the solutions from SWE-Agent with Claude 4 Sonnet are functionally correct, only 11.8% are secure." (p. 1)
- "The feature description only contains the desired functionality, without implementation details or security guidance." (p. 2)
- "Since one solution can always be secure if it does not implement any meaningful feature, we care only about the security of those functionally correct solutions." (p. 6)
- "This indicates that, if vibe coding users accept the solution after it passes functional tests, around 80% of the time, the solution will leave security vulnerabilities in the repository." (p. 6)
- "This indicates that although current reasoning-oriented post-training can significantly improve functional correctness, it remains insufficient for security." (p. 7)
- "As shown, insecure solutions are more likely to become secure, but correct-and-secure solutions are also more likely to regress to incorrect." (p. 8)
- "We find that 6.5% of the security unit tests are coupled to the ground-truth implementation." (p. 19)
- "SUSVIBES currently emphasizes Python ecosystems and uses test outcomes as a practical proxy for security; however, CWE annotations and tests may be insufficient, and we do not claim coverage of all exploit modalities." (p. 24)

## Reading

## Connections

## Disagreements
