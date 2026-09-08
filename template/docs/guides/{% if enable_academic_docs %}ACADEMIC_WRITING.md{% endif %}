# Academic Writing (學術寫作規範)

**Version**: 2.0.0  
**Module**: ACADEMIC_WRITING  
**Loading**: Conditional (`project.type = "academic"`)  
**Purpose**: Academic writing conventions, structure, and style guidelines for research projects.

---

## Overview

This guide defines **academic writing standards** for research projects using this scaffolding. It covers paper structure, writing style, argumentation, and ethical considerations.

**Scope**:
- ✅ Academic writing principles
- ✅ Research paper structure
- ✅ Argumentation and evidence
- ✅ Writing style and clarity
- ✅ Ethical considerations
- ❌ Citation formats (see CITATION_MANAGEMENT module)

**Loading Trigger**: `project.type = "academic"`, keywords: "paper", "thesis", "research", "citation", "academic"

---

## Core Principles

### 1. Clarity and Precision

**Academic writing prioritizes clarity over literary style.**

✅ **Good** (clear, precise):
```
This study examines the impact of code review frequency on software 
defect rates in open-source projects (N=150). We hypothesize that 
projects with daily code reviews exhibit 30% fewer critical bugs 
compared to those with weekly reviews.
```

❌ **Bad** (vague, imprecise):
```
This research looks at how code review affects bugs. We think more 
reviews might help reduce problems in software projects.
```

**Why**: Precision enables reproducibility and verification.

### 2. Objectivity

**Present findings without personal bias or emotional language.**

✅ **Good**:
```
The results indicate a statistically significant correlation 
(r=0.72, p<0.01) between team size and code review duration.
```

❌ **Bad**:
```
Obviously, larger teams take forever to complete code reviews, which 
is a huge problem that everyone knows about.
```

### 3. Evidence-Based Claims

**Every claim requires supporting evidence.**

✅ **Good**:
```
Previous research demonstrates that test-driven development reduces 
defect density by 40-80% (Erdogmus et al., 2005; Nagappan et al., 2008).
```

❌ **Bad**:
```
Everyone knows TDD produces better code quality.
```

### 4. Academic Honesty

**Attribute all ideas, quotes, and data to original sources.**

- ✅ Cite direct quotes
- ✅ Paraphrase with citation
- ✅ Cite data sources
- ❌ Never plagiarize
- ❌ Never fabricate data

---

## Research Paper Structure

### IMRAD Format (Standard)

**Structure**: Introduction, Methods, Results, and Discussion

```
Title Page
Abstract
1. Introduction
   1.1 Background
   1.2 Research Question
   1.3 Contribution
2. Related Work
3. Methodology
   3.1 Research Design
   3.2 Data Collection
   3.3 Analysis Methods
4. Results
   4.1 Quantitative Findings
   4.2 Qualitative Findings
5. Discussion
   5.1 Interpretation
   5.2 Implications
   5.3 Limitations
6. Conclusion
7. References
Appendices (optional)
```

### Section Guidelines

#### Title

**Rule**: Informative, concise, keyword-rich.

✅ **Good**:
```
The Impact of Code Review Frequency on Software Defect Rates: 
An Empirical Study of 150 Open-Source Projects
```

❌ **Bad**:
```
Code Review Study
```

**Guidelines**:
- 10-15 words optimal
- Include key variables
- Avoid jargon in titles
- No abbreviations (except well-known)

#### Abstract

**Rule**: Self-contained summary (150-250 words).

**Structure**:
1. **Background** (1-2 sentences)
2. **Objective** (1 sentence)
3. **Methods** (2-3 sentences)
4. **Results** (2-3 sentences)
5. **Conclusion** (1 sentence)

**Example**:
```
Background: Code review practices vary widely across software projects, 
yet their impact on defect rates remains understudied. 

Objective: This study examines the relationship between code review 
frequency and software defect rates in open-source projects.

Methods: We analyzed 150 GitHub repositories over 12 months, measuring 
review frequency (daily vs. weekly) and defect rates (critical bugs per 
1000 lines of code). Linear regression and ANOVA were used for analysis.

Results: Projects with daily code reviews exhibited 32% fewer critical 
defects (M=2.3, SD=0.8) compared to weekly reviews (M=3.4, SD=1.2), 
t(148)=5.67, p<0.001. Team size moderated this effect (β=0.18, p=0.03).

Conclusion: Frequent code reviews significantly reduce software defects, 
suggesting daily review cycles as a best practice for quality assurance.

Keywords: code review, software defects, open-source, empirical study
```

