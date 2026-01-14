# Annotate Topic Slides

## Usage

```
/annotate-topic-slides <topic-id>
```

## Arguments

- **topic-id**: Topic identifier (e.g., "markdown", "dependency-injection")

## Examples

```
/annotate-topic-slides markdown
/annotate-topic-slides startup
/annotate-topic-slides production
```

## What it does?

Review each content.yaml for the topic and decide what prose should be planned. The prose section
will be added in generated Sphinx documentation for the topic. It should include:

- More textual descriptions (sort of legends) for most diagrams that aren't entirely self-explanatory.
- Connective tissue that would result in the topic reading better as a document.
- Additional reference data when applicable.

The agent will output topics/<topic_id>/plan/prose_plan.md with a plan for what prose sections should
be added to the topic.

The agent should be honest about what it knows well versus what needs more research. The plan that gets
outputted should include research steps and open questions.
