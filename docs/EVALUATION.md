# Answer evaluation

We checked the 20 selected dataset reference question–answer pairs against their
linked USCIS material. That was separate from checking our system’s generated
answers. The final reference review supported 18 references as written and gave
two scope clarifications.

This step assesses the 50 saved system responses: 20 naturalization questions and
five out-of-scope questions, each with BM25 and MiniLM evidence. We compared the
exact passages supplied to the model with each saved output and the verified USCIS
material. The generator, prompt, and settings stayed fixed; we generated no new
responses.
The CSV records application status, displayed answer, evidence IDs, protocol ratings,
and a reason for every judgment. Rejected raw text is noted separately and is not
treated as displayed or successful. The original records remain unchanged.

For in-scope questions, BM25 produced seven supported useful answers out of 20;
MiniLM produced three. BM25 also had one partial answer, one appropriate abstention,
five unnecessary abstentions, and six validation failures. MiniLM had one partial
answer, one incorrect displayed answer, three unnecessary abstentions, and 12
validation failures. Neither method had an execution failure. All five out-of-scope
cases received appropriate abstentions with each method. The table gives every
count with its denominator. These ratings come from an assisted review; student
ratings are still pending. Reviewer details are in the assessment metadata and
assistance disclosure. Conditional ratings apply only to substantive drafts
that the app displayed. Rating dimensions are factual support (F), citation relevance
(C), question coverage (Q), conditions (Cond), and readability (R); cells give score
counts in 0/1/2 order. Failed outputs have no displayed-answer ratings.

| Set | N | Drafts shown | Supported useful | Partial | Incorrect | Appropriate abstention | Unnecessary abstention | Validation failure | Conditional ratings (0/1/2 counts) |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| In scope, BM25 | 20 | 8 | 7/20 | 1/20 | 0/20 | 1/20 | 5/20 | 6/20 | F 0/1/7; C 0/0/8; Q 0/0/8; Cond 0/1/7; R 0/0/8 |
| In scope, MiniLM | 20 | 5 | 3/20 | 1/20 | 1/20 | 0/20 | 3/20 | 12/20 | F 1/1/3; C 1/1/3; Q 1/1/3; Cond 1/1/3; R 0/0/5 |
| Out of scope, BM25 | 5 | 0 | 0/5 | 0/5 | 0/5 | 5/5 | 0/5 | 0/5 | N/A; no substantive drafts |
| Out of scope, MiniLM | 5 | 0 | 0/5 | 0/5 | 0/5 | 5/5 | 0/5 | 0/5 | N/A; no substantive drafts |

The out-of-scope evidence did not answer those questions. This is a good result on
five cases, not evidence of robust out-of-scope detection. Evidence availability also differed: BM25 supplied enough information for
19/20 in-scope questions; MiniLM did for 14/20, with one more uncertain. Both methods
unnecessarily abstained on the answerable filing-date test question (`qa-5c7a593817d2`);
BM25 also did so on the marital-union question (`qa-1c9ac2bdd353`).

The displayed MiniLM answer for `qa-c9e78deeb174` gives 1946 as the last major oath
addition, while the supplied history identifies the 1952 INA addition. BM25’s
`qa-210bd866a25c` answer gives the right definition but adds an alienage-bar claim
without all the source’s conditions. Some raw responses were better than what the
app delivered: correct text for `qa-f074b4c28745` and `qa-4609d6be9c7d` was rejected
by validation, so neither counts as an answer. MiniLM’s raw `qa-b941678d80de` text
says 30 days instead of the 15-day response period, but it was also rejected.

These results compare only the saved runs on this fixed set. They do not show that
either retrieval method is generally better, and they do not evaluate legal advice
or every naturalization question. The 50 responses are separate from the 20
reference checks, and student ratings remain pending.
