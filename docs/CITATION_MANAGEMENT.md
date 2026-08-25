# Citation Management (引用管理)

**Version**: 2.0.0  
**Module**: CITATION_MANAGEMENT  
**Loading**: Conditional (`project.type = "academic"`)  
**Purpose**: Citation formats (APA, MLA, Chicago, IEEE), reference management tools, and best practices.

---

## Overview

This guide covers **citation formats and reference management** for academic research. It provides rules for four major citation styles and guidance on reference management tools.

**Scope**:
- ✅ Four citation styles (APA, MLA, Chicago, IEEE)
- ✅ In-text citations
- ✅ Reference list formatting
- ✅ Reference management tools
- ❌ Writing style and structure (see ACADEMIC_WRITING module)

**Loading Trigger**: `project.type = "academic"`, keywords: "reference", "bibliography", "APA", "MLA", "citation"

**Configuration**: Set `academic.citation_style` in `config.toml`.

---

## Citation Style Selection

### Style by Discipline

| Style | Disciplines | Parenthetical | Footnote/Endnote |
|-------|-------------|---------------|------------------|
| **APA** | Social sciences, education, psychology | ✅ | ❌ |
| **MLA** | Humanities, literature, arts | ✅ | ❌ |
| **Chicago** | History, arts, humanities | ❌ | ✅ (Notes-Bibliography) |
| **IEEE** | Engineering, computer science | ✅ (numerical) | ❌ |

**Configuration** (`config.toml`):
```toml
[academic]
citation_style = "APA"  # APA | MLA | Chicago | IEEE
field = "computer_science"
```

---

## APA Style (7th Edition)

**Used in**: Psychology, education, social sciences

### In-Text Citations

#### Basic Format

**Parenthetical**:
```
Recent research shows code review reduces defects (Smith, 2020).
```

**Narrative**:
```
Smith (2020) found that code review reduces defects by 30%.
```

#### Multiple Authors

**Two authors**:
```
(Smith & Jones, 2020)
Smith and Jones (2020) demonstrated...
```

**Three or more authors**:
```
(Smith et al., 2020)  # Use "et al." for 3+ authors
Smith et al. (2020) examined...
```

#### Multiple Works

**Same author, same year**:
```
(Smith, 2020a, 2020b)
```

**Different authors**:
```
(Jones, 2019; Smith, 2020; Wang, 2021)  # Alphabetical order
```

#### Direct Quotes

**Short quote** (< 40 words):
```
Smith (2020) stated that "code review is essential for quality" (p. 45).
```

**Long quote** (≥ 40 words):
```
Smith (2020) elaborated on code review benefits:
  
  Code review serves multiple purposes beyond defect detection. It 
  facilitates knowledge transfer, enforces coding standards, and builds 
  collective code ownership. Teams that review code daily exhibit 
  stronger cohesion and shared understanding. (p. 47)
```

#### Secondary Sources

**Original**: Brown (cited in Smith, 2020)

**Reference list**: Only cite Smith (2020), not Brown.

### Reference List

**Order**: Alphabetical by author last name

**Hanging indent**: First line flush left, subsequent lines indented 0.5"

#### Journal Article

**Format**:
```
Author, A. A., & Author, B. B. (Year). Title of article. Title of Journal, 
Volume(Issue), page–page. https://doi.org/xxx
```

**Example**:
```
Smith, J. A., & Jones, M. B. (2020). The impact of code review on software 
quality. Journal of Software Engineering, 15(3), 234–250. 
https://doi.org/10.1234/jse.2020.1234
```

#### Book

**Format**:
```
Author, A. A. (Year). Title of book (Edition). Publisher. 
https://doi.org/xxx
```

**Example**:
```
Martin, R. C. (2008). Clean code: A handbook of agile software craftsmanship. 
Prentice Hall.
```

#### Book Chapter

**Format**:
```
Author, A. A. (Year). Title of chapter. In E. E. Editor (Ed.), Title of book 
(pp. xxx–xxx). Publisher. https://doi.org/xxx
```

**Example**:
```
Gamma, E. (1994). Design patterns: Abstraction and reuse of object-oriented 
design. In O. Nierstrasz (Ed.), ECOOP '93 — Object-oriented programming 
(pp. 406–431). Springer.
```

#### Conference Paper

**Format**:
```
Author, A. A. (Year, Month day–day). Title of paper [Conference presentation]. 
Conference Name, Location. https://doi.org/xxx
```

**Example**:
```
Bacchelli, A., & Bird, C. (2013, May 18–26). Expectations, outcomes, and 
challenges of modern code review [Conference presentation]. International 
Conference on Software Engineering, San Francisco, CA, United States. 
https://doi.org/10.1109/ICSE.2013.6606617
```

#### Website

