---
type: source
title: "Asleep at the Keyboard? Assessing the Security of GitHub Copilot's Code Contributions"
authors: [Hammond Pearce, Baleegh Ahmad, Benjamin Tan, Brendan Dolan-Gavitt, Ramesh Karri]
year: 2021
venue: arXiv
source_type: preprint
interest: independent
doi:
url: https://arxiv.org/abs/2108.09293v3
pdf: "[[references/pdfs/sprint1/asleep_on_keyboard.pdf]]"
snapshot:
status: summarised
summarised_by: claude-sonnet-5-5
reviewed_by:
tags:
  - topic/ai-code-security
  - topic/secure-coding-standards
  - method/static-analysis-scoring
---

## Stated by the source

### What it is about

The paper asks whether the code suggested by GitHub Copilot, in its August 2021 technical preview, tends to be insecure, how often, and which features of the context make it more or less so (p. 1). It targets developers using AI pair programmers, especially security novices, and the designers of such tools. The object is Copilot's default behaviour on small, hand-built completion scenarios in Python, C and Verilog, scored against MITRE's Common Weakness Enumeration (CWE) (p. 1, p. 4).

### Argument

The paper starts from a premise about how the tool works. Copilot is built on Codex, a GPT-3 model fine-tuned on GitHub code, and it returns the most likely completion for its context, not the best one by any metric such as performance or security (p. 2). Because that training code includes insecure patterns, the authors expect the model to reproduce them, and they note that earlier work on Codex looked at only one weakness type (insecure crypto parameters) and asked for a larger study (p. 1, p. 2).

The method turns this into a measurement. The authors write incomplete program snippets, called **CWE scenarios**, in which a naive functional completion could contain a given weakness. They ask Copilot for up to 25 options per scenario, assemble each option into a program, and test it for the one targeted CWE with CodeQL or, where that cannot be done, by manual inspection (p. 4, p. 5). The classification is deliberately conservative: an option counts as vulnerable only if it definitively contains vulnerable code. Partial completions and calls to undefined helper functions are scored non-vulnerable, functional correctness is not assessed, and exploitability is not considered (p. 4, p. 5).

Three axes of diversity structure the experiments (p. 5). **Diversity of weakness** (DOW) covers three scenarios for each of 18 CWEs from the 2021 MITRE Top 25. The result is mixed. Cross-site scripting, missing authentication and permission assignment were mostly handled safely, while path traversal, NULL pointer dereference, OS command injection and password storage were mostly vulnerable (p. 7, p. 8, p. 9). The authors link the differences to what public code usually looks like: for instance, "best practice" context such as credentials loaded from environment variables seems to pull Copilot toward better code, and legacy code keeps teaching obsolete practices such as MD5 hashing (p. 9, p. 13). In several scenarios the highest-confidence suggestion was the vulnerable one (p. 9).

**Diversity of prompt** (DOP) fixes one scenario, SQL injection (CWE-89), and mutates it in 16 ways: meta-information (author flag, tabs, misspellings), comment wording, and code context (p. 9, p. 10). Most mutations moved results little. Changes that carry no semantic content, such as rewording a comment, could still flip the top suggestion from safe to vulnerable (p. 11). The strongest effect came from the code already in the file: a non-vulnerable SQL function above the task removed vulnerable suggestions, and a vulnerable one pushed nearly all suggestions to vulnerable (p. 11). The authors hypothesise that the presence of vulnerable or safe SQL in the codebase is the strongest predictor of what Copilot generates next (p. 11).

**Diversity of domain** (DOD) moves to Verilog hardware CWEs, a less common domain, with six hardware CWEs chosen because they could be marked manually (p. 11). Copilot often failed to produce syntactically valid Verilog, mixing in SystemVerilog and confusing wire and reg, which the authors attribute to less training data (p. 13). Among the programs it did produce, the fraction vulnerable was lower than in software (p. 11, p. 13).

The paper concludes that the response is mixed, with about 40% of options vulnerable across all axes, and that top-ranked suggestions matter because novices may accept the "best" one (p. 13). It states that Copilot will raise productivity but that developers should stay vigilant and pair it with security-aware tooling at training and generation time (p. 14).

### Interlocutors

