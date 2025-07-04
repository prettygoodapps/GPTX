#!/usr/bin/env python3
"""
Migration script to clean up old project structure.

This script helps migrate from the old app/ structure to the new
src/gptx/ structure by removing old files and updating references.
"""

import os
import shutil
import sys
from pathlib import Path
from typing import List


def confirm_action(message: str) -> bool:
    """
    Ask user for confirmation.

    Args:
        message: Confirmation message

    Returns:
        True if user confirms, False otherwise
    """
    response = input(f"{message} (y/N): ").strip().lower()
    return response in ("y", "yes")


def remove_old_structure(project_root: Path) -> None:
    """
    Remove old project structure files.

    Args:
        project_root: Path to project root directory
    """
    old_paths = [
        project_root / "app",
        project_root / "run.py",
        project_root / "test_api.py",
        project_root / "requirements.txt",
    ]

    removed_files: List[str] = []

    for path in old_paths:
        if path.exists():
            if confirm_action(f"Remove {path}?"):
                if path.is_dir():
                    shutil.rmtree(path)
                    print(f"✅ Removed directory: {path}")
                else:
                    path.unlink()
                    print(f"✅ Removed file: {path}")
                removed_files.append(str(path))
            else:
                print(f"⏭️  Skipped: {path}")

    if removed_files:
        print(f"\n📝 Removed {len(removed_files)} old files/directories")
    else:
        print("\n📝 No old files were removed")


def update_gitignore(project_root: Path) -> None:
    """
    Update .gitignore for new structure.

    Args:
        project_root: Path to project root directory
    """
    gitignore_path = project_root / ".gitignore"

    # Standard Python .gitignore entries
    gitignore_content = """# Byte-compiled / optimized / DLL files
__pycache__/
*.py[cod]
*$py.class

# C extensions
*.so

# Distribution / packaging
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
share/python-wheels/
*.egg-info/
.installed.cfg
*.egg
MANIFEST

# PyInstaller
*.manifest
*.spec

# Installer logs
pip-log.txt
pip-delete-this-directory.txt

# Unit test / coverage reports
htmlcov/
.tox/
.nox/
.coverage
.coverage.*
.cache
nosetests.xml
coverage.xml
*.cover
*.py,cover
.hypothesis/
.pytest_cache/
cover/

# Translations
*.mo
*.pot

# Django stuff:
*.log
local_settings.py
db.sqlite3
db.sqlite3-journal

# Flask stuff:
instance/
.webassets-cache

# Scrapy stuff:
.scrapy

# Sphinx documentation
docs/_build/

# PyBuilder
.pybuilder/
target/

# Jupyter Notebook
.ipynb_checkpoints

# IPython
profile_default/
ipython_config.py

# pyenv
.python-version

# pipenv
Pipfile.lock

# poetry
poetry.lock

# pdm
.pdm.toml

# PEP 582
__pypackages__/

# Celery stuff
celerybeat-schedule
celerybeat.pid

# SageMath parsed files
*.sage.py

# Environments
.env
.venv
env/
venv/
ENV/
env.bak/
venv.bak/

# Spyder project settings
.spyderproject
.spyproject

# Rope project settings
.ropeproject

# mkdocs documentation
/site

# mypy
.mypy_cache/
.dmypy.json
dmypy.json

# Pyre type checker
.pyre/

# pytype static type analyzer
.pytype/

# Cython debug symbols
cython_debug/

# PyCharm
.idea/

# VS Code
.vscode/
!.vscode/extensions.json

# Project specific
.env.local
.env.production
node_modules/
hardhat-cache/
artifacts/
cache/
typechain-types/
"""

    if gitignore_path.exists():
        if confirm_action("Update .gitignore with standard Python entries?"):
            with open(gitignore_path, "w", encoding="utf-8") as f:
                f.write(gitignore_content)
            print("✅ Updated .gitignore")
        else:
            print("⏭️  Skipped .gitignore update")
    else:
        with open(gitignore_path, "w", encoding="utf-8") as f:
            f.write(gitignore_content)
        print("✅ Created .gitignore")


def check_new_structure(project_root: Path) -> bool:
    """
    Check if new structure exists.

    Args:
        project_root: Path to project root directory

    Returns:
        True if new structure exists, False otherwise
    """
    required_paths = [
        project_root / "src" / "gptx",
        project_root / "tests",
        project_root / "pyproject.toml",
        project_root / "Makefile",
    ]

    missing_paths = [path for path in required_paths if not path.exists()]

    if missing_paths:
        print("❌ New structure is incomplete. Missing:")
        for path in missing_paths:
            print(f"   - {path}")
        return False

    print("✅ New structure is complete")
    return True


def main() -> None:
    """Main migration function."""
    project_root = Path(__file__).parent.parent

    print("🔄 GPTX Exchange Migration to Kilo Code Compliance")
    print("=" * 50)

    # Check if new structure exists
    if not check_new_structure(project_root):
        print("\n❌ Cannot proceed with migration - new structure is incomplete")
        sys.exit(1)

    print("\n📋 This script will:")
    print("   1. Remove old app/ directory structure")
    print("   2. Remove old run.py and test_api.py files")
    print("   3. Remove old requirements.txt")
    print("   4. Update .gitignore")

    if not confirm_action("\nProceed with migration?"):
        print("❌ Migration cancelled")
        sys.exit(0)

    print("\n🧹 Cleaning up old structure...")
    remove_old_structure(project_root)

    print("\n📝 Updating configuration files...")
    update_gitignore(project_root)

    print("\n✅ Migration completed successfully!")
    print("\n📋 Next steps:")
    print("   1. Run 'make setup' to install dependencies")
    print("   2. Run 'make validate-all' to verify compliance")
    print("   3. Run 'make dev' to start development server")


if __name__ == "__main__":
    main()
