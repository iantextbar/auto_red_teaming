---
type: source
title: Do Users Write More Insecure Code with AI Assistants?
authors: [Neil Perry, Megha Srivastava, Deepak Kumar, Dan Boneh]
year: 2023
venue: Proceedings of the 2023 ACM SIGSAC Conference on Computer and Communications Security (CCS '23)
source_type: peer-reviewed
interest: independent
doi: 10.1145/3576915.3623157
url: https://arxiv.org/abs/2211.03622
pdf: "[[references/pdfs/sprint1/ai_assistants_insecure_code.pdf]]"
snapshot:
status: summarised
summarised_by: claude-sonnet-5-5
reviewed_by:
tags: []
---

## Stated by the source

### What it is about

The paper reports a controlled user study of how people interact with an AI code assistant, built on OpenAI's Codex, while solving security-related programming tasks (p. 1). It pursues three research questions: whether users write more insecure code with access to an assistant, whether they trust the assistant to write secure code, and how their prompt language and behaviour affect the vulnerabilities in their code (p. 1). The tasks span Python, JavaScript and C, and the audience is the security and human-computer interaction community and the designers of future code assistants (p. 1, p. 2).

### Argument

The authors start from a gap. Earlier work had shown that Copilot-style tools can emit insecure code for a small set of synthetic prompts, but no study had measured security risk in the context of how developers actually choose to use the tools. Productivity studies give a mixed picture, and the authors note that for security goals optimising for productivity may not be the right objective if it breeds misplaced trust (p. 1, p. 2). The only comparable controlled study, by Sandoval et al., used a weaker model with fixed parameters and only C, and found inconclusive results (p. 2).

Their first move is a between-subjects comparison. Participants solved the same tasks with or without an assistant, and the authors coded each solution for correctness and security by hand. They report that the assistant group wrote less secure code on four of five tasks, with the exception of the C task, where results were mixed (p. 5, p. 7). The mechanism they describe is that the assistant returns code that works but lacks security context. Examples are trivial ciphers and unauthenticated encryption, unsafe randomness in signing, path checks without canonicalisation, and SQL built by string concatenation (p. 5–7). They add that participants often accepted such output after testing only for functional correctness (p. 5).

The second move is about confidence. In the post-study survey, assistant users on average believed their answers were more secure than control users did, despite often providing more insecure answers (p. 8). Trust was inversely related to security: participants with secure solutions trusted the assistant less than those with insecure ones (p. 8). The authors read this as a shift of burden from writing code to testing it, which is worrying if developers are not skilled at security testing (p. 8). They use copying of AI output as a behavioural proxy for trust, and normalised edit distance to show that secure answers usually required significant edits by the user (p. 8).

The third move analyses prompts, using a taxonomy borrowed from query-refinement research (function declaration, specification, instruction, library, language, helper, model close, and others) and a set of repair strategies (p. 10, p. 11). The authors report that prompts containing code, such as function declarations or helpers, and long prompts were more often accepted (p. 10). Cycles in which the user feeds the model's previous output back as the next prompt ("model close") fell sharply among prompts behind secure answers, which the authors read as over-reliance on generated output (p. 10). Participants who raised the temperature, rephrased and added context tended to end with more secure code, which the authors tentatively link to developing a "mental model" of the assistant (p. 11).

The discussion concludes that assistants may lower the barrier to entry yet give inexperienced users a false sense of security (p. 1, p. 11). It recommends prompt refinement, integrated warnings and validation tests, secure library defaults, user education, exposing parameters such as temperature, and filtering or re-weighting training data with static analysis (p. 12, p. 13).

### Interlocutors

- Pearce et al. 2022 (Asleep at the keyboard): showed Copilot can produce security mistakes on synthetic prompts; the paper takes this as its motivation and extends it to real users (p. 1, p. 2). Role: foundation.
- Sandoval et al. 2022: the only prior controlled user study of security with AI assistance; found inconclusive effects on a C task with fixed parameters (p. 2). Role: counterpoint.
- Jiang et al. 2022 (natural language programming strategies): supplies the query-repair framework and the finding that users expand prompt scope over time (p. 11). Role: foundation.
- Chen et al. 2021 (Codex) and Fried et al. 2022 (InCoder): the model families underlying the assistants studied (p. 1, p. 2). Role: foundation.
- Tabachnyk and Nikolov 2022, Vaithilingam et al. 2022, Ziegler et al. 2022: productivity and usability studies reporting mixed or inconclusive results (p. 2). Role: counterpoint.

### Methodology

The study is a randomised between-subjects user study with mixed-methods coding. Participants were randomly assigned to an experiment group with an AI assistant or a control group without one, at roughly a two-to-one ratio (p. 3). The authors built a desktop application that logged queries, responses, accepted outputs and final code, and recorded screen and audio (p. 3). Two authors coded correctness and security for every solution against per-task rubrics, with a third resolving disagreements by majority, and also tagged each mistake as stemming from the AI, the internet or the user (p. 4). Cohen's kappa ranged from 0.7 to 0.96 for correctness and 0.68 to 0.88 for security (p. 4).

Statistical tests were Welch's t-test and the chi-squared test for categorical data, plus per-task logistic regression with a Benjamini-Hochberg correction, controlling for security class, student status and years of programming (p. 3, p. 4, p. 16). The authors acknowledge subjectivity in the coding approach (p. 4).

### Empirical base

54 participants were recruited, 47 retained after excluding prescreening failures and drop-outs: 33 in the experiment group and 14 in the control group (p. 3). They were undergraduates (66%), graduates (19%) and professionals (15%) from two US universities and four companies, with 87% aged 18–24 (p. 3, p. 4). Each had up to two hours and a $30 gift card (p. 3). The model was codex-davinci-002 (p. 10).

### Findings

- Assistant users were less secure on four of five tasks; the C task showed mixed results (p. 5, p. 7).
- Encryption (Q1): assistant users were significantly more likely to write insecure solutions (p = 0.017) and to use trivial ciphers (p = 0.018) (p. 5).
- Signing (Q2): 3% of assistant users wrote a secure solution against 21% of controls (p = 0.039) (p. 5).
- Sandboxed directory (Q3): 12% against 29% secure; failure to handle symlinks was more common with the assistant (p = 0.019) (p. 6, p. 7).
- SQL (Q4): 36% of assistant users wrote injectable code against 7% of controls (p = 0.041) (p. 7).
- C strings (Q5): inconclusive overall, though assistant users were significantly more likely to introduce integer overflow (p. 7).
- Assistant users believed their answers more secure than controls did on every question, and users with secure solutions trusted the AI less than users with insecure ones (p. 8).
- Secure answers were associated with higher temperature, more context and repeated rephrasing, while repeatedly reusing model output was associated with insecure answers (p. 10, p. 11).

### What the source offers

- A released study apparatus (an Electron/React UI) and anonymised interaction data, including prompts, for replication (p. 1, p. 3).
- Per-task rubrics for grading security of encryption, signing, path sandboxing, SQL and C string code (p. 5–7).
- A prompt taxonomy and a repair-strategy taxonomy applied to a real prompt log (p. 10, p. 11).
- Counts of mistake origin (AI versus non-AI) for each vulnerability type (p. 16).

### Stated gaps and limitations

The authors say the participants were mainly students, who may not represent regular assistant users; professionals may have stronger security backgrounds and incentives to test (p. 12). The study environment was artificial, with time limits and no job consequences, and UI aspects such as latency may have affected results (p. 12). The sample is small, and a larger one would be needed to assess subtler effects such as background or native language (p. 12). They also note that the degree of AI influence on each response is hard to establish (p. 11).

### Key claims

- Participants with access to an AI assistant wrote significantly less secure code than those without access, in a study of 47 participants on security tasks (p. 1).
- Assistant users were more likely to believe they had written secure code (p. 1).
- Assistant users were less secure on four of the five analysed tasks, and results on the C task were mixed (p. 5, p. 7).
- Participants with secure solutions reported lower trust in the assistant than participants with insecure ones (p. 8).
- Participants who specified task instructions, function declarations and helper functions generated more secure code (p. 1).
- Reusing the assistant's previous output as the next prompt can magnify or replicate security problems (p. 1, p. 10).
- Adjusting temperature may influence code security, though the authors treat the link as possible rather than established (p. 11).
- In every mistake type, the AI was involved in at least as many mistakes as the participant (p. 12).

## Extracted facts

- Tasks: Q1 symmetric encrypt/decrypt in Python; Q2 ECDSA signing in Python; Q3 file access restricted to "/safedir" in Python; Q4 SQL insert in JavaScript; Q5 integer to comma-separated string in C; Q6 display user input in the browser (JavaScript) (p. 2).
- Q6 was dropped from analysis because it was too vague and many participants simply called alert or console.log (p. 3). Participants were told they would solve six questions, but five are analysed.
- Time per question was 11–14 minutes, except Q5 at 31 minutes; the maximum was two hours (p. 3).
- Randomisation was about two-to-one experiment to control; 33 experiment and 14 control participants after exclusions (p. 3).
- Q1 correctness: 67% of assistant users against 79% of controls (p. 5).
- Q2 correctness: 55% against 64% (p. 5).
- Q4 correctness: 52% of assistant users against 64% of controls; secure solutions 36% against 50% (p. 7).
- Regression group coefficient (Experiment versus Control): Q1 -2.1437, p = 0.018; Q2 -2.0244, p = 0.166; Q3 -0.5404, p = 0.562; Q4 -0.8841, p = 0.279; Q5 0.9709, p = 0.254; all questions pooled -0.6315, p = 0.056 (p. 6).
- Trust ratings, secure versus insecure solvers: Q3 1.5 vs 4.0; Q2 1.0 vs 3.53 (p. 8). Mean beliefs of security for Q1: 3.5 for assistant users with insecure answers vs 2.0 for controls with insecure answers (p. 9).
- Share of AI outputs copied, without versus with security experience: Q1 22.4% / 9.2%; Q4 25.3% / 6.67%; Q5 0% (p. 9).
- 87% of secure responses needed significant edits relative to the closest AI output (p. 8).
- Prompt types, share of users: function declaration 63.8%, specification 63.8%, model close 61.7%, library 53.1%, language 48.9%, instruction 21.3%, security language 4.3% (p. 10).
- Long prompts led to acceptance in 42.7% of cases against 15.7% for short prompts (p. 10).
- Temperature: 48.5% of participants never adjusted it and 51.5% never adjusted response length; the default temperature was 0 (p. 9, p. 11).
- Assistant users made on average 4.6 queries per question; the most common repair type was changing prompt type (48.9% of prompts, 97.0% of users) (p. 11).
- Mistakes involving the AI within the experiment group: auth 58%, symlink 73%, parent path 61%, random 48%, SQL injection 30%, against non-AI 9%, 15%, 15%, 15% and 6% respectively (p. 16).
- Inconsistency: Section 4 says significance was tested with a chi-squared test for categorical variables (p. 5), while Appendix 9.6 says significance for particular security buckets uses Welch's unequal variance t-test (p. 16).

## Quotes

- "we find that participants who had access to an AI assistant wrote significantly less secure code than those without access to an assistant" (p. 1)
- "Participants with access to an AI assistant were also more likely to believe they wrote secure code" (p. 1)
- "Participants with access to an AI assistant were far more likely to write incorrect and insecure solutions compared to the control group." (p. 5)
- "We observe that the AI assistant often writes correct SQL queries but uses string concatenation instead of prepared statements" (p. 7)
- "87% of secure responses required significant edits from users" (p. 8)
- "relying too much on generated output often did not result in a secure answer" (p. 10)
- "participants who provided insecure code were less likely to modify" (p. 12)
- "our participant group consisted mainly of university students which likely do not represent the population that is most likely to use AI assistants" (p. 12)

## Reading

## Connections

## Disagreements
