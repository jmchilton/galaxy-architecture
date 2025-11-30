# Plan a Topic for Slide Generation

Generate a structured slide plan for a topic by analyzing code paths and pull request history from research notes.

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

**Agent A: Code-Based Slide Plan**
- Reads all `path_*.md` files from `topics/<topic-id>/notes/`
- Proposes slides based on code architecture and current implementation
- Flexible slide count based on topic complexity
- For each slide:
  - Title
  - Key points (3-5 bullets)
  - Proposed diagrams (descriptions of what diagram would show, not full implementations)
  - Code references if relevant
- Writes to: `topics/<topic-id>/plan/code_based_plan.md`
- Creates diagram TODO list at end of plan

**Agent B: PR-Based Slide Plan**
- Reads all `pr_*.md` files from `topics/<topic-id>/notes/`
- Proposes slides based on evolution, history, and why decisions were made
- Flexible slide count based on topic complexity
- Same format as Agent A (simpler slide format: title + bullets + diagram ideas)
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

```markdown
## Slide Title

- Key point 1
- Key point 2
- Key point 3

**Proposed Diagram:** Activity diagram showing X process
**Code References:** file.py:function(), component.vue
```

## Diagram Proposals

Agents should propose diagrams when helpful:
- **Activity diagrams** - Process flows, pipelines
- **Mindmaps** - Concept relationships, component organization
- **Class diagrams** - Object models, inheritance
- **Sequence diagrams** - API interactions, event flows
- **File tree diagrams** - Directory structure (using mindmap format)

Diagrams can be:
- Inline PlantUML code (if simple and agent has enough info)
- Descriptive text (e.g., "Sequence diagram showing API call from client → backend → database")
- TODO items for later creation

## Next Steps After Planning

After this command completes with `final_plan.md`:
1. Review and refine the plan
2. Create diagrams from TODO list (using PlantUML)
3. Generate actual `content.yaml` with slide content (separate command/process)
4. Build slides using `make build-slides`

## Requirements

- Topic must have been researched with `/research-topic <topic-id>` first
- Research notes must exist in `topics/<topic-id>/notes/`
