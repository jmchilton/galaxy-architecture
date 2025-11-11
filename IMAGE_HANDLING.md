# Image Handling Guide

This document describes how images are handled across the Galaxy Architecture documentation project, including their sources in training-material, patterns in slides, and how they're processed for different output contexts.

## 1. Image Sources in training-material Repository

Images in training-material come from multiple locations:

### 1.1 Development/Architecture Images
**Location**: `training-material/topics/dev/images/`

**Examples**:
- `docker-chart.png`
- `biocontainers.png`
- `gitter_galaxyproject.png`
- `galaxy_main_scheme.png`
- Various `.png` and `.svg` files for dev topics

**Pattern in Content**: Referenced as `../../images/filename.png`
- From `topics/dev/tutorials/architecture-{topic}/slides.md`
- Goes up 2 levels (to `topics/`) then into `dev/images/`

### 1.2 Shared/Common Images
**Location**: `training-material/shared/images/`

**Examples**:
- `GTNLogo1000.png` - GTN logo used across training material
- `conda_logo.png` - Bioconda logo
- Other shared branding/utility images

**Pattern in Content**: Referenced as `{{ site.baseurl }}/assets/images/filename.png`
- GTN template variable that gets rendered by Jekyll
- `{{ site.baseurl }}` becomes the web root path in GTN
- Maps to `/assets/images/` in built training-material

### 1.3 Core/Project-Specific Images
**Location**: `galaxy-architecture-branch-main/images/`

**Examples**:
- `app_py2.plantuml.svg`
- `app_types.plantuml.svg`
- Various PlantUML-generated architecture diagrams
- Custom diagrams and screenshots

**Pattern in Content**: Referenced as `../../../../images/filename.svg` or `../../images/filename.svg`
- Relative paths from content location to images in this project

## 2. Image Patterns in Content Files

### 2.1 Markdown Image Syntax
All images use standard markdown syntax:
```markdown
![alt text](path/to/image.png)
```

### 2.2 Path Patterns in content.yaml

**Training-Material Dev Images**:
```markdown
![Docker](../../images/docker-chart.png)
```
- From `topics/dev/tutorials/architecture-{topic}/`
- Path goes: `../../images/` (up to dev, then into images)

**Shared Images**:
```markdown
![Bioconda]({{ site.baseurl }}/assets/images/conda_logo.png)
```
- GTN-specific template variable
- Gets rendered by Jekyll during build

**Project-Specific Images**:
```markdown
![App Architecture](../../images/app_py2.plantuml.svg)
![App Architecture](../../../../images/app_types.plantuml.svg)
```
- Depth varies: `../../` or `../../../../` depending on block location
- Points to `./images/` at project root

## 3. Image Copying Strategy

### 3.1 Which Images Get Copied
**Sources that are copied INTO this project**:
- Training-material dev images (docker-chart.png, etc.) ✓ COPY
- Training-material shared images (GTNLogo1000.png, conda_logo.png) ✓ COPY
- Project-specific images (PlantUML SVGs) ✓ ALREADY HERE

