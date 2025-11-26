"""Pydantic models for metadata.yaml and content.yaml validation."""

from enum import Enum
from pathlib import Path
from typing import Annotated, Literal, Optional

from pydantic import (
    BaseModel,
    Field,
    field_validator,
    model_validator,
)


# ============================================================================
# Metadata Models
# ============================================================================

class TrainingMetadata(BaseModel):
    """Training slide metadata.

    Defines the learning objectives and structure for training materials.
    """
    tutorial_number: Annotated[int, Field(description="Tutorial number in training-material (e.g., 1 for architecture-1-ecosystem)", ge=1, le=99)]
    subtitle: Annotated[str, Field(description="Subtitle for title slide (e.g., 'The architecture of the ecosystem.')")]
    questions: Annotated[list[str], Field(min_length=1, description="Learning questions this topic addresses")]
    objectives: Annotated[list[str], Field(min_length=1, description="Learning objectives for trainees")]
    key_points: Annotated[list[str], Field(min_length=1, description="Key takeaways from the training")]
    time_estimation: Annotated[str, Field(description="Estimated time to complete (e.g., '30m', '1h')")]
    prerequisites: Annotated[list[str], Field(default_factory=list, description="Topic IDs that should be learned first")]
    previous_to: Annotated[Optional[str], Field(None, description="Topic ID that precedes this topic in sequence")]
    continues_to: Annotated[Optional[str], Field(None, description="Topic ID that follows this topic in sequence")]


class SphinxMetadata(BaseModel):
    """Sphinx documentation metadata.

    Controls how the topic appears in Galaxy's Sphinx documentation.
    """
    section: Annotated[str, Field(description="Top-level section (e.g., 'Architecture')")]
    subsection: Annotated[Optional[str], Field(None, description="Subsection within the section")]



class TopicMetadata(BaseModel):
    """Complete topic metadata from metadata.yaml.

    This is the source of truth for topic configuration across all output formats.
    """

    # Required fields
    topic_id: Annotated[str, Field(description="Unique identifier (lowercase, hyphenated)")]
    title: Annotated[str, Field(description="Human-readable title")]

    # Output format metadata
    training: Annotated[TrainingMetadata, Field(description="Training slide configuration")]
    sphinx: Annotated[Optional[SphinxMetadata], Field(None, description="Sphinx documentation configuration")]

    # Contributors
    contributors: Annotated[
        list[str],
        Field(min_length=1, description="List of contributors (e.g., GitHub usernames)")
    ]

    # Cross-references
    related_topics: Annotated[
        list[str],
        Field(default_factory=list, description="Related topic IDs for cross-referencing")
    ]
    related_code_paths: Annotated[
        list[str],
        Field(default_factory=list, description="Galaxy code paths relevant to this topic")
    ]

    @field_validator('topic_id')
    @classmethod
    def validate_topic_id(cls, v: str) -> str:
        """Validate topic_id format (lowercase, hyphenated)."""
        if not v:
            raise ValueError("topic_id cannot be empty")
        if not v.islower():
            raise ValueError("topic_id must be lowercase")
        if ' ' in v:
            raise ValueError("topic_id cannot contain spaces (use hyphens)")
        if v.startswith('-') or v.endswith('-'):
            raise ValueError("topic_id cannot start or end with hyphen")
        if '--' in v:
            raise ValueError("topic_id cannot contain consecutive hyphens")
        return v

    @field_validator('related_topics')
    @classmethod
    def validate_no_self_reference(cls, v: list[str], info) -> list[str]:
        """Ensure topic doesn't reference itself."""
        topic_id = info.data.get('topic_id')
        if topic_id and topic_id in v:
            raise ValueError(f"Topic cannot reference itself in related_topics")
        return v

    @field_validator('related_code_paths')
    @classmethod
    def validate_code_paths(cls, v: list[str]) -> list[str]:
        """Validate code path format."""
        for path in v:
            if path.startswith('/'):
                raise ValueError(f"Code path should be relative: {path}")
        return v


# ============================================================================
# Content Models
# ============================================================================

class ContentBlockType(str, Enum):
    """Type of content block."""
    PROSE = "prose"
    SLIDE = "slide"


class DocRenderConfig(BaseModel):
    """Configuration for rendering in documentation (Sphinx).

    Controls how content appears in continuous documentation format.
    """
    render: Annotated[bool, Field(True, description="Whether to include in documentation")]
    heading_level: Annotated[
        Optional[int],
        Field(None, ge=1, le=6, description="Heading level for this section (1-6)")
    ]


class SlideRenderConfig(BaseModel):
    """Configuration for rendering in training slides.

    Controls how content appears in slide presentation format.
    """
    render: Annotated[bool, Field(True, description="Whether to include in slides")]
    class_: Annotated[
        Optional[str],
        Field(None, description="CSS classes to apply to slides (e.g., 'center', 'reduce90', 'enlarge150')")
    ]
    layout_name: Annotated[
        Optional[str],
        Field(None, description="Named layout to reference (e.g., 'left-aligned')")
    ]


