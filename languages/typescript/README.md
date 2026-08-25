# TypeScript Language Configuration

This directory contains TypeScript-specific configuration files for your project.

## 📁 Files

- **`.gitignore.ts`** - TypeScript-specific gitignore rules
- **`tsconfig.json`** - TypeScript compiler configuration
- **`package.json.example`** - Package.json example with scripts

## 🚀 Quick Start

```bash
# Copy TypeScript-specific gitignore
cat languages/typescript/.gitignore.ts >> .gitignore

# Copy TypeScript configuration
cp languages/typescript/tsconfig.json .

# Copy package.json template
cp languages/typescript/package.json.example package.json

# Install dependencies
npm install
```

## 🛠️ Tools & Setup

### Required
- **Node.js 20+**: [Install Node.js](https://nodejs.org/)
- **TypeScript**: Installed via npm

### Recommended
- **ESLint**: `npm install -D eslint @typescript-eslint/parser @typescript-eslint/eslint-plugin`
- **Prettier**: `npm install -D prettier`
- **Vitest**: `npm install -D vitest`

## 📝 Project Structure

```
your-project/
├── src/
│   ├── index.ts
│   └── utils/
├── tests/
│   └── index.test.ts
├── dist/
├── tsconfig.json
├── package.json
└── README.md
```

## 🧪 Common Commands

```bash
# Build
npm run build

# Development mode
npm run dev

# Run tests
npm test

# Lint
npm run lint

# Format
npm run format
```

## 📚 Resources

- [TypeScript Handbook](https://www.typescriptlang.org/docs/handbook/intro.html)
- [TypeScript Deep Dive](https://basarat.gitbook.io/typescript/)
- [Total TypeScript](https://www.totaltypescript.com/)
