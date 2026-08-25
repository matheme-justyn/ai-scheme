# Go-specific gitignore

# Binaries for programs and plugins
*.exe
*.exe~
*.dll
*.so
*.dylib

# Test binary, built with `go test -c`
*.test

# Output of the go coverage tool, specifically when used with LiteIDE
*.out

# Dependency directories (remove the comment below to include it)
vendor/

# Go workspace file
go.work

# Air - Live reload for Go apps
tmp/

# Built binaries
bin/
dist/

# Coverage reports
coverage.txt
coverage.html
*.cover

# Profiling data
*.prof
*.pprof

# IDE-specific
.vscode/
.idea/

# Environment variables
.env
.env.local