**Format**:
```
Author, A. A. (Year, Month Day). Title of page. Site Name. URL
```

**Example**:
```
Mozilla Foundation. (2023, March 15). JavaScript documentation. MDN Web Docs. 
https://developer.mozilla.org/en-US/docs/Web/JavaScript
```

#### Software/Code

**Format**:
```
Author, A. A. (Year). Title of software (Version x.x) [Software]. URL
```

**Example**:
```
OpenAI. (2023). ChatGPT (Version 4) [Large language model]. 
https://openai.com/chatgpt
```

---

## MLA Style (9th Edition)

**Used in**: Literature, arts, humanities

### In-Text Citations

#### Basic Format

**Parenthetical**:
```
Code review reduces defects (Smith 45).
```

**Narrative**:
```
Smith argues that code review "is essential for quality" (45).
```

#### Multiple Authors

**Two authors**:
```
(Smith and Jones 34)
```

**Three or more authors**:
```
(Smith et al. 67)
```

#### Multiple Works

**Same author**:
```
(Smith, "Code Review" 23; Smith, "Software Quality" 45)
```

**Different authors**:
```
(Jones 12; Smith 34; Wang 56)
```

#### No Author

**Use shortened title**:
```
("Software Quality" 12)
```

### Works Cited

**Order**: Alphabetical by author last name (or title if no author)

**Hanging indent**: First line flush left, subsequent lines indented 0.5"

#### Journal Article

**Format**:
```
Author Last Name, First Name. "Article Title." Journal Title, vol. X, no. X, 
Year, pp. XX-XX. DOI or URL.
```

**Example**:
```
Smith, John A., and Mary B. Jones. "The Impact of Code Review on Software 
Quality." Journal of Software Engineering, vol. 15, no. 3, 2020, pp. 234-250. 
https://doi.org/10.1234/jse.2020.1234.
```

#### Book

**Format**:
```
Author Last Name, First Name. Title of Book. Edition (if not 1st), Publisher, 
Year.
```

**Example**:
```
Martin, Robert C. Clean Code: A Handbook of Agile Software Craftsmanship. 
Prentice Hall, 2008.
```

#### Book Chapter

**Format**:
```
Author Last Name, First Name. "Chapter Title." Title of Book, edited by 
Editor First Last, Publisher, Year, pp. XX-XX.
```

**Example**:
```
Gamma, Erich. "Design Patterns: Abstraction and Reuse of Object-Oriented 
Design." ECOOP '93 — Object-Oriented Programming, edited by Oscar Nierstrasz, 
Springer, 1994, pp. 406-431.
```

#### Website

**Format**:
```
Author Last Name, First Name. "Page Title." Website Name, Publisher, Date, 
URL. Accessed Day Month Year.
```

**Example**:
```
Mozilla Foundation. "JavaScript Documentation." MDN Web Docs, Mozilla, 
15 Mar. 2023, https://developer.mozilla.org/en-US/docs/Web/JavaScript. 
Accessed 16 Mar. 2026.
```

---

## Chicago Style (17th Edition)

**Used in**: History, arts, humanities

**Two systems**: Notes-Bibliography (N-B) and Author-Date (A-D)

### Notes-Bibliography System

**Used for**: Humanities (history, literature, arts)

#### Footnotes/Endnotes

**First citation** (full):
```
1. John A. Smith and Mary B. Jones, "The Impact of Code Review on Software 
Quality," Journal of Software Engineering 15, no. 3 (2020): 234–50, 
https://doi.org/10.1234/jse.2020.1234.
```

**Subsequent citations** (short):
```
5. Smith and Jones, "Code Review," 240.
```

**Ibid** (same work, consecutive citations):
```
5. Smith and Jones, "Code Review," 240.
6. Ibid., 242.
```

#### Bibliography

**Order**: Alphabetical by author last name

**Format** (journal article):
```
Smith, John A., and Mary B. Jones. "The Impact of Code Review on Software 
Quality." Journal of Software Engineering 15, no. 3 (2020): 234–50. 
https://doi.org/10.1234/jse.2020.1234.
```

**Format** (book):
```
Martin, Robert C. Clean Code: A Handbook of Agile Software Craftsmanship. 
Upper Saddle River, NJ: Prentice Hall, 2008.
```

### Author-Date System

**Used for**: Sciences, social sciences (when Chicago required)

**In-text**: Same as APA (Smith 2020, 45)

**Reference list**: Similar to APA

---

## IEEE Style

**Used in**: Engineering, computer science, electronics

### In-Text Citations

**Numerical system**: [1], [2], [3]

**Order**: By appearance in text (not alphabetical)

**Examples**:
```
Code review reduces defects [1]. Multiple studies [2], [3], [4] confirm this.

Smith [1] found that daily reviews are most effective.

Recent work [1]–[4] demonstrates...  # Range notation
```