#### Introduction

**Rule**: Establish context → identify gap → state contribution.

**Structure** (3-4 pages):
1. **Opening**: Broad context (1-2 paragraphs)
2. **Problem Statement**: What's unsolved? (2-3 paragraphs)
3. **Research Question**: Specific question (1 paragraph)
4. **Contribution**: What's new? (1-2 paragraphs)
5. **Organization**: Paper roadmap (1 paragraph)

**Example Opening**:
```
Software quality assurance relies on multiple practices, including 
testing, static analysis, and code review (Fagan, 1976; Bacchelli & 
Bird, 2013). While testing identifies runtime errors, code review 
addresses design flaws and maintainability issues (McIntosh et al., 
2014). Despite widespread adoption, the optimal code review frequency 
remains unclear, with practices ranging from continuous review to 
weekly batches (Rigby & Bird, 2013).

[Continue with problem statement, research question, contribution...]
```

#### Related Work

**Rule**: Critical synthesis, not exhaustive summary.

**Organization Options**:
- **Chronological**: Trace evolution of ideas
- **Thematic**: Group by topic/theme
- **Methodological**: Organize by research method
- **Hybrid**: Combine approaches

**Example** (thematic):
```
## 2. Related Work

### 2.1 Code Review Practices
Early code review research focused on formal inspections (Fagan, 1976), 
where teams met to review code synchronously. Recent work examines 
modern, tool-supported review (Bacchelli & Bird, 2013; Rigby & Bird, 
2013), finding that asynchronous review dominates open-source projects.

### 2.2 Code Review and Defect Detection
Several studies link code review to defect reduction. Kemerer and 
Paulk (2009) found 30-40% defect reduction in inspected code. 
McIntosh et al. (2014) showed review coverage correlates with lower 
post-release defects (r=-0.46). However, review frequency's role 
remains underexplored.

### 2.3 Research Gap
While prior work establishes code review's benefits, no large-scale 
study examines review frequency's impact. This paper addresses this 
gap by analyzing 150 projects over 12 months.
```

#### Methodology

**Rule**: Enable reproducibility.

**Essential Details**:
- Research design (experimental, survey, case study)
- Participants/sample (size, selection criteria)
- Materials/instruments (tools, questionnaires)
- Procedure (step-by-step)
- Data analysis (statistical tests, software)
- Ethical approval (IRB number if applicable)

**Example**:
```
## 3. Methodology

### 3.1 Research Design
This observational study employs a correlational design to examine the 
relationship between code review frequency (independent variable) and 
software defect rates (dependent variable) in open-source projects.

### 3.2 Sample Selection
We selected 150 GitHub repositories meeting the following criteria:
- ≥100 commits in past 12 months
- ≥3 contributors
- Active issue tracking
- Clear code review policy documented in CONTRIBUTING.md

Projects were stratified by language (JavaScript: 50, Python: 50, 
Java: 50) to control for language-specific effects.

### 3.3 Data Collection
Data were collected via GitHub API (v3) over 12 months (Jan-Dec 2025):
- Review frequency: Daily average of merged pull requests
- Defect rates: Critical bugs per 1000 LOC (labeled "bug" + "critical")
- Team size: Number of unique contributors
- Project age: Months since first commit

### 3.4 Analysis
Linear regression analyzed review frequency's effect on defects, 
controlling for team size and project age. ANOVA compared daily vs. 
weekly review groups. Significance threshold: α=0.05. Analysis conducted 
in R (v4.3.0) using lm() and aov() functions.
```

#### Results

**Rule**: Present findings without interpretation.

**Guidelines**:
- Report all results (including null findings)
- Use tables/figures for complex data
- Include descriptive statistics (M, SD, range)
- Report inferential statistics (t, F, p, effect size)
- State assumptions checked (normality, homoscedasticity)

**Example**:
```
## 4. Results

### 4.1 Descriptive Statistics
Table 1 presents descriptive statistics for all variables. Mean defect 
rate was 2.85 bugs per 1000 LOC (SD=1.15, range: 0.5-6.2). Review 
frequency averaged 4.3 reviews per day (SD=2.1, range: 0.8-12.5).

[Table 1: Descriptive Statistics]

### 4.2 Regression Analysis
Linear regression (Table 2) revealed review frequency significantly 
predicted defect rates (β=-0.42, t=-6.78, p<0.001), explaining 28% of 
variance (R²=0.28, adjusted R²=0.26). Each additional daily review 
reduced defects by 0.15 bugs per 1000 LOC (95% CI: [-0.19, -0.11]).

Team size showed a significant moderating effect (β=0.18, p=0.03), 
suggesting larger teams benefit more from frequent reviews.

[Table 2: Regression Results]

### 4.3 Group Comparison
ANOVA compared daily review (n=87) vs. weekly review (n=63) projects 
(Figure 1). Daily review projects exhibited significantly lower defect 
rates (M=2.3, SD=0.8) than weekly review projects (M=3.4, SD=1.2), 
F(1,148)=32.15, p<0.001, η²=0.18 (large effect).

[Figure 1: Defect Rates by Review Frequency]
```

