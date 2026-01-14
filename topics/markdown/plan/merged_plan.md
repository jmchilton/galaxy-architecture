# Merged Slide Plan: Galaxy Markdown Architecture

## Source Plans Summary

### Code-Based Plan (29 slides)
Focuses on **current architecture**:
- Backend parsing layer (markdown_parse.py, markdown_util.py)
- Rendering pipeline and handler pattern
- Frontend component tree (Markdown.vue, elements)
- Editor architecture (TextEditor, CellEditor)
- Design principles and extensibility

**Strengths:** Clear component relationships, data flow diagrams, code patterns

### PR-Based Plan (37 slides)
Focuses on **evolution over time**:
- 2019 foundation (syntax decision, two-stage architecture)
- 2020 PDF export and metadata
- 2023 tool integration
- 2024-25 cell editor and validation

**Strengths:** Problem→solution narrative, design decision context, historical progression

---

## Flow Options

### Flow A: Architecture-First (25-30 slides)

Start with current architecture, sprinkle historical context where relevant.

**Structure:**
1. What is Galaxy Markdown? (problem + solution concept)
2. Two-flavor architecture (diagram)
3. Backend parsing layer (4 slides)
4. Backend rendering pipeline (5 slides)
5. Frontend components (5 slides)
6. Editor (3 slides)
7. Document types comparison (1 slide)
8. Extensibility (2 slides)
9. Summary (2 slides)

**Pros:**
- Efficient for developers who need to work with the code
- Clear mental model of current system
- Easier to navigate to specific topics

**Cons:**
- Loses "why" context
- May feel dry without narrative arc
- Design decisions presented as facts, not choices

**Best for:** Technical deep-dives, onboarding developers to codebase

---

### Flow B: Evolution-First (30-35 slides)

Tell the story chronologically, ending with current state.

**Structure:**
1. Timeline overview (diagram)
2. The portability problem (2019)
3. Foundation: syntax, two-stage architecture (3 slides)
4. Making it portable: PDF export (3 slides)
5. Expanding capabilities: metadata, visualizations (4 slides)
6. Tool integration (3 slides)
7. Modern editing experience (5 slides)
8. Current architecture summary (4 slides)
9. Design principles emerged (2 slides)
10. Future directions (1 slide)

**Pros:**
- Strong narrative arc (problem → solution)
- Explains "why" behind design decisions
- Shows evolution = easier to understand trade-offs
- Natural diff opportunities for code evolution

**Cons:**
- Takes longer to get to "how it works now"
- Some historical details may not matter for current usage
- Risk of too much PR-level detail

**Best for:** Training sessions, understanding design decisions, Galaxy history

---

### Flow C: Hybrid/Thematic (28-32 slides)

Group by concept, mixing code architecture + history for each.

**Structure:**
1. Introduction: What + Why (3 slides)
2. **Theme: Portability** (5 slides)
   - Problem (history)
   - Two-flavor solution (architecture)
   - ID encoding (code)
3. **Theme: Transformation Pipeline** (6 slides)
   - PDF export requirement (history)
   - Pipeline architecture (code)
   - Handler pattern (code)
4. **Theme: Frontend Rendering** (5 slides)
   - Component evolution (history)
   - Current component tree (architecture)
   - Element types (code)
5. **Theme: Editing Experience** (5 slides)
   - Evolution from text to cells (history)
   - Dual-mode architecture (code)
   - Validation (code + history)
6. **Theme: Document Types** (3 slides)
   - Reports vs Pages vs Tool Outputs
   - Trust boundaries
7. Summary + Future (3 slides)

**Pros:**
- Best of both worlds: "what" and "why" together
- Concepts stick better with context
- Each theme self-contained
- Flexible for time constraints (skip themes)

**Cons:**
- More complex to construct
- Some redundancy in transitions
- May feel less linear

**Best for:** Comprehensive tutorials, mixed audience

---

## Comparison Table

| Aspect | Flow A | Flow B | Flow C |
|--------|--------|--------|--------|
| Narrative | Weak | Strong | Moderate |
| Technical depth | High | Moderate | High |
| Historical context | Low | High | Moderate |
| Time to "how it works" | Fast | Slow | Medium |
| Flexibility | High | Low | High |
| Recommended duration | 20-30 min | 35-45 min | 30-40 min |

---

## Recommended Flow: C (Hybrid/Thematic)

**Rationale:**
- Galaxy Markdown has both interesting architecture AND interesting history
- Thematic grouping lets audience understand "what" and "why" together
- Flexible for different time slots
- Each theme can stand alone for reference

**However:**
- If audience is pure developers needing to modify code → Flow A
- If goal is Galaxy history/design philosophy → Flow B

---

## Consolidated Diagram List

Both plans propose similar diagrams. Consolidated unique diagrams:

### High Priority (Core to any flow)
1. **Two-Flavor Transformation** - Sequence: labels → IDs
2. **Rendering Pipeline** - Sequence: 5 stages
3. **Handler Class Hierarchy** - Class diagram
4. **Frontend Component Tree** - Component/tree
5. **Design Principles** - Concept mindmap (YAML)

### Medium Priority (Important for depth)
6. **PDF Export Pipeline** - Sequence
7. **Backend Parser Components** - Component diagram
8. **Cell Editor Architecture** - Component/mockup
9. **Validation Flow** - Flowchart
10. **Document Types Comparison** - Matrix/table

### Nice to Have
11. **Evolution Timeline** - Mermaid timeline
12. **Store Data Flow** - Component diagram
13. **File Structure Mindmap** - File mindmap (YAML)
14. **ID Encoding Flow** - Sequence

---

## Questions for User

1. **Which flow?** A (Architecture) / B (Evolution) / C (Hybrid)
2. **Target duration?** 15min / 30min / 45min
3. **Audience level?** Beginner / Intermediate / Advanced Galaxy developers
4. **Any slides to add/remove?** Specific topics to emphasize or skip?
5. **Diagram priorities?** Which diagrams are most valuable?
