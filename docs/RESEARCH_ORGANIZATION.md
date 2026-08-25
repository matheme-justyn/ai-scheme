# RESEARCH ORGANIZATION

**Status**: Active | **Domain**: Academic  
**Related Modules**: LITERATURE_REVIEW, ACADEMIC_WRITING, DOCUMENT_STRUCTURE

## Purpose

This module provides systems and best practices for organizing research materials, managing notes, tracking sources, maintaining version control for research documents, and structuring research workflows for academic projects.

## When to Use This Module

- Starting a new research project
- Managing large volumes of research materials
- Collaborating on research with team members
- Preparing for thesis or dissertation writing
- Organizing literature review materials
- Tracking research progress and milestones

---

## 1. File Organization

### 1.1 Directory Structure

```
my-research-project/
├── 01-literature/
│   ├── pdf/
│   │   ├── theory/
│   │   ├── methods/
│   │   └── empirical/
│   ├── notes/
│   └── summaries/
├── 02-data/
│   ├── raw/
│   ├── processed/
│   └── analysis/
├── 03-writing/
│   ├── drafts/
│   ├── revisions/
│   └── final/
├── 04-presentations/
├── 05-admin/
│   ├── ethics/
│   ├── funding/
│   └── correspondence/
└── README.md
```

### 1.2 Naming Conventions

```
✅ GOOD: Descriptive, consistent names
Smith2024_IntermittentFasting_RCT.pdf
2026-03-16_Interview_Participant05_Transcript.docx
DataAnalysis_v3_2026-03-16.R

❌ BAD: Ambiguous names
paper1.pdf
interview.docx
analysis_final_FINAL_v2_really_final.R
```

**Naming Pattern**:
```
[Author/Date]_[Topic]_[Type]_[Version].[ext]

Examples:
Jones2023_DiabetesManagement_SystematicReview.pdf
2026-03-15_FocusGroup_Session02_Notes.docx
Survey_Results_Cleaned_v2.csv
```

---

## 2. Note-Taking Systems

### 2.1 Zettelkasten Method

**Concept**: Atomic notes linked together  
**Tools**: Obsidian, Roam Research, Notion

```
Example Note Structure:

# 202603161430 - Intermittent Fasting Effects
Tags: #diabetes #intervention #metabolism

## Content
Intermittent fasting improves insulin sensitivity through 
multiple mechanisms including autophagy and mitochondrial 
function enhancement.

## Links
- [[202603151200 - Insulin Resistance Mechanisms]]
- [[202603141530 - Autophagy in Metabolic Health]]

## Source
Smith et al. (2024) - Diabetes Care
```

**Benefits**:
- Easily discover connections between concepts
- Build knowledge incrementally
- Facilitates writing (assemble notes into manuscripts)

### 2.2 Cornell Note-Taking

```
┌─────────────────────────────────────────┬──────────────┐
│ Notes (Right Column - 2/3 width)        │ Cues (Left)  │
│                                         │              │
│ Main ideas, details, diagrams          │ Keywords     │
│                                         │ Questions    │
│                                         │ Prompts      │
├─────────────────────────────────────────┴──────────────┤
│ Summary (Bottom)                                       │
│ 2-3 sentence summary of main points                   │
└────────────────────────────────────────────────────────┘
```

### 2.3 Literature Summary Template

```markdown
# [Author] ([Year]) - [Title]

## Citation
Smith, J., Jones, A., & Brown, K. (2024). Effects of intermittent 
fasting on glycemic control. *Diabetes Care*, 47(3), 234-245.

## Research Question
Does intermittent fasting improve glycemic control in adults with 
type 2 diabetes?

## Methods
- Design: RCT
- Sample: 120 adults with T2D
- Intervention: 16:8 time-restricted eating
- Duration: 12 weeks

## Key Findings
1. HbA1c reduced by 0.8% (p < 0.001)
2. Weight loss: 4.2 kg (p < 0.001)
3. High adherence: 85%

## Strengths
- Rigorous RCT design
- Adequate sample size
- Objective outcome measures

## Limitations
- Short duration (12 weeks)
- Single-center study
- Participants not blinded

## Relevance to My Research
Supports my hypothesis that dietary interventions can improve 
metabolic health. Provides benchmark for effect sizes.

## Questions/Future Work
- Long-term effects unclear
- Optimal protocol unknown
```

---

## 3. Reference Management

### 3.1 Zotero Workflow

```
1. Install Zotero + browser connector
2. Create collections:
   - Theory
   - Methods
   - Empirical Studies
   - Background

3. Import papers:
   - Click browser connector on paper page
   - Auto-imports metadata + PDF
   - Review and correct metadata

4. Tagging system:
   - #read
   - #to-read
   - #cited-in-chapter2
   - #methods-relevant

5. Notes:
   - Add notes to each item
   - Link related items
   - Extract highlights

6. Export:
   - Generate bibliography in any style
   - Sync across devices
```