#### Discussion

**Rule**: Interpret findings, acknowledge limitations, suggest future work.

**Structure**:
1. **Summary**: Restate key findings (1 paragraph)
2. **Interpretation**: Explain what results mean (2-3 paragraphs)
3. **Comparison**: Relate to prior work (1-2 paragraphs)
4. **Implications**: Practical/theoretical impact (1-2 paragraphs)
5. **Limitations**: Study weaknesses (1 paragraph)
6. **Future Work**: Next research steps (1 paragraph)

**Example**:
```
## 5. Discussion

### 5.1 Summary of Findings
This study found that code review frequency significantly impacts 
software defect rates, with daily reviews reducing critical bugs by 
32% compared to weekly reviews. Team size moderated this effect, 
suggesting larger teams benefit disproportionately from frequent review.

### 5.2 Interpretation
The negative correlation between review frequency and defects likely 
stems from faster feedback loops. Daily reviews catch errors before 
they cascade, reducing technical debt accumulation (Cunningham, 1992). 
Weekly reviews, conversely, allow defects to compound, increasing 
remediation cost (Boehm & Basili, 2001).

### 5.3 Relation to Prior Work
Our findings align with McIntosh et al.'s (2014) conclusion that review 
coverage reduces defects. However, we extend their work by demonstrating 
frequency's independent effect beyond coverage. This suggests review 
timing matters as much as thoroughness.

### 5.4 Implications
Practically, our results recommend daily code review cycles for quality-
critical projects. Theoretically, this supports continuous integration's 
fast-feedback principle (Fowler, 2006), suggesting code review should 
integrate with CI/CD pipelines.

### 5.5 Limitations
This study has three limitations. First, observational design precludes 
causal claims; experimental studies should test causality. Second, GitHub 
data may not generalize to enterprise settings. Third, defect labeling 
relies on maintainer judgment, introducing subjectivity.

### 5.6 Future Work
Future research should: (1) conduct randomized controlled trials varying 
review frequency, (2) examine review depth vs. frequency tradeoffs, and 
(3) investigate review automation's moderating role.
```

#### Conclusion

**Rule**: Brief summary + take-home message.

**Length**: 1 paragraph (4-6 sentences)

**Example**:
```
## 6. Conclusion

This study examined code review frequency's impact on software defects 
in 150 open-source projects. Results indicate daily reviews reduce 
critical bugs by 32% compared to weekly reviews (p<0.001). Team size 
moderates this effect, with larger teams benefiting more. These findings 
suggest daily code review cycles as best practice for quality assurance. 
Future experimental work should test causality and explore review depth 
tradeoffs.
```

---

## Writing Style

### Verb Tense

**Rule**: Follow discipline conventions.

| Section | Tense | Example |
|---------|-------|---------|
| **Abstract** | Past (methods/results) | "We analyzed 150 projects and found..." |
| **Introduction** | Present (general truths) | "Software quality assurance relies on..." |
| **Related Work** | Past or present perfect | "Smith (2020) demonstrated..." or "Research has shown..." |
| **Methods** | Past | "We collected data via GitHub API" |
| **Results** | Past | "Results revealed a significant correlation" |
| **Discussion** | Present (interpretation) | "These findings suggest..." |
| **Conclusion** | Present | "This study demonstrates..." |

### Voice

**Rule**: Prefer active voice; use passive for objectivity.

✅ **Active** (more direct):
```
We analyzed 150 repositories using linear regression.
```

✅ **Passive** (more objective):
```
One hundred fifty repositories were analyzed using linear regression.
```

**Guideline**: Active for methods, passive for results/conclusions.

### Person

**Rule**: Varies by discipline and journal.

| Style | Disciplines | Example |
|-------|-------------|---------|
| **First person plural** ("we") | STEM, social sciences | "We hypothesize that..." |
| **Third person** ("the authors") | Traditional humanities | "The authors propose..." |
| **Passive/impersonal** | Natural sciences (older) | "It is proposed that..." |

