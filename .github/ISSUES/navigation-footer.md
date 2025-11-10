# Add Navigation Footer to Generated Slides

## Summary

The original GTN slides include a navigation footer at the end that provides links to previous and next tutorials in the architecture series. This footer is currently missing from the generated slides.

## Current State

The generated slides end without any navigation footer. The original slides include:

```markdown
.footnote[Previous: [Frameworks]({% link topics/dev/tutorials/architecture-5-frameworks/slides.html %}) | Next: [Tasks]({% link topics/dev/tutorials/architecture-7-tasks/slides.html %})]
```

## Requirements

1. **Add navigation footer support** to the slide generator (`outputs/training-slides/build.py`)
2. **Metadata schema** - Add optional `navigation` field to `metadata.yaml`:
   ```yaml
   training:
     navigation:
       previous: architecture-frameworks  # topic_id of previous tutorial
       next: architecture-tasks  # topic_id of next tutorial
   ```
3. **Template update** - Add footer to `outputs/training-slides/template.html` at the end:
   ```jinja2
   {% if navigation %}
   .footnote[Previous: [{{ navigation.previous_title }}]({% link topics/dev/tutorials/architecture-{{ navigation.previous_id }}/slides.html %}) | Next: [{{ navigation.next_title }}]({% link topics/dev/tutorials/architecture-{{ navigation.next_id }}/slides.html %})]
   {% endif %}
   ```
4. **Build script** - Resolve topic IDs to titles and generate navigation links

## Implementation Notes

- The footer should only appear if both `previous` and `next` are specified
- Topic IDs should be resolved to their display titles from metadata
- The footer uses GTN's `{% link %}` template tag for proper URL generation
- Should match the format: `Previous: [Title](link) | Next: [Title](link)`

## Related

- Original slide format: `~/workspace/training-material/topics/dev/tutorials/architecture-6-dependency-injection/slides.html` (line 441)
- Current template: `outputs/training-slides/template.html`
- Build script: `outputs/training-slides/build.py`

## Acceptance Criteria

- [ ] Navigation footer appears at end of generated slides when metadata includes navigation
- [ ] Footer format matches original GTN slides
- [ ] Links resolve correctly to previous/next tutorials
- [ ] Footer only appears when both previous and next are specified
- [ ] Documentation updated to explain navigation metadata