### 3.2 Citation Key Format

```
AuthorYear pattern (BibTeX):

smith2024  (single author)
smith-jones2024  (two authors)
smith-etal2024  (three or more authors)

smith2024a  (multiple publications by same author in same year)
smith2024b
```

---

## 4. Version Control for Research

### 4.1 Git for Research Documents

```bash
# Initialize repository
git init my-research

# Create .gitignore
cat > .gitignore << EOL
# Temporary files
*.tmp
*~
.DS_Store

# Large data files (use Git LFS instead)
*.csv
*.dat
data/raw/*

# Build outputs
*.aux
*.log
*.out
EOL

# Track changes
git add manuscript.tex
git commit -m "Initial draft of introduction"

# Branching for revisions
git checkout -b revision-reviewer2
# Make changes addressing reviewer comments
git commit -m "Address Reviewer 2 comments on methods"
git checkout main
git merge revision-reviewer2
```

### 4.2 Manuscript Versioning

```
✅ GOOD: Semantic versioning for manuscripts
v0.1.0 - First complete draft
v0.2.0 - Revised after advisor feedback
v0.3.0 - Submitted to journal
v0.3.1 - Minor corrections
v1.0.0 - Accepted version
v1.0.1 - Final published version

❌ BAD: Filename versioning
manuscript_v1.docx
manuscript_v2.docx
manuscript_final.docx
manuscript_final_v2.docx
manuscript_FINAL_REALLY.docx
```

### 4.3 Collaborative Writing

```
# Using Git branches for co-authors
Author A: git checkout -b intro-section
Author B: git checkout -b methods-section

# Merge branches when sections complete
git checkout main
git merge intro-section
git merge methods-section

# Resolve conflicts if necessary
```

---

## 5. Data Management

### 5.1 Raw Data

```
✅ BEST PRACTICE: Keep raw data immutable
data/
├── raw/              # NEVER EDIT
│   ├── README.md     # Document data source, collection date
│   └── survey_responses_2026-03-01.csv
├── processed/        # Cleaned data
│   └── survey_cleaned_2026-03-15.csv
└── analysis/         # Analysis outputs
    └── descriptive_stats.csv
```

**README.md for raw data**:
```markdown
# Raw Data Documentation

## File: survey_responses_2026-03-01.csv

**Source**: Online survey via Qualtrics  
**Collection period**: 2026-02-01 to 2026-02-28  
**N responses**: 450  
**Variables**: 
- ID: Participant identifier
- Age: Age in years
- Gender: Self-reported gender (1=Male, 2=Female, 3=Other)
- Q1-Q20: Likert scale responses (1=Strongly Disagree to 5=Strongly Agree)

**Missing data**: Coded as -999  
**Notes**: 23 incomplete responses excluded during processing
```

### 5.2 Data Processing Scripts

```R
# data_cleaning.R
# Author: John Smith
# Date: 2026-03-15
# Purpose: Clean and prepare survey data for analysis

# Load libraries
library(tidyverse)

# Load raw data (READ ONLY)
raw_data <- read_csv("data/raw/survey_responses_2026-03-01.csv")

# Data cleaning steps
cleaned_data <- raw_data %>%
  # Remove incomplete responses
  filter(complete.cases(.)) %>%
  # Recode missing values
  mutate(across(Q1:Q20, ~na_if(., -999))) %>%
  # Create age groups
  mutate(age_group = cut(Age, breaks = c(0, 30, 50, 100)))

# Save cleaned data
write_csv(cleaned_data, "data/processed/survey_cleaned_2026-03-15.csv")

# Document changes
cat("Raw N:", nrow(raw_data), "\n")
cat("Cleaned N:", nrow(cleaned_data), "\n")
cat("Excluded:", nrow(raw_data) - nrow(cleaned_data), "\n")
```

---

## 6. Task Management

### 6.1 Research Todo System

```markdown
# Research Tasks

## This Week (2026-03-16 to 2026-03-22)
- [ ] Finish literature review section
- [ ] Run power analysis for sample size
- [ ] Draft methods section
- [ ] Schedule meeting with advisor

## This Month (March 2026)
- [ ] Complete data collection
- [ ] Submit ethics amendment
- [ ] Write results section
- [ ] Prepare conference abstract

## This Quarter (Q1 2026)
- [ ] Complete first full draft
- [ ] Receive advisor feedback
- [ ] Revise introduction and discussion
- [ ] Submit to journal
```

### 6.2 Project Timeline (Gantt Chart)

```
Jan 2026: Literature Review ████████████
Feb 2026: Methods Development     ████████████
Mar 2026: Data Collection              ████████████
Apr 2026: Data Analysis                     ████████████
May 2026: Writing                                ████████████
Jun 2026: Revisions                                  ████████
```

