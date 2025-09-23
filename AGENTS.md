# Agent Instructions

tags: [agents, ai-instructions, repository-guidelines, ai-collaboration, project-template, guidelines]

## Repository Overview

This is **The Axiom Engine** - a philosophical framework development project, not a traditional software repository.
It focuses on developing principles for ethical governance and societal systems based on the "Sovereign Triad"
(Truth, Wisdom, Humanity).

## Navigation Structure

- **`01_CORE/`**: Canonical, immutable documents - the "source of truth"
- **`04_RESEARCH/`**: Published articles and explorations
- **`05_RESOURCES/`**: Onboarding guides and reference materials
- **`06_COMMUNITY/`**: Collaboration and discussion space
- **`07_VISUALS/`**: Visual assets and diagrams supporting the framework
- **`docs/`**: AI guidance and documentation navigation
- **`proposals/`**: Application blueprints and frameworks
- **`case-studies/`**: Evidence and analysis files

## Essential Starting Points

1. **Onboarding**: Start with `05_RESOURCES/ONBOARDING.md`
2. **Core Framework**: See `framework.yaml` for machine-readable principles
3. **Documentation Map**: Use `docs/index.md` for document navigation
4. **AI Guidelines**: Reference `AGENTS.md` and `docs/AI-guide.md`

## Documentation Conventions

- Use clear, descriptive filenames
- Add metadata tags at document tops (e.g., `tags: [philosophy, triad, feedback-loop]`)
- Include brief summaries for accessibility
- Update `docs/index.md` when adding new documents
- Remove or refactor outdated content to maintain repository cleanliness

## Core Principles

The framework centers on:

- **Truth**: Uncompromising pursuit of verifiable reality
- **Wisdom**: Discernment to apply truth ethically and effectively
- **Humanity**: All action must serve human dignity, agency, and flourishing
- **Golden Rule**: "Thou shalt not infringe" - protecting individual sovereignty

## Development Commands

**Documentation Site Commands:**

- `npm run dev` - Start MkDocs development server (live-reload at <http://localhost:8000>)
- `npm run build` - Build static documentation site to `site/` directory
- `npm run preview` - Preview built site locally
- `npm run deploy` - Deploy documentation to GitHub Pages
- `npm run install` - Install Python dependencies (MkDocs)

**Note**: This is primarily a documentation repository. There are no traditional lint or test commands. Work involves
reading, writing, and organizing markdown files according to the established conventions.
