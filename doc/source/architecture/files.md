# Files

> 📊 [View as training slides](../../../outputs/training-slides/generated/architecture-files/slides.html)

## Learning Questions
- How is the Galaxy codebase organized?
- Where do I find different components?
- What is the difference between `lib` and `packages`?

## Learning Objectives
- Navigate the Galaxy repository structure
- Understand the `lib` vs `packages` organization
- Locate key files and directories

## Galaxy Files and Directory Structure

*The physical architecture of the Galaxy code.*

## Files and Directories

*The physical architecture of the Galaxy code.*

## Project Docs

![Project Files](../_images/core_files_project_docs.mindmap.plantuml.svg)

## Code

![Code](../_images/core_files_code.mindmap.plantuml.svg)

## Scripts

![Scripts](../_images/core_files_scripts.mindmap.plantuml.svg)

## Test Sources

![Test Source Files](../_images/core_files_test.mindmap.plantuml.svg)

## Continuous Integration

![Continuous Integration Files](../_images/core_files_ci.mindmap.plantuml.svg)

## One Repository, Two Views of a Project

![Two Views of Galaxy Python Project](../_images/core_files_code_python_2_views.mindmap.plantuml.svg)

`lib` contains a single monolithic view of the `galaxy` namespace.

Each sub-directory of `packages` contains a logical subset of this `galaxy` namespace. Directory symbolic links are used to ensure the same files are used.

## Package Structure

![package structure](../_images/core_packages.plantuml.svg)

## PyPI

![galaxy-tool-util on PyPI](../_images/core_tool_util_pypi.png)

![Package Files](../_images/core_files_code_package.mindmap.plantuml.svg)

## Key Takeaways
- Project documentation in root (README, CONTRIBUTING, CODE_OF_CONDUCT)
- Code in `lib` (monolithic) and `packages` (modular)
- Tests in `test` and `lib/galaxy_test`
- CI configuration in `.github`
- Packages are published to PyPI
