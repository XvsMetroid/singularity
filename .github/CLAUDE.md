# Claude Instructions

This document provides specific instructions for Claude when working with The Axiom Engine repository.
For universal AI guidelines that apply to all agents, see `ai-guidelines.md`.

## Big Picture

The Axiom Engine is a philosophical operating system designed to build adaptive, ethical societies. The repository is structured to mirror the framework's fractal nature, with a clear separation between canonical documents, research, and community contributions.

- **`01_CORE/`**: The "source of truth," containing the most refined, canonical documents.
- **`04_RESEARCH/`**: Polished articles and raw intellectual explorations.
- **`05_RESOURCES/`**: Onboarding guides, simple explanations, and reference materials.
- **`06_COMMUNITY/`**: A space for collaboration, RFCs, and open discussion.
- **`framework.yaml`**: A machine-readable summary of the core concepts.

## Developer Workflow

- **Onboarding**: Start with `05_RESOURCES/ONBOARDING.md` to understand the project's vision and reading order.
- **Contribution**: Follow the guidelines in `CONTRIBUTING.md`, including the Contributor Ladder.
- **Community**: Engage in discussions in `06_COMMUNITY/` and respond to RFCs.
- **Versioning**: The framework is versioned in `framework.yaml` and changes are tracked in `CHANGELOG.md`.

## Project-Specific Conventions

- **Numbered Folders**: The numbered folders (`01_CORE`, `04_RESEARCH`, etc.) indicate the order of importance and provide intuitive navigation.
- **Metadata**: Documents should begin with a summary and, where possible, metadata tags (e.g., `tags: [philosophy, triad, feedback-loop]`).
- **Visuals**: Diagrams and flowcharts are created using Mermaid syntax and stored in `07_VISUALS/`.

## Integration Points

- The framework is designed to be applied to real-world organizations. See `proposals/P-05_Pilot_Program_Methodology.md` for an example.
- The system's principles are intended to govern AI ethics, constitutional reform, and global governance. See the `proposals/` folder for more.

## Key Files

- `05_RESOURCES/ONBOARDING.md`: The starting point for all contributors.
- `01_CORE/00_The_Constitution.md`: The master document for the framework.
- `framework.yaml`: The machine-readable summary of the core logic.
- `CONTRIBUTING.md`: Guidelines for contributing to the project.
- `CHANGELOG.md`: A record of all significant changes.

## Claude-Specific Guidelines

**Primary Reference**: Follow all guidelines in `.github/ai-guidelines.md` - this document contains Claude-specific additions only.

**Advanced Capabilities**: As Claude Code, you have access to:
- File system operations (Read, Write, Edit, Glob, Grep)
- Bash command execution
- Multi-tool orchestration for complex tasks
- TodoWrite for task management and progress tracking

**Task Management Protocol**:
- Use TodoWrite tool to plan and track multi-step tasks
- Mark tasks as in_progress before starting work
- Complete tasks immediately after finishing (don't batch completions)
- Only have ONE task in_progress at any time

**Claude Code Integration**:
- Use available development commands proactively when appropriate
- Reference specific code locations using `file_path:line_number` format
- Batch tool calls together for optimal performance when possible
- Run validation commands (`npm run test`, `npm run lint`) after significant changes

**Framework Validation**:
- Before major edits, understand existing code conventions and patterns
- Check that codebase uses required libraries before suggesting them
- Follow security best practices - never expose secrets or keys
- Maintain repository organization - eliminate duplicates and redundancy

**Professional Objectivity**:
- Prioritize technical accuracy over validating user beliefs
- Apply rigorous standards to all ideas and disagree when necessary
- Provide objective guidance even if not what user wants to hear
- Investigate to find truth rather than confirming assumptions