- Chen et al. 2021 (Codex technical report): describes the model family behind Copilot; the paper takes its architecture and its Appendix G.3 on insecure crypto parameters, and extends it to the Top 25 weaknesses. Role: foundation and counterpoint (p. 2).
- MITRE CWE and the 2021 CWE Top 25: supply the taxonomy of weaknesses and the choice of what to test, including the hardware CWE view of 2020. Role: foundation (p. 1, p. 2, p. 11).
- GitHub CodeQL: the main automated detector, run with the python-security-and-quality suite of 153 security properties. Role: data source and instrument (p. 4).
- GitHub's Copilot documentation: warns that Copilot output should be used with tests, security tools and judgement, and discloses training on public code with insecure patterns. Role: target of the paper's check (p. 1).
- Austin et al. 2021 and Chen et al. 2021: prior evaluations of generated code for functional correctness. Role: counterpoint, since the paper holds there is no systematic examination of security (p. 1, p. 2).

### Methodology

This is an empirical, scenario-based evaluation of a closed black-box tool, run through its editor interface in default settings, with the temperature and other generation parameters left at their secret defaults (p. 4). Scenarios came from the CodeQL repository, MITRE's examples, or were written by the authors, and Copilot was asked for 25 options per scenario (p. 4). Options that did not compile were dropped, except those fixable by a trivial edit such as one brace, which a regex tool fixed (p. 4). Detection used CodeQL configured for the single targeted CWE, with manual marking for cases CodeQL could not handle and for Verilog (p. 5, p. 13). The scripts and dataset are released (p. 5, p. 15).

### Empirical base

89 scenarios and 1,689 valid programs in total (p. 1). DOW: 54 scenarios, 18 CWEs, 1,084 valid programs (p. 5). DOP: 17 scenarios, 407 programs (p. 10). DOD: 18 scenarios, 198 programs (p. 11). Copilot technical preview, August 2021, with CodeQL 2.5.7, Python 3.8.10 and gcc 9.3.0 (p. 3, p. 5).

### Findings

- Across DOW, 44.00% of valid programs were vulnerable and 44.44% of scenarios had a vulnerable top-scoring suggestion; the rate was 50.29% in C and 38.35% in Python (p. 5).
- Per-CWE variation was wide: CWE-79 had no vulnerable top suggestion and 19% vulnerable options, while CWE-22 had only vulnerable top suggestions and 60% vulnerable options (p. 9).
- Three scenarios had a very high-confidence vulnerable top option: 476-1 (0.96), 200-0 (0.93) and 416-2 (0.92) (p. 9).
- In DOP, 37.35% of programs were vulnerable and scores stayed close to the control except when a safe or vulnerable SQL function was added to the file (p. 10, p. 11).
- In DOD, 28.28% of the programs were vulnerable, and Copilot struggled to produce valid Verilog (p. 11, p. 13).
- Overall, 39.33% of top options and 40.73% of all options were vulnerable (p. 13).

### What the source offers

- A released dataset of 89 security-relevant completion scenarios and the framework to run them, with all generated options archived (p. 5, p. 14, p. 15).
- An operational definition of "vulnerable" for generated snippets: a binary, single-CWE, conservative classification without exploitability or functional correctness (p. 4, p. 5).
- A snapshot of Copilot's 2021 behaviour per CWE, usable as a baseline for later model versions.

### Stated gaps and limitations

The authors acknowledge that CodeQL cannot reason about memory buffer sizes and that some CWEs need information beyond the file, that it may have marked some safe code vulnerable, and that manual marking is debatable (p. 13). Sample sizes per scenario may not support statistical conclusions, because queries were manual and rate-limited and the "mean prob" score has no formal definition (p. 13). Outputs are not reproducible because the model is closed and may be retrained (p. 13, p. 14). The scenarios are artificial and real code is messier, and the authors do not draw conclusions about the security of GitHub code in general (p. 13, p. 14). Weaknesses needing context outside a single file, and seven Top 25 CWEs, were left out (p. 3, p. 5, p. 15).

### Key claims

- Across 89 scenarios and 1,689 programs, approximately 40% of Copilot's generated programs were vulnerable (p. 1).
- In the weakness-diversity experiment, 44.00% of 1,084 valid programs contained the targeted CWE, and 24 of 54 scenarios had a vulnerable top-scoring suggestion (p. 5).
- Copilot's vulnerability rate varied strongly by weakness: CWE-79 scenarios had no vulnerable top suggestion, CWE-22 scenarios had only vulnerable ones (p. 9).
- Semantically irrelevant changes to a prompt, such as comment wording, could change whether the top suggestion was vulnerable in the SQL injection scenario (p. 11).
- The authors hypothesise that existing vulnerable or non-vulnerable SQL in the file is the strongest predictor of whether Copilot generates injectable SQL (p. 11).
- The authors theorise that Copilot's uneven security quality comes from the community-provided code it was trained on, and that outdated practices persist in the training set (p. 13).
- In hardware (Verilog) scenarios, 28.28% of 198 valid programs were vulnerable, but Copilot often failed to produce valid Verilog (p. 11, p. 13).
- The authors state that the sample sizes may not support statistical conclusions (p. 13).

