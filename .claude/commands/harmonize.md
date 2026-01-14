# Harmonize Agentic Operation

Improve alignment between architecture documentation and generated agentic operations.

This command orchestrates the positive feedback loop between architecture documentation in this repository and agentic operations for acting on the Galaxy codebase. The goal is to make commands as sharp and intelligent as possible while being completely generated from architecture documentation.

## Usage

```
/harmonize <existing-command-path> <topic-id> <operation-name>
```

## Arguments

- **existing-command-path**: Path to current slash command (e.g., `~/.claude/commands/review-di.md`)
- **topic-id**: Topic in this repo (e.g., `dependency-injection`)
- **operation-name**: Operation from metadata.yaml (e.g., `review-di`)

## Your Task

### Phase 1: Load and Analyze

1. **Read the existing command** from the supplied path
2. **Read topic content**: `topics/<topic>/metadata.yaml` and `topics/<topic>/content.yaml`
3. **Read the operation's prompt** from metadata.yaml
4. **Create directory** `topics/<topic>/harmonize/` if needed
5. **Write analysis** to `topics/<topic>/harmonize/<op>_analysis.md`:

```markdown
# Harmonization Analysis: <operation-name>

## Information in Command NOT in Docs

<!-- List specific patterns, examples, guidance present in command but missing from content.yaml -->

- [ ] ...

## Information in Docs NOT in Command

<!-- List architectural content from content.yaml not reflected in the command -->

- [ ] ...

## Gaps in Operation Prompt

<!-- What does the prompt ask for that the docs can't provide? -->

- [ ] ...
```

### Phase 2: Generate Fresh Command

Launch a **subagent** to generate a fresh command in isolation:

```
Use the Task tool with:
- subagent_type: "general-purpose"
- prompt: |
    Run the /generate-agentic-op skill with arguments: <topic-id> <operation-name>

    This will read topics/<topic>/metadata.yaml and content.yaml, then generate
    a command to generated_agentic_operations/commands/<topic>-<op>.md

    Return the path to the generated file when complete.
```

**Why a subagent?** The generation task should reason fresh from the documentation without being influenced by knowledge of the existing command or harmonization goals. This isolation ensures we see what the docs *actually* produce.

After the subagent completes, read the generated file at `generated_agentic_operations/commands/<topic>-<op>.md` for Phase 3 comparison.

### Phase 3: Compare Commands

Read both commands and append a comparison section to the analysis file:

```markdown
## Command Comparison

| Dimension | Original | Generated | Winner |
|-----------|----------|-----------|--------|
| Specificity of code patterns | ... | ... | ... |
| Coverage of anti-patterns | ... | ... | ... |
| Actionability of guidance | ... | ... | ... |
| Use of related_code_paths | ... | ... | ... |
| Alignment with docs | ... | ... | ... |

## Key Differences

1. ...
2. ...
3. ...
```

### Phase 4: Generate Recommendations

Write recommendations to `topics/<topic>/harmonize/<op>_recommendations.md`.

Split into two categories - this separation is critical:

```markdown
# Harmonization Recommendations: <operation-name>

## Documentation Improvements

<!-- Changes to content.yaml to add missing reference info -->
<!-- These become the source of truth that commands are generated from -->

1. Add prose block about X
2. Expand slide Y to include Z pattern
3. Add agent-context block for anti-patterns
4. Add example code showing pattern W

## Prompt Improvements

<!-- Changes to metadata.yaml operation prompt -->
<!-- NOT content duplication - prompts should reference docs, not repeat them -->
<!-- Focus on: how to interact with agent, prods to pull specific info from docs -->

1. Add instruction to consult related_code_paths for examples
2. Add TODO marker for agent to extract patterns from docs
3. Refine scope/focus of the operation
4. Clarify input format expectations
```

### Phase 5: Summary

Output a brief summary to the user:
- What gaps were found
- Key differences between original and generated commands
- Top 3 actionable recommendations
- Paths to created artifacts

## Important Notes

- **Documentation is source of truth** - prompts should reference docs, not duplicate content
- **Create concrete artifacts** - don't just think, write files
- **Isolation matters** - Phase 2 subagent must not see the existing command
- **Prompt changes are about interaction** - how to guide the agent to use docs, not what to embed
- If prose content is too verbose for slides, suggest prose blocks or agent-context blocks
