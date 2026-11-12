---
type: source
title: "No Need to Lift a Finger Anymore? Assessing the Quality of Code Generation by ChatGPT"
authors: [Zhijie Liu, Yutian Tang, Xiapu Luo, Yuming Zhou, Liang Feng Zhang]
year: 2024
venue: arXiv (cs.SE)
source_type: preprint
interest: independent
doi:
url: https://arxiv.org/abs/2308.04838v2
pdf: "[[references/pdfs/sprint2/no_need_to_lift_a_finger_anymore.pdf]]"
snapshot:
status: summarised
summarised_by: claude-sonnet-5-5
reviewed_by:
tags: [topic/ai-code-security, topic/vulnerability-repair, method/static-analysis-scoring, method/execution-based-evaluation]
---

## Stated by the source

### What it is about

The paper is an empirical assessment of the quality of code produced by ChatGPT (GPT-3.5, `gpt-3.5-turbo-0301`) along three axes: functional correctness, complexity and security (p. 1, p. 4). It also tests ChatGPT's dialog ability, that is, a multi-round process in which the tool's error or vulnerability feedback is fed back to the model so that it fixes its own code (p. 3). It is addressed to researchers working on LLM-based code generation and asks five research questions: correctness, multi-round fixing, complexity, security and the effect of non-determinism (p. 2).

### Argument

The paper starts from the premise that LLMs are trained on internet data of uncertain quality, so the quality of the code they generate cannot be assumed (p. 2). It aims to simulate real-world use rather than to find the best prompt: the prompt design principle is to give enough information while exploiting dialog ability, and the default temperature of 0.7 is kept (p. 4). Two datasets are used: 728 LeetCode algorithm problems in five languages, split into problems published before and after 2021 because ChatGPT's training data predate 2021 (p. 3, p. 5), and 54 CWE code scenarios, taken from Pearce et al., that are small incomplete C or Python snippets for the model to complete (p. 22).

On correctness, the paper reports a large gap between pre-2021 problems (average Accepted rate 68.41%) and post-2021 problems (20.27%), and attributes it to possible exposure to the training set; it adds that 6 of the sampled easy and medium pre-2021 solutions were Type-2 clones of ground truth solutions (p. 6, p. 8). It then analyses failing code by hand. Wrong-answer code is classified by defect class and by logic cause, namely Wrong Detail (WD), Misunderstanding Certain Content (MCC) and Misunderstanding Problem (MP). Compile and runtime errors are classified from judge messages. Timeouts are classified as Aligned but Inefficient Algorithm Implementation (AIAI), Functionally Correct but Misaligned Algorithm (CMA) and Functionally Incorrect Algorithm (IA) (p. 9, p. 10, p. 15, p. 16). Multi-round fixing repairs few wrong answers (25 of 157 pairs) but most compile and runtime errors, and the paper concludes that ChatGPT lacks grasp of logical details and struggles with problems that need complex reasoning (p. 10, p. 11).

On complexity, measured by cyclomatic and cognitive complexity, the paper finds Python3 code the least complex and C the most, with code complexity rising with problem difficulty in a way comparable to human solutions, and with multi-round fixing preserving or raising complexity levels (p. 17, p. 19, p. 21).

On security, the paper reports two results. For LeetCode-generated C, C++ and Java code, CodeQL flagged 183 vulnerable snippets, 91.8% of them for a missing NULL test after allocation (p. 22). For the CWE scenarios, 33.32% of the valid snippets were vulnerable, 51.64% in C and 17.08% in Python3, with strong variation by CWE and scenario (p. 23, p. 26). Feeding CodeQL's CWE message back to ChatGPT fixed all sampled LeetCode snippets and 143 of 160 CWE snippets, and the paper concludes that pairing ChatGPT with a vulnerability detector can mitigate vulnerabilities in the generated code (p. 22, p. 25, p. 27, p. 29). The final move tests non-determinism: repeating generations ten times shows variation in status, complexity and vulnerabilities at temperature 0.7, while temperature 0 gave identical results for one-round generation but not for multi-round fixing (p. 27, p. 29).

### Interlocutors

- Pearce et al. 2022 (Asleep at the keyboard, on Copilot): source of the CWE scenarios and the experimental setup for security, and the model for generating many samples per scenario (p. 22, p. 33). Role: data source and foundation.
- Fan et al. 2022 and Tan et al. 2017 (CodeFlaws): the defect classification from the repair perspective, reused to classify wrong-answer code (p. 8). Role: foundation.
- Dong et al. 2023 (self-collaboration): the source for setting the maximum round number to 5 (p. 10, p. 32-33). Role: foundation.
- Nguyen and Nadi 2022 (Copilot on 33 LeetCode problems): earlier assessment of generated-code quality (p. 33). Role: counterpoint.
- Liu et al. 2023 (Refining ChatGPT-generated code): code quality issues of ChatGPT in Java and Python, repair with feedback; the paper says it differs by covering five languages, deeper causes, complexity and security (p. 33). Role: counterpoint.

