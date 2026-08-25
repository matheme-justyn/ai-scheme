# TypeScript-specific gitignore

# Compiled output
dist/
build/
out/
*.js
*.js.map
*.d.ts
!vite.config.ts
!vitest.config.ts

# Dependencies
node_modules/

# Testing
coverage/
.nyc_output/

# TypeScript cache
*.tsbuildinfo
.tsbuildinfo

# Environment variables
.env
.env.local
.env.*.local

# IDE
.vscode/
.idea/

# Logs
logs/
*.log
npm-debug.log*
yarn-debug.log*
yarn-error.log*

# OS
.DS_Store
Thumbs.db
