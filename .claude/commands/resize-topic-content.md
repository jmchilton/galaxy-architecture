# Resize Topic Content

## Usage

```
/resize-topic-content <topic-id>
```

## Arguments

- **topic-id**: Topic identifier (e.g., "markdown", "dependency-injection")

## Examples

```
/resize-topic-content markdown
/resize-topic-content startup
/resize-topic-content production
```

## What it does

Generate the slides and open them using the Playwright MCP. If the playwright MCP isn't available - cancel the command and assist the user in setting it up.

Walk through each slide and assess the size of the content on screen. If there is room grow the size of the content (adjust the class to do this). Alternatively if the content doesn't fit - you can reduce the size.

The size of the content is determined by the class field in content.yaml for the slide. If none of these classes is set for the slide - that is baseline. If a class is set
they mean this:

| `reduce70` | Very long code blocks (10+ lines) or wide code |
| `reduce90` | Medium-long code blocks (5-10 lines) |
| `enlarge120` | 4-5 bullets, or tables with 5+ rows |
| `enlarge150` | 3-4 bullets, small tables (3-4 rows) |
| `enlarge200` | Critical takeaways, 2-3 bullets |

Once you've updated the slides - regenerate the slides and retest the output. If some of the content still
feels incorrectly sized - report this to the user.

Finish with a summary of what changed, what looks good now and what still needs work.