### Methodology

An empirical evaluation. Prompts are built from a four-part template (content, examples, template, command) and sent once per problem and language in a fresh conversation (p. 5, p. 6). Correctness is judged by the LeetCode online judge, with status rates and Wilcoxon rank-sum tests with Cliff's Delta (p. 5). Security is judged by CodeQL, with manual checking by the authors for some scenarios (p. 22). Complexity is measured with SonarQube and cccc (p. 17). Error causes are classified manually by two graduate students, with a senior analyst resolving disagreements (p. 8). Multi-round fixing allows at most 5 rounds (10 in a follow-up), feeding judge or CodeQL messages as the next prompt, with a token-limit strategy that drops the earliest dialog blocks (p. 4, p. 10).

### Empirical base

- 728 LeetCode algorithm problems (354 post-2021, 374 pre-2021), 1,770 and 1,870 prompts across C, C++, Java, Python3 and JavaScript, one generation per prompt (p. 5).
- 18 CWEs with 54 scenarios in C and Python, 60 generations per scenario (p. 22).
- Model `gpt-3.5-turbo-0301`, temperature 0.7, round limit 5 (p. 4).
- Non-determinism study: 18 problems times 5 languages times 10 trials, at temperatures 0.7 and 0, plus 20 CWE scenarios at temperature 0 (p. 27).

### Findings

- Pre-2021 problems get an average Accepted rate of 68.41% against 20.27% for post-2021 problems, and the rate falls as difficulty rises (p. 6).
- C is the weakest language for correctness (31.28% overall) against 44.75% to 50.00% for the other four (p. 8).
- Multi-round fixing turns only 15.9% of wrong-answer pairs into accepted code, but most compile (70%) and runtime (78%) errors are changed to another status (p. 10, p. 13, p. 15).
- Generated code in C is the most complex and Python3 the least; complexity rises with difficulty and multi-round fixing keeps or raises it (p. 17, p. 19, p. 21).
- 33.32% of valid snippets in the CWE scenarios are vulnerable; no scenario of the Information Leakage group is red, while Unsafe Memory Operation has 4 of 6 red (p. 26).
- Multi-round vulnerability fixing with tool feedback succeeds for 89.4% of sampled CWE snippets, but weakly for Input Validation and Information Leakage (p. 25, p. 26).
- Output varies across repeated trials at temperature 0.7, and temperature 0 stabilises one-round generation only (p. 27).

### What the source offers

- A per-CWE, per-scenario table of vulnerability rates for ChatGPT with CodeQL as the oracle (p. 23).
- A taxonomy of failures in generated code (defect, compile, runtime and timeout classes) and a documented fix-by-feedback protocol (p. 9, p. 12, p. 14, p. 16).
- An online artifact with scripts and raw data (p. 2).

### Stated gaps and limitations

The paper acknowledges that ChatGPT is closed-source and its training data unknown, so contamination of the problems cannot be established; that the results reflect one model version at one time; and that LeetCode problems and CWE scenarios may not represent real-world tasks (p. 32). It also notes that CodeQL may flag secure code as vulnerable, that vulnerability detection covers only some languages (C, C++, Java for LeetCode; C and Python for CWE scenarios), and that each problem-language pair was queried only once (p. 32).

### Key claims

- On LeetCode problems, ChatGPT (GPT-3.5) had an average Accepted rate of 68.41% on pre-2021 problems and 20.27% on post-2021 problems across five languages (p. 6).
- Across all problems, the Accepted rate for C (31.28%) was lower than for C++, Java, Python3 and JavaScript (44.75% to 50.00%) (p. 8).
- In multi-round fixing, only 25 of 157 wrong-answer pairs (15.9%) were fixed, and the paper attributes this to a lack of grasp of logical details and of complex reasoning (p. 10, p. 11).
- Code generated by ChatGPT for the sampled LeetCode problems in C, C++ and Java was most often flagged for a missing NULL test after memory allocation, 91.8% of 183 vulnerable snippets (p. 22).
- In the CWE scenarios, 994 of 2,983 valid snippets (33.32%) were vulnerable, 51.64% in C against 17.08% in Python3 (p. 26).
- Feeding CodeQL's CWE information back to ChatGPT fixed 143 of 160 sampled vulnerable snippets (89.4%), which the paper takes to suggest that combining ChatGPT with vulnerability detection tools can mitigate vulnerabilities (p. 25, p. 27).
- Multi-round fixing generally preserves or increases the complexity level of the code (p. 21).
- At temperature 0.7 the same prompt gives different statuses, complexity and vulnerability outcomes across trials, while temperature 0 made one-round outputs consistent but not multi-round fixing (p. 27, p. 29).

## Extracted facts

- Prompt template parts: Content, Examples, Template, Command; one conversation per problem (p. 5, p. 6).
- Difficulty ratio hard : medium : easy is 1 : 2 : 1 for both periods; 142 similar-question pairs between periods were checked manually by two graduate students and found sufficiently different (p. 5).
- Statistics: average Accepted rate over five languages differs between periods with p = 0.008 and effect size 1 (p. 6).
- Post-2021 Accepted rates by difficulty: hard 0.66%, medium 13.90%, easy 52.47%; pre-2021: 40.13%, 70.95%, 89.80% (p. 6, p. 7).
- Post-2021 Accepted rates by language: C 15.38%, C++ 19.37%, Java 20.17%, Python3 23.93%, JavaScript 22.51%; pre-2021: 47.24%, 68.63%, 76.37%, 75.35%, 74.44% (p. 6, p. 8).
- Compile or runtime errors occur with similar probability across periods, 14.23% on average (p. 8).
- Wrong-answer analysis: 50 problems, 157 pairs; 115 consistently classified at first, consistency ratio 0.7325 (p. 8).
- Wrong-answer fixing: 25 of 157 fixed in at most 5 rounds, 16 at easy level, 21 of the 25 in a single round; with 10 rounds on 10 further unfixed pairs, 2 were fixed (p. 10, p. 11).
- Compile errors: 159 of 314 are the empty-body class "constant function"; 115 fixed, 40 accepted; runtime errors: 194 snippets, 143 fixed, 52 accepted; timeouts: 140 snippets, 44 fixed (p. 11, p. 12, p. 13, p. 15, p. 16).
- Complexity: low plus moderate cyclomatic complexity is 54.9% for C and above 66% for the other languages; Python3 has 44.5% low and 8.5% very high (p. 17).
- Cross-language comparison: for the same problem, 55.5% of cyclomatic and 76.5% of cognitive combinations differ by one level at most (p. 20).
- Security, LeetCode code: C, C++, Java only; CWE-787, 416, 476, 190 and 119 with 30 queries (Java only four CWE-190 queries); no detections for CWE-416 and CWE-190; 15 snippets sampled per query for fixing (p. 21, p. 22).
- Security, CWE scenarios: valid rate 99.07%; Table 19 colours scenarios as green, orange, yellow, red (0%, up to 5%, up to 50%, above 50%): 18, 4, 16, 16 scenarios (p. 23, p. 26).
- Non-determinism design: 9 post-2021 and 9 pre-2021 problems, 5 languages, 10 trials at temperature 0.7 and 0; example, problem 2224 in JavaScript gave 50% A., 10% W.A., 10% T.L.E., 30% R.E. (p. 27).
- Temperature 0: statuses and complexity consistent in 10 trials except problem 2532 in Python3; generated code identical for every problem-language pair except that one (p. 27).
- Token-limit check: halving the maximum output tokens produced snippets that all had compile or syntax errors (p. 30, p. 31).
- Two counts of the compile-error snippets: the text says 312 snippets with C.E. in the analysis, while Table 7 and the text sum to 314 (p. 11, p. 12). Unresolved.
- The text says 60 snippets were generated per CWE scenario, while the valid counts in Table 19 imply smaller denominators in several rows (for example 53 valid at 98.1% means 54 generated) (p. 22, p. 23). Unresolved.
- The CWE multi-round fixing result is stated as 89.4% (143/160), and in the RQ4 answer as "100% and 89.4%", the 100% referring to the LeetCode-code fixing (p. 25, p. 27).

## Quotes

- "ChatGPT is better at generating functionally correct code for problems before 2021 in different languages than problems after 2021 with 48.14% advantage in Accepted rate on judgment platform" (p. 1)
- "The goal of our prompt design is not to find the optimal prompt that maximizes ChatGPT’s performance." (p. 4)
- "ChatGPT lacks the ability to grasp logical details, even though these details may be straightforward for humans." (p. 11)
- "the multi-round fixing process with ChatGPT generally preserves or increases the complexity levels of code snippets" (p. 21)
- "The code generated by ChatGPT does not perform a NULL test after allocating memory in C or C++ languages, which may lead to potential vulnerabilities." (p. 22)
- "ChatGPT generates 2,983 (99.07%) valid code snippets successfully where 994 (33.32%) are vulnerable." (p. 26)
- "setting the temperature to 0 may be a potential strategy to mitigate the non-determinism of ChatGPT in one-round process." (p. 27)
- "CodeQL may report a code as vulnerable when it is actually secure." (p. 32)

## Reading

## Connections

## Disagreements
