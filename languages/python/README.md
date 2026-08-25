# Python Language Configuration

This directory contains Python-specific configuration files for your project.

## 📁 Files

- **`.gitignore.python`** - Python-specific gitignore rules
- **`pyproject.toml`** - Modern Python project configuration
- **`requirements.txt.example`** - Dependencies example

## 🚀 Quick Start

```bash
# Copy Python-specific gitignore
cat languages/python/.gitignore.python >> .gitignore

# Copy project configuration
cp languages/python/pyproject.toml .

# Copy requirements file
cp languages/python/requirements.txt.example requirements.txt

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## 🛠️ Tools & Setup

### Required
- **Python 3.11+**: [Install Python](https://www.python.org/downloads/)

### Recommended
- **Ruff**: Fast linter and formatter - `pip install ruff`
- **Pytest**: Testing framework - `pip install pytest`
- **Mypy**: Static type checker - `pip install mypy`

## 📝 Project Structure

```
your-project/
├── src/
│   └── your_package/
│       ├── __init__.py
│       └── main.py
├── tests/
│   ├── __init__.py
│   └── test_main.py
├── pyproject.toml
├── requirements.txt
└── README.md
```

## 🧪 Common Commands

```bash
# Run tests
pytest

# Run with coverage
pytest --cov=src

# Lint and format
ruff check .
ruff format .

# Type checking
mypy src/
```

## 📚 Resources

- [Python Best Practices](https://docs.python-guide.org/)
- [PEP 8 Style Guide](https://peps.python.org/pep-0008/)
- [Real Python Tutorials](https://realpython.com/)
