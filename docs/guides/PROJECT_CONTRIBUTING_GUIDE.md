# Project Contributing Guide

When using this scaffolding for your project, you should create your own `CONTRIBUTING.md` to guide contributors.

## What to Include

A good CONTRIBUTING.md typically includes:

### 1. **Welcome Message**
Thank contributors and explain the purpose.

### 2. **Code of Conduct**
Link to CODE_OF_CONDUCT.md or state expectations.

### 3. **How to Contribute**
- Reporting bugs
- Suggesting features
- Submitting pull requests
- Asking questions

### 4. **Development Setup**
```bash
# Clone the repository
git clone https://github.com/your-username/your-project.git
cd your-project

# Install dependencies
npm install  # or pip install -r requirements.txt, etc.

# Run tests
npm test

# Start development server
npm run dev
```

### 5. **Coding Standards**
- Refer to AGENTS.md for coding conventions
- Linter/formatter requirements
- Test coverage expectations
- Commit message format

### 6. **Pull Request Process**
- Branch naming convention (e.g., `feature/add-login`, `fix/memory-leak`)
- How to write PR descriptions
- Review process and timeline
- When PRs get merged

### 7. **Issue Templates**
Mention the issue templates in `.github/ISSUE_TEMPLATE/`

## Template Structure

# Contributing to [Project Name]

Thank you for your interest in contributing! 🎉

## Table of Contents
- [Code of Conduct](#code-of-conduct)
- [How to Contribute](#how-to-contribute)
- [Development Setup](#development-setup)
- [Coding Standards](#coding-standards)
- [Pull Request Process](#pull-request-process)
- [Questions](#questions)

## Code of Conduct

[Your code of conduct or link to CODE_OF_CONDUCT.md]

## How to Contribute

### 🐛 Report Bugs
Use the [Bug Report template](.github/ISSUE_TEMPLATE/bug_report.md)

### 💡 Suggest Features
Use the [Feature Request template](.github/ISSUE_TEMPLATE/feature_request.md)

### 🔀 Submit Pull Requests
1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (follow commit format in AGENTS.md)
4. Push to your branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## Development Setup

[Your setup instructions]

## Coding Standards

- Follow conventions in [AGENTS.md](./AGENTS.md)
- Write tests for new features
- Run linter before committing: `npm run lint`
- Ensure all tests pass: `npm test`

## Pull Request Process

1. Update documentation if needed
2. Add tests for new functionality
3. Ensure CI passes
4. Request review from maintainers
5. Address review feedback
6. Once approved, maintainers will merge

## Questions

- Open a [Discussion](https://github.com/your-username/your-project/discussions)
- Email: your-email@example.com

## Different Contribution Policies

### Open to All Contributions
We welcome contributions from everyone! Please submit PRs freely.

### Selective Contributions
We appreciate your interest! Please open an issue first to discuss 
your proposed changes before starting work.

### No PRs Accepted
This is a personal/company project. We're not accepting PRs, but 
feel free to fork and customize for your needs.

### Company/Team Only
This repository is for internal team members only. External 
contributions are not accepted.

## Examples from Popular Projects

- [React](https://github.com/facebook/react/blob/main/CONTRIBUTING.md)
- [Vue.js](https://github.com/vuejs/vue/blob/dev/.github/CONTRIBUTING.md)
- [TypeScript](https://github.com/microsoft/TypeScript/blob/main/CONTRIBUTING.md)
- [Rust](https://github.com/rust-lang/rust/blob/master/CONTRIBUTING.md)

## This Scaffolding's Contributing Policy

The scaffolding itself (`.scaffolding/CONTRIBUTING.md`) states we don't accept PRs. 
This is because it's a personal template.

**Your project is different!** You should:
1. Create your own `CONTRIBUTING.md` in project root
2. Define your own contribution policy
3. Customize based on your project needs

## Resources

- [GitHub's Contributing Guide Template](https://docs.github.com/en/communities/setting-up-your-project-for-healthy-contributions/setting-guidelines-for-repository-contributors)
- [Contributor Covenant](https://www.contributor-covenant.org/) - Code of Conduct template
- [All Contributors](https://allcontributors.org/) - Recognize all contributors
