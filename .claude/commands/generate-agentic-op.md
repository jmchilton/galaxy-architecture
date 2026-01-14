# Generate Agentic Operation Artifact

Generate Claude slash command or skill from topic content by reading and reasoning about what's architecturally relevant.

## Usage

```
/generate-agentic-op <topic-id> <operation-name>
```

## Arguments

- **topic-id**: Topic identifier (e.g., "dependency-injection")
- **operation-name**: Operation name from metadata.yaml (e.g., "implement-di-refactor")

## Examples

```
/generate-agentic-op dependency-injection implement-di-refactor
/generate-agentic-op file-sources implement-file-source
```

## Your Task

1. **Load source content:**
   - Read `topics/<topic-id>/metadata.yaml`
   - Read `topics/<topic-id>/content.yaml`
   - Validate that the operation exists in agentic_operations

2. **Understand the operation:**
   - Read the operation's `prompt` field to understand the development task
   - If the prompt contains a TODO item, it is a indication that this is information you should
     generate from the topic content and embed in the generated artifact.
   - Determine the operation type (claude-slash-command or claude-skill)

3. **Reason about relevant content:**
   - Review all content blocks in content.yaml
   - Determine what architectural information is relevant for THIS operation
   - Consider:
     - What concepts does someone need to understand?
     - What code patterns should they follow?
     - What pitfalls should they avoid?
     - What examples would be most helpful?
   - For commands: Be concise, focus on immediate task needs
   - For skills: Be comprehensive, provide deeper architectural context

4. **Create the artifact:**
   - Write to: `generated_agentic_operations/commands/<topic>-<op>.md` (for commands)
   - Or: `generated_agentic_operations/skills/<topic>-<op>.md` (for skills)
   - Include:
     - Operation prompt and purpose
     - Relevant architectural concepts from content.yaml
     - Key points and objectives from metadata.yaml
     - Related code paths (Galaxy codebase assumed available)
     - Code examples where helpful
   - Format the content in a way that works well for Claude to use as context

5. **Generate improvement suggestions:**
   - Analyze what content could make this artifact more effective
   - Write suggestions to `topics/<topic-id>/suggestions/<operation>.md`
   - Include specific, actionable ideas for enhancing content.yaml

## Important Notes

- **DO NOT mechanically copy** all content - use judgment about what's relevant
- **DO** If either the files you're asked to generate already exist, do not read them, back them up,
  and your new summary to the supplied path.
- **DO** synthesize and reformulate content appropriately for the operation
- **DO** prominently feature related_code_paths (Galaxy available at these paths)
- **DO** fail if the operation doesn't exist or content is insufficient
- **DO** create output directories if they don't exist

## Requirements

- Topic must have agentic_operations defined in metadata.yaml
- Operation name must match entry in metadata.yaml
- content.yaml should have sufficient relevant content for the operation
