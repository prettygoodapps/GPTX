# Contributing to GPTX Green AI Ledger

We welcome contributions to the GPTX Green AI Ledger project! By following these guidelines, you can help us maintain a high-quality, consistent, and sustainable codebase aligned with enterprise-level best practices for commercial applications.

## 🎯 Project Goals & Principles

Our development is guided by these core principles:

*   **Sustainability First:** All features and changes should align with our mission to measure, manage, and mitigate the carbon footprint of AI workloads.
*   **High-Quality Code Standards:** We prioritize clean, maintainable, robust, and secure code.
*   **Automated Workflows:** We leverage automation for consistency, efficiency, and reliability in development, testing, and deployment.
*   **Transparency & Verifiability:** Especially for blockchain-related components, clarity and auditability are paramount.

## 🛠️ Development Workflow & Tools

To ensure alignment with our goals, we utilize a set of automated tools and follow specific practices.

### Code Style & Quality

We enforce consistent code style and quality using automated tools. For a comprehensive check, run:

*   **Full Validation:** `make validate-all` (This command orchestrates formatting, linting, type checking, and security scanning.)

### Testing & Reliability

All contributions must include appropriate tests (unit, integration) to ensure functionality, prevent regressions, and maintain reliability.

*   **Framework:** `Pytest` (Python testing framework).
*   **Coverage:** Aim for high code coverage (minimum 80%) to ensure thorough testing.
*   **Run Tests:** `make test` (This command executes the test suite with coverage reporting.)

### Security

Security is a paramount concern. We integrate security practices throughout the development lifecycle.

*   **Automated Scanning:** `Bandit` (as part of `make lint`) helps identify common security vulnerabilities.
*   **Input Validation:** `Pydantic` models are used extensively for robust data validation at API boundaries.
*   **Best Practices:** Adhere to secure coding principles, especially when dealing with sensitive data or blockchain interactions.

## 📝 Documentation & Communication

Clear and up-to-date documentation is vital for collaboration and project understanding.

*   **Code Comments:** Explain *why* complex logic or non-obvious decisions were made, rather than just *what* the code does.
*   **Markdown Files:** Keep project-level documentation (e.g., `README.md`, `ARCHITECTURE.md`) current.
*   **Commit Messages:** Follow Conventional Commits for a clear and consistent history.
    *   **Format:** `type(scope): subject` (e.g., `feat(api): add carbon estimation endpoint`)
    *   **Types:** `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`, etc.

## 🚀 Contribution Process

1.  **Fork the repository** and create a new branch (`git checkout -b feature/your-feature-name`).
2.  **Implement your changes**, adhering to the code style and quality guidelines.
3.  **Write or update tests** to cover your changes.
4.  **Run all local validation checks** (`make validate-all` and `make test`) to ensure everything passes.
5.  **Commit your changes** using the Conventional Commits format.
6.  **Push your branch** to your fork.
7.  **Open a Pull Request** to the `main` branch. Provide a clear description of your changes and reference any related issues.

## 🤖 Guidelines for Automated Agents

For automated agents interacting with this repository, please adhere to the following to ensure compliant context and effective collaboration:

*   **Infer & Adhere:** Always infer and strictly adhere to the existing code style, project structure, and architectural patterns present in the codebase.
*   **Validate All Changes:** Before proposing or committing any modifications, execute the project's full suite of validation checks (`make validate-all`) and tests (`make test`). Only proceed if all checks pass without errors or warnings.
*   **Atomic & Focused:** Aim for small, atomic changes that address a single, clearly defined concern.
*   **Reliable Text Replacement:** When modifying existing code, read the file content, perform string replacements using Python's built-in methods, and then write the modified content back to the file. This ensures precise and reliable changes.
*   **Explain Intent:** For significant or non-obvious changes, include a concise explanation of the rationale (`why`) behind the modification.
*   **Respect `.gitignore`:** Do not modify, create, or interact with files or directories listed in `.gitignore`.
*   **No External Assumptions:** Do not assume the presence, appropriateness, or usage of any external libraries, frameworks, or tools unless they are explicitly declared in the project's dependency management files (`pyproject.toml`, `package.json`, etc.) or explicitly instructed by the user.