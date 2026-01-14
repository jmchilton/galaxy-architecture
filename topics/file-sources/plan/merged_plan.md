# File Sources Slide Plan - Merged Proposal

## Overview

This document presents three alternative flows for the File Sources architecture slides, synthesizing insights from both code-based and evolution-based perspectives. Each flow targets the 20-minute tutorial format (12-18 slides) with different pedagogical approaches.

**Target Audience:** Galaxy developers and advanced admins
**Duration:** 20 minutes
**Total Research:** 16 code paths + 11 PRs analyzed

---

## Flow Options Summary

| Flow | Approach | Best For | Strengths | Trade-offs |
|------|----------|----------|-----------|------------|
| **A: Architecture-First** | Bottom-up code structure | Developers implementing plugins | Deep technical detail, clear contracts | Less context on "why" decisions made |
| **B: Evolution-First** | Chronological PR history | Understanding design rationale | Shows problem→solution arc | May feel scattered without code anchor |
| **C: Hybrid/Thematic** | Concept-driven synthesis | Broad audience, teaching | Balanced depth + context | Requires careful flow management |

---

## Flow A: Architecture-First (Code-Heavy)

### Philosophy
Start with current architecture, work from abstractions down to implementations. Show how components fit together, then zoom into specific plugins and features.

### Slide Outline (16 slides)

1. **File Sources Overview** - Three-tier architecture, plugin discovery, URI routing
2. **Core Contracts** - FilesSource interface (SingleFileSource, SupportsBrowsing, combined)
3. **URI Resolution** - Scoring algorithm, find_best_match(), scheme examples
4. **User Context** - FileSourcesUserContext protocol, access control, vault integration

5. **fsspec Abstraction** - FsspecFilesSource, 40+ backends, _open_fs() pattern
6. **PyFilesystem2 Alternative** - When to use, pagination differences, protocol quirks
7. **POSIX Foundation** - Stock sources (FTP, library, user imports), security patterns

8. **S3 Plugin Deep-Dive** - Configuration, custom endpoints, bucket normalization
9. **Zenodo Integration** - InvenioRDM protocol, DOI workflow, draft vs published
10. **Hugging Face Example** - fsspec-based simplicity, AI/ML use cases

11. **Template Catalog** - FileSourceTemplateCatalog, Pydantic models, two-tier config
12. **Template Expansion** - Jinja2 contexts (variables, secrets, user, environ)
13. **User Instance Lifecycle** - CRUD operations, validation, connection testing
14. **OAuth2 Pattern** - Authorization flow, token storage, pre-generated UUIDs

15. **Remote Files API** - Browsing endpoints, formats (uri/flat/jstree), pagination
16. **File Sources API** - Template management, instance CRUD, testing endpoints

### Diagram Priorities (16 total)
**High Priority (7):**
1. Component architecture (ConfiguredFileSources → plugins)
2. FilesSource interface hierarchy
3. fsspec plugin class hierarchy
4. Template catalog model structure
5. Template expansion data flow
6. User instance creation sequence
7. Remote Files API request flow

**Medium Priority (6):**
3. URI resolution scoring sequence
7. POSIX stock sources deployment
9. Zenodo state diagram
12. Template resolution card diagram
13. OAuth2 authorization sequence
16. File Sources REST API hierarchy

**Lower Priority (3):**
4. User context protocol relationships
6. fsspec vs PyFilesystem2 comparison table
8. S3 file listing sequence
10. HuggingFace component integration
11. (duplicate removed)
14. (duplicate removed)
15. (duplicate removed)

### Pros
- Clear mental model of current architecture
- Easy to reference specific code locations
- Plugin developers can immediately understand contracts
- Logical progression from interface → implementation

### Cons
- Doesn't explain WHY architecture evolved this way
- May feel dry without problem context
- Harder to appreciate fsspec/Pydantic without seeing old approach
- Students unfamiliar with Galaxy may struggle with context

---

## Flow B: Evolution-First (History-Driven)

### Philosophy
Tell the story chronologically. Show problems faced, solutions implemented, and architectural patterns that emerged over 5 years. Build toward current state as synthesis.

### Slide Outline (16 slides)

1. **The Problem (Pre-2020)** - Hardcoded upload paths, no extensibility
2. **Foundation: Plugin Architecture (2020)** - FilesSource interface, ConfiguredFileSources, PyFilesystem2
3. **Initial Plugins (2020)** - POSIX (FTP, imports), WebDAV, Dropbox

