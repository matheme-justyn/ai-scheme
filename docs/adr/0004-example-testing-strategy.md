# 4. Testing Strategy

Date: 2026-02-25

## Status

Accepted

## Context

We need to establish a comprehensive testing strategy that:

- Ensures code quality and reliability
- Catches bugs early in development
- Enables confident refactoring
- Supports continuous deployment
- Balances test coverage with development speed

Current situation:
- Team has varying testing experience
- Need to test both frontend (React) and backend (Node.js)
- Limited CI/CD pipeline capacity
- 3-month MVP timeline

## Decision

We will implement a **Test Pyramid** approach with the following layers:

### 1. Unit Tests (70% of tests)
**What**: Test individual functions and components in isolation

**Tools**:
- **Frontend**: Vitest + React Testing Library
- **Backend**: Vitest + Node.js
- **Mocking**: vi.mock()

**Coverage Target**: 80%+ for business logic

**Examples**:
```typescript
// Unit test example
describe('calculateTotal', () => {
  it('should sum item prices correctly', () => {
    const items = [{ price: 10 }, { price: 20 }];
    expect(calculateTotal(items)).toBe(30);
  });
  
  it('should handle empty array', () => {
    expect(calculateTotal([])).toBe(0);
  });
});
```

**When to Write**:
- All utility functions
- Business logic
- State management
- React components (behavior, not implementation)

### 2. Integration Tests (20% of tests)
**What**: Test interaction between components/modules

**Tools**:
- **Frontend**: Vitest + React Testing Library (multi-component tests)
- **Backend**: Supertest + Test Database
- **Database**: PostgreSQL test instance (dockerized)

**Examples**:
```typescript
// API integration test
describe('POST /api/v1/users', () => {
  it('should create user and return 201', async () => {
    const response = await request(app)
      .post('/api/v1/users')
      .send({ name: 'John', email: 'john@example.com' });
    
    expect(response.status).toBe(201);
    expect(response.body.data).toHaveProperty('id');
  });
});
```

**When to Write**:
- API endpoints
- Database interactions
- Multi-component workflows
- Authentication/authorization flows

### 3. End-to-End Tests (10% of tests)
**What**: Test entire user workflows from UI to database

**Tools**:
- **Framework**: Playwright
- **Environment**: Staging environment
- **Data**: Seeded test data

**Examples**:
```typescript
// E2E test example
test('user can complete signup flow', async ({ page }) => {
  await page.goto('/signup');
  await page.fill('[name="email"]', 'test@example.com');
  await page.fill('[name="password"]', 'SecurePass123');
  await page.click('button[type="submit"]');
  
  await expect(page).toHaveURL('/dashboard');
  await expect(page.locator('h1')).toContainText('Welcome');
});
```

**When to Write**:
- Critical user journeys (signup, checkout, etc.)
- Cross-browser compatibility
- Visual regression testing

## Testing Principles

### 1. Test Behavior, Not Implementation
```typescript
// ❌ Bad: Testing implementation details
expect(component.state.count).toBe(1);

// ✅ Good: Testing behavior
expect(screen.getByText('Count: 1')).toBeInTheDocument();
```

### 2. Write Tests First (TDD)
- Write failing test
- Write minimal code to pass
- Refactor
- Repeat

### 3. Keep Tests Fast
- Unit tests: < 100ms each
- Integration tests: < 1s each
- E2E tests: < 30s each
- **Run frequently**: Unit tests on every save, integration on commit, E2E on PR

### 4. Test in Isolation
- No shared state between tests
- Use beforeEach/afterEach for cleanup
- Mock external dependencies

### 5. Clear Test Names
```typescript
// ❌ Bad
it('works', () => { ... });

// ✅ Good
it('should return 404 when user does not exist', () => { ... });
```

## CI/CD Integration

### Pre-commit
- Lint
- Type check
- Unit tests (changed files only)

### On Pull Request
- Full unit test suite
- Integration tests
- E2E tests (critical paths only)
- Coverage report

### Pre-deployment
- Full test suite
- E2E tests (all scenarios)
- Performance tests

## Coverage Requirements

| Layer | Minimum Coverage | Target Coverage |
|-------|-----------------|-----------------|
| Unit Tests | 70% | 80%+ |
| Integration Tests | 50% | 70% |
| E2E Tests | Critical paths | Major workflows |

**Coverage exceptions**:
- Configuration files
- Type definitions
- Third-party integrations (mock instead)

## Test Data Management

### Unit Tests
- Use hardcoded test data
- Factory functions for complex objects

### Integration Tests
- Test database seeded before each test
- Use transactions (rollback after test)

### E2E Tests
- Dedicated test environment
- Seed data before suite
- Clean up after suite

## Consequences

### Positive

- **Confidence**: Can refactor and deploy without fear
- **Documentation**: Tests serve as living documentation
- **Bug Prevention**: Catch regressions early
- **Faster Development**: Less time debugging in production
- **CI/CD**: Automated quality gates
- **Team Alignment**: Shared understanding of expected behavior

### Negative

- **Initial Investment**: Takes time to write tests
- **Maintenance**: Tests need updates when features change
- **False Security**: Bad tests give false confidence
- **Slow CI**: Full test suite may slow down pipeline
- **Test Data**: Managing test data adds complexity

### Risks

- **Flaky Tests**: Intermittent failures in E2E tests
  - *Mitigation*: Retry failed tests, use explicit waits, avoid sleep()
- **Over-Testing**: Testing implementation details slows refactoring
  - *Mitigation*: Focus on behavior, not implementation
- **Under-Testing**: Skipping tests to meet deadlines
  - *Mitigation*: Required coverage gates in CI

## Alternatives Considered

### Alternative 1: Manual Testing Only
- **Pros**: No test code to maintain, faster initial development
- **Cons**: High risk of regressions, slow feedback, not scalable

### Alternative 2: 100% E2E Testing
- **Pros**: Tests real user flows, high confidence
- **Cons**: Slow, flaky, expensive to maintain, hard to debug

### Alternative 3: Integration-Heavy Testing
- **Pros**: Good coverage of real interactions
- **Cons**: Slower than unit tests, harder to isolate failures

## Tools Summary

```json
{
  "unit": ["vitest", "@testing-library/react"],
  "integration": ["supertest", "test-containers"],
  "e2e": ["@playwright/test"],
  "coverage": ["vitest", "istanbul"],
  "ci": ["github-actions"]
}
```

## Implementation Timeline

- **Week 1**: Setup Vitest, write first unit tests
- **Week 2**: Integration test framework, test database
- **Week 3**: Playwright setup, first E2E test
- **Week 4**: CI/CD integration, coverage reports
- **Ongoing**: TDD for new features

## References

- [Testing Library Guiding Principles](https://testing-library.com/docs/guiding-principles/)
- [Playwright Best Practices](https://playwright.dev/docs/best-practices)
- [Vitest Documentation](https://vitest.dev/)
- [Test Pyramid](https://martinfowler.com/articles/practical-test-pyramid.html)
- [Kent C. Dodds - Testing Trophy](https://kentcdodds.com/blog/the-testing-trophy-and-testing-classifications)

## Review Schedule

Review this strategy:
- After first 100 tests written
- Every 3 months
- When adding new testing layers
- If CI/CD time exceeds 10 minutes
