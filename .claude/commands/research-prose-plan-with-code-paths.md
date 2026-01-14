# Research Prose Plan with Code Paths

## Usage

```
/research-prose-plan-with-code-paths <topic-id>
```

## Arguments

- **topic-id**: Topic identifier (e.g., "markdown", "dependency-injection")

## Examples

```
/research-prose-plan-with-code-paths markdown
/research-prose-plan-with-code-paths startup
/research-prose-plan-with-code-paths production
```

## What it does?

This should be used after initial slides have been finalized (topics/<topic_id>/content.yaml) and a topic
for adding prose has been generated (topics/<topic_id>/plan/prose_plan.md).

For each code path research document found (topics/<topic_id>/notes/path_*md), serially launch a subagent
and instruct it to read the slide content, the slide metadata, and the prose plan, as well as the
research note for that code path. The subagent should produce a report that contains any relevant 
information about open prose plan topics as well as suggestions for additional content that should be
captured in prose blocks.

The agent executing this command will evaluate whether the information provided is useful for augmenting 
prose plan and it will augment it with suggestions that are accepted or research that seems valuable in
answering open questions.
