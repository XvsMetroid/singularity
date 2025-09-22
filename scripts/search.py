#!/usr/bin/env python3
"""
Search for concepts and principles across The Axiom Engine framework.
Provides semantic search and principle alignment analysis.
"""

import re
import sys
import argparse
from pathlib import Path
from typing import Dict, List, Tuple
from collections import defaultdict

class FrameworkSearcher:
    def __init__(self, root_dir: Path):
        self.root_dir = root_dir
        self.core_principles = {
            "truth": ["truth", "verifiable", "reality", "fact", "evidence"],
            "wisdom": ["wisdom", "discernment", "ethical", "judgment", "understanding"],
            "humanity": ["humanity", "dignity", "flourishing", "agency", "human"],
            "golden_rule": ["infringe", "sovereignty", "freedom", "autonomy", "liberty"]
        }

    def search_concept(self, query: str, context_lines: int = 2) -> List[Tuple[Path, List[str]]]:
        """Search for a concept across all documents."""
        results = []
        pattern = re.compile(re.escape(query), re.IGNORECASE)

        for md_file in self.root_dir.glob("**/*.md"):
            if "node_modules" in str(md_file) or "site" in str(md_file):
                continue

            try:
                lines = md_file.read_text(encoding='utf-8').splitlines()
                matches = []

                for i, line in enumerate(lines):
                    if pattern.search(line):
                        # Get context
                        start = max(0, i - context_lines)
                        end = min(len(lines), i + context_lines + 1)
                        context = lines[start:end]
                        matches.append({
                            'line_num': i + 1,
                            'line': line,
                            'context': context,
                            'start_line': start + 1
                        })

                if matches:
                    results.append((md_file, matches))

            except Exception as e:
                print(f"Error reading {md_file}: {e}", file=sys.stderr)

        return results

    def analyze_principle_coverage(self, file_path: Path = None) -> Dict:
        """Analyze how well documents cover core principles."""
        coverage = defaultdict(lambda: defaultdict(int))

        if file_path:
            files = [file_path] if file_path.exists() else []
        else:
            files = self.root_dir.glob("**/*.md")

        for md_file in files:
            if "node_modules" in str(md_file) or "site" in str(md_file):
                continue

            try:
                content = md_file.read_text(encoding='utf-8').lower()
                rel_path = md_file.relative_to(self.root_dir)

                for principle, keywords in self.core_principles.items():
                    count = sum(content.count(keyword) for keyword in keywords)
                    if count > 0:
                        coverage[str(rel_path)][principle] = count

            except Exception as e:
                print(f"Error analyzing {md_file}: {e}", file=sys.stderr)

        return dict(coverage)

    def find_related_documents(self, query: str, max_results: int = 5) -> List[Tuple[Path, int]]:
        """Find documents most related to a query."""
        relevance_scores = []

        for md_file in self.root_dir.glob("**/*.md"):
            if "node_modules" in str(md_file) or "site" in str(md_file):
                continue

            try:
                content = md_file.read_text(encoding='utf-8').lower()

                # Calculate relevance score
                score = 0

                # Direct query matches
                score += content.count(query.lower()) * 10

                # Check for principle alignment
                for principle, keywords in self.core_principles.items():
                    if any(keyword in query.lower() for keyword in keywords):
                        score += sum(content.count(kw) for kw in keywords)

                if score > 0:
                    relevance_scores.append((md_file, score))

            except Exception:
                continue

        # Sort by relevance and return top results
        relevance_scores.sort(key=lambda x: x[1], reverse=True)
        return relevance_scores[:max_results]

    def extract_definitions(self) -> Dict[str, List[Tuple[str, str]]]:
        """Extract definitions from glossary and other documents."""
        definitions = {}

        # First check glossary
        glossary_path = self.root_dir / "01_CORE" / "03_Glossary_of_Terms.md"
        if glossary_path.exists():
            content = glossary_path.read_text(encoding='utf-8')

            # Pattern for definitions (various formats)
            patterns = [
                r'\*\*([^*]+)\*\*:\s*([^\n]+)',  # **Term**: Definition
                r'### ([^\n]+)\n([^\n]+)',        # ### Term \n Definition
                r'- \*\*([^*]+)\*\*:\s*([^\n]+)'  # - **Term**: Definition
            ]

            for pattern in patterns:
                matches = re.findall(pattern, content)
                for term, definition in matches:
                    term = term.strip()
                    if term not in definitions:
                        definitions[term] = []
                    definitions[term].append((definition.strip(), "Glossary"))

        return definitions


