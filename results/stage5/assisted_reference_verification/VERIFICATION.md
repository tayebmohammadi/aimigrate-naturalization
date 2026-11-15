# Assisted verification of 20 fixed reference answers

**Reviewer:** OpenAI Codex (coding assistant). **Student confirmation:** pending for all rows. This is not independent student evaluation. No Qwen answers were generated or graded. Original Stage 5A files are unchanged.

Reviewed 20 fixed selected rows: 14 supported as written; 6 supported with a scope/context qualification; 0 need correction; 0 unverifiable.

The dataset answers and spans below are preserved as generated dataset material, not treated as unquestioned gold labels. Each row was checked against the linked official text and surrounding context. Review used Stage 5A official captures dated November 14, 2026; seven relevant pages were freshly fetched by direct request and inspected in this review. The web reader returned 403. These checks are not claims of full-page identity or permanent legal currency.

## Findings at a glance

| QA ID | Question (short) | Verdict | Main scope note |
|---|---|---|---|
| `qa-1c9ac2bdd353` | What is the marital union requirement under INA 319(a) for spouses of U.S. citizens residing in the United States? | Supported as written | The question names the INA 319(a) domestic-spouse category and asks only for its marital-union duration. The reference gives the table requirement. |
| `qa-dcd6fb096bd9` | Which agency should revocation of naturalization cases for military members be referred to? | Supported with a scope/context qualification | The linked section refers to a narrowly defined group of possible revocation cases based on military naturalization and early other-than-honorable separation. “Such ca… |
| `qa-9db9beac80a9` | What factors should a USCIS officer consider when conducting the naturalization interview regarding the applican… | Supported as written | This answers the question about understanding during the interview. The surrounding discussion permits rephrasing or supplementing questions; it does not create an aut… |
| `qa-be519f64475f` | What standard is used to determine whether an expedited oath ceremony should be granted? | Supported with a scope/context qualification | The answer accurately states the discretionary considerations but omits the section’s threshold of sufficient cause. The agency or court may consider such circumstance… |
| `qa-36bbfce529b8` | Who has delegated authority to administer the Oath of Allegiance and issue certificates at USCIS? | Supported as written | The listed officials have delegated authority for USCIS administrative oath ceremonies and certificate issuance, which is the question’s scope. |
| `qa-5a7336ab968c` | Who has exclusive authority to administer the Oath during a judicial naturalization ceremony? | Supported as written | The answer matches the rule for judicial naturalization ceremonies. It does not conflict with USCIS authority for administrative ceremonies. |
| `qa-b941678d80de` | How long does an applicant have to respond to a USCIS motion to reopen after being notified? | Supported as written | The page gives the 15-day response period for the described motion and grounds. This is distinct from a 30-day request for a denial hearing. |
| `qa-73e8e4e98534` | What marital status requirement applies to surviving spouses of deceased service members under INA 319(d)? | Supported as written | The question asks about the surviving-spouse category under INA 319(d); the table states the marital-union condition at the service member’s death. |
| `qa-f0ba3e1e977e` | Does having been eligible for an English language exception affect the language in which the Oath of Allegiance … | Supported as written | This directly answers whether an English-test exception changes the oath’s language. Interpreters and separate oath accommodations remain possible. |
| `qa-f2fa5cd76241` | What information does the DCII check reveal? | Supported as written | The cited section describes the check’s purpose as revealing derogatory information in military records. It is not an eligibility or approval determination. |
| `qa-4609d6be9c7d` | What does an 'Honorable' discharge characterization indicate about a service member's conduct? | Supported as written | The page defines the characterization using these alternative grounds. The reference preserves the “or” and does not claim naturalization is automatic. |
| `qa-c9e78deeb174` | What was the last major addition to the Oath of Allegiance and when was it made? | Supported as written | The historical explanation in the linked chapter supports both the year/law and the clause identified. |
| `qa-210bd866a25c` | What is the definition of an 'exemption from military service' for naturalization purposes? | Supported as written | The source provides both branches of the definition. Separate surrounding rules concerning alienage and service are not implied by this definition alone. |
| `qa-4ecbcc440b1c` | What is the difference between INA 328 and INA 329 regarding military service naturalization? | Supported with a scope/context qualification | The question asks for the high-level distinction, which the reference gives. It is not a complete eligibility comparison and must not imply the provisions share servic… |
| `qa-4385aaa06495` | Under what general conditions does USCIS issue a Certificate of Naturalization? | Supported with a scope/context qualification | The reference accurately states the general rule, but “general” matters: the section describes medical-disability oath-waiver circumstances and PRC/ARC surrender requi… |
| `qa-5c7a593817d2` | Who will take the 2008 naturalization civics test? | Supported as written | The linked USCIS study page states the filing-date cutoff; the question and reference use the filing date, not interview date. The answer is time-sensitive. |
| `qa-f4ac028b6dd2` | What is the physical presence requirement under INA 319(a) for spouses of U.S. citizens residing in the United S… | Supported with a scope/context qualification | The reference gives the physical-presence row. The same table places it in the INA 319(a) category and separately lists three years of residence after becoming an LPR;… |
| `qa-f074b4c28745` | What happens if an applicant refuses to explain the basis of their objection to the oath during the interview? | Supported with a scope/context qualification | The dataset source span directly supports the additional interview opportunity. The RFE direction appears in the following paragraph, not in that span; the linked full… |
| `qa-071175958a7d` | How long must an alien have served in the U.S. armed forces to qualify for peacetime naturalization? | Supported as written | The question asks the duration for peacetime service naturalization, and the page states at least one year of honorable service. Other statutory criteria remain outsid… |
| `qa-a9d1c7e47d92` | How long does an applicant have to file a hearing request after receiving a denial notice? | Supported as written | The answer gives the filing deadline asked for. The page separately discusses scheduling the hearing; that is not part of this 30-day filing answer. |

