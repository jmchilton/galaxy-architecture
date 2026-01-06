# PR #20805: Add Hugging Face 🤗 file source and user-defined template

**Author:** David López (@davelopez)
**Merged:** August 28, 2025
**URL:** https://github.com/galaxyproject/galaxy/pull/20805
**Requires:** PR #20799, PR #20806
**Built on:** fsspec base (PR #20698)

## Overview

Adds **Hugging Face Hub file source** enabling Galaxy users to directly access and import AI/ML models, datasets, and files from Hugging Face. Includes user-defined template for personal model repositories.

## Hugging Face Hub Background

### What is Hugging Face?

Leading platform for AI/ML models and datasets:
- 350,000+ models (transformers, diffusers, etc.)
- 100,000+ datasets
- Community-driven sharing and collaboration
- Version control for models (Git-based)
- Model cards with metadata and documentation

### Why Galaxy Integration?

**Use Cases:**
1. **Model Import**: Download pre-trained models for Galaxy tools
2. **Dataset Access**: Import ML training/test datasets
3. **Reproducibility**: Reference specific model versions in workflows
4. **Collaboration**: Share Galaxy-generated models via Hugging Face

## Implementation

### Built on fsspec

Leverages fsspec's Hugging Face backend:
```python
class HuggingFaceFilesSource(FsspecFilesSource[HFTemplateConfig, HFConfig]):
    plugin_type = "huggingface"

    def _get_fs(self, context: FilesSourceRuntimeContext[HFConfig]):
        return fsspec.filesystem(
            "hf",
            repo_id=context.resolved_config.repo_id,
            token=context.resolved_config.token,  # Optional for private repos
            repo_type=context.resolved_config.repo_type  # "model", "dataset", or "space"
        )
```

### Configuration Options

**Repository Selection:**
- `repo_id`: Organization/repository (e.g., "bert-base-uncased", "username/my-model")
- `repo_type`: Type of repository ("model", "dataset", or "space")
- `revision`: Git ref (branch, tag, or commit SHA) - defaults to "main"

**Authentication:**
- `token`: Optional Hugging Face access token for private repositories

## User-Defined Template

### Template Configuration

In `production_huggingface.yml`:
```yaml
- id: huggingface
  name: Hugging Face Hub
  description: |
    Access models and datasets from Hugging Face Hub.
    Browse public repositories or use your access token
    for private repositories.
  variables:
    repo_id:
      type: string
      help: Repository identifier (e.g., "bert-base-uncased" or "username/my-model")
    repo_type:
      type: string
      help: Type of repository ("model", "dataset", or "space")
      default: "model"
    revision:
      type: string
      help: Git revision (branch, tag, or commit SHA)
      default: "main"
  secrets:
    token:
      help: Hugging Face access token (optional, required for private repos)
      required: false
  configuration:
    type: huggingface
    repo_id: '{{ variables.repo_id }}'
    repo_type: '{{ variables.repo_type }}'
    revision: '{{ variables.revision }}'
    token: '{{ secrets.token }}'
```

### User Workflow

1. **Navigate to File Source Instances**
   - User Preferences → Manage File Sources

2. **Select Hugging Face Template**
   - Click "Create" → Choose "Hugging Face Hub"

3. **Configure Repository**
   - Enter repository ID (e.g., "google/flan-t5-small")
   - Select repo type (model/dataset/space)
   - Optionally specify revision

4. **Add Token (if needed)**
   - For private repos, add Hugging Face token
   - Token stored securely in Vault

5. **Browse and Import**
   - Upload dialog → Choose from repository → Select Hugging Face instance
   - Browse model files, datasets, etc.
   - Import into Galaxy

## Screenshots from PR

### Repository Configuration Form
Shows:
- Repository ID field
- Repo type selector
- Revision field
- Token input (masked)

### Browsing Hugging Face Repository
Shows:
- Directory structure of model repository
- Model files (safetensors, config.json, etc.)
- Dataset files
- Navigation breadcrumbs

## Use Cases

### 1. Importing Pre-trained Models

Tool developers can:
- Download BERT, GPT, T5, etc. for inference
- Access specific model versions
- Ensure reproducibility with revision pinning

### 2. Accessing ML Datasets

Data scientists can:
- Import benchmark datasets (GLUE, SQuAD, etc.)
- Access domain-specific datasets
- Use Galaxy tools for data preprocessing

### 3. Sharing Galaxy Outputs

Researchers can:
- Train models in Galaxy
- Export to Hugging Face for sharing
- Publish with model cards and documentation

### 4. Workflow Reproducibility

Galaxy workflows can:
- Reference specific model versions
- Document exact model used in analysis
- Enable others to reproduce results

## Repository Types

### Models
- Pre-trained transformer models
- Diffusion models
- Computer vision models
- Audio/speech models

### Datasets
- Benchmark datasets (NLP, CV, etc.)
- Custom datasets
- Preprocessed data

### Spaces
- Interactive demos
- Applications built on models

## Configuration Example

### Public Model Repository
```yaml
repo_id: "google/flan-t5-small"
repo_type: "model"
revision: "main"
# No token needed
```

### Private Dataset
```yaml
repo_id: "username/private-dataset"
repo_type: "dataset"
revision: "v1.0"
token: ${user.user_vault.read_secret('preferences/huggingface/token')}
```

### Specific Commit
```yaml
repo_id: "bert-base-uncased"
repo_type: "model"
revision: "a1b2c3d4e5f6"  # Specific commit SHA
```

## Documentation Implications

### Key Concepts to Cover

1. **Hugging Face Hub Overview**: What it is, why integrate
2. **Repository Types**: Models vs datasets vs spaces
3. **Git Versioning**: Using revisions for reproducibility
4. **Access Tokens**: When needed, how to create
5. **Browsing vs Downloading**: Understanding file structures

### User Guide

**Setting Up Hugging Face File Source:**
1. Create Hugging Face account (if accessing private repos)
2. Generate access token
3. Create file source instance in Galaxy
4. Browse and import files

**Common Workflows:**
- Importing pre-trained model for Galaxy tool
- Accessing benchmark dataset
- Exporting Galaxy-trained model

### Admin Guide

**Installation:**
```bash
# Add to file_source_templates.yml
- include: ./lib/galaxy/files/templates/examples/production_huggingface.yml
```

**Requirements:**
- fsspec with Hugging Face backend
- Network access to huggingface.co
- Optional: Vault for token storage

### Tool Developer Guide

**Using Hugging Face Models in Tools:**
- Referencing models via file sources
- Version pinning for reproducibility
- Handling model files in tools

## Security Considerations

**Token Storage:**
- Tokens stored in Vault
- Never exposed in logs or UI
- User-owned, not shared

**Access Control:**
- Respects Hugging Face permissions
- Private repos require valid token
- Galaxy doesn't cache credentials

## Performance Considerations

**Large Files:**
- Some models are multi-GB
- Consider Galaxy storage quotas
- Lazy loading where possible

**Caching:**
- Hugging Face Hub has CDN
- Galaxy can cache imported files
- Trade-off: space vs speed

## Testing

**Manual Testing Instructions from PR:**
1. Add template to `config/file_source_templates.yml`
2. Start Galaxy server
3. Navigate to file_source_instances/index
4. Select "Hugging Face Hub" template
5. Configure repository and create instance
6. Upload → Choose from repository → Select instance
7. Browse repository

**Test Scenarios:**
- Public model repository
- Private repository with token
- Dataset repository
- Specific revision/tag/commit

## Future Directions

**Potential Enhancements:**
- Write support (upload Galaxy outputs to HF)
- Model card generation from Galaxy metadata
- Integration with Galaxy ML tools
- Hugging Face Spaces for Galaxy visualizations

## Technical Details

**Diff size:** 415 lines (compact due to fsspec base)
**Dependencies:** fsspec with huggingface backend
**Testing:** Manual testing instructions provided
**Configuration:** User-defined template included
**Plugin Type:** Built on FsspecFilesSource