**Modern trend**: First person plural (we/our) increasingly accepted.

### Hedging

**Rule**: Use hedging language for claims, not for established facts.

**Hedging words**: "suggest", "indicate", "may", "appear to", "likely"

✅ **Good**:
```
These results suggest that daily reviews may reduce defects.
```

❌ **Too strong**:
```
These results prove that daily reviews eliminate defects.
```

❌ **Too weak**:
```
We found some possible relationships that might potentially indicate...
```

---

## Argumentation

### Claim-Evidence-Reasoning

**Structure**: Claim → Evidence → Reasoning

**Example**:
```
[Claim] Code review frequency impacts software quality.

[Evidence] In our study, daily review projects exhibited 32% fewer 
defects (M=2.3) compared to weekly review projects (M=3.4), F(1,148)=
32.15, p<0.001.

[Reasoning] This difference likely stems from faster feedback loops, 
which prevent error cascading and reduce technical debt accumulation 
(Cunningham, 1992).
```

### Logical Fallacies to Avoid

| Fallacy | Description | Example |
|---------|-------------|---------|
| **Hasty generalization** | Broad claim from small sample | "5 projects showed improvement, so all projects will" |
| **False cause** | Assumes correlation = causation | "Reviews increased, defects decreased → reviews caused decrease" |
| **Appeal to authority** | Relies on authority, not evidence | "As Knuth said, optimization is evil, so we don't optimize" |
| **Straw man** | Attacks distorted opponent argument | "Critics claim reviews are useless, but..." |
| **Ad hominem** | Attacks person, not argument | "Smith's study is flawed because he's inexperienced" |

### Counterarguments

**Rule**: Acknowledge and address opposing views.

**Example**:
```
Critics might argue that daily reviews impose excessive overhead, 
reducing developer productivity (Rigby & Bird, 2013). However, our 
data show no significant correlation between review frequency and 
commit velocity (r=0.08, p=0.32), suggesting reviews don't slow 
development when properly tooled.
```

---

## Tables and Figures

### When to Use

**Table**: Precise numerical values, comparisons

**Figure**: Trends, distributions, relationships

**Neither**: Simple comparisons (state in text)

### Table Guidelines

**Rule**: Self-explanatory with caption.

**Example**:
```
Table 1
Descriptive Statistics for Study Variables

Variable              M      SD    Min    Max    N
Review frequency     4.3    2.1    0.8   12.5   150
Defect rate          2.85   1.15   0.5    6.2   150
Team size            8.7    4.3    3.0   25.0   150
Project age (months) 36.2  18.5   12.0   84.0   150

Note. Review frequency = daily average merged PRs. Defect rate = 
critical bugs per 1000 LOC. All projects N=150.
```

### Figure Guidelines

**Rule**: Clear axes, legend, caption.

**Example Caption**:
```
Figure 1. Defect rates by code review frequency. Daily review projects 
(n=87) exhibited significantly lower defect rates than weekly review 
projects (n=63), F(1,148)=32.15, p<0.001. Error bars represent ±1 SE.
```

---

## Common Mistakes

### 1. Overclaiming

❌ **Overclaim**:
```
This study proves that daily reviews are superior.
```

✅ **Appropriate**:
```
This study provides evidence that daily reviews reduce defects in 
open-source projects.
```

### 2. Missing Citations

❌ **Missing**:
```
Code review improves quality.
```

✅ **Cited**:
```
Code review improves quality (Fagan, 1976; Bacchelli & Bird, 2013).
```

### 3. Results in Discussion

❌ **Results in discussion**:
```
[In Discussion] We found that daily reviews reduced defects by 32%.
```

✅ **Interpretation in discussion**:
```
[In Discussion] The 32% defect reduction (reported in Results) suggests 
daily reviews provide faster feedback, preventing error cascading.
```

### 4. Vague Language

❌ **Vague**:
```
Many projects used code review, and some had fewer bugs.
```

✅ **Precise**:
```
87 of 150 projects (58%) used daily code review, and these exhibited 
32% fewer defects (M=2.3 vs. 3.4, p<0.001).
```

---

## Ethical Considerations

### Plagiarism

**Definition**: Using others' work without attribution.

**Types**:
- **Verbatim**: Copying text word-for-word
- **Paraphrasing**: Rewording without citation
- **Self-plagiarism**: Reusing your own published work

**Prevention**:
- ✅ Always cite sources
- ✅ Use quotation marks for direct quotes
- ✅ Paraphrase + cite
- ✅ Use plagiarism detection tools (Turnitin, iThenticate)

