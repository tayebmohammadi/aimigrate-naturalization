# Final verification of the 20 selected dataset references

We checked all 20 selected reference answers against their linked USCIS pages. The generated drafts have a [separate evaluation](../../docs/EVALUATION.md).

OpenAI Codex separately checked the relevant text and nearby conditions from 16 USCIS pages captured on November 15, 2026 (America/New_York). All 16 requests succeeded. Codex found support for 18 answers as written and identified two that needed scope clarifications. We removed a client-side configuration value from the saved HTML copies and kept the policy text and links intact.

[Verification table](final_verification.csv) · [Access records](access_records.jsonl) · [USCIS captures](live_pages/)

| QA ID | Question | Finding | Necessary clarification |
|---|---|---|---|
| `qa-1c9ac2bdd353` | What is the marital union requirement under INA 319(a) for spouses of U.S. citizens residing in the United States? | Supported as written | None; the reference answers the question at its stated scope. |
| `qa-dcd6fb096bd9` | Which agency should revocation of naturalization cases for military members be referred to? | Supported with material scope clarification | The ICE referral applies to the specific military-service and discharge circumstances in the preceding paragraph, not every military naturalization revocation. |
| `qa-9db9beac80a9` | What factors should a USCIS officer consider when conducting the naturalization interview regarding the applicant's understanding? | Supported as written | None; the reference answers the question at its stated scope. |
| `qa-be519f64475f` | What standard is used to determine whether an expedited oath ceremony should be granted? | Supported with material scope clarification | An expedited ceremony request requires sufficient cause, and the decision remains discretionary. |
| `qa-36bbfce529b8` | Who has delegated authority to administer the Oath of Allegiance and issue certificates at USCIS? | Supported as written | None; the reference answers the question at its stated scope. |
| `qa-5a7336ab968c` | Who has exclusive authority to administer the Oath during a judicial naturalization ceremony? | Supported as written | None; the reference answers the question at its stated scope. |
| `qa-b941678d80de` | How long does an applicant have to respond to a USCIS motion to reopen after being notified? | Supported as written | None; the reference answers the question at its stated scope. |
| `qa-73e8e4e98534` | What marital status requirement applies to surviving spouses of deceased service members under INA 319(d)? | Supported as written | None; the reference answers the question at its stated scope. |
| `qa-f0ba3e1e977e` | Does having been eligible for an English language exception affect the language in which the Oath of Allegiance is administered? | Supported as written | None; the reference answers the question at its stated scope. |
| `qa-f2fa5cd76241` | What information does the DCII check reveal? | Supported as written | None; the reference answers the question at its stated scope. |
| `qa-4609d6be9c7d` | What does an 'Honorable' discharge characterization indicate about a service member's conduct? | Supported as written | None; the reference answers the question at its stated scope. |
| `qa-c9e78deeb174` | What was the last major addition to the Oath of Allegiance and when was it made? | Supported as written | None; the reference answers the question at its stated scope. |
| `qa-210bd866a25c` | What is the definition of an 'exemption from military service' for naturalization purposes? | Supported as written | None; the reference answers the question at its stated scope. |
| `qa-4ecbcc440b1c` | What is the difference between INA 328 and INA 329 regarding military service naturalization? | Supported as written | None; the reference answers the question at its stated scope. |
| `qa-4385aaa06495` | Under what general conditions does USCIS issue a Certificate of Naturalization? | Supported as written | None; the reference answers the question at its stated scope. |
| `qa-5c7a593817d2` | Who will take the 2008 naturalization civics test? | Supported as written | None; the reference answers the question at its stated scope. |
| `qa-f4ac028b6dd2` | What is the physical presence requirement under INA 319(a) for spouses of U.S. citizens residing in the United States? | Supported as written | None; the reference answers the question at its stated scope. |
| `qa-f074b4c28745` | What happens if an applicant refuses to explain the basis of their objection to the oath during the interview? | Supported as written | None; the reference answers the question at its stated scope. |
| `qa-071175958a7d` | How long must an alien have served in the U.S. armed forces to qualify for peacetime naturalization? | Supported as written | None; the reference answers the question at its stated scope. |
| `qa-a9d1c7e47d92` | How long does an applicant have to file a hearing request after receiving a denial notice? | Supported as written | None; the reference answers the question at its stated scope. |

For `qa-f074b4c28745`, the linked page gives the request-for-evidence instruction in the paragraph after the dataset’s quoted excerpt. The full linked section supports the reference answer.
