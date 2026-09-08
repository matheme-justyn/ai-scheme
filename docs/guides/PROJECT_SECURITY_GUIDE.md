# Project Security Policy Guide

When using this scaffolding for your project, you should create your own `SECURITY.md` to define how security vulnerabilities are handled.

## Why You Need SECURITY.md

- **Responsible Disclosure**: Provide a clear channel for security researchers
- **Trust**: Shows you take security seriously
- **GitHub Integration**: GitHub displays it in the Security tab
- **Compliance**: Some industries require documented security policies

## What to Include

### 1. **Supported Versions**
Which versions receive security updates

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 2.x.x   | :white_check_mark: |
| 1.x.x   | :x:                |
| < 1.0   | :x:                |

### 2. **Reporting a Vulnerability**
How to report security issues

## Reporting a Vulnerability

**DO NOT** open a public issue for security vulnerabilities.

Instead:
- Email: security@your-domain.com
- Use GitHub's private vulnerability reporting (if enabled)
- Expect response within 48 hours

### 3. **Security Update Process**
How you handle vulnerabilities

## Security Update Process

1. Vulnerability reported
2. We investigate within 48 hours
3. If confirmed, we develop a fix
4. Fix is released in a security patch
5. Public disclosure after patch is available

### 4. **Bug Bounty Program** (Optional)
If you offer rewards

## Bug Bounty Program

We offer rewards for valid security vulnerabilities:
- Critical: $500-$2000
- High: $200-$500
- Medium: $50-$200

See [bounty program details](link) for scope and rules.

## Template Structure

# Security Policy

## Supported Versions

[Version table]

## Reporting a Vulnerability

Please report security vulnerabilities by emailing security@your-domain.com

**Do not** open public issues for security problems.

### What to Include in Your Report

- Description of the vulnerability
- Steps to reproduce
- Potential impact
- Suggested fix (if any)

### What to Expect

- **Response Time**: Within 48 hours
- **Investigation**: We'll verify and assess severity
- **Fix Timeline**: Critical issues within 7 days, others within 30 days
- **Disclosure**: We'll coordinate disclosure timing with you
- **Credit**: We'll acknowledge your contribution (if desired)

## Security Update Process

1. Report received
2. Vulnerability confirmed and severity assessed
3. Fix developed and tested
4. Security advisory published
5. Patch released
6. Public disclosure

## Security Best Practices

When using this project:
- Keep dependencies up to date
- Use environment variables for secrets (never commit .env)
- Enable 2FA on deployment platforms
- Review security advisories regularly

## Contact

- Email: security@your-domain.com
- PGP Key: [link to public key]

## Hall of Fame

We thank these security researchers:
- [Name] - [Vulnerability] - [Date]

## Different Approaches

### Open Source Project
We welcome responsible disclosure from security researchers.
Public acknowledgment and potential bounties available.

### Company/Internal Project
Report to internal security team via security@company.com
Follow company security incident response policy.

### Personal Project
Please email me at personal@email.com with any security concerns.
I'll do my best to address issues promptly.

### No Active Maintenance
This project is no longer actively maintained. Use at your own risk.
Forks are encouraged if you need security updates.

## GitHub Security Features

### Enable Private Vulnerability Reporting

Go to: Settings → Security → Enable private vulnerability reporting

This allows security researchers to privately report issues directly on GitHub.

### Security Advisories

When you fix a vulnerability:
1. Create a Security Advisory
2. Request a CVE (if applicable)
3. Publish the advisory after patch is released

### Dependabot Alerts

Enable Dependabot to automatically detect vulnerable dependencies:
- Settings → Security & analysis → Enable Dependabot alerts

## Common Vulnerability Types to Address

### Web Applications
- SQL Injection
- XSS (Cross-Site Scripting)
- CSRF (Cross-Site Request Forgery)
- Authentication bypass
- Authorization issues

### APIs
- API key exposure
- Rate limiting bypass
- Injection attacks
- Data exposure

### Dependencies
- Vulnerable npm packages
- Outdated libraries
- Supply chain attacks

## Examples from Popular Projects

- [Node.js Security Policy](https://github.com/nodejs/node/blob/main/SECURITY.md)
- [Ruby on Rails Security Policy](https://github.com/rails/rails/blob/main/SECURITY.md)
- [Django Security Policy](https://github.com/django/django/blob/main/SECURITY.md)

## This Scaffolding's Security Policy

The scaffolding itself (`.scaffolding/SECURITY.md`) is for the template code, not your project.

**Your project needs its own policy!**

Create `SECURITY.md` in your project root with:
1. Your contact information
2. Your response timeline commitments
3. Your disclosure process
4. Project-specific security considerations

## Resources

- [GitHub Security Lab](https://securitylab.github.com/)
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [CVE Program](https://www.cve.org/)
- [Security.txt](https://securitytxt.org/) - Machine-readable security policy