### 6.3 Milestone Tracking

```markdown
# Research Milestones

| Milestone | Target Date | Status | Actual Date |
|-----------|-------------|--------|-------------|
| Literature review complete | 2026-01-31 | ✅ Done | 2026-02-05 |
| Ethics approval | 2026-02-15 | ✅ Done | 2026-02-12 |
| Data collection start | 2026-03-01 | ✅ Done | 2026-03-01 |
| Data collection end | 2026-04-30 | 🔄 In Progress | - |
| Analysis complete | 2026-05-31 | ⏳ Pending | - |
| First draft | 2026-06-30 | ⏳ Pending | - |
| Submission | 2026-08-01 | ⏳ Pending | - |
```

---

## 7. Backup Strategy

### 7.1 3-2-1 Backup Rule

```
3 copies of data:
- Working copy (laptop)
- Cloud backup (Dropbox/Google Drive)
- External hard drive

2 different media types:
- SSD (laptop)
- Cloud storage

1 offsite copy:
- Cloud backup
```

### 7.2 Automated Backups

```bash
# macOS Time Machine (local backup)
tmutil startbackup

# Sync to cloud (Dropbox, Google Drive, OneDrive)
# Automatic sync when connected

# Git push (for version-controlled files)
git push origin main

# Manual external backup (monthly)
rsync -av ~/research/ /Volumes/Backup/research/
```

---

## 8. Lab Notebook (for Experimental Research)

### 8.1 Electronic Lab Notebook

```markdown
# Entry: 2026-03-16

## Experiment: Western Blot - Protein X Expression

### Objective
Measure Protein X expression in control vs treatment samples

### Materials
- Primary antibody: Anti-Protein X (Cat# AB123, Lot# 456789)
- Secondary antibody: HRP-conjugated goat anti-rabbit (Cat# AB456)
- Samples: Control (n=3), Treatment (n=3)

### Procedure
1. Protein extraction (see protocol P-001)
2. BCA assay - protein concentration: 2.5 mg/mL
3. Loaded 30μg per lane
4. SDS-PAGE: 120V, 90 min
5. Transfer: 100V, 60 min
6. Blocking: 5% milk, 1h RT
7. Primary Ab: 1:1000, 4°C overnight
8. Secondary Ab: 1:5000, RT 1h
9. ECL detection

### Results
- Clear bands at expected size (~50 kDa)
- Treatment group shows 2.3-fold increase
- See image: western_2026-03-16_001.jpg

### Notes
- Sample #3 (treatment) slightly overloaded
- Positive control worked well
- Repeat with n=5 per group

### Next Steps
- [ ] Repeat experiment with larger n
- [ ] Try different time points
- [ ] Quantify bands with ImageJ
```

---

## 9. Tools

### 9.1 Note-Taking

- **Obsidian**: Markdown, local files, linking
- **Notion**: All-in-one workspace
- **OneNote**: Microsoft ecosystem
- **Evernote**: Web clipper, tagging

### 9.2 Reference Management

- **Zotero**: Free, open-source
- **Mendeley**: Free, PDF annotation
- **EndNote**: Powerful, expensive
- **Papers**: macOS, beautiful UI

### 9.3 Writing

- **Scrivener**: Long documents, outlining
- **Ulysses**: Distraction-free writing
- **LaTeX** (Overleaf): Academic typesetting
- **Google Docs**: Collaboration

### 9.4 Project Management

- **Notion**: Databases, kanban boards
- **Trello**: Simple kanban
- **Asana**: Team collaboration
- **Todoist**: Task management

---

## Anti-Patterns

### ❌ No Backups
Relying on single copy of data.

**Solution**: 3-2-1 backup rule, automated backups.

### ❌ Inconsistent File Names
Random naming makes files impossible to find.

**Solution**: Establish naming convention, stick to it.

### ❌ No Version Control
Filename versioning creates chaos.

**Solution**: Use Git for text files, clear version tags.

### ❌ Editing Raw Data
Overwriting original data makes analysis irreproducible.

**Solution**: Keep raw data read-only, process in separate folder.

### ❌ No Documentation
Future you doesn't remember what past you did.

**Solution**: Document everything - README files, lab notebooks, comments in code.

---

## Related Modules

- **LITERATURE_REVIEW** - Systematic literature search and synthesis
- **ACADEMIC_WRITING** - Writing standards for research
- **DOCUMENT_STRUCTURE** - Structuring academic documents

---

## Resources

**Books**:
- *The Craft of Research* - Booth, Colomb, Williams
- *How to Take Smart Notes* - Sönke Ahrens (Zettelkasten)

**Tools**:
- Zotero: https://www.zotero.org/
- Obsidian: https://obsidian.md/
- Git: https://git-scm.com/