## Extracted facts

- Instrument: CodeQL 2.5.7, python-security-and-quality suite, 153 security properties; manual marking where CodeQL could not be used (p. 4, p. 5).
- Setup: up to 25 options requested per scenario; default Copilot parameters; Python, C and Verilog (p. 4).
- Valid programs: syntactically compliant, compilable and unique; Copilot did not always return 25 distinct suggestions (p. 5).
- Scenario sources: CodeQL repository, MITRE examples, authors (p. 4).
- DOW: 54 scenarios over 18 CWEs, 1,084 valid programs, 477 vulnerable (44.00%), 24 vulnerable top-scoring (44.44%) (p. 5).
- DOW by language: C, 25 scenarios, 513 programs, 258 vulnerable (50.29%), 13 top vulnerable (52.00%); Python, 29 scenarios, 571 programs, 219 vulnerable (38.35%), 11 top vulnerable (37.93%) (p. 5, p. 6).
- DOP: 17 scenarios, 407 programs, 152 vulnerable (37.35%); control had 6 of 25 vulnerable and a non-vulnerable top option (p. 10).
- DOP, adding a non-vulnerable SQL function (C-2): 18 valid, 0 vulnerable; adding a vulnerable one (C-3): 18 valid, 17 vulnerable (p. 10).
- DOP, author flag: Andrey Petrov 4 vulnerable of 25; lead author of the paper 11 of 24 (p. 10).
- DOD: six hardware CWEs, 3 scenarios each, 18 scenarios, 198 programs, 56 vulnerable (28.28%), 7 top vulnerable (38.89%); scenario 1254-2 produced no valid program (p. 11, p. 12).
- Overall: 39.33% of top options and 40.73% of all options vulnerable (p. 13).
- CWEs excluded from the Top 25: 352, 287, 862, 276, 611, 918, 77, for reasons of context, architecture or tooling (p. 15).
- Scenarios with the highest mean vulnerable scores: 22-0 (0.83), 125-1 (0.76), 787-0 (0.74) (p. 9).
- Password hashing (CWE-522): Copilot frequently produced MD5 or single-round SHA-256; importing bcrypt improved results but the top suggestion was still vulnerable (p. 9).
- Dataset and code: https://doi.org/10.5281/zenodo.5225650 (p. 15).
- Inconsistencies: the DOP text gives "4 (25.53%)" scenarios with a vulnerable top option out of 17, which is not 25.53% (p. 10). Table III labels two rows D-5, and the text describes D-7 (docstring) where the table has D-6 (p. 10, p. 11). The abstract says approximately 40%; the discussion gives 40.73% of options (p. 1, p. 13).
- The paper does not report a significance test, and says so (p. 13).

## Quotes

- "Of these, we found approximately 40 % to be vulnerable." (p. 1)
- "the model will not necessarily generate the best code (by whatever metric you choose—performance, security, etc.) but rather the one that best matches the code that came before." (p. 2)
- "we mark an option as vulnerable only if it definitively contains vulnerable code." (p. 5)
- "This was the first CWE where the majority of options are vulnerable, suggesting that much of the training data (open source projects) may feature vulnerable system call code." (p. 7)
- "Copilot struggled with all scenarios, with all top suggestions being vulnerable." (p. 8)
- "We hypothesize that the presence of either vulnerable or non-vulnerable SQL in a codebase is therefore the strongest predictor of whether or not there would be other vulnerable SQL in the codebase" (p. 11)
- "small changes in Copilot’s prompt (i.e. scenarios D-1, D-2, and D-3) can impact the safety of the generated code with regard to the top-suggested program option, even when they have no semantic meaning (they are only changes to comments)." (p. 11)
- "Un-maintained and legacy code uses insecure hashes, and so Copilot continues suggesting them." (p. 13)
- "It is difficult to make claims on statistical significance of all our results, but we believe that the empirical findings are nevertheless noteworthy." (p. 13)
- "developers should remain vigilant (‘awake’) when using Copilot as a co-pilot." (p. 14)

## Reading

## Connections

## Disagreements
