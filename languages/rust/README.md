# Rust Language Configuration

This directory contains Rust-specific configuration files for your project.

## 📁 Files

- **`.gitignore.rust`** - Rust-specific gitignore rules
- **`Cargo.toml.example`** - Cargo manifest example
- **`rustfmt.toml`** - Rust formatter configuration

## 🚀 Quick Start

```bash
# Copy Rust-specific gitignore
cat languages/rust/.gitignore.rust >> .gitignore

# Copy Cargo configuration
cp languages/rust/Cargo.toml.example Cargo.toml

# Copy formatter configuration
cp languages/rust/rustfmt.toml .

# Initialize new Rust project (or use existing)
cargo init

# Build project
cargo build
```

## 🛠️ Tools & Setup

### Required
- **Rust 1.75+**: [Install Rust](https://www.rust-lang.org/tools/install)

### Recommended
- **Clippy**: Linter (included with Rust) - `cargo clippy`
- **Rustfmt**: Formatter (included with Rust) - `cargo fmt`
- **Cargo Watch**: Auto-rebuild - `cargo install cargo-watch`

## 📝 Project Structure

```
your-project/
├── src/
│   ├── main.rs
│   └── lib.rs
├── tests/
│   └── integration_test.rs
├── Cargo.toml
├── Cargo.lock
└── README.md
```

## 🧪 Common Commands

```bash
# Build
cargo build

# Build (release mode)
cargo build --release

# Run
cargo run

# Test
cargo test

# Lint
cargo clippy

# Format
cargo fmt

# Check (fast compile check)
cargo check
```

## 📚 Resources

- [The Rust Programming Language](https://doc.rust-lang.org/book/)
- [Rust by Example](https://doc.rust-lang.org/rust-by-example/)
- [Rustlings](https://github.com/rust-lang/rustlings)