class ContentBlock(BaseModel):
    """Single content block in content.yaml.

    Represents one unit of content (prose paragraph or slide) with rendering
    configuration for different output formats.
    """

    type: Annotated[ContentBlockType, Field(description="Type of content block")]
    id: Annotated[str, Field(description="Unique identifier for this block")]

    # Content sources (mutually exclusive - validated below)
    content: Annotated[
        Optional[str],
        Field(None, description="Inline content (for short blocks)")
    ]
    file: Annotated[
        Optional[str],
        Field(None, description="Single fragment file path (relative to topic dir)")
    ]
    fragments: Annotated[
        Optional[list[str]],
        Field(None, description="Multiple fragment file paths to combine")
    ]

    # Slide-specific fields
    heading: Annotated[
        Optional[str],
        Field(None, description="Heading text (optional for slides)")
    ]
    separator: Annotated[
        str,
        Field("\n\n", description="Separator when combining fragments")
    ]

    # Convenience field: CSS classes for slides (shorthand for slides.class_)
    class_: Annotated[
        Optional[str],
        Field(None, alias='class', description="CSS classes for slides (shorthand for slides.class_)")
    ]

    # Rendering configuration with smart defaults
    doc: Annotated[
        DocRenderConfig,
        Field(default_factory=DocRenderConfig, description="Documentation rendering config")
    ]
    slides: Annotated[
        SlideRenderConfig,
        Field(default_factory=SlideRenderConfig, description="Slide rendering config")
    ]

    @model_validator(mode='after')
    def apply_smart_defaults(self):
        """Apply smart defaults based on content type."""
        # Propagate convenience field 'class_' to slides.class_
        if self.class_ and not self.slides.class_:
            self.slides.class_ = self.class_

        if self.type == ContentBlockType.PROSE:
            # Prose: render in docs by default, NOT in slides
            if self.doc.render is True:  # Using default
                self.doc.render = True
            if self.slides.render is True:  # Using default
                self.slides.render = False

        elif self.type == ContentBlockType.SLIDE:
            # Slides: render in BOTH docs and slides by default
            if self.doc.render is True:  # Using default
                self.doc.render = True
            if self.slides.render is True:  # Using default
                self.slides.render = True

        return self

    @model_validator(mode='after')
    def validate_content_source(self):
        """Ensure exactly one content source is specified, or allow empty for heading-only slides."""
        # Check for non-empty sources (None, empty string, and empty lists don't count)
        sources = [
            self.content if (self.content is not None and self.content.strip()) else None,
            self.file,
            self.fragments if self.fragments else None,
        ]
        non_none = [s for s in sources if s is not None]

        if len(non_none) == 0:
            # Allow empty content only for slides with headings (section dividers)
            if self.type == ContentBlockType.SLIDE and self.heading:
                return self
            raise ValueError(
                f"Block '{self.id}': must specify one of 'content', 'file', or 'fragments'"
            )
        if len(non_none) > 1:
            raise ValueError(
                f"Block '{self.id}': cannot specify multiple content sources"
            )

        return self

    @model_validator(mode='after')
    def validate_slide_heading(self):
        """Slides may optionally have headings (empty string is allowed)."""
        # No validation needed - heading is optional for all slides
        return self

    @field_validator('id')
    @classmethod
    def validate_id_format(cls, v: str) -> str:
        """Validate block ID format (lowercase, hyphenated)."""
        if not v:
            raise ValueError("Block id cannot be empty")
        if not v.islower():
            raise ValueError(f"Block id must be lowercase: {v}")
        if ' ' in v:
            raise ValueError(f"Block id cannot contain spaces: {v}")
        return v

    @field_validator('file')
    @classmethod
    def validate_file_path(cls, v: Optional[str]) -> Optional[str]:
        """Validate file path format."""
        if v and v.startswith('/'):
            raise ValueError(f"File path should be relative: {v}")
        return v

    @field_validator('fragments')
    @classmethod
    def validate_fragments_paths(cls, v: Optional[list[str]]) -> Optional[list[str]]:
        """Validate fragment paths format."""
        if v:
            if len(v) == 0:
                raise ValueError("fragments list cannot be empty (use file or content instead)")
            for path in v:
                if path.startswith('/'):
                    raise ValueError(f"Fragment path should be relative: {path}")
        return v

    def resolve_content(self, base_dir: Path) -> str:
        """Resolve content from file/fragments references.

        Args:
            base_dir: Base directory for resolving relative paths (topic directory)

        Returns:
            Resolved content string

        Raises:
            FileNotFoundError: If referenced file doesn't exist
        """
        if self.content is not None:
            return self.content

        elif self.file:
            file_path = base_dir / self.file
            if not file_path.exists():
                raise FileNotFoundError(
                    f"Block '{self.id}': fragment not found: {self.file}"
                )
            return file_path.read_text()

        elif self.fragments:
            parts = []
            for frag in self.fragments:
                frag_path = base_dir / frag
                if not frag_path.exists():
                    raise FileNotFoundError(
                        f"Block '{self.id}': fragment not found: {frag}"
                    )
                parts.append(frag_path.read_text())
            return self.separator.join(parts)

        raise ValueError(f"Block '{self.id}': no content source specified")