### Reference List

**Order**: Numerical (by appearance in text)

**Format**: [X] A. A. Author, "Title," Journal, vol. X, no. X, pp. XX–XX, Month Year.

#### Journal Article

**Example**:
```
[1] J. A. Smith and M. B. Jones, "The impact of code review on software 
    quality," J. Softw. Eng., vol. 15, no. 3, pp. 234–250, Mar. 2020, 
    doi: 10.1234/jse.2020.1234.
```

#### Book

**Example**:
```
[2] R. C. Martin, Clean Code: A Handbook of Agile Software Craftsmanship. 
    Upper Saddle River, NJ: Prentice Hall, 2008.
```

#### Conference Paper

**Example**:
```
[3] A. Bacchelli and C. Bird, "Expectations, outcomes, and challenges of 
    modern code review," in Proc. Int. Conf. Softw. Eng., San Francisco, 
    CA, USA, May 2013, pp. 712–721, doi: 10.1109/ICSE.2013.6606617.
```

#### Website

**Example**:
```
[4] Mozilla Foundation, "JavaScript documentation," MDN Web Docs, Mar. 15, 
    2023. [Online]. Available: 
    https://developer.mozilla.org/en-US/docs/Web/JavaScript
```

---

## Reference Management Tools

### Tool Comparison

| Tool | Cost | Platform | Features | Best For |
|------|------|----------|----------|----------|
| **Zotero** | Free | Win/Mac/Linux | Browser plugin, PDF management | General use, budget-conscious |
| **Mendeley** | Free (paid Pro) | Win/Mac/Linux | Social features, annotations | Collaboration |
| **EndNote** | Paid | Win/Mac | Advanced features, library sharing | Institutions with license |
| **Papers** | Paid | Mac/iOS | Apple ecosystem, design | Mac users |
| **JabRef** | Free | Win/Mac/Linux | BibTeX management | LaTeX users |

### Zotero (Recommended)

**Why Zotero**:
- ✅ Free and open-source
- ✅ Cross-platform
- ✅ Browser integration (Chrome, Firefox, Safari)
- ✅ Word/LibreOffice plugins
- ✅ Group libraries for collaboration
- ✅ 300 MB free storage (expandable)

**Setup**:
1. Download: https://www.zotero.org/download/
2. Install Zotero Connector (browser extension)
3. Install word processor plugin (Zotero → Preferences → Cite → Install Plugin)

**Workflow**:
```
1. Browse journal website
2. Click Zotero Connector icon → auto-save reference + PDF
3. Organize in collections (folders)
4. Cite in Word: Insert → Zotero → Add/Edit Citation
5. Generate bibliography: Insert → Zotero → Add/Edit Bibliography
```

**Collections Structure**:
```
My Library
├── Literature Review
│   ├── Code Review
│   ├── Software Quality
│   └── Agile Methods
├── Methodology
│   ├── Statistical Methods
│   └── Research Design
└── Current Project
    ├── To Read
    ├── Read
    └── Cited
```

### BibTeX (for LaTeX)

**File**: `references.bib`

**Format**:
```bibtex
@article{smith2020code,
  title={The impact of code review on software quality},
  author={Smith, John A and Jones, Mary B},
  journal={Journal of Software Engineering},
  volume={15},
  number={3},
  pages={234--250},
  year={2020},
  doi={10.1234/jse.2020.1234}
}

@book{martin2008clean,
  title={Clean Code: A Handbook of Agile Software Craftsmanship},
  author={Martin, Robert C},
  year={2008},
  publisher={Prentice Hall}
}
```

**Usage in LaTeX**:
```latex
\documentclass{article}
\usepackage{natbib}  % Or biblatex

\begin{document}

Code review reduces defects \citep{smith2020code}. 
Martin \citeyear{martin2008clean} emphasizes clean code practices.

\bibliographystyle{apalike}  % Or plainnat, ieeetr, chicago
\bibliography{references}

\end{document}
```

**JabRef**: GUI for managing .bib files  
Download: https://www.jabref.org/

---

## Common Citation Mistakes

### 1. Missing Citations

❌ **Uncited claim**:
```
Code review improves software quality.
```

✅ **Properly cited**:
```
Code review improves software quality (Smith, 2020; Jones, 2021).
```

### 2. Incorrect Format

❌ **Wrong order**:
```
(2020, Smith)  # Correct APA: (Smith, 2020)
```

❌ **Missing page number** (direct quote):
```
"Code review is essential" (Smith, 2020).  # Needs page: (Smith, 2020, p. 45)
```

### 3. Inconsistent Style

❌ **Mixed styles**:
```
(Smith, 2020)  # APA
[1]            # IEEE
```

✅ **Consistent style** (choose one and stick to it)

