# Slide Design Guide

Reference for creating effective Galaxy architecture slides. Used by `/plan-a-topic` command.

## Core Principles

### 1. Visual-First Slides
The best slides lead with diagrams/visuals, not text. A centered diagram with minimal text teaches more than bullet lists.

**Good:**
```yaml
- type: slide
  id: app_decomposed
  class: center
  content: |
    ![Decomposed App](../../images/app_decomposed.plantuml.svg)
```

**Weak:**
```yaml
- type: slide
  heading: "App Architecture"
  content: |
    - The app is decomposed into managers
    - Each manager handles specific domain
    - Managers communicate via DI container
```

### 2. Problem → Solution Narrative

Structure slides to show **what's wrong**, then **how to fix it**.

**Pattern from dependency-injection:**
1. Show problematic code (god object usage)
2. Explain why it's problematic
3. Show improved approach
4. Explain benefits

Example flow:
- Slide: "A Typical Usage" (problematic code)
- Slide: "Problematic Dependency Graph"
- Slide: "Design Benefits of Injecting Dependencies" (solution)

### 3. Code Evolution via Diffs

Show before/after with actual diffs, not separate code blocks.

**Effective:**
```yaml
- type: slide
  id: di_unified_approach
  class: reduce70
  content: |
    ```diff
    -def get_tags_manager() -> TagsManager:
    -    return TagsManager()
    -
    -
     @cbv(router)
     class FastAPITags:
    -    manager: TagsManager = Depends(get_tags_manager)
    +    manager: TagsManager = depends(TagsManager)
    ```

    Unified DI approach is *less verbose*, works uniformly.
```

### 4. One Concept Per Slide

Each slide should communicate ONE idea. If you have 5 bullet points, consider 5 slides.

**Good progression (from tasks/):**
- Slide: Show request processing diagram
- Slide: "Web servers are a terrible place to do work" (single point, `enlarge120`)
- Slide: Show Celery infrastructure diagram
- Slide: Celery overview image
- Slide: "Downsides of Celery" (single counterpoint)

### 5. Code Examples Should Be Real

Use actual Galaxy code paths and patterns. Slides reference real files.

**Good:**
```yaml
content: |
  See `lib/galaxy/tools/imp_exp/__init__.py`:

  ```python
  from galaxy.schema.tasks import SetupHistoryExportJob
  ...
  export_history.delay(request=request)
  ```
```

## Slide Types

### Diagram Slides (Most Valuable)
- `class: center` for centered diagrams
- Minimal or no heading
- Let the diagram speak

```yaml
- type: slide
  id: celery-overview
  class: center
  content: '![Celery Overview](../../images/core_backend_celery.plantuml.svg)'
```

### Code Pattern Slides
- Show concrete, runnable examples
- Use `class: reduce70` or `reduce90` for long code
- Include brief explanation after code block

```yaml
- type: slide
  id: simple-task
  heading: A Simple Task
  content: |
    ```python
    @galaxy_task(ignore_result=True, action="setting up export history job")
    def export_history(
        model_store_manager: ModelStoreManager,
        request: SetupHistoryExportJob,
    ):
        model_store_manager.setup_history_export_job(request)
    ```
```

### Concept Slides
- Use `class: enlarge120`, `enlarge150`, or `enlarge200` for emphasis
- Keep bullet points to 3-4 max
- Short, punchy text

```yaml
- type: slide
  id: best-practices
  heading: Best Practices
  class: enlarge200
  content: |
    - Place tasks in `galaxy.celery.tasks`.
    - Keep tasks thin (delegate to managers).
    - Ensure injected components are decomposed.
    - Place request types in `galaxy.schema.tasks`.
```

### Quote/Callout Slides
- Use blockquotes for definitions/citations
- Good for establishing concepts

