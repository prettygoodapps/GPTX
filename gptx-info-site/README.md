# GPTX Exchange

A decentralized AI model marketplace built with FastAPI, enabling secure trading of AI models with blockchain integration and carbon offset tracking.

## 🚀 Features

- **AI Model Trading**: Secure marketplace for AI model exchange
- **Blockchain Integration**: Ethereum-based smart contracts for transactions
- **Carbon Offset Tracking**: Environmental impact monitoring and offsetting
- **Multi-Provider Support**: Integration with OpenAI, Anthropic, and other AI providers
- **RESTful API**: Comprehensive API with automatic documentation
- **Type Safety**: Full type hints and validation with Pydantic
- **Production Ready**: Comprehensive testing, logging, and monitoring

## 🏗️ Architecture

This project follows Kilo Code compliance standards with:

- **Python 3.9+** with modern async/await patterns
- **FastAPI** framework for high-performance APIs
- **SQLAlchemy** ORM with PostgreSQL support
- **Pydantic** for data validation and settings management
- **Poetry** for dependency management
- **Comprehensive testing** with pytest and 80%+ coverage
- **Code quality tools** (Black, isort, mypy, flake8, bandit)
- **Pre-commit hooks** for automated quality checks

## 📁 Project Structure

```
gptx-info-site/
├── src/gptx/                 # Main application package
│   ├── core/                 # Core functionality
│   │   ├── config.py         # Configuration management
│   │   ├── database.py       # Database models and setup
│   │   └── logging.py        # Logging configuration
│   ├── routers/              # API route handlers
│   │   ├── tokens.py         # Token management endpoints
│   │   ├── exchange.py       # Exchange functionality
│   │   └── carbon.py         # Carbon offset tracking
│   ├── services/             # Business logic services
│   │   ├── ai_providers.py   # AI provider integrations
│   │   └── blockchain.py     # Blockchain interactions
│   └── main.py               # FastAPI application entry point
├── tests/                    # Test suite
│   ├── unit/                 # Unit tests
│   ├── integration/          # Integration tests
│   └── conftest.py           # Test configuration
├── scripts/                  # Development scripts
│   ├── dev_server.py         # Development server
│   ├── check_docstrings.py   # Docstring validation
│   └── migrate_to_compliance.py # Migration helper
├── pyproject.toml            # Project configuration
├── Makefile                  # Development commands
└── .pre-commit-config.yaml   # Pre-commit hooks
```

## 🛠️ Development Setup

### Prerequisites

- Python 3.9+
- Poetry (for dependency management)
- PostgreSQL (for database)
- Node.js (for blockchain development)

### Quick Start

1. **Clone and setup**:
   ```bash
   git clone <repository-url>
   cd gptx-info-site
   make setup
   ```

2. **Configure environment**:
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

3. **Run development server**:
   ```bash
   make dev
   ```

4. **Run tests**:
   ```bash
   make test
   ```

5. **Validate code quality**:
   ```bash
   make validate-all
   ```

### Available Commands

```bash
# Setup and installation
make setup              # Install dependencies and pre-commit hooks
make install            # Install dependencies only

# Development
make dev                # Start development server
make shell              # Start Python shell with project context

# Code Quality
make lint               # Run all linters (black, isort, flake8, mypy)
make format             # Format code with black and isort
make type-check         # Run mypy type checking
make security           # Run bandit security checks

# Testing
make test               # Run test suite
make test-unit          # Run unit tests only
make test-integration   # Run integration tests only
make coverage           # Generate coverage report

# Documentation
make docs               # Check docstring coverage
make validate-all       # Run all validation checks

# Cleanup
make clean              # Remove cache and build files
```

## 🔧 Configuration

The application uses Pydantic Settings for configuration management. Key settings:

```python
# Environment variables
DATABASE_URL=postgresql://user:pass@localhost/gptx
OPENAI_API_KEY=your_openai_key
ANTHROPIC_API_KEY=your_anthropic_key
ETHEREUM_RPC_URL=your_ethereum_rpc
SECRET_KEY=your_secret_key
```

## 📊 API Documentation

Once running, visit:
- **Interactive API docs**: http://localhost:8000/docs
- **ReDoc documentation**: http://localhost:8000/redoc
- **Health check**: http://localhost:8000/health

### Key Endpoints

- `GET /health` - Health check and system status
- `POST /tokens/` - Create new AI model token
- `GET /tokens/` - List available tokens
- `POST /exchange/trade` - Execute trade between tokens
- `GET /exchange/rates` - Get current exchange rates
- `POST /carbon/offset` - Purchase carbon offsets
- `GET /carbon/footprint` - Calculate carbon footprint

## 🧪 Testing

The project includes comprehensive testing:

- **Unit tests**: Test individual components in isolation
- **Integration tests**: Test complete workflows and API endpoints
- **Fixtures**: Reusable test data and mocks
- **Coverage**: Minimum 80% code coverage requirement

Run specific test categories:
```bash
pytest tests/unit/                    # Unit tests only
pytest tests/integration/             # Integration tests only
pytest --cov=src/gptx --cov-report=html  # Coverage report
```

## 🔒 Security

Security measures implemented:

- **Input validation** with Pydantic models
- **SQL injection protection** with SQLAlchemy ORM
- **Security scanning** with Bandit
- **Dependency scanning** with Safety
- **Environment variable protection**
- **Rate limiting** and request validation

## 🌱 Carbon Offset Integration

The platform includes carbon footprint tracking:

- **Automatic calculation** of AI model training/inference emissions
- **Carbon offset marketplace** integration
- **Sustainability reporting** and metrics
- **Green AI provider** prioritization

## 🚀 Deployment

### Production Deployment

1. **Build and test**:
   ```bash
   make validate-all
   ```

2. **Configure production environment**:
   ```bash
   export ENVIRONMENT=production
   export DATABASE_URL=your_production_db
   # Set other production variables
   ```

3. **Run with production server**:
   ```bash
   poetry run uvicorn gptx.main:app --host 0.0.0.0 --port 8000
   ```

### Docker Deployment

```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY pyproject.toml poetry.lock ./
RUN pip install poetry && poetry install --no-dev
COPY src/ ./src/
CMD ["poetry", "run", "uvicorn", "gptx.main:app", "--host", "0.0.0.0"]
```

## 🤝 Contributing

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/amazing-feature`
3. **Make changes** following the code style
4. **Run validation**: `make validate-all`
5. **Commit changes**: `git commit -m 'Add amazing feature'`
6. **Push to branch**: `git push origin feature/amazing-feature`
7. **Open a Pull Request**

### Code Style

- **Black** for code formatting
- **isort** for import sorting
- **Type hints** for all functions
- **Docstrings** for all public functions (Google style)
- **Comprehensive tests** for new features

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

- **Documentation**: Check the `/docs` endpoint when running
- **Issues**: Open an issue on GitHub
- **Discussions**: Use GitHub Discussions for questions

## 🗺️ Roadmap

- [ ] Advanced AI model analytics
- [ ] Multi-chain blockchain support
- [ ] Enhanced carbon tracking algorithms
- [ ] Mobile API endpoints
- [ ] Real-time trading dashboard
- [ ] Advanced security features

---

**Built with ❤️ using Kilo Code standards for production-ready Python applications.**