### 4. Overc citing

❌ **Excessive**:
```
Code review (Smith, 2020) is a process (Jones, 2019) where developers 
(Wang, 2021) examine code (Brown, 2022) to find defects (Lee, 2023).
```

✅ **Balanced**:
```
Code review is a process where developers examine code to find defects 
(Smith, 2020; Jones, 2019; Wang, 2021).
```

### 5. Underciting

❌ **Insufficient**:
```
Numerous studies show code review reduces defects (Smith, 2020).
```

✅ **Adequate**:
```
Multiple studies show code review reduces defects by 30-80% 
(Smith, 2020; Jones, 2019; Wang, 2021; Lee, 2018).
```

---

## DOI and Persistent Identifiers

### Digital Object Identifier (DOI)

**Format**: https://doi.org/10.1234/jse.2020.1234

**Why use DOI**:
- ✅ Permanent link (URLs may break)
- ✅ Required by many journals
- ✅ Easier to locate paper

**Finding DOI**:
- Journal article page (usually top of article)
- CrossRef: https://www.crossref.org/
- Google Scholar (click "Cite" → check citation)

**In APA**:
```
Smith, J. A. (2020). Title. Journal, 15(3), 234–250. 
https://doi.org/10.1234/jse.2020.1234
```

**In MLA**:
```
Smith, John A. "Title." Journal, vol. 15, no. 3, 2020, pp. 234-250, 
https://doi.org/10.1234/jse.2020.1234.
```

### Other Identifiers

| Identifier | Use Case | Example |
|------------|----------|---------|
| **ISBN** | Books | 978-0-13-235088-4 |
| **ISSN** | Journals | 0098-5589 |
| **ORCID** | Author ID | 0000-0002-1825-0097 |
| **arXiv** | Preprints | arXiv:2012.12345 |

---

## Citation Checklist

Before submission, verify:

**In-Text Citations**:
- [ ] All claims have citations
- [ ] Direct quotes have page numbers
- [ ] Multiple authors formatted correctly (et al. for 3+)
- [ ] Consistent citation style throughout

**Reference List**:
- [ ] All in-text citations appear in reference list
- [ ] All reference list entries cited in text
- [ ] Alphabetical order (APA, MLA, Chicago) or numerical (IEEE)
- [ ] Hanging indent (APA, MLA, Chicago)
- [ ] Consistent formatting (capitalization, punctuation)
- [ ] DOIs included where available
- [ ] No broken URLs

**Tools**:
- [ ] Reference manager database backed up
- [ ] Citation style set correctly in word processor
- [ ] Bibliography auto-generated (not manually typed)

---

## Quick Reference

### Citation Style Selection

```
Social Sciences (Psychology, Education) → APA
Humanities (Literature, Arts) → MLA
History, Arts → Chicago (Notes-Bibliography)
Engineering, CS → IEEE
```

### Tool Selection

```
Free, cross-platform → Zotero
LaTeX user → JabRef + BibTeX
Mac ecosystem → Papers
Institution license → EndNote
```

### In-Text Format

| Style | Format | Example |
|-------|--------|---------|
| **APA** | (Author, Year) | (Smith, 2020) |
| **MLA** | (Author Page) | (Smith 45) |
| **Chicago N-B** | Superscript number¹ | ¹ (see footnote) |
| **Chicago A-D** | (Author Year, Page) | (Smith 2020, 45) |
| **IEEE** | [Number] | [1] |

---

## Related Documentation

- **[ACADEMIC_WRITING](./ACADEMIC_WRITING.md)** - Research paper structure and writing style
- **[TERMINOLOGY](./terminology/academic/)** - Academic terminology
- **[STYLE_GUIDE](./STYLE_GUIDE.md)** - General writing conventions

---

## Resources

### Official Style Guides

- **APA**: https://apastyle.apa.org/ (7th edition)
- **MLA**: https://style.mla.org/ (9th edition)
- **Chicago**: https://www.chicagomanualofstyle.org/ (17th edition)
- **IEEE**: https://journals.ieeeauthorcenter.ieee.org/ (2021 edition)

### Citation Generators

- **Citation Machine**: https://www.citationmachine.net/
- **EasyBib**: https://www.easybib.com/
- **Zotero**: https://zbib.org/ (instant bibliography)
- **DOI2BIB**: https://www.doi2bib.org/ (DOI to BibTeX)

**Warning**: Always verify generated citations against official guides.

### Reference Managers

- **Zotero**: https://www.zotero.org/
- **Mendeley**: https://www.mendeley.com/
- **EndNote**: https://endnote.com/
- **JabRef**: https://www.jabref.org/

---

**Version**: 2.0.0  
**Last Updated**: 2026-03-16  
**Maintainer**: my-vibe-scaffolding template
