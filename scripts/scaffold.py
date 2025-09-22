#!/usr/bin/env python3
"""
Scaffold new documents for The Axiom Engine framework.
Creates properly formatted documents with metadata and structure.
"""

import sys
import argparse
from datetime import datetime
from pathlib import Path

TEMPLATES = {
    "research": {
        "dir": "04_RESEARCH/Explorations",
        "template": """tags: [{tags}]
author: {author}
date: {date}
status: draft

# {title}

## Abstract

[Brief summary of this exploration]

## Introduction

[Context and motivation]

## Core Alignment

### Truth
[How this relates to the pursuit of verifiable reality]

### Wisdom
[How this applies discernment and ethical consideration]

### Humanity
[How this serves human dignity and flourishing]

## Analysis

[Main content and exploration]

## Implications

[Practical applications and consequences]

## Conclusion

[Summary and key takeaways]

## References

- The Sovereign Triad Framework
- [Additional references]
"""
    },
    "proposal": {
        "dir": "proposals",
        "template": """tags: [{tags}]
author: {author}
date: {date}
status: draft

# {title}

## Executive Summary

[1-2 paragraph overview]

## Problem Statement

[What issue does this proposal address?]

## Proposed Solution

### Approach
[High-level approach]

### Implementation
[Specific steps and methods]

## Framework Alignment

- **Truth**: [Alignment with truth principle]
- **Wisdom**: [Alignment with wisdom principle]
- **Humanity**: [Alignment with humanity principle]
- **Golden Rule**: [How this respects "Thou shalt not infringe"]

## Expected Outcomes

[What success looks like]

## Risk Assessment

[Potential challenges and mitigation]

## Timeline

[Implementation phases]

## Resources Required

[What is needed for implementation]
"""
    },
    "guide": {
        "dir": "05_RESOURCES/Simple_Guides",
        "template": """tags: [{tags}]
author: {author}
date: {date}
type: guide

# {title}

## Overview

[What this guide covers in simple terms]

## Key Concepts

1. **Concept 1**: [Simple explanation]
2. **Concept 2**: [Simple explanation]
3. **Concept 3**: [Simple explanation]

## Step-by-Step Guide

### Step 1: [Action]
[Clear instructions]

### Step 2: [Action]
[Clear instructions]

### Step 3: [Action]
[Clear instructions]

## Practical Examples

### Example 1
[Concrete scenario]

### Example 2
[Concrete scenario]

## Common Questions

**Q: [Question]**
A: [Answer]

**Q: [Question]**
A: [Answer]

## Further Reading

- [Related documents]
- [Additional resources]
"""
    },
    "rfc": {
        "dir": "06_COMMUNITY/RFC",
        "template": """# RFC: {title}

tags: [{tags}, rfc]
author: {author}
date: {date}
status: draft

## Summary

[One paragraph summary of the proposal]

## Motivation

[Why is this needed? What problem does it solve?]

## Detailed Design

[The technical details of the proposal]

## Framework Impact

### Principles
- How does this affect Truth?
- How does this affect Wisdom?
- How does this affect Humanity?

### Implementation
[How will this be implemented in the framework?]

## Drawbacks

[Why should we not do this?]

## Alternatives

[What other designs have been considered?]

## Prior Art

[Related work and existing solutions]

## Unresolved Questions

[What questions remain to be answered?]

## Community Input

[Space for community feedback and discussion]
"""
    }
}


def create_document(doc_type: str, title: str, author: str, tags: str):
    """Create a new document from template."""
    if doc_type not in TEMPLATES:
        print(f"❌ Unknown document type: {doc_type}")
        print(f"Available types: {', '.join(TEMPLATES.keys())}")
        return False

    template_info = TEMPLATES[doc_type]

    # Create filename from title
    filename = title.lower().replace(" ", "-").replace(":", "")
    filename = "".join(c for c in filename if c.isalnum() or c in "-_")

    # Add prefix for RFCs
    if doc_type == "rfc":
        # Find next RFC number
        rfc_dir = Path(template_info["dir"])
        existing_rfcs = list(rfc_dir.glob("*.md"))
        next_num = len(existing_rfcs) + 1
        filename = f"{next_num:03d}_{filename}"

    filepath = Path(template_info["dir"]) / f"{filename}.md"

    # Check if file exists
    if filepath.exists():
        response = input(f"⚠️  File {filepath} already exists. Overwrite? (y/N): ")
        if response.lower() != 'y':
            print("Cancelled.")
            return False

    # Format the template
    content = template_info["template"].format(
        title=title,
        author=author,
        tags=tags,
        date=datetime.now().strftime("%Y-%m-%d")
    )

    # Create directory if needed
    filepath.parent.mkdir(parents=True, exist_ok=True)

    # Write the file
    filepath.write_text(content)

    print(f"✅ Created {doc_type} document: {filepath}")
    return True


def main():
    parser = argparse.ArgumentParser(
        description="Scaffold new documents for The Axiom Engine framework"
    )
    parser.add_argument(
        "type",
        choices=TEMPLATES.keys(),
        help="Type of document to create"
    )
    parser.add_argument(
        "title",
        help="Title of the document"
    )
    parser.add_argument(
        "--author",
        default="Contributor",
        help="Author name (default: Contributor)"
    )
    parser.add_argument(
        "--tags",
        default="philosophy, triad",
        help="Comma-separated tags (default: philosophy, triad)"
    )

    args = parser.parse_args()

    success = create_document(
        args.type,
        args.title,
        args.author,
        args.tags
    )

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()