def format_search_results(results: List[Tuple[Path, List[dict]]], root_dir: Path):
    """Format search results for display."""
    if not results:
        print("No results found.")
        return

    print(f"\n🔍 Found {sum(len(matches) for _, matches in results)} matches in {len(results)} files:\n")

    for file_path, matches in results:
        rel_path = file_path.relative_to(root_dir)
        print(f"📄 {rel_path}")

        for match in matches[:3]:  # Limit to 3 matches per file
            print(f"  Line {match['line_num']}: {match['line'].strip()}")

        if len(matches) > 3:
            print(f"  ... and {len(matches) - 3} more matches")
        print()


def format_principle_coverage(coverage: Dict):
    """Format principle coverage analysis."""
    if not coverage:
        print("No documents analyzed.")
        return

    print("\n📊 Principle Coverage Analysis:\n")

    # Calculate totals
    principle_totals = defaultdict(int)
    for doc, principles in coverage.items():
        for principle, count in principles.items():
            principle_totals[principle] += count

    # Show summary
    print("Overall Coverage:")
    for principle in ["truth", "wisdom", "humanity", "golden_rule"]:
        count = principle_totals.get(principle, 0)
        bar = "█" * min(20, count // 5)
        print(f"  {principle:12} {bar} ({count} references)")

    print("\n\nTop Documents by Principle Coverage:")
    sorted_docs = sorted(
        coverage.items(),
        key=lambda x: sum(x[1].values()),
        reverse=True
    )[:5]

    for doc, principles in sorted_docs:
        total = sum(principles.values())
        print(f"\n  {doc} (Total: {total})")
        for principle, count in principles.items():
            print(f"    - {principle}: {count}")


def main():
    parser = argparse.ArgumentParser(
        description="Search The Axiom Engine framework"
    )
    subparsers = parser.add_subparsers(dest="command", help="Command to run")

    # Concept search
    search_parser = subparsers.add_parser("concept", help="Search for a concept")
    search_parser.add_argument("query", help="Search query")
    search_parser.add_argument(
        "--context",
        type=int,
        default=2,
        help="Context lines to show (default: 2)"
    )

    # Principle coverage
    coverage_parser = subparsers.add_parser(
        "coverage",
        help="Analyze principle coverage"
    )
    coverage_parser.add_argument(
        "--file",
        type=Path,
        help="Specific file to analyze (default: all files)"
    )

    # Related documents
    related_parser = subparsers.add_parser(
        "related",
        help="Find related documents"
    )
    related_parser.add_argument("query", help="Query to find related documents")
    related_parser.add_argument(
        "--max",
        type=int,
        default=5,
        help="Maximum results (default: 5)"
    )

    # Definitions
    def_parser = subparsers.add_parser(
        "definitions",
        help="Extract all definitions"
    )

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    root_dir = Path(__file__).parent.parent
    searcher = FrameworkSearcher(root_dir)

    if args.command == "concept":
        results = searcher.search_concept(args.query, args.context)
        format_search_results(results, root_dir)

    elif args.command == "coverage":
        coverage = searcher.analyze_principle_coverage(args.file)
        format_principle_coverage(coverage)

    elif args.command == "related":
        results = searcher.find_related_documents(args.query, args.max)
        if results:
            print(f"\n📚 Documents related to '{args.query}':\n")
            for doc, score in results:
                rel_path = doc.relative_to(root_dir)
                print(f"  {score:4d} - {rel_path}")
        else:
            print("No related documents found.")

    elif args.command == "definitions":
        definitions = searcher.extract_definitions()
        if definitions:
            print("\n📖 Extracted Definitions:\n")
            for term in sorted(definitions.keys()):
                print(f"**{term}**")
                for definition, source in definitions[term]:
                    print(f"  - {definition} [{source}]")
                print()
        else:
            print("No definitions found.")


if __name__ == "__main__":
    main()