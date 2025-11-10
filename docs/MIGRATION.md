# Migration Plan: Moving to Galaxy Repository

This document outlines the long-term plan to migrate this architecture documentation system into the main Galaxy repository.

## Current State

**Location**: `github.com/jmchilton/galaxy-architecture` (experimental repository)

**Status**: Proof of concept - validating approach before organizational adoption

**Goal**: Eventually move into Galaxy repository as the source of truth for architecture documentation

## Why Migrate?

1. **Co-location**: Architecture docs should live with Galaxy code
2. **Visibility**: Easier for contributors to find and update
3. **Integration**: Can reference code directly, stay in sync with changes
4. **Maintenance**: Single repository reduces overhead

## Prerequisites

Before migration can happen, we need to:

### ✅ Completed

- [x] Prove the concept works (structured content → multiple outputs)
- [x] Validate approach with at least one topic (dependency-injection)
- [x] Build working slide generator
- [x] Create validation framework
- [x] Document the system

### ⏳ Still Needed

- [ ] Migrate multiple topics (prove repeatability)
- [ ] Get feedback from Galaxy contributors
- [ ] Demonstrate value (time saved, consistency improvements)
- [ ] Build Sphinx output generator (for Galaxy docs)
- [ ] Get organizational buy-in
- [ ] Plan integration with existing Galaxy docs structure

## Migration Strategy

### Phase 1: Preparation (Current)

**Goal**: Prove the system works and gather evidence

**Tasks**:
- Complete proof of concept with 2-3 topics
- Document time savings and quality improvements
- Build all planned output formats
- Create migration proposal

**Timeline**: Weeks 1-4

### Phase 2: Proposal

**Goal**: Present migration plan to Galaxy community

**Deliverables**:
- Migration proposal document
- Demo of system capabilities
- Comparison: before/after workflow
- Integration plan for Galaxy repo

**Decision Criteria**:
- Does it save time?
- Does it improve quality?
- Is it maintainable?
- Do contributors want it?

### Phase 3: Integration Planning

**Goal**: Plan how to integrate into Galaxy repository

**Considerations**:
- **Location**: Where in Galaxy repo? (`docs/architecture/`? `lib/galaxy/docs/architecture/`?)
- **Structure**: Keep same structure or adapt to Galaxy conventions?
- **CI/CD**: Integrate with Galaxy's CI (validation, generation)
- **Workflow**: How do contributors update architecture docs?
- **Outputs**: Where do generated slides/docs go?
- **Dependencies**: Can we use Galaxy's existing tooling?

### Phase 4: Migration

**Goal**: Move content and tooling into Galaxy

**Steps**:
1. Create directory structure in Galaxy repo
2. Copy topics and tooling
3. Set up CI integration
4. Update documentation
5. Announce to community
6. Deprecate experimental repo

**Timeline**: 1-2 weeks (depending on review process)

### Phase 5: Transition

**Goal**: Maintain both repos during transition period

**Strategy**:
- Keep experimental repo as read-only archive
- All updates go to Galaxy repo
- Redirect links to Galaxy repo
- Eventually archive experimental repo

## Integration Points

### Galaxy Repository Structure

Proposed location:
```
galaxy/
├── docs/
│   └── architecture/          # Architecture documentation source
│       ├── topics/
│       ├── outputs/
│       ├── scripts/
│       └── images/
├── lib/galaxy/
│   └── docs/                  # Generated docs (if needed)
└── .github/workflows/
    └── validate-architecture.yml
```

### CI Integration

**Validation**: Run on every PR that touches architecture docs
**Generation**: Generate outputs when docs change
**Testing**: Run test suite as part of Galaxy CI

### Workflow Integration

**Updating Docs**:
1. Edit markdown in `docs/architecture/topics/`
2. PR triggers validation
3. CI generates outputs
4. Review includes generated outputs
5. Merge updates both source and outputs

## Challenges & Solutions

### Challenge: Tooling Dependencies

**Problem**: Galaxy repo may not want additional Python dependencies

**Solution**: 
- Use existing Galaxy dependencies where possible
- Keep dependencies minimal (PyYAML, Jinja2)
- Consider vendoring if needed

### Challenge: Output Location

**Problem**: Where do generated slides/docs live?

**Solution**:
- Slides: Continue syncing to training-material repo (or move there)
- Sphinx docs: Integrate into Galaxy docs build
- Hub articles: Separate publication workflow

### Challenge: Contributor Workflow

**Problem**: Contributors may not know about new system

**Solution**:
- Clear documentation in Galaxy repo
- Examples and templates
- Validation errors guide contributors
- CI provides feedback

### Challenge: Maintenance Burden

**Problem**: More tooling = more maintenance

**Solution**:
- Keep tooling simple
- Well-documented
- Automated testing
- Clear ownership

## Success Metrics

Migration is successful if:

1. ✅ Architecture docs are easier to update
2. ✅ Multiple output formats stay in sync
3. ✅ Contributors adopt the workflow
4. ✅ Documentation quality improves
5. ✅ Time to update docs decreases

## Timeline Estimate

- **Preparation**: 2-4 weeks (current phase)
- **Proposal & Review**: 2-4 weeks
- **Integration Planning**: 1-2 weeks
- **Migration**: 1-2 weeks
- **Transition**: 2-4 weeks

**Total**: 8-16 weeks from start to full migration

## Decision Points

### When to Migrate?

**Ready when**:
- System is proven with multiple topics
- All planned output formats work
- Community feedback is positive
- Integration plan is clear

**Not ready if**:
- Still experimental/unproven
- Major issues unresolved
- No clear integration path
- Community resistance

### When to Delay?

- Galaxy repo structure changes pending
- Major refactoring in progress
- Resource constraints
- Better alternatives emerge

## Alternative: Keep Separate

If migration doesn't happen, we can:

- Keep as separate repository
- Sync outputs to Galaxy/training-material
- Use for architecture docs only
- Maintain independently

**Pros**: Freedom to experiment, no organizational overhead

**Cons**: Not co-located with code, less visibility, duplicate maintenance

## Questions to Resolve

1. Where exactly in Galaxy repo should this live?
2. How do we handle training-material integration?
3. Who maintains the tooling?
4. What's the review process for architecture docs?
5. How do we handle breaking changes to the system?

## Next Steps

1. Complete proof of concept (Phase 1)
2. Gather feedback and metrics
3. Write formal migration proposal
4. Present to Galaxy community
5. Iterate based on feedback
6. Execute migration plan

---

**Last Updated**: 2025-01-15  
**Status**: Planning phase - proof of concept in progress