class TopicContent(BaseModel):
    """Complete content sequence from content.yaml.

    Ordered list of content blocks that define the topic's narrative flow.
    """
    root: Annotated[
        list[ContentBlock],
        Field(min_length=1, description="Ordered list of content blocks")
    ]

    def __iter__(self):
        return iter(self.root)

    def __getitem__(self, item):
        return self.root[item]

    def __len__(self):
        return len(self.root)

    @field_validator('root')
    @classmethod
    def validate_unique_ids(cls, v: list[ContentBlock]) -> list[ContentBlock]:
        """Ensure all block IDs are unique within the topic."""
        ids = [block.id for block in v]
        duplicates = [id for id in ids if ids.count(id) > 1]
        if duplicates:
            raise ValueError(f"Duplicate block IDs found: {set(duplicates)}")
        return v

    @field_validator('root')
    @classmethod
    def validate_at_least_one_slide(cls, v: list[ContentBlock]) -> list[ContentBlock]:
        """Ensure there's at least one slide for training materials."""
        has_slide = any(block.type == ContentBlockType.SLIDE for block in v)
        if not has_slide:
            raise ValueError("Content must include at least one slide block")
        return v


# ============================================================================
# Loader Functions
# ============================================================================

def load_metadata(topic_name: str, topics_dir: Path = Path("topics")) -> TopicMetadata:
    """Load and validate metadata.yaml for a topic.

    Args:
        topic_name: Topic identifier (directory name)
        topics_dir: Base directory containing all topics

    Returns:
        Validated TopicMetadata instance

    Raises:
        FileNotFoundError: If metadata.yaml doesn't exist
        ValidationError: If metadata is invalid
    """
    topic_dir = topics_dir / topic_name
    metadata_file = topic_dir / "metadata.yaml"

    if not metadata_file.exists():
        raise FileNotFoundError(
            f"metadata.yaml not found for topic: {topic_name}"
        )

    import yaml
    with open(metadata_file) as f:
        data = yaml.safe_load(f)

    return TopicMetadata(**data)


def load_content(topic_name: str, topics_dir: Path = Path("topics")) -> TopicContent:
    """Load and validate content.yaml for a topic.

    Args:
        topic_name: Topic identifier (directory name)
        topics_dir: Base directory containing all topics

    Returns:
        Validated TopicContent instance

    Raises:
        FileNotFoundError: If content.yaml doesn't exist
        ValidationError: If content structure is invalid
    """
    topic_dir = topics_dir / topic_name
    content_file = topic_dir / "content.yaml"

    if not content_file.exists():
        raise FileNotFoundError(
            f"content.yaml not found for topic: {topic_name}"
        )

    import yaml
    with open(content_file) as f:
        data = yaml.safe_load(f)

    return TopicContent(root=data)


def validate_topic_structure(
    topic_name: str,
    topics_dir: Path = Path("topics")
) -> tuple[TopicMetadata, TopicContent]:
    """Load and validate both metadata and content for a topic.

    This also cross-validates between metadata and content (e.g., checking
    that referenced images exist, related topics are valid, etc.)

    Args:
        topic_name: Topic identifier (directory name)
        topics_dir: Base directory containing all topics

    Returns:
        Tuple of (metadata, content) if validation succeeds

    Raises:
        FileNotFoundError: If files don't exist
        ValidationError: If validation fails
        ValueError: If cross-validation fails
    """
    topic_dir = topics_dir / topic_name

    # Load both files
    metadata = load_metadata(topic_name, topics_dir)
    content = load_content(topic_name, topics_dir)

    # Verify metadata.topic_id matches directory name
    if metadata.topic_id != topic_name:
        raise ValueError(
            f"Topic ID mismatch: directory is '{topic_name}' but "
            f"metadata.yaml has topic_id '{metadata.topic_id}'"
        )

    # Verify all content blocks can resolve their content
    for block in content:
        try:
            block.resolve_content(topic_dir)
        except FileNotFoundError as e:
            raise FileNotFoundError(f"Content validation failed: {e}")

    # Verify related topics exist
    for related_id in metadata.related_topics:
        related_dir = topics_dir / related_id
        if not related_dir.exists():
            raise ValueError(f"Related topic not found: {related_id}")

    return metadata, content
