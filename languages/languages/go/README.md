# Go Language Configuration

This directory contains Go-specific configuration files for your project.

## 📁 Files

- **`.gitignore.go`** - Go-specific gitignore rules
- **`.golangci.yml`** - GolangCI-Lint configuration
- **`Makefile`** - Common Go commands
- **`go.mod.example`** - Go module example

## 🚀 Quick Start

```bash
# Copy Go-specific gitignore
cat templates/languages/go/.gitignore.go >> .gitignore

# Copy linter configuration
cp templates/languages/go/.golangci.yml .

# Copy Makefile
cp templates/languages/go/Makefile .

# Initialize Go module
go mod init github.com/your-username/your-project
```

## 🛠️ Tools & Setup

### Required
- **Go 1.21+**: [Install Go](https://go.dev/doc/install)

### Recommended
- **GolangCI-Lint**: `brew install golangci-lint` or see [installation guide](https://golangci-lint.run/usage/install/)
- **Air**: Live reload for Go apps - `go install github.com/cosmtrek/air@latest`

## 📝 Project Structure

```
your-project/
├── cmd/
│   └── app/
│       └── main.go
├── internal/
│   ├── handler/
│   ├── service/
│   └── repository/
├── pkg/
│   └── utils/
├── go.mod
├── go.sum
├── Makefile
└── .golangci.yml
```

## 🧪 Common Commands

```bash
# Run tests
make test

# Run with coverage
make test-coverage

# Lint code
make lint

# Build binary
make build

# Run locally
make run
```

## 📚 Resources

- [Effective Go](https://go.dev/doc/effective_go)
- [Go Code Review Comments](https://github.com/golang/go/wiki/CodeReviewComments)
- [Standard Go Project Layout](https://github.com/golang-standards/project-layout)
