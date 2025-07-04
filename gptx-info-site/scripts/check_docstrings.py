#!/usr/bin/env python3
"""
Docstring validation script for GPTX Exchange.

This script checks that all public functions, classes, and methods
have proper docstrings following Google style conventions.
"""

import ast
import sys
from pathlib import Path
from typing import List, Tuple, Union


class DocstringChecker(ast.NodeVisitor):
    """AST visitor to check for missing docstrings."""

    def __init__(self) -> None:
        """Initialize the docstring checker."""
        self.issues: List[Tuple[str, int, str]] = []
        self.current_file = ""

    def check_file(self, file_path: Path) -> List[Tuple[str, int, str]]:
        """
        Check a Python file for missing docstrings.

        Args:
            file_path: Path to the Python file to check

        Returns:
            List of issues found (file, line, message)
        """
        self.current_file = str(file_path)
        self.issues = []

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()

            tree = ast.parse(content, filename=str(file_path))
            self.visit(tree)
        except Exception as e:
            self.issues.append((self.current_file, 0, f"Error parsing file: {e}"))

        return self.issues

    def _has_docstring(
        self, node: Union[ast.FunctionDef, ast.ClassDef, ast.AsyncFunctionDef]
    ) -> bool:
        """Check if a node has a docstring."""
        if not node.body:
            return False

        first_stmt = node.body[0]
        return (
            isinstance(first_stmt, ast.Expr)
            and isinstance(first_stmt.value, ast.Constant)
            and isinstance(first_stmt.value.value, str)
        )

    def _is_private(self, name: str) -> bool:
        """Check if a name is private (starts with underscore)."""
        return name.startswith("_")

    def visit_ClassDef(self, node: ast.ClassDef) -> None:
        """Visit class definitions."""
        if not self._is_private(node.name) and not self._has_docstring(node):
            self.issues.append(
                (
                    self.current_file,
                    node.lineno,
                    f"Public class '{node.name}' missing docstring",
                )
            )

        self.generic_visit(node)

    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        """Visit function definitions."""
        if not self._is_private(node.name) and not self._has_docstring(node):
            self.issues.append(
                (
                    self.current_file,
                    node.lineno,
                    f"Public function '{node.name}' missing docstring",
                )
            )

        self.generic_visit(node)

    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef) -> None:
        """Visit async function definitions."""
        if not self._is_private(node.name) and not self._has_docstring(node):
            self.issues.append(
                (
                    self.current_file,
                    node.lineno,
                    f"Public async function '{node.name}' missing docstring",
                )
            )

        self.generic_visit(node)


def check_docstrings(src_dir: Path) -> int:
    """
    Check all Python files in src directory for missing docstrings.

    Args:
        src_dir: Path to the source directory

    Returns:
        Number of issues found
    """
    checker = DocstringChecker()
    total_issues = 0

    # Find all Python files
    python_files = list(src_dir.rglob("*.py"))

    if not python_files:
        print(f"No Python files found in {src_dir}")
        return 0

    print(f"Checking {len(python_files)} Python files for docstrings...")

    for file_path in python_files:
        issues = checker.check_file(file_path)

        if issues:
            print(f"\n{file_path}:")
            for _, line_no, message in issues:
                print(f"  Line {line_no}: {message}")
            total_issues += len(issues)

    if total_issues == 0:
        print("✅ All public functions and classes have docstrings!")
    else:
        print(f"\n❌ Found {total_issues} missing docstrings")

    return total_issues


def main() -> None:
    """Main entry point."""
    project_root = Path(__file__).parent.parent
    src_dir = project_root / "src"

    if not src_dir.exists():
        print(f"Source directory not found: {src_dir}")
        sys.exit(1)

    issues = check_docstrings(src_dir)
    sys.exit(1 if issues > 0 else 0)


if __name__ == "__main__":
    main()
