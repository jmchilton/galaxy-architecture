# Add Project Slide to Ecosystem Content

Add a new project slide to `topics/ecosystem/content.yaml`.

## Usage

```
/add-project-slide <project-url>
```

## Arguments

- **project-url**: Full URL to the project (e.g., https://github.com/galaxyproject/pulsar, https://github.com/bgruening/docker-galaxy-stable)

## Examples

```
/add-project-slide https://github.com/galaxyproject/some-new-project
/add-project-slide https://github.com/usegalaxy-eu/some-project
```

## What it does

1. Fetches the project README or description from the URL
2. Reads the existing slides in `topics/ecosystem/content.yaml` to understand:
   - The slide structure and naming patterns
   - Where different project categories belong (user-facing, plugins, deployers, etc.)
3. Extracts project name and organization from the URL
4. Generates a new slide block following the established pattern with:
   - Unique `id` based on the project
   - Link to the project
   - Brief description extracted from README
   - Appropriate styling class (usually `enlarge150`)
5. Determines the correct section for the project (user-facing apps, plugin developers, deployers/admins, etc.)
6. Inserts the new slide in the appropriate location in `topics/ecosystem/content.yaml`
7. Validates the file with `make validate` to ensure YAML is correct
8. Builds Sphinx docs to verify the change works

## Notes

- Deduces slide structure at runtime - no need to prescribe exact format
- Handles both GitHub and other URLs
- Automatically extracts relevant project description from README
- Places project in appropriate category based on content analysis
