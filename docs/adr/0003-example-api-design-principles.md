# 3. API Design Principles

Date: 2026-02-25

## Status

Accepted

## Context

We need to establish consistent API design principles for our REST API to ensure:

- Developer-friendly interface for frontend team
- Maintainability as the API grows
- Clear error handling and debugging
- Performance and scalability
- Security best practices

Current situation:
- Team has mixed experience with API design
- Will have multiple services consuming the API (web, mobile, third-party)
- Need to support versioning for backward compatibility

## Decision

We will follow these API design principles:

### 1. RESTful Resource Design
- Use nouns for endpoints, not verbs
- Use HTTP methods semantically (GET, POST, PUT, PATCH, DELETE)
- Nest resources logically

**Examples:**
```
✅ GET    /users/:id
✅ POST   /users
✅ PATCH  /users/:id
✅ DELETE /users/:id
✅ GET    /users/:id/posts

❌ GET /getUser?id=123
❌ POST /createUser
❌ GET /deleteUser?id=123
```

### 2. Consistent Response Format
All API responses follow this structure:

```typescript
// Success
{
  "data": { ... },
  "meta": {
    "timestamp": "2026-02-25T10:30:00Z",
    "requestId": "uuid"
  }
}

// Error
{
  "error": {
    "code": "RESOURCE_NOT_FOUND",
    "message": "User with ID 123 not found",
    "details": { ... }
  },
  "meta": {
    "timestamp": "2026-02-25T10:30:00Z",
    "requestId": "uuid"
  }
}
```

### 3. HTTP Status Codes
Use standard HTTP status codes appropriately:

- **200 OK**: Successful GET, PATCH, PUT
- **201 Created**: Successful POST
- **204 No Content**: Successful DELETE
- **400 Bad Request**: Invalid input
- **401 Unauthorized**: Missing/invalid authentication
- **403 Forbidden**: Authenticated but not authorized
- **404 Not Found**: Resource doesn't exist
- **409 Conflict**: Resource conflict (e.g., duplicate email)
- **422 Unprocessable Entity**: Validation errors
- **429 Too Many Requests**: Rate limit exceeded
- **500 Internal Server Error**: Server error

### 4. Versioning Strategy
- Use URL versioning: `/api/v1/users`
- Maintain at least 2 versions during transition
- Deprecation warnings in response headers
- Sunset dates communicated 6 months in advance

### 5. Pagination
For list endpoints:

```typescript
GET /api/v1/users?page=1&limit=20&sort=-createdAt

Response:
{
  "data": [...],
  "meta": {
    "pagination": {
      "page": 1,
      "limit": 20,
      "total": 150,
      "totalPages": 8
    }
  }
}
```

### 6. Filtering & Searching
```typescript
// Filtering
GET /api/v1/users?status=active&role=admin

// Searching
GET /api/v1/users?search=john

// Sorting
GET /api/v1/users?sort=-createdAt,name
```

### 7. Field Selection (Sparse Fieldsets)
```typescript
// Only return specific fields
GET /api/v1/users?fields=id,name,email
```

### 8. Security
- **Authentication**: JWT in `Authorization: Bearer <token>` header
- **Rate Limiting**: 100 requests per minute per IP
- **CORS**: Whitelist specific origins
- **Input Validation**: All inputs validated with Zod
- **SQL Injection Prevention**: Use Prisma ORM (parameterized queries)
- **Sensitive Data**: Never log passwords, tokens, or PII

## Consequences

### Positive

- **Consistency**: All endpoints follow same patterns, easier to learn and use
- **Predictability**: Developers can predict API behavior
- **Debugging**: Request IDs and structured errors simplify troubleshooting
- **Versioning**: API can evolve without breaking existing clients
- **Security**: Built-in protections against common vulnerabilities
- **Performance**: Pagination and field selection reduce payload sizes

### Negative

- **Overhead**: More boilerplate code for consistent response formatting
- **Complexity**: Versioning adds deployment and maintenance complexity
- **Documentation**: Requires comprehensive API documentation
- **Learning Curve**: Team needs to learn and follow these conventions

### Risks

- **Over-Engineering**: May be excessive for simple APIs
  - *Mitigation*: Start simple, add complexity as needed
- **Breaking Changes**: Mistakes in versioning strategy can break clients
  - *Mitigation*: Automated tests for API contract, deprecation warnings
- **Performance**: Response wrapping adds slight overhead
  - *Mitigation*: Negligible impact, benefits outweigh costs

## Alternatives Considered

### Alternative 1: GraphQL
- **Pros**: Client-specified queries, strong typing, single endpoint
- **Cons**: Higher complexity, requires Apollo/GraphQL expertise, harder to cache

### Alternative 2: gRPC
- **Pros**: High performance, bi-directional streaming, strong typing
- **Cons**: Not web-browser friendly, requires code generation, steeper learning curve

### Alternative 3: No Versioning
- **Pros**: Simpler deployment, no version management
- **Cons**: Breaking changes affect all clients immediately, no graceful migration path

## Tools & Implementation

- **Validation**: Zod for request/response validation
- **Documentation**: OpenAPI 3.0 (Swagger)
- **Testing**: Supertest for API integration tests
- **Rate Limiting**: express-rate-limit
- **CORS**: cors middleware

## References

- [REST API Design Best Practices](https://restfulapi.net/)
- [OpenAPI Specification](https://swagger.io/specification/)
- [HTTP Status Codes](https://httpstatuses.com/)
- [Microsoft API Guidelines](https://github.com/microsoft/api-guidelines)
- [Google API Design Guide](https://cloud.google.com/apis/design)

## Review Schedule

Review these principles:
- After 3 months of production use
- When onboarding new team members (gather feedback)
- If major scaling or architectural changes occur