**Sources that are NOT copied**:
- External/online images (https://, http://) ✗ NO COPY
- Images in training-material that don't appear in our content ✗ NO COPY

### 3.2 Copy Process

**Script**: Not currently automated, done manually as needed

**When to Copy**:
1. When adding new content from training-material that references images
2. When encountering "image not found" errors during build
3. During initial content migration

**How to Copy**:
```bash
# Copy from training-material (run from project root)
cp ~/workspace/training-material/topics/dev/images/*.png images/
cp ~/workspace/training-material/shared/images/GTNLogo1000.png images/
cp ~/workspace/training-material/shared/images/conda_logo.png images/
```

### 3.3 Storage Location in This Project
**Primary location**: `./images/` (project root)

All images go to the same flat directory regardless of source:
- `images/docker-chart.png` (from dev/)
- `images/conda_logo.png` (from shared/)
- `images/app_py2.plantuml.svg` (already in project)

**Secondary location**: `doc/source/_images/` (Sphinx internal)
- Auto-managed by Sphinx during build
- DO NOT MANUALLY MODIFY
- Sphinx populates this from discovered image references

## 4. Sphinx Documentation Path Handling

### 4.1 What Happens During Sphinx Build

1. **Source markdown**: `doc/source/architecture/ecosystem.md`
   - Contains original paths: `../../images/...`, `{{ site.baseurl }}/...`, etc.

2. **Path rewriting Stage 1**: `outputs/sphinx-docs/build.py` → `process_markdown_for_sphinx()`
   - Converts GTN template variables: `{{ site.baseurl }}/assets/images/` → `../_images/`
   - Function location: Lines 145-197

3. **Path rewriting Stage 2**: `outputs/sphinx-docs/build.py` → `rewrite_image_paths_for_sphinx()`
   - Converts relative paths to normalized format
   - Function location: Lines 200-235

4. **Markdown generation**: Final markdown written to `doc/source/architecture/`
   - Mixed paths: some `../images/`, some `../_images/`

5. **Sphinx processing**: Sphinx builds HTML from markdown
   - Discovers image references in markdown
   - Copies referenced images to `doc/build/html/_images/`
   - Generates correct relative paths in final HTML

6. **Manual image copying**: Makefile step (optional, for redundancy)
   - `./images/` → `doc/build/html/images/` (separate from Sphinx's `_images/`)
   - Makefile line 42: `cp images/*.png images/*.svg doc/build/html/images/ 2>/dev/null || true`

### 4.2 Path Rewriting Rules for Sphinx - Stage 1

**Function**: `process_markdown_for_sphinx(markdown: str) -> str`

**What it does**: Handles GTN template variables FIRST, before other rewrites

**Conversion Rules**:
```python
# GTN template variables ONLY (highest priority)
{{ site.baseurl }}/assets/images/filename.png → ../_images/filename.png
```

**Important**: This happens BEFORE the second stage rewriting, so GTN variables use `_images` while regular images use `images`

### 4.3 Path Rewriting Rules for Sphinx - Stage 2

**Function**: `rewrite_image_paths_for_sphinx(markdown: str) -> str`

**What it does**: Normalizes remaining relative paths to Sphinx structure

**Conversion Rules**:
```python
# Shared images from training-material (if not already converted by Stage 1)
../../../../shared/images/ → ../images/

# Dev images from training-material
../../images/ → ../images/

# Generic 4-level paths (from this project)
../../../../images/ → ../images/
```

**Why two stages?** GTN variables use `../_images/` (Sphinx's standard) while everything else uses `../images/` (our local copy)

### 4.4 Final Sphinx HTML Paths

**For GTN template images**:
- From markdown: `![logo](../_images/GTNLogo1000.png)`
- Sphinx processes: Copies to `doc/build/html/_images/GTNLogo1000.png`
- Final HTML: `<img src="_images/GTNLogo1000.png"/>`

**For regular images**:
- From markdown: `![Docker](../images/docker-chart.png)`
- Sphinx processes: Copies to `doc/build/html/images/docker-chart.png`
- Final HTML: `<img src="images/docker-chart.png"/>`

### 4.5 The Dual-Directory System

**Why two directories?**
- `doc/source/_images/`: Sphinx's standard managed directory
- `doc/build/html/images/`: Our redundant copy for additional images
- They may overlap but serve different purposes

**Which one is used?**
- GTN variables → `_images/` (processed by Sphinx)
- Regular images → `images/` (copied by Makefile, processed by Sphinx)
- Sphinx ensures both work

## 5. Local HTML Slides Path Handling

### 5.1 What Happens During HTML Slides Generation

1. **Content loading**: `outputs/training-slides/build.py` loads from `content.yaml`
   - Original paths: `../../images/...`, `../../../../shared/images/...`, `{{ site.baseurl }}/...`

2. **Path rewriting**: `rewrite_image_paths_for_html()` for standalone HTML
   - Converts to: `../../../../images/filename.png`
   - Function location: Lines 20-61

3. **Markdown generation**: Slides markdown with rewritten paths
   - Embedded in HTML textarea for Remark.js

4. **Dynamic path detection**: JavaScript in HTML wrapper (if needed)
   - Checks context and may adjust paths at runtime
   - Location: `outputs/training-slides/html_wrapper_template.html` lines 210-258

5. **Image copying**: Manual step copies to `doc/build/html/images/`
   - Supports Sphinx context viewing

### 5.2 Path Rewriting Rules for HTML Slides

**Function**: `rewrite_image_paths_for_html(markdown: str, topic_name: str) -> str`

**Conversion Rules**:
```python
# Shared images from training-material
../../../../shared/images/ → ../../../../images/

# Dev images from training-material
../../images/ → ../../../../images/

# GTN template variables - BROKEN - NEEDS FIX
{{ site.baseurl }}/assets/images/ → ./assets/images/  (DOES NOT EXIST)
```

**Why `../../../../images/`?**
- HTML file location: `outputs/training-slides/generated/architecture-{topic}/slides.html`
- Images location: `./images/` (project root)
- Depth: 4 levels up from slides → root

### 5.3 Known Issue: GTN Template Variables in HTML Slides

**Problem**: The pattern `{{ site.baseurl }}/assets/images/GTNLogo1000.png` is converted to `./assets/images/GTNLogo1000.png`

**Current Code** (lines 35-40 in build.py):
```python
# Handle GTN template variables - replace with placeholder that won't error
markdown = re.sub(
    r'\{\{\s*site\.baseurl\s*\}\}',
    '.',  # Use dot to point to root, effective path becomes ./assets/images/...
    markdown
)
```

**Problem**: `./assets/images/` directory doesn't exist, so images fail to load with 404 errors

**Solution Options**:
1. Convert to: `../../../../images/` (same as other rewritten paths)
2. Create `./assets/images/` symlink or directory copy (not recommended)
3. Skip GTN variables - don't include GTN-branded images in standalone slides

**Recommended Fix**: Change the regex to convert directly to `../../../../images/` instead of using `{{ site.baseurl }}` placeholder.

### 5.4 Dynamic Path Detection in JavaScript

**Location**: `outputs/training-slides/html_wrapper_template.html` (Lines 210-258)

**Current Implementation**:
```javascript
// Default path
let workingPath = '../../../../images/';

// If in Sphinx context, use shorter path
if (window.location.href.includes('_downloads')) {
    workingPath = '../../images/';
}

// Rewrite markdown if needed
if (workingPath !== '../../../../images/') {
    markdown = markdown.replace(/\.\.\/\.\.\/\.\.\/\.\.\/images\//g, workingPath);
    source.textContent = markdown;
}
```

**What it does**:
1. Detects if HTML is viewed from Sphinx's `_downloads/` directory
2. If so, rewrites `../../../../images/` → `../../images/`
3. Otherwise keeps default paths

**Limitation**: Only handles the `_downloads` case, doesn't try alternative paths

**Dead Code**:
- `possibleBasePaths` array defined but never used
- `checkPath()` function defined but never used
- These were left over from an earlier implementation attempt

### 5.5 Final HTML Slide Paths

**Direct viewing**:
- File: `outputs/training-slides/generated/architecture-{topic}/slides.html`
- Image path: `../../../../images/filename.png`
- Resolves to: `./images/filename.png` ✓

**Sphinx download context**:
- File: `doc/build/html/_downloads/{hash}/slides.html`
- Path detected: `_downloads` in URL
- Image path rewritten to: `../../images/filename.png`
- Resolves to: `doc/build/html/images/filename.png` ✓

## 6. Current Issues and Limitations

### 6.1 GTN Template Variables Broken in HTML Slides
**Problem**: Converts to `./assets/images/` which doesn't exist
**Impact**: GTNLogo1000.png and similar images don't load in standalone HTML slides
**Status**: NEEDS FIX - Recommend converting to `../../../../images/` instead

### 6.2 Dead Code in JavaScript Path Detection
**Problem**:
- `possibleBasePaths` array defined but never used
- `checkPath()` function defined but never called
**Impact**: Misleading code, potential maintenance confusion
**Status**: NEEDS CLEANUP - Remove dead code or implement the fallback logic

### 6.3 Dual Directory System Creates Confusion
**Problem**: Images live in both `./images/`, `doc/source/_images/`, and `doc/build/html/images/`
**Impact**: Unclear which is "the" image directory, fragile copy process
**Status**: ACCEPTABLE but should be better documented

### 6.4 Image Discovery Not Automated
**Problem**: No automated detection of missing images
**Current State**: Manual copying when errors encountered
**Improvement Needed**: Script to detect and copy missing images automatically

### 6.5 Makefile Copy Command Is Fragile
**Problem**:
```bash
cp images/*.png images/*.svg doc/build/html/images/ 2>/dev/null || true
```
- Silent failures if target directory doesn't exist
- Doesn't copy `.txt` files (PlantUML source files)
- Suppresses all errors invisibly

**Impact**: May fail silently during builds
**Status**: SHOULD IMPROVE - Add better error handling

## 7. Recommended Workflow

### 7.1 When Adding New Content from training-material

1. **Copy content**: Migrate slides/markdown
2. **Check for images**: Grep content for image patterns
3. **Identify sources**: Determine if from dev or shared
4. **Copy images**: Run copy commands for needed images
5. **Test locally**: Open slides to verify image loading
6. **Build Sphinx**: Run `make build-sphinx`
7. **Check browser**: View HTML docs for image rendering
8. **Check both contexts**: Direct slides AND Sphinx downloads

### 7.2 When Adding Custom Images to This Project

1. **Add to images/**: Place in `./images/` directory
2. **Reference in content**: Use appropriate relative path depth
3. **Test in all contexts**: Direct viewing, Sphinx docs, Sphinx slides
4. **Update documentation**: Note new image location

### 7.3 Debugging Image Not Found Errors

1. **Check console**: Note the attempted file path
2. **Identify pattern**: Is it `../../`, `../../../../`, or `{{ site.baseurl }}`?
3. **Find source**: Check training-material or local `images/`
4. **Copy if needed**: Use copy commands above
5. **Rebuild**: Run appropriate build command
6. **Re-test**: Verify image appears in ALL contexts (Sphinx docs, direct slides, Sphinx slides download)

## 8. Files Involved

### Core Image Handling Files
- `outputs/training-slides/build.py` - HTML slides generation and path rewriting
- `outputs/training-slides/html_wrapper_template.html` - JavaScript path detection
- `outputs/sphinx-docs/build.py` - Sphinx markdown generation and TWO-STAGE path rewriting
- `Makefile` - Image copying step for Sphinx build
- `images/` - Repository of all accessible images

### Configuration
- `doc/source/conf.py` - Sphinx configuration
- `topics/*/content.yaml` - Image references in content

## 9. Testing Checklist

- [ ] Direct HTML slide viewing works
- [ ] Sphinx documentation displays images
- [ ] Sphinx slide downloads display images
- [ ] No console 404 errors for images
- [ ] Both dev and shared images work
- [ ] GTN template variables work (or are handled appropriately)
- [ ] Custom project images work
- [ ] External URLs bypass path rewriting
- [ ] All image formats (png, svg, jpg) are copied

## 10. TODO Items for Image Handling Improvements

1. **Fix GTN template variables in HTML slides** - Change `./assets/images/` → `../../../../images/`
2. **Remove dead code** - Delete unused `possibleBasePaths` and `checkPath()`
3. **Improve Makefile robustness** - Better error handling, copy all image types
4. **Create image validation script** - Auto-detect missing images and copy from training-material
5. **Consolidate image directories** - Consider single source directory approach
6. **Document _images discovery** - Clarify what Sphinx does with `_images/` directory
