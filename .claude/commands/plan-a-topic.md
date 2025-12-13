# Plan a Topic for Slide Generation

Generate a structured slide plan for a topic by analyzing code paths and pull request history from research notes.

**IMPORTANT**: Before planning, read these guides:
- `docs/SLIDE_GUIDE.md` - Slide design principles
- `docs/DIAGRAM_GUIDE.md` - Diagram types and when to use each

Key slide principles:
- Visual-first: diagrams > bullets
- Problem → Solution narrative flow
- One concept per slide
- Use diffs for code evolution
- Real Galaxy code examples with file paths

Key diagram guidance:
- See existing examples in `images/` for patterns
- Choose diagram type that best communicates the point
- File mindmaps (YAML) can be validated against filesystem

## Usage

```
/plan-a-topic <topic-id>
```

## Arguments

- **topic-id**: Topic identifier (e.g., "markdown", "dependency-injection")

## Examples

```
/plan-a-topic markdown
/plan-a-topic startup
/plan-a-topic production
```

## What it does

### 1. Validate Prerequisites
- Check that `topics/<topic-id>/metadata.yaml` exists
- Check that research notes exist in `topics/<topic-id>/notes/`:
  - Looks for `path_*.md` files (code path summaries)
  - Looks for `pr_*.md` files (pull request summaries)
- If notes missing, prompts user to run `/research-topic <topic-id>` first
- Creates `topics/<topic-id>/plan/` directory

### 2. Spawn Two Parallel Subagents (Distinct Perspectives)

**Both agents MUST first read `docs/SLIDE_GUIDE.md` and `docs/DIAGRAM_GUIDE.md`** to understand effective slide and diagram design.

**Agent A: Code-Based Slide Plan**
- Reads `docs/SLIDE_GUIDE.md` and `docs/DIAGRAM_GUIDE.md` first
- Reads all `path_*.md` files from `topics/<topic-id>/notes/`
- Proposes slides based on code architecture and current implementation
- Follows slide design principles: visual-first, one concept per slide
- Proposes diagrams that best communicate each point (see DIAGRAM_GUIDE.md for examples)
- For each slide:
  - Type (diagram/code-pattern/concept/quote)
  - Title
  - Content idea (one sentence)
  - Proposed diagram with type justification
  - Suggested class (center/reduce70/enlarge150)
- Writes to: `topics/<topic-id>/plan/code_based_plan.md`
- Creates diagram TODO list at end of plan

**Agent B: PR-Based Slide Plan**
- Reads `docs/SLIDE_GUIDE.md` and `docs/DIAGRAM_GUIDE.md` first
- Reads all `pr_*.md` files from `topics/<topic-id>/notes/`
- Proposes slides showing problem → solution evolution
- Uses diffs for code migration slides
- Proposes diagrams that show evolution/change
- Same format as Agent A
- Writes to: `topics/<topic-id>/plan/pr_based_plan.md`
- Creates diagram TODO list at end of plan

**Note:** Agents run in parallel to generate distinct perspectives. Diagrams can be:
- Inline PlantUML (` ```plantuml ` blocks) if agent has enough info
- Descriptive proposals (e.g., "Activity diagram showing markdown processing pipeline")
- References to separate files (e.g., "See diagrams/markdown_pipeline.puml")

### 3. Main Agent: Merge & Flow Proposals

Reads both plans and creates 2-3 alternative slide flows:

**Flow A: Architecture-First** (code-heavy approach)
- Start with current architecture
- Explain components and patterns
- Sprinkle historical context where relevant
- Best for: Technical deep-dives, API documentation

**Flow B: Evolution-First** (history-driven approach)
- Start with problem/requirements
- Show how solution evolved through PRs
- End with current architecture as result
- Best for: Understanding design decisions, training

**Flow C: Hybrid/Thematic** (concept-based approach)
- Group by concepts/themes
- Mix code + history for each concept
- Show "what it is" + "why it's that way"
- Best for: Comprehensive tutorials

Writes to: `topics/<topic-id>/plan/merged_plan.md` with:
- Overview of both source plans
- Comparison table of the 3 flows
- Pros/cons for each flow
- Recommended flow with rationale

### 4. User Decision Point

Presents the flows and asks:
1. **Which flow?** (A/B/C or custom combination)
2. **Any slides to add/remove/reorder?**
3. **Target duration?** (15min/30min/45min - helps determine detail level)
4. **Audience level?** (beginner/intermediate/advanced - affects terminology/depth)
5. **Any other high-level direction?**

### 5. Finalize Plan

- Updates `merged_plan.md` with user choices
- Creates `topics/<topic-id>/plan/final_plan.md` with:
  - Chosen flow with slide outline
  - User preferences noted
  - Consolidated diagram TODO list
  - Next steps for content generation

## Output Files

```
topics/<topic-id>/plan/
├── code_based_plan.md        # Code architecture perspective
├── pr_based_plan.md           # Evolution/history perspective
├── merged_plan.md             # Analysis + 3 flow options
└── final_plan.md              # User-selected flow + preferences
```

## Slide Format (Simplified for Planning)

**Read `docs/SLIDE_GUIDE.md` first!** Effective slides are:
- Diagram-centric (centered visual, minimal text)
- Code-pattern slides (real code from Galaxy with file path)
- Concept slides (3-4 bullets max, use enlarge classes)

```markdown
## Slide Title

**Type:** diagram | code-pattern | concept | quote

**Content idea:** [One sentence describing the slide]

**Proposed Diagram:** Activity diagram showing X process
**Code References:** lib/galaxy/path/file.py:function()
**Class:** center | reduce70 | enlarge150
```

### Slide Type Guidelines (from SLIDE_GUIDE.md)

1. **Diagram slides**: `class: center`, no heading, let visual speak
2. **Code slides**: Show real file path, use reduce70/90 for long code
3. **Concept slides**: 3-4 bullets max, use enlarge120/150/200
4. **Quote slides**: Blockquote for definitions, cite source

## Diagram Proposals

**See `docs/DIAGRAM_GUIDE.md` for examples and patterns.**

Available diagram types:
- **PlantUML**: Sequence, Class, Component, Object, Activity, Mindmap
- **Mermaid**: Timeline, Flowchart, State, Gantt, User Journey
- **File Mindmaps** (YAML): Validated directory structures

Choose based on what communicates best. See `images/` for existing examples.

Diagram TODO format:
```markdown
**Diagram TODO:** Sequence diagram showing tool execution
- Participants: client, ToolsController, app.toolbox, tool
- Phases: "Render Form", "Submit Form"
- Show loop for parameter combinations
- Reference: images/core_tool_sequence.plantuml.txt
```

## Next Steps After Planning

After this command completes with `final_plan.md`:
1. Review and refine the plan
2. Create diagrams from TODO list (using PlantUML)
3. Generate actual `content.yaml` with slide content (separate command/process)
4. Build slides using `make build-slides`

## Requirements

- Topic must have been researched with `/research-topic <topic-id>` first
- Research notes must exist in `topics/<topic-id>/notes/`
