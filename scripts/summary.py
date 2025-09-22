#!/usr/bin/env python3
"""
Generate summaries and reports for The Axiom Engine framework.
"""

import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List
import yaml

class FrameworkSummarizer:
    def __init__(self, root_dir: Path):
        self.root_dir = root_dir

    def generate_inventory(self) -> Dict:
        """Generate a complete inventory of all documents."""
        inventory = {
            "generated": datetime.now().isoformat(),
            "statistics": {},
            "documents": {}
        }

        doc_count = 0
        total_lines = 0
        by_category = {}

        for md_file in sorted(self.root_dir.glob("**/*.md")):
            if "node_modules" in str(md_file) or "site" in str(md_file):
                continue

            rel_path = md_file.relative_to(self.root_dir)
            category = str(rel_path).split('/')[0] if '/' in str(rel_path) else "root"

            try:
                content = md_file.read_text(encoding='utf-8')
                lines = len(content.splitlines())
                doc_count += 1
                total_lines += lines

                # Extract title
                title = "Untitled"
                for line in content.splitlines()[:5]:
                    if line.startswith("# "):
                        title = line[2:].strip()
                        break

                # Count by category
                if category not in by_category:
                    by_category[category] = 0
                by_category[category] += 1

                # Store document info
                if category not in inventory["documents"]:
                    inventory["documents"][category] = []

                inventory["documents"][category].append({
                    "path": str(rel_path),
                    "title": title,
                    "lines": lines,
                    "size": md_file.stat().st_size
                })

            except Exception as e:
                print(f"Error processing {md_file}: {e}", file=sys.stderr)

        inventory["statistics"] = {
            "total_documents": doc_count,
            "total_lines": total_lines,
            "by_category": by_category
        }

        return inventory

    def generate_principle_report(self) -> str:
        """Generate a report on principle usage across the framework."""
        report = []
        report.append("# Principle Usage Report")
        report.append(f"\nGenerated: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n")

        principles = {
            "Truth": ["truth", "verifiable", "reality", "fact"],
            "Wisdom": ["wisdom", "discernment", "ethical", "judgment"],
            "Humanity": ["humanity", "dignity", "flourishing", "human"],
            "Golden Rule": ["infringe", "sovereignty", "freedom", "autonomy"]
        }

        principle_counts = {p: 0 for p in principles}
        document_coverage = {p: [] for p in principles}

        for md_file in self.root_dir.glob("**/*.md"):
            if "node_modules" in str(md_file) or "site" in str(md_file):
                continue

            try:
                content = md_file.read_text(encoding='utf-8').lower()
                rel_path = md_file.relative_to(self.root_dir)

                for principle, keywords in principles.items():
                    count = sum(content.count(kw) for kw in keywords)
                    if count > 0:
                        principle_counts[principle] += count
                        document_coverage[principle].append(str(rel_path))

            except Exception:
                continue

        # Generate report
        report.append("## Overall Principle References\n")
        for principle, count in sorted(principle_counts.items(), key=lambda x: x[1], reverse=True):
            report.append(f"- **{principle}**: {count} references")

        report.append("\n## Document Coverage by Principle\n")
        for principle, docs in document_coverage.items():
            report.append(f"### {principle}")
            report.append(f"Found in {len(docs)} documents:")
            for doc in docs[:5]:  # Show top 5
                report.append(f"- {doc}")
            if len(docs) > 5:
                report.append(f"- ... and {len(docs) - 5} more")
            report.append("")

        return "\n".join(report)

    def generate_structure_map(self) -> str:
        """Generate a markdown map of the repository structure."""
        lines = []
        lines.append("# Repository Structure Map")
        lines.append(f"\nGenerated: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n")

        # Define the expected structure
        structure = {
            "01_CORE": "Canonical framework documents",
            "04_RESEARCH": "Research and explorations",
            "05_RESOURCES": "Guides and resources",
            "06_COMMUNITY": "Community contributions",
            "07_VISUALS": "Visual representations",
            "proposals": "Implementation proposals",
            "case-studies": "Real-world applications"
        }

        for dir_name, description in structure.items():
            dir_path = self.root_dir / dir_name
            if not dir_path.exists():
                lines.append(f"\n## {dir_name} ⚠️ MISSING")
                lines.append(f"*{description}*")
                continue

            lines.append(f"\n## {dir_name}")
            lines.append(f"*{description}*\n")

            # List markdown files
            md_files = list(dir_path.glob("**/*.md"))
            if md_files:
                for md_file in sorted(md_files)[:10]:  # Limit to 10 per section
                    rel_path = md_file.relative_to(dir_path)

                    # Get title
                    try:
                        content = md_file.read_text(encoding='utf-8')
                        title = "Untitled"
                        for line in content.splitlines()[:5]:
                            if line.startswith("# "):
                                title = line[2:].strip()
                                break
                        lines.append(f"- `{rel_path}`: {title}")
                    except Exception:
                        lines.append(f"- `{rel_path}`")

                if len(md_files) > 10:
                    lines.append(f"- ... and {len(md_files) - 10} more files")
            else:
                lines.append("- *No documents*")

        return "\n".join(lines)


def main():
    import argparse

    parser = argparse.ArgumentParser(
        description="Generate summaries for The Axiom Engine framework"
    )
    parser.add_argument(
        "report",
        choices=["inventory", "principles", "structure"],
        help="Type of report to generate"
    )
    parser.add_argument(
        "--output",
        "-o",
        help="Output file (default: stdout)"
    )
    parser.add_argument(
        "--format",
        choices=["markdown", "json"],
        default="markdown",
        help="Output format (default: markdown)"
    )

    args = parser.parse_args()

    root_dir = Path(__file__).parent.parent
    summarizer = FrameworkSummarizer(root_dir)

    if args.report == "inventory":
        result = summarizer.generate_inventory()
        if args.format == "json":
            output = json.dumps(result, indent=2)
        else:
            # Convert to markdown
            output = "# Document Inventory\n\n"
            output += f"Generated: {result['generated']}\n\n"
            output += "## Statistics\n"
            for key, value in result['statistics'].items():
                output += f"- **{key}**: {value}\n"
            output += "\n## Documents by Category\n"
            for category, docs in result['documents'].items():
                output += f"\n### {category}\n"
                for doc in docs:
                    output += f"- {doc['title']} (`{doc['path']}`)\n"

    elif args.report == "principles":
        output = summarizer.generate_principle_report()

    elif args.report == "structure":
        output = summarizer.generate_structure_map()

    # Output results
    if args.output:
        Path(args.output).write_text(output)
        print(f"✅ Report saved to {args.output}")
    else:
        print(output)


if __name__ == "__main__":
    main()