4. **Write Support (Sept 2020)** - Export operations, write_from() addition
5. **Security (Apr 2021)** - Role/group permissions, boolean expressions

6. **The Big Unification (Feb 2023)** - URLs through file sources, protocol convergence
7. **Credential Injection (Feb 2023)** - url_regex, http_headers, site-specific auth

8. **Paradigm Shift: User-Defined Sources (May 2024)** - Template catalog, user instances
9. **Template Anatomy (May 2024)** - Jinja templating, variables/secrets, versioning
10. **OAuth 2.0 Integration (Oct 2024)** - Dropbox example, token management

11. **Zenodo & Pagination (Apr-May 2024)** - DOI archival, server-side pagination

12. **Pydantic Revolution (Aug 2025)** - Two-tier config, strong typing, linting
13. **fsspec Integration (Aug 2025)** - 10x code reduction, 40+ backends
14. **Hugging Face Example (Aug 2025)** - Real-world fsspec simplicity

15. **Evolution Timeline** - 5-year milestone chart (2020-2025)
16. **Complete Architecture** - Synthesis showing all layers and paradigms

### Diagram Priorities (16 total)
**High Priority (8):**
1. Before/after plugin architecture
6. URL handling convergence (before/after)
8. Template catalog architecture
10. OAuth flow sequence
13. Plugin complexity comparison (before/after fsspec)
15. Evolution timeline (Mermaid gantt)
16. Complete architecture synthesis

**Medium Priority (5):**
2. Plugin interface and operations
4. Read vs write operations flow
7. URL routing with credentials
9. Template resolution flow
11. Pagination architecture

**Lower Priority (3):**
3. Base class hierarchy
5. Access control decision tree
12. Two-tier configuration
14. Hugging Face integration simplicity

### Pros
- Motivates each design decision with real problems
- Shows continuity and evolution of thinking
- Easier to remember (story vs facts)
- Highlights fsspec/Pydantic value by contrast
- Natural audience engagement (problem → solution)

### Cons
- May feel disorganized without architectural anchor
- Harder to reference specific components later
- Chronology doesn't always match logical dependencies
- Some PR details may distract from core concepts

---

## Flow C: Hybrid/Thematic (Concept-Driven)

### Philosophy
Organize by architectural concepts rather than code structure or history. Each theme tells a mini-story: problem, evolution, current implementation. Best of both worlds.

### Slide Outline (16 slides)

