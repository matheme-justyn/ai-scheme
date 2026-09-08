# ADR_TEMPLATE

**Status**: Active | Domain: Collaboration  
**Related Modules**: README_STRUCTURE, RELEASE_PROCESS, GIT_WORKFLOW

## Purpose

This module provides guidance for writing Architecture Decision Records (ADRs). ADRs document important architectural decisions, context, alternatives considered, and consequences. Use this module to maintain a decision log that explains why your system is built the way it is.

## When to Use This Module

Reference this module when:
- Making significant architectural decisions
- Choosing between technology options
- Establishing patterns or conventions
- Documenting design trade-offs
- Onboarding new team members to architectural decisions
- Reviewing past decisions

## ADR Structure

### Basic Template

```markdown
# ADR-NNNN: Title in Imperative Form

**Status**: Proposed | Accepted | Deprecated | Superseded  
**Date**: YYYY-MM-DD  
**Deciders**: [List people involved in decision]  
**Technical Story**: [Link to ticket/issue]

## Context and Problem Statement

What is the issue we're facing? What factors influence this decision?

## Decision Drivers

* Driver 1 (e.g., performance requirements)
* Driver 2 (e.g., team expertise)
* Driver 3 (e.g., budget constraints)

## Considered Options

* Option 1
* Option 2
* Option 3

## Decision Outcome

Chosen option: "[option 1]", because [justification].

### Positive Consequences

* Good consequence 1
* Good consequence 2

### Negative Consequences

* Bad consequence 1
* Bad consequence 2

## Pros and Cons of the Options

### Option 1: [Name]

Description of option 1.

* ✅ Good, because [argument a]
* ✅ Good, because [argument b]
* ❌ Bad, because [argument c]

### Option 2: [Name]

Description of option 2.

* ✅ Good, because [argument a]
* ❌ Bad, because [argument b]
* ❌ Bad, because [argument c]

## Links

* [Related ADR](./0002-related-decision.md)
* [External Resource](https://example.com)
```

## Real-World Examples

### Example 1: Database Selection

```markdown
# ADR-0001: Use PostgreSQL as Primary Database

**Status**: Accepted  
**Date**: 2024-01-15  
**Deciders**: Engineering Team  
**Technical Story**: [TICKET-123]

## Context and Problem Statement

We need to select a database for our application that handles:
- Complex relationships between entities
- ACID transactions
- JSON data storage
- Full-text search capabilities
- Expected to scale to 10M+ records

## Decision Drivers

* Strong consistency requirements for financial transactions
* Need for complex queries with JOINs
* Team has PostgreSQL expertise
* Open-source preference
* Budget: $500/month maximum

## Considered Options

* PostgreSQL
* MySQL
* MongoDB
* DynamoDB

## Decision Outcome

Chosen option: "PostgreSQL", because it provides the best balance of features, team familiarity, and cost.

### Positive Consequences

* Native JSON support for flexible schemas
* Excellent full-text search with extensions
* Strong ACID guarantees
* Free and open-source
* Team already familiar with it

### Negative Consequences

* Requires vertical scaling (less horizontal than NoSQL)
* More complex operational overhead than managed solutions

## Pros and Cons of the Options

### PostgreSQL

* ✅ ACID transactions
* ✅ Complex queries with JOINs
* ✅ JSON support (jsonb)
* ✅ Full-text search
* ✅ Team expertise
* ✅ Open-source
* ❌ Vertical scaling limitations
* ❌ Self-hosting overhead

### MySQL

* ✅ ACID transactions
* ✅ Wide adoption
* ✅ Replication support
* ❌ Weaker JSON support
* ❌ Less advanced full-text search
* ❌ Less team familiarity

### MongoDB

* ✅ Horizontal scaling
* ✅ Flexible schema
* ✅ JSON-native
* ❌ No ACID transactions (until v4.0)
* ❌ Complex aggregation pipelines
* ❌ No team expertise

### DynamoDB

* ✅ Fully managed
* ✅ Infinite scaling
* ✅ Pay-per-use
* ❌ Limited query flexibility
* ❌ Expensive for our use case
* ❌ Vendor lock-in

## Links

* [PostgreSQL Documentation](https://www.postgresql.org/docs/)
* [AWS RDS PostgreSQL](https://aws.amazon.com/rds/postgresql/)
```

### Example 2: Authentication Method

