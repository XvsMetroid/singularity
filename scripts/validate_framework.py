#!/usr/bin/env python3
"""
Validation script for The Axiom Engine framework.
Checks document structure, consistency, and adherence to core principles.
"""

import os
import re
import sys
import yaml
import json
from pathlib import Path
from typing import Dict, List, Set, Tuple

class FrameworkValidator:
    def __init__(self, root_dir: Path):
        self.root_dir = root_dir
        self.errors = []
        self.warnings = []
        self.core_principles = ["truth", "wisdom", "humanity"]
        self.required_dirs = [
            "01_CORE",
            "04_RESEARCH",
            "05_RESOURCES",
            "06_COMMUNITY",
            "07_VISUALS"
        ]

    def validate_all(self) -> bool:
        """Run all validation checks."""
        print("🔍 Validating The Axiom Engine framework...")

        self.check_directory_structure()
        self.check_core_documents()
        self.check_metadata_tags()
        self.check_cross_references()
        self.check_principle_alignment()
        self.validate_framework_yaml()

        return self.report_results()

    def check_directory_structure(self):
        """Verify required directories exist."""
        print("\n📁 Checking directory structure...")
        for dir_name in self.required_dirs:
            dir_path = self.root_dir / dir_name
            if not dir_path.exists():
                self.errors.append(f"Required directory missing: {dir_name}")
            elif not dir_path.is_dir():
                self.errors.append(f"Path exists but is not a directory: {dir_name}")

    def check_core_documents(self):
        """Verify essential core documents exist."""
        print("📄 Checking core documents...")
        core_docs = [
            "01_CORE/00_The_Constitution.md",
            "01_CORE/01_The_Genesis_and_Cognitive_Methodology.md",
            "01_CORE/03_Glossary_of_Terms.md"
        ]

        for doc in core_docs:
            doc_path = self.root_dir / doc
            if not doc_path.exists():
                self.errors.append(f"Core document missing: {doc}")

    def check_metadata_tags(self):
        """Check if markdown files have proper metadata tags."""
        print("🏷️  Checking metadata tags...")
        md_files = self.root_dir.glob("**/*.md")

        for file_path in md_files:
            if "node_modules" in str(file_path) or "site" in str(file_path):
                continue

            content = file_path.read_text(encoding='utf-8')

            # Check for tags at the top of the file
            if not re.search(r'^tags:\s*\[.*\]', content, re.MULTILINE):
                rel_path = file_path.relative_to(self.root_dir)
                if str(rel_path).startswith(("01_CORE", "04_RESEARCH", "05_RESOURCES")):
                    self.warnings.append(f"Missing metadata tags: {rel_path}")

    def check_cross_references(self):
        """Validate internal document references."""
        print("🔗 Checking cross-references...")
        md_files = list(self.root_dir.glob("**/*.md"))
        existing_files = {str(f.relative_to(self.root_dir)) for f in md_files}

        for file_path in md_files:
            if "node_modules" in str(file_path) or "site" in str(file_path):
                continue

            content = file_path.read_text(encoding='utf-8')

            # Find markdown links
            links = re.findall(r'\[.*?\]\((.*?\.md)\)', content)

            for link in links:
                if link.startswith("http"):
                    continue

                # Resolve relative paths
                if not link.startswith("/"):
                    link_path = (file_path.parent / link).resolve()
                    try:
                        rel_link = link_path.relative_to(self.root_dir)
                    except ValueError:
                        continue
                else:
                    rel_link = link.lstrip("/")

                if str(rel_link) not in existing_files:
                    rel_path = file_path.relative_to(self.root_dir)
                    self.warnings.append(f"Broken link in {rel_path}: {link}")

    def check_principle_alignment(self):
        """Check if documents reference core principles."""
        print("🎯 Checking principle alignment...")

        for doc_dir in ["04_RESEARCH", "proposals"]:
            dir_path = self.root_dir / doc_dir
            if not dir_path.exists():
                continue

            md_files = dir_path.glob("**/*.md")

            for file_path in md_files:
                content = file_path.read_text(encoding='utf-8').lower()

                # Check if at least one core principle is mentioned
                principles_found = [p for p in self.core_principles if p in content]

                if not principles_found:
                    rel_path = file_path.relative_to(self.root_dir)
                    self.warnings.append(
                        f"Document doesn't reference core principles: {rel_path}"
                    )

    def validate_framework_yaml(self):
        """Validate framework.yaml structure."""
        print("⚙️  Validating framework.yaml...")
        yaml_path = self.root_dir / "framework.yaml"

        if not yaml_path.exists():
            self.errors.append("framework.yaml is missing")
            return

        try:
            with open(yaml_path, 'r') as f:
                framework = yaml.safe_load(f)

            # Check required sections
            required_sections = ["core_principles", "golden_rule", "feedback_loop"]
            for section in required_sections:
                if section not in framework:
                    self.errors.append(f"framework.yaml missing section: {section}")

            # Validate core principles
            if "core_principles" in framework:
                principles = framework["core_principles"]
                if "sovereign_triad" not in principles:
                    self.errors.append("framework.yaml missing sovereign_triad")
                elif "components" in principles["sovereign_triad"]:
                    components = principles["sovereign_triad"]["components"]
                    for principle in ["truth", "wisdom", "humanity"]:
                        if principle not in components:
                            self.errors.append(
                                f"framework.yaml missing core principle: {principle}"
                            )

        except yaml.YAMLError as e:
            self.errors.append(f"framework.yaml is invalid YAML: {e}")
        except Exception as e:
            self.errors.append(f"Error reading framework.yaml: {e}")

    def report_results(self) -> bool:
        """Print validation results and return success status."""
        print("\n" + "="*50)
        print("VALIDATION RESULTS")
        print("="*50)

        if not self.errors and not self.warnings:
            print("✅ All validation checks passed!")
            return True

        if self.errors:
            print(f"\n❌ Found {len(self.errors)} error(s):")
            for error in self.errors:
                print(f"  • {error}")

        if self.warnings:
            print(f"\n⚠️  Found {len(self.warnings)} warning(s):")
            for warning in self.warnings[:10]:  # Limit to first 10
                print(f"  • {warning}")
            if len(self.warnings) > 10:
                print(f"  ... and {len(self.warnings) - 10} more warnings")

        print("\n" + "="*50)

        if self.errors:
            print("❌ Validation failed with errors")
            return False
        else:
            print("✅ Validation passed with warnings")
            return True


def main():
    """Main entry point."""
    root_dir = Path(__file__).parent.parent
    validator = FrameworkValidator(root_dir)

    success = validator.validate_all()
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()