**THEME 1: Plugin Architecture & Extensibility (3 slides)**
1. **The Problem & Solution** - Pre-2020 hardcoding → plugin architecture (PR #9888)
2. **Core Abstractions** - FilesSource interface, BaseFilesSource, ConfiguredFileSources
3. **URI Routing** - Scoring algorithm, scheme handling, find_best_match()

**THEME 2: Filesystem Abstraction Layers (3 slides)**
4. **PyFilesystem2 Foundation (2020)** - Original abstraction, server-side pagination
5. **fsspec Revolution (2025)** - 40+ backends, 10x code reduction (PR #20698)
6. **Comparison & Migration** - When to use each, plugin simplicity examples

**THEME 3: Plugin Implementations (3 slides)**
7. **Stock Plugins** - POSIX (FTP, imports), security patterns, template expansion
8. **Cloud Storage** - S3 (custom endpoints), Azure, Dropbox (OAuth 2.0)
9. **Research Data** - Zenodo (DOI workflow), Hugging Face (AI/ML), InvenioRDM

**THEME 4: User-Defined Sources (4 slides)**
10. **Paradigm Shift (2024)** - From admin-only to user-driven (PR #18127)
11. **Template System** - Pydantic models, Jinja2 expansion, validation (PR #20728)
12. **OAuth 2.0 Integration** - Dropbox flow, token management (PR #18272)
13. **Instance Lifecycle** - CRUD, testing, upgrade workflow

**THEME 5: URL Convergence & API (2 slides)**
14. **URL Unification (2023)** - All protocols through file sources, credential injection (PR #15497)
15. **API Integration** - Remote Files API (browsing), File Sources API (templates/instances)

**THEME 6: Summary (1 slide)**
16. **Complete Architecture** - All layers, timeline callouts, current state

### Diagram Priorities (16 total)
**High Priority (9):**
1. Problem → plugin architecture (before/after)
2. FilesSource interface hierarchy
3. URI resolution scoring
5. fsspec plugin hierarchy
6. fsspec vs PyFilesystem2 comparison
11. Template catalog + Pydantic models
12. OAuth2 flow
14. URL convergence (before/after)
15. Remote Files API flow

**Medium Priority (5):**
4. POSIX deployment diagram
7. Stock plugins configuration
9. Zenodo state diagram
13. Instance creation sequence
16. Complete architecture

**Lower Priority (2):**
8. S3 sequence diagram
10. Hugging Face example

### Thematic Benefits

**Theme 1 (Plugin Arch):**
- Establishes foundation with historical context
- Shows problem → solution immediately
- Core contracts clear before diving into implementations

**Theme 2 (Abstractions):**
- Directly compares old (PyFilesystem2) vs new (fsspec)
- Shows value of fsspec with code reduction examples
- Natural place for Hugging Face "wow" example

**Theme 3 (Implementations):**
- Concrete examples grouped by use case
- Stock → Cloud → Research progression
- Shows plugin diversity without overwhelming

**Theme 4 (User-Defined):**
- Complete story: problem → templates → OAuth → lifecycle
- Most innovative Galaxy feature, deserves focused attention
- Pydantic naturally fits here (template validation)

**Theme 5 (Convergence & API):**
- URL unification shows architectural maturity
- API layer demonstrates complete integration
- Natural lead-in to summary

**Theme 6 (Summary):**
- Synthesis diagram with timeline annotations
- Reinforces all themes in single view

### Pros
- Balanced: technical depth + historical context
- Organized by concepts, not accidents of structure
- Each theme is self-contained story
- Flexibility: themes can be reordered or condensed
- Accommodates mixed audience (devs + admins)

### Cons
- Requires careful transitions between themes
- Some architectural details split across themes
- More complex to maintain slide continuity
- May feel like "everything bagel" approach

---

## Recommendation: Flow C (Hybrid/Thematic)

**Rationale:**

1. **Audience Fit:** Tutorial targets both developers (implementing plugins) and admins (configuring sources). Hybrid approach serves both.

2. **Pedagogical Value:** Each theme provides complete story arc (problem → evolution → solution), improving retention vs pure architecture or history.

3. **Galaxy Context:** File Sources is a mature, evolved system. Showing "current state only" (Flow A) loses valuable design lessons. Showing "history only" (Flow B) makes it harder to reference code later.

4. **Diagram Efficiency:** 16 diagrams with clear priorities. High-priority diagrams (9) can be created first, medium/low added if time permits.

5. **Flexibility:** Themes can be condensed if time runs short:
   - 20min target: All 6 themes (16 slides)
   - 15min: Drop Theme 6, merge Themes 4-5 (12 slides)
   - 30min: Add code snippets, live demos (20+ slides)

6. **Future-Proofing:** New features can be added to existing themes without restructuring entire deck.

**Implementation Priority:**
1. Create high-priority diagrams (9 diagrams)
2. Write slide markdown for Theme 1-2 (foundation)
3. Get user feedback on structure before completing Themes 3-6
4. Add medium/low priority diagrams as time permits

---

## Questions for User

Before proceeding with content generation, please clarify:

1. **Flow Preference:** A (Architecture), B (Evolution), or C (Hybrid)? Or a modified version?

2. **Target Duration:** Stick with 20min (16 slides) or adjust to 15min (12 slides) / 30min (20 slides)?

3. **Audience Level:** Confirmed as "intermediate developers + advanced admins" or adjust?

4. **Diagram Scope:** Should I create all 16 diagrams, or focus on high-priority (7-9) first?

5. **Code Snippets:** Do you want inline code examples (yaml configs, Python snippets) in slides, or keep it purely diagram-driven?

6. **Special Topics:** Any specific aspects to emphasize or de-emphasize?
   - fsspec migration strategy?
   - OAuth 2.0 security details?
   - Template best practices?
   - Performance considerations (pagination, caching)?

---

## Next Steps

Once user provides preferences, I will:

1. Generate final slide plan in `topics/file-sources/plan/final_plan.md`
2. Create `topics/file-sources/content.yaml` with slide definitions
3. Write slide content in `topics/file-sources/fragments/`
4. Generate diagram source files in `images/` directory
5. Update `topics/file-sources/metadata.yaml` if needed
6. Validate complete topic with `make validate`