```markdown
# ADR-0002: Use JWT for API Authentication

**Status**: Accepted  
**Date**: 2024-01-20  
**Deciders**: Backend Team  
**Technical Story**: [TICKET-456]

## Context and Problem Statement

Our application needs an authentication mechanism for:
- RESTful API consumed by web and mobile clients
- Microservices architecture (5+ services)
- Expected: 10,000 concurrent users

Session-based auth requires centralized state. JWT is stateless but has token revocation challenges.

## Decision Drivers

* Stateless architecture preferred for scaling
* Multiple services need to validate auth
* Mobile clients need persistent auth
* Need to scale horizontally

## Considered Options

* JWT (JSON Web Tokens)
* Session-based auth with Redis
* OAuth 2.0 with external provider

## Decision Outcome

Chosen option: "JWT with short expiry (15 min) + refresh tokens (7 days)", because it provides stateless authentication while mitigating revocation risks.

### Positive Consequences

* No centralized session store needed
* Services can validate tokens independently
* Works well with mobile clients
* Easy to scale horizontally

### Negative Consequences

* Token revocation requires additional infrastructure
* Token size larger than session IDs
* Secrets management complexity

## Pros and Cons of the Options

### JWT

* ✅ Stateless (no session store needed)
* ✅ Self-contained (includes user info)
* ✅ Works across services
* ❌ Difficult to revoke immediately
* ❌ Larger payload than session IDs

### Session-based with Redis

* ✅ Easy revocation
* ✅ Small session IDs
* ✅ Familiar pattern
* ❌ Requires Redis (state dependency)
* ❌ All services need Redis access
* ❌ Single point of failure

### OAuth 2.0 (External)

* ✅ Managed solution
* ✅ SSO capabilities
* ❌ External dependency
* ❌ Additional latency
* ❌ Cost per active user

## Implementation Details

* Access token expiry: 15 minutes
* Refresh token expiry: 7 days
* Refresh token stored in database for revocation
* Token rotation on refresh

## Links

* [JWT.io](https://jwt.io/)
* [RFC 7519 - JWT](https://tools.ietf.org/html/rfc7519)
* [ADR-0001: Database Selection](./0001-use-postgresql.md)
```

### Example 3: Superseding an ADR

```markdown
# ADR-0010: Use REST for All APIs

**Status**: Superseded by [ADR-0025](./0025-use-graphql.md)  
**Date**: 2024-03-01  
**Deciders**: Engineering Team

## Context and Problem Statement

[Original context...]

## Decision Outcome

Superseded. See [ADR-0025](./0025-use-graphql.md) for new decision to use GraphQL due to changed requirements.
```

```markdown
# ADR-0025: Migrate to GraphQL for Public API

**Status**: Accepted  
**Date**: 2024-07-15  
**Supersedes**: [ADR-0010](./0010-use-rest.md)  
**Deciders**: Engineering Team

## Context and Problem Statement

Since ADR-0010, requirements have changed:
- Mobile clients need to minimize data transfer
- Frontend needs nested data in single request
- Over-fetching causing performance issues

REST requires multiple roundtrips for related data. GraphQL allows clients to request exactly what they need.

[Rest of ADR...]
```

## ADR Workflow

### 1. Create ADR

```bash
# Generate ADR number
LAST_ADR=$(ls docs/adr/*.md | sort -V | tail -1 | grep -oP '\d{4}')
NEXT_ADR=$(printf "%04d" $((10#$LAST_ADR + 1)))

# Create file
cat > docs/adr/${NEXT_ADR}-your-decision.md << 'EOF'
# ADR-${NEXT_ADR}: Your Decision Title

**Status**: Proposed
**Date**: $(date +%Y-%m-%d)
**Deciders**: [Your Team]

[Content...]
EOF
```

### 2. Review Process

1. Create Pull Request with ADR
2. Team reviews and discusses
3. Update ADR based on feedback
4. Merge when consensus reached
5. Update Status to "Accepted"

### 3. Maintenance

- Keep ADRs immutable after acceptance
- Supersede instead of editing
- Link related ADRs
- Update index/table of contents

## ADR Index Template

```markdown
# Architecture Decision Records

* [ADR-0001](./0001-use-postgresql.md) - Use PostgreSQL as Primary Database
* [ADR-0002](./0002-use-jwt-auth.md) - Use JWT for API Authentication
* [ADR-0003](./0003-adopt-monorepo.md) - Adopt Monorepo Structure
* [ADR-0010](./0010-use-rest.md) - ~~Use REST for All APIs~~ (Superseded by ADR-0025)
* [ADR-0025](./0025-use-graphql.md) - Migrate to GraphQL for Public API

## By Status

### Accepted
* ADR-0001, ADR-0002, ADR-0003, ADR-0025

### Proposed
* (None currently)

### Deprecated
* (None)

### Superseded
* ADR-0010 (by ADR-0025)
```

## Best Practices

### DO ✅

- **Write ADRs at decision time** - Don't retroactively document
- **Focus on "why"** - Context matters more than "what"
- **Be concise but complete** - Include enough detail to understand later
- **Number sequentially** - 0001, 0002, 0003...
- **Keep them immutable** - Don't edit after acceptance, supersede instead
- **Link related ADRs** - Build decision narrative
- **Include diagrams** - Visualize architecture when helpful

### DON'T ❌

- **Document trivial decisions** - Reserve for significant choices
- **Write novels** - Keep under 2 pages if possible
- **Skip alternatives** - Show you considered options
- **Forget consequences** - Document trade-offs honestly
- **Leave status ambiguous** - Always set clear status
- **Delete old ADRs** - Supersede, don't delete

## Tools

### ADR Tools CLI

```bash
# Install
npm install -g adr-log

# Initialize ADR directory
adr init docs/adr

# Create new ADR
adr new "Use PostgreSQL as Primary Database"

# Generate index
adr generate toc > docs/adr/README.md

# Link ADRs
adr link 0002 "Supersedes" 0001
```

## Related Modules

- **README_STRUCTURE** - Project documentation
- **RELEASE_PROCESS** - Version and changelog
- **GIT_WORKFLOW** - Git commit and PR conventions