```yaml
- type: slide
  id: god_object
  heading: "A God object"
  content: |
    > "a God object is an object that knows too much or does too much."

    https://en.wikipedia.org/wiki/God_object

    Not only does `app` know too much, it's used everywhere.
```

## Effective Patterns

### 1. Mindmap Overview → Detail Slides
Start with a mindmap showing structure, then dive into specific areas.

**From files/:**
- Slide: Project Docs mindmap
- Slide: Code mindmap
- Slide: Scripts mindmap
- Slide: Test Sources mindmap

### 2. Architecture Diagram → Zoom In
Show high-level, then progressively zoom.

**From tasks/:**
- Slide: ASGI app request processing
- Slide: "Zoom in on Backend" (controllers)
- Slide: Infrastructure including Celery

### 3. Success Stories
After teaching pattern, show real wins.

**From tasks/:**
- Slide: "Existing Tasks Success Stories"
- Slide: PDF Export Problems (the problem)
- Slide: Short Term Storage (the solution)
- Slide: Robust PDF Export (the code)

### 4. Future Work / Next Steps
End with where things are going.

```yaml
- type: slide
  id: future-work
  heading: Future Work
  class: enlarge200
  content: |
    - *Migrating tool submission to tasks*
    - Workflow scheduling
    - Importing shared histories

    https://github.com/galaxyproject/galaxy/issues/11721
```

## Class Usage

| Class | When to Use |
|-------|-------------|
| `center` | Diagram-only slides |
| `reduce70` | Very long code blocks (10+ lines) or wide code |
| `reduce90` | Medium-long code blocks (5-10 lines) |
| `enlarge120` | 4-5 bullets, or tables with 5+ rows |
| `enlarge150` | 3-4 bullets, small tables (3-4 rows) |
| `enlarge200` | Critical takeaways, 2-3 bullets |

## Extended Explanations

Don't use `???` speaker notes. Instead, use prose blocks in content.yaml.

Prose blocks appear in generated documentation but not in slides - perfect for detailed explanations that support a visual slide.

```yaml
- type: slide
  id: celery-infrastructure
  class: center
  content: |
    ![Infrastructure including Celery](../../images/core_backend_celery.plantuml.svg)

- type: prose
  id: celery-infrastructure-explanation
  content: |
    Handling a task off to Celery allows the web server to respond right
    away. Celery is meant for long running tasks that would otherwise
    block the request/response cycle.
```

This keeps slides clean while preserving valuable context in the documentation.

## Anti-Patterns to Avoid

### Wall of Text
Don't put paragraphs on slides. Use prose blocks for extended explanations.

### Too Many Bullets
More than 5 bullets = split into multiple slides or use a diagram.

### Code Without Context
Always show where code lives (`See lib/galaxy/...`) and why it matters.

### Abstract Without Concrete
Every concept needs at least one real code example.

### Missing Visuals
If you can draw it, draw it. Diagrams > bullets.

## Slide Planning Checklist

For each slide, ask:

1. **What's the ONE thing?** - Single concept per slide
2. **Can this be a diagram?** - Visual > text
3. **Is this real code?** - Use actual Galaxy paths
4. **What's the narrative?** - Problem → Solution flow
5. **Right size class?** - Adjust font for content amount

## Topic Flow Templates

### Pattern Introduction
1. Context diagram (center)
2. Problem statement (enlarge)
3. Problematic code example
4. Why it's problematic (bullets)
5. Solution concept
6. Solution code (with diff if migrating)
7. Benefits summary (enlarge)
8. Framework integration examples
9. Best practices (enlarge)
10. Success stories
11. Future work

### Component Overview
1. High-level architecture diagram
2. Component breakdown (mindmap)
3. Zoom into each component (2-3 slides each)
4. Integration points
5. Usage examples
6. Best practices

### Process/Pipeline
1. Full pipeline diagram
2. Step-by-step breakdown
3. Code for each step
4. Edge cases/error handling
5. Configuration options
6. Testing approach