Full reference answers, spans, source sections, evidence excerpts, reasons, expected-answer qualifications, access date, and verification mode follow for each row.

## Detailed findings

### 1. qa-1c9ac2bdd353 — Supported as written

**Question:** What is the marital union requirement under INA 319(a) for spouses of U.S. citizens residing in the United States?
**Source:** [Chapter 1 - Purpose and Background](https://www.uscis.gov/policy-manual/volume-12-part-g-chapter-1) (`doc-4f8fc2552e27`), section: INA 319(a), Table: Spouses of U.S. Citizens Residing in United States.
**Original dataset reference:** Under INA 319(a), the applicant must be married and living in marital union for at least 3 years prior to filing.
**Original dataset span:** “Married and living in marital union for at least 3 years prior to filing”
**Evidence excerpt:** “Married and living in marital union for at least 3 years prior to filing.”
**Reason:** The question names the INA 319(a) domestic-spouse category and asks only for its marital-union duration. The reference gives the table requirement.
**Expected answer after qualification:** No correction needed; retain the three-year-before-filing and INA 319(a) context.
**Access:** 2026-11-14; New direct-curl capture, inspected for this review; web reader returned HTTP 403.

### 2. qa-dcd6fb096bd9 — Supported with a scope/context qualification

**Question:** Which agency should revocation of naturalization cases for military members be referred to?
**Source:** [Chapter 7 - Revocation of Naturalization](https://www.uscis.gov/policy-manual/volume-12-part-i-chapter-7) (`doc-a3fdb28eca82`), section: Military Naturalization Based on Service on or after November 24, 2003; revocation paragraph.
**Original dataset reference:** Such cases should be referred to U.S. Immigration and Customs Enforcement (ICE).
**Original dataset span:** “Such cases should be referred to U.S. Immigration and Customs Enforcement (ICE).”
**Evidence excerpt:** “Such cases should be referred to U.S. Immigration and Customs Enforcement (ICE).”
**Reason:** The linked section refers to a narrowly defined group of possible revocation cases based on military naturalization and early other-than-honorable separation. “Such cases” must not be generalized to every military naturalization revocation.
**Expected answer after qualification:** Qualified: refer the specific possible-revocation cases described in this section to ICE; this is not an automatic revocation rule.
**Access:** 2026-11-14; New direct-curl capture, inspected for this review; web reader returned HTTP 403.

### 3. qa-9db9beac80a9 — Supported as written

**Question:** What factors should a USCIS officer consider when conducting the naturalization interview regarding the applicant's understanding?
**Source:** [Chapter 3 - Evidence and the Record](https://www.uscis.gov/policy-manual/volume-12-part-f-chapter-3) (`doc-923af438741b`), section: Naturalization Interview; applicant understanding/English proficiency discussion.
**Original dataset reference:** The officer should take into consideration the education level of the applicant and his or her knowledge of the English language.
**Original dataset span:** “The officer should take into consideration the education level of the applicant and his or her knowledge of the English language.”
**Evidence excerpt:** “The officer should take into consideration the education level of the applicant and his or her knowledge of the English language.”
**Reason:** This answers the question about understanding during the interview. The surrounding discussion permits rephrasing or supplementing questions; it does not create an automatic test exemption.
**Expected answer after qualification:** No correction needed; those factors concern the officer’s assessment of understanding.
**Access:** 2026-11-14; Dated official USCIS archive/fetch record dated 2026-11-14; relevant text and surrounding context inspected.

### 4. qa-be519f64475f — Supported with a scope/context qualification

**Question:** What standard is used to determine whether an expedited oath ceremony should be granted?
**Source:** [Chapter 6 - Judicial and Expedited Oath Ceremonies](https://www.uscis.gov/policy-manual/volume-12-part-j-chapter-6) (`doc-b0a18538fdef`), section: Expedited Oath Ceremonies; sufficient cause and compelling/humanitarian circumstances.
**Original dataset reference:** The court or the USCIS District Director may consider special circumstances of a compelling or humanitarian nature when determining whether to grant an expedited oath ceremony.
**Original dataset span:** “In determining whether to grant an expedited oath ceremony, the court or the USCIS District Director may consider special circumstances of a compelling or humanitarian nature.”
**Evidence excerpt:** “The court or the USCIS District Director may consider special circumstances of a compelling or humanitarian nature.”
**Reason:** The answer accurately states the discretionary considerations but omits the section’s threshold of sufficient cause. The agency or court may consider such circumstances; a request is not guaranteed.
**Expected answer after qualification:** Qualified: with sufficient cause, the court or USCIS District Director may consider compelling or humanitarian special circumstances; the decision is discretionary.
**Access:** 2026-11-14; New direct-curl capture, inspected for this review; web reader returned HTTP 403.

### 5. qa-36bbfce529b8 — Supported as written

**Question:** Who has delegated authority to administer the Oath of Allegiance and issue certificates at USCIS?
**Source:** [Chapter 1 - Purpose and Background](https://www.uscis.gov/policy-manual/volume-12-part-k-chapter-1) (`doc-e496890fccd0`), section: Authority to Administer the Oath of Allegiance and Issue Certificates; administrative ceremonies.
**Original dataset reference:** USCIS District Directors, Field Office Directors, and other USCIS officers acting on their behalf have delegated authority to administer the Oath of Allegiance in USCIS administrative oath ceremonies and to issue certificates.
**Original dataset span:** “USCIS District Directors, Field Office Directors, and other USCIS officers acting on their behalf, have delegated authority to administer the Oath of Allegiance in USCIS administrative oath ceremonies and to issue certificates.”
**Evidence excerpt:** “USCIS District Directors, Field Office Directors, and other USCIS officers acting on their behalf have delegated authority.”
**Reason:** The listed officials have delegated authority for USCIS administrative oath ceremonies and certificate issuance, which is the question’s scope.
**Expected answer after qualification:** No correction needed; keep the administrative-ceremony scope.
**Access:** 2026-11-14; Dated official USCIS archive/fetch record dated 2026-11-14; relevant text and surrounding context inspected.

### 6. qa-5a7336ab968c — Supported as written

**Question:** Who has exclusive authority to administer the Oath during a judicial naturalization ceremony?
**Source:** [Chapter 2 - The Oath of Allegiance](https://www.uscis.gov/policy-manual/volume-12-part-j-chapter-2) (`doc-17e2abba0b9e`), section: Judicial Oath of Allegiance; judicial ceremony authority.
**Original dataset reference:** During judicial naturalization ceremonies, the judge in the district of proper jurisdiction has exclusive authority to administer the Oath.
**Original dataset span:** “During judicial naturalization ceremonies, the judge in the district of proper jurisdiction has exclusive authority to administer the Oath.”
**Evidence excerpt:** “The judge in the district of proper jurisdiction has exclusive authority to administer the Oath.”
**Reason:** The answer matches the rule for judicial naturalization ceremonies. It does not conflict with USCIS authority for administrative ceremonies.
**Expected answer after qualification:** No correction needed; retain “judicial” and “proper jurisdiction.”
**Access:** 2026-11-14; Dated official USCIS archive/fetch record dated 2026-11-14; relevant text and surrounding context inspected.

### 7. qa-b941678d80de — Supported as written

**Question:** How long does an applicant have to respond to a USCIS motion to reopen after being notified?
**Source:** [Chapter 5 - Motion to Reopen](https://www.uscis.gov/policy-manual/volume-12-part-b-chapter-5) (`doc-2d6ddd760266`), section: Motion to Reopen; response period after notice.
**Original dataset reference:** The applicant has 15 days to respond to the motion to reopen and overcome the derogatory information or provide good cause for failing to appear at the Oath ceremony.
**Original dataset span:** “The applicant has 15 days to respond to the motion to reopen and overcome the derogatory information or provide good cause for failing to appear at the Oath ceremony.”
**Evidence excerpt:** “The applicant has 15 days to respond to the motion to reopen.”
**Reason:** The page gives the 15-day response period for the described motion and grounds. This is distinct from a 30-day request for a denial hearing.
**Expected answer after qualification:** No correction needed; the period is tied to the specified motion-to-reopen procedure.
**Access:** 2026-11-14; Dated official USCIS archive/fetch record dated 2026-11-14; relevant text and surrounding context inspected.

### 8. qa-73e8e4e98534 — Supported as written

**Question:** What marital status requirement applies to surviving spouses of deceased service members under INA 319(d)?
**Source:** [Chapter 1 - Purpose and Background](https://www.uscis.gov/policy-manual/volume-12-part-g-chapter-1) (`doc-4f8fc2552e27`), section: INA 319(d), Table: Spouses of Deceased Service Members.
**Original dataset reference:** Under INA 319(d), the applicant must have been married and living in marital union at the time of the service member's death.
**Original dataset span:** “Must have been married and living in marital union at time of death”
**Evidence excerpt:** “Must have been married and living in marital union at time of death.”
**Reason:** The question asks about the surviving-spouse category under INA 319(d); the table states the marital-union condition at the service member’s death.
**Expected answer after qualification:** No correction needed; do not import INA 319(a)’s three-year duration.
**Access:** 2026-11-14; New direct-curl capture, inspected for this review; web reader returned HTTP 403.

### 9. qa-f0ba3e1e977e — Supported as written

**Question:** Does having been eligible for an English language exception affect the language in which the Oath of Allegiance is administered?
**Source:** [Chapter 2 - The Oath of Allegiance](https://www.uscis.gov/policy-manual/volume-12-part-j-chapter-2) (`doc-17e2abba0b9e`), section: Oath of Allegiance; language of oath.
**Original dataset reference:** No. The Oath of Allegiance is administered in the English language regardless of whether the applicant was eligible for an exception to the English language requirements.
**Original dataset span:** “The Oath of Allegiance is administered in the English language, regardless of whether the applicant was eligible for an exception to the English language requirements.”
**Evidence excerpt:** “The Oath of Allegiance is administered in the English language, regardless of whether the applicant was eligible for an exception to the English language requirements.”
**Reason:** This directly answers whether an English-test exception changes the oath’s language. Interpreters and separate oath accommodations remain possible.
**Expected answer after qualification:** No correction needed; distinguish English-test exceptions from the language of oath administration.
**Access:** 2026-11-14; Dated official USCIS archive/fetch record dated 2026-11-14; relevant text and surrounding context inspected.

### 10. qa-f2fa5cd76241 — Supported as written

**Question:** What information does the DCII check reveal?
**Source:** [Chapter 6 - Required Background Checks](https://www.uscis.gov/policy-manual/volume-12-part-i-chapter-6) (`doc-1c92b0878249`), section: Military Record Checks; Defense Clearance and Investigations Index (DCII).
**Original dataset reference:** The DCII check should show whether the applicant has any derogatory information in his or her military records.
**Original dataset span:** “The DCII check should show whether the applicant has any derogatory information in his or her military records.”
**Evidence excerpt:** “The DCII check should show whether the applicant has any derogatory information in his or her military records.”
**Reason:** The cited section describes the check’s purpose as revealing derogatory information in military records. It is not an eligibility or approval determination.
**Expected answer after qualification:** No correction needed; limit the claim to the military-record check.
**Access:** 2026-11-14; Dated official USCIS archive/fetch record dated 2026-11-14; relevant text and surrounding context inspected.

### 11. qa-4609d6be9c7d — Supported as written

**Question:** What does an 'Honorable' discharge characterization indicate about a service member's conduct?
**Source:** [Chapter 2 - One Year of Military Service during Peacetime (INA 328)](https://www.uscis.gov/policy-manual/volume-12-part-i-chapter-2) (`doc-dbcb4b30c441`), section: Discharge Characterization; Honorable discharge.
**Original dataset reference:** An Honorable discharge indicates the service member generally met the standards of acceptable conduct and performance of duty, or their service was so meritorious that any other characterization would be inappropriate.
**Original dataset span:** “The service member generally has met the standards of acceptable conduct and performance of duty for service members or is otherwise so meritorious that any other characterization would be inappropriate.”
**Evidence excerpt:** “The service member generally has met the standards of acceptable conduct and performance of duty, or is otherwise so meritorious that any other characterization would be inappropriate.”
**Reason:** The page defines the characterization using these alternative grounds. The reference preserves the “or” and does not claim naturalization is automatic.
**Expected answer after qualification:** No correction needed; preserve the alternative grounds.
**Access:** 2026-11-14; Dated official USCIS archive/fetch record dated 2026-11-14; relevant text and surrounding context inspected.

### 12. qa-c9e78deeb174 — Supported as written

**Question:** What was the last major addition to the Oath of Allegiance and when was it made?
**Source:** [Chapter 1 - Purpose and Background](https://www.uscis.gov/policy-manual/volume-12-part-j-chapter-1) (`doc-6afa448abbc0`), section: Historical Background; INA of 1952 addition to the Oath.
**Original dataset reference:** The last major addition to the Oath of Allegiance was added by the Immigration and Nationality Act of 1952, which provided the section about performing work of national importance under civilian direction.
**Original dataset span:** “The last major addition to the Oath of Allegiance was added by the Immigration and Nationality Act of 1952, which provided the section of the Oath of Allegiance about performing work of national importance under civilian direction.”
**Evidence excerpt:** “The last major addition was made by the Immigration and Nationality Act of 1952, adding work of national importance under civilian direction.”
**Reason:** The historical explanation in the linked chapter supports both the year/law and the clause identified.
**Expected answer after qualification:** No correction needed; retain the civilian-direction element.
**Access:** 2026-11-14; Dated official USCIS archive/fetch record dated 2026-11-14; relevant text and surrounding context inspected.

### 13. qa-210bd866a25c — Supported as written

**Question:** What is the definition of an 'exemption from military service' for naturalization purposes?
**Source:** [Chapter 4 - Permanent Bars to Naturalization](https://www.uscis.gov/policy-manual/volume-12-part-i-chapter-4) (`doc-40c9769bfb31`), section: Exemptions and Discharges from Military Service; definition.
**Original dataset reference:** An exemption from military service is either a permanent exemption from induction into the U.S. armed services or the release or discharge from military training or service in the U.S. armed forces.
**Original dataset span:** “An exemption from military service is either a permanent exemption from induction into the U.S. armed services or the release or discharge from military training or service in the U.S. armed forces.”
**Evidence excerpt:** “An exemption from military service is either a permanent exemption from induction or release or discharge from military training or service in the U.S. armed forces.”
**Reason:** The source provides both branches of the definition. Separate surrounding rules concerning alienage and service are not implied by this definition alone.
**Expected answer after qualification:** No correction needed; retain both branches and do not infer a universal citizenship bar.
**Access:** 2026-11-14; Dated official USCIS archive/fetch record dated 2026-11-14; relevant text and surrounding context inspected.

### 14. qa-4ecbcc440b1c — Supported with a scope/context qualification

**Question:** What is the difference between INA 328 and INA 329 regarding military service naturalization?
**Source:** [Chapter 3 - Military Service during Hostilities (INA 329)](https://www.uscis.gov/policy-manual/volume-12-part-i-chapter-3) (`doc-e2fd02d7b899`), section: Military Naturalization During Hostilities; INA 328 and INA 329 overview.
**Original dataset reference:** INA 328 is a general provision for alien military service members, while INA 329 is a special provision for service during specific designated periods of hostilities.
**Original dataset span:** “In addition to the general provisions for naturalization, including the provision for alien military service members under Immigration and Nationality Act (INA) section 328, Congress also provided a special provision for service during specific hostilities.”
**Evidence excerpt:** “INA 328 is a general provision for alien military service members; INA 329 is a special provision for service during specific designated periods of hostilities.”
**Reason:** The question asks for the high-level distinction, which the reference gives. It is not a complete eligibility comparison and must not imply the provisions share service-duration rules or guarantee eligibility.
**Expected answer after qualification:** Qualified: this is only the general-versus-designated-hostilities distinction; details and other requirements differ.
**Access:** 2026-11-14; New direct-curl capture, inspected for this review; web reader returned HTTP 403.

### 15. qa-4385aaa06495 — Supported with a scope/context qualification

**Question:** Under what general conditions does USCIS issue a Certificate of Naturalization?
**Source:** [Chapter 3 - Certificate of Naturalization](https://www.uscis.gov/policy-manual/volume-12-part-k-chapter-3) (`doc-4d490c4d821f`), section: Issuance of Certificate; general rule and oath/card exceptions.
**Original dataset reference:** USCIS issues a Certificate of Naturalization after an officer approves the Application for Naturalization and the applicant has taken the Oath of Allegiance.
**Original dataset span:** “In general, USCIS issues a Certificate of Naturalization after an officer approves the Application for Naturalization and the applicant has taken the Oath of Allegiance.”
**Evidence excerpt:** “In general, USCIS issues a Certificate of Naturalization after approval and the Oath of Allegiance.”
**Reason:** The reference accurately states the general rule, but “general” matters: the section describes medical-disability oath-waiver circumstances and PRC/ARC surrender requirements, including a lost/destroyed-card waiver.
**Expected answer after qualification:** Qualified: state the general approval-plus-oath rule and note the medical-disability oath waiver and applicable card-surrender/waiver rules when describing all cases.
**Access:** 2026-11-14; New direct-curl capture, inspected for this review; web reader returned HTTP 403.

### 16. qa-5c7a593817d2 — Supported as written

**Question:** Who will take the 2008 naturalization civics test?
**Source:** [Study for the Test](https://www.uscis.gov/citizenship/find-study-materials-and-resources/study-for-the-test) (`doc-5d78307a4098`), section: Study for the Test; 2008 civics test filing-date cutoff.
**Original dataset reference:** Aliens who file Form N-400 to apply for naturalization before Oct. 20, 2025, will take the 2008 naturalization civics test.
**Original dataset span:** “Aliens who file Form N-400 to apply for naturalization before Oct. 20, 2025, will take the 2008 naturalization civics test.”
**Evidence excerpt:** “Applicants filing Form N-400 before October 20, 2025 take the 2008 naturalization civics test.”
**Reason:** The linked USCIS study page states the filing-date cutoff; the question and reference use the filing date, not interview date. The answer is time-sensitive.
**Expected answer after qualification:** No correction needed for the stated cutoff; recheck the page for any later policy change before future use.
**Access:** 2026-11-14; New direct-curl capture, inspected for this review; web reader returned HTTP 403.

### 17. qa-f4ac028b6dd2 — Supported with a scope/context qualification

**Question:** What is the physical presence requirement under INA 319(a) for spouses of U.S. citizens residing in the United States?
**Source:** [Chapter 1 - Purpose and Background](https://www.uscis.gov/policy-manual/volume-12-part-g-chapter-1) (`doc-4f8fc2552e27`), section: INA 319(a), Table: Spouses of U.S. Citizens Residing in United States.
**Original dataset reference:** Under INA 319(a), the applicant must have been physically present in the United States for 18 months during the period of residence.
**Original dataset span:** “18 months during period of residence”
**Evidence excerpt:** “18 months during period of residence.”
**Reason:** The reference gives the physical-presence row. The same table places it in the INA 319(a) category and separately lists three years of residence after becoming an LPR; physical presence is not continuous residence or marital union.
**Expected answer after qualification:** Qualified: at least 18 months of physical presence during the relevant three-year residence period under the INA 319(a) domestic-spouse category.
**Access:** 2026-11-14; New direct-curl capture, inspected for this review; web reader returned HTTP 403.

### 18. qa-f074b4c28745 — Supported with a scope/context qualification

**Question:** What happens if an applicant refuses to explain the basis of their objection to the oath during the interview?
**Source:** [Chapter 3 - Oath of Allegiance Modifications and Waivers](https://www.uscis.gov/policy-manual/volume-12-part-j-chapter-3) (`doc-df824279f137`), section: Oath Modification; interview opportunity and following RFE paragraph.
**Original dataset reference:** If the applicant refuses to explain the basis of the objection, the officer should provide the applicant an additional opportunity to establish eligibility for the modification before concluding the interview, and should issue a Request for Evidence (RFE).
**Original dataset span:** “or the applicant refuses to explain the basis of the objection, the officer should provide the applicant an additional opportunity to establish eligibility for the modification before concluding the interview.”
**Evidence excerpt:** “If the applicant refuses to explain the basis, the officer should provide an additional opportunity to establish eligibility before concluding the interview.”
**Reason:** The dataset source span directly supports the additional interview opportunity. The RFE direction appears in the following paragraph, not in that span; the linked full page supports the combined reference answer.
**Expected answer after qualification:** Qualified: the span alone omits the RFE; the full section adds an RFE opportunity to submit evidence. Do not describe this as automatic approval.
**Access:** 2026-11-14; New direct-curl capture, inspected for this review; web reader returned HTTP 403.

### 19. qa-071175958a7d — Supported as written

**Question:** How long must an alien have served in the U.S. armed forces to qualify for peacetime naturalization?
**Source:** [Chapter 2 - One Year of Military Service during Peacetime (INA 328)](https://www.uscis.gov/policy-manual/volume-12-part-i-chapter-2) (`doc-dbcb4b30c441`), section: Peacetime Naturalization; honorable-service requirement.
**Original dataset reference:** The alien must have served honorably at any time in the U.S. armed forces for a period or periods totaling at least 1 year.
**Original dataset span:** “The alien must have served honorably at any time in the U.S. armed forces for a period or periods totaling at least 1 year.”
**Evidence excerpt:** “The applicant must have served honorably for periods totaling at least 1 year.”
**Reason:** The question asks the duration for peacetime service naturalization, and the page states at least one year of honorable service. Other statutory criteria remain outside this duration answer.
**Expected answer after qualification:** No correction needed; service duration alone does not establish eligibility.
**Access:** 2026-11-14; Dated official USCIS archive/fetch record dated 2026-11-14; relevant text and surrounding context inspected.

### 20. qa-a9d1c7e47d92 — Supported as written

**Question:** How long does an applicant have to file a hearing request after receiving a denial notice?
**Source:** [Chapter 6 - USCIS Hearing and Judicial Review](https://www.uscis.gov/policy-manual/volume-12-part-b-chapter-6) (`doc-1662f655ac19`), section: Hearing before an Immigration Officer; filing deadline.
**Original dataset reference:** The applicant or authorized representative must file the request with USCIS within 30 days after the applicant receives the notice of denial.
**Original dataset span:** “The applicant or authorized representative must file the request with USCIS within 30 days after the applicant receives the notice of denial.”
**Evidence excerpt:** “The applicant or authorized representative must file the request with USCIS within 30 days after receipt of the denial notice.”
**Reason:** The answer gives the filing deadline asked for. The page separately discusses scheduling the hearing; that is not part of this 30-day filing answer.
**Expected answer after qualification:** No correction needed; distinguish filing the request from when the hearing is held.
**Access:** 2026-11-14; Dated official USCIS archive/fetch record dated 2026-11-14; relevant text and surrounding context inspected.

## Four qualifications already flagged in Stage 5A

- `qa-dcd6fb096bd9`: ICE referral applies to the specific possible military-basis revocation cases described in the preceding section (including the relevant naturalization date and early other-than-honorable separation); it is not a general rule for all revocations.
- `qa-4ecbcc440b1c`: the answer gives only the broad INA 328 general-provision / INA 329 designated-hostilities distinction, not a complete comparison of eligibility or service-duration requirements.
- `qa-4385aaa06495`: certificate issuance after approval and oath is the general rule; the page also has a medical-disability oath-waiver provision and PRC/ARC surrender rules with a lost/destroyed-card waiver.
- `qa-f074b4c28745`: the quoted dataset span supports another opportunity during the interview; the RFE instruction is in the following paragraph. The linked full section supports the combined expected answer.

## Additional context qualifications found

- `qa-be519f64475f`: the reference omits the “sufficient cause” threshold. The court or USCIS District Director may consider compelling or humanitarian circumstances; expedited ceremony is discretionary.
- `qa-f4ac028b6dd2`: 18 months of physical presence is during the applicable INA 319(a) residence period (the table separately lists three years after LPR status). The numeric reference is correct but benefits from that context.

No reference required correction at the question’s stated scope, and none was unverifiable from the available snapshot/current captures. This does not certify every answer as complete for broader questions.

## Attribution and verification

OpenAI Codex (coding assistant) read the saved question selection, original dataset references/spans, preliminary expected notes, official-page archive/fetch records, and relevant current official material. For seven pages, the assistant made a direct request after the web reader returned 403, then inspected the relevant section and surrounding text; all seven returned HTTP 200. The other rows were checked against the dated November 14 official archives and fetch records. This is an assisted preliminary source verification. Student confirmation remains pending; it is not independent student evaluation. No model was run and no answer-generation result was assessed.