### Data Integrity

**Rules**:
- ❌ Never fabricate data
- ❌ Never falsify results
- ❌ Never selectively report (omit inconvenient findings)
- ✅ Report all results, including null findings
- ✅ Correct errors immediately if found post-publication

### Authorship

**Rule**: Authorship based on substantial contribution.

**ICMJE Criteria** (all 4 required):
1. Substantial contribution to conception/design/acquisition/analysis
2. Drafting or revising manuscript critically
3. Approval of final version
4. Agreement to be accountable for all aspects

**Not sufficient alone**: Data collection, funding, supervision

### Conflicts of Interest

**Disclose**:
- Financial interests (funding, stock ownership)
- Personal relationships (family, close collaborators)
- Institutional affiliations

**Example Disclosure**:
```
This research was funded by XYZ Corporation. Author A is a paid 
consultant for XYZ Corp. Authors B and C declare no conflicts of interest.
```

---

## Revision Checklist

Before submission, verify:

**Content**:
- [ ] Research question clearly stated
- [ ] Methods enable reproducibility
- [ ] Results answer research question
- [ ] Discussion interprets findings
- [ ] Limitations acknowledged
- [ ] All claims supported by evidence

**Citations**:
- [ ] All sources cited
- [ ] Citation style consistent (see CITATION_MANAGEMENT)
- [ ] In-text citations match reference list
- [ ] No missing references

**Writing**:
- [ ] Clear, concise prose
- [ ] Correct verb tense per section
- [ ] Logical flow between paragraphs
- [ ] No jargon without definition
- [ ] Spelling and grammar checked

**Tables/Figures**:
- [ ] All tables/figures referenced in text
- [ ] Captions self-explanatory
- [ ] Data match manuscript statistics
- [ ] High-resolution figures

**Formatting**:
- [ ] Follows journal/conference guidelines
- [ ] Correct citation format
- [ ] Page numbers present
- [ ] Line numbers (if required)

---

## Journal/Conference Submission

### Choosing a Venue

**Factors**:
- **Scope**: Does your topic fit?
- **Impact factor**: Citation metrics (use with caution)
- **Acceptance rate**: 10-30% typical for top venues
- **Review process**: Single/double-blind, peer review
- **Timeline**: Submission to decision (3-6 months typical)

**Resources**:
- Journal finder tools (Elsevier Journal Finder, Springer Journal Suggester)
- Conference rankings (CORE, Qualis)
- Ask advisor for recommendations

### Submission Process

1. **Prepare manuscript**: Follow author guidelines exactly
2. **Cover letter**: Briefly summarize contribution
3. **Suggest reviewers**: 3-5 experts in field (optional)
4. **Submit**: Via journal/conference system
5. **Await decision**: 3-6 months typical
6. **Respond to reviews**: Address all comments

### Responding to Reviews

**Rule**: Polite, point-by-point responses.

**Template**:
```
We thank the reviewers for their thoughtful comments. Below, we address 
each point raised.

Reviewer 1, Comment 1: "The sample size seems small."

Response: We agree that a larger sample would strengthen conclusions. 
We have added text to Limitations (p. 15) acknowledging this. We also 
clarified that our power analysis (α=0.05, β=0.20) indicates N=150 
provides adequate power (0.95) to detect medium effects (d=0.5).

[Continue for all comments]
```

---

## Related Documentation

- **[CITATION_MANAGEMENT](./CITATION_MANAGEMENT.md)** - Citation styles (APA, MLA, Chicago, IEEE)
- **[TERMINOLOGY](./terminology/academic/)** - Academic terminology
- **[STYLE_GUIDE](./STYLE_GUIDE.md)** - General writing conventions

---

## Resources

### Writing Guides

- **Strunk & White**: The Elements of Style (classic)
- **APA Manual**: Publication Manual (7th ed.) for social sciences
- **Turabian**: A Manual for Writers (humanities)
- **Day & Gastel**: How to Write and Publish a Scientific Paper

### Tools

- **Grammar**: Grammarly, ProWritingAid
- **Plagiarism**: Turnitin, iThenticate
- **Reference Management**: Zotero, Mendeley, EndNote
- **LaTeX**: Overleaf (collaborative writing)
- **Markdown**: Pandoc (convert to Word/PDF)

### Communities

- **Stack Exchange Academia**: Academic writing questions
- **Reddit r/AskAcademia**: Peer advice
- **Writing centers**: University resources

---

**Version**: 2.0.0  
**Last Updated**: 2026-03-16  
**Maintainer**: my-vibe-scaffolding template
