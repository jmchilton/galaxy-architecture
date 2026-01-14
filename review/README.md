# Galaxy Architecture Review Plugin

Build infrastructure for the `claude-galaxy-plugins` marketplace.

See the [root README](../README.md#agentic-code-review) for:
- The feedback loop between documentation, commands, and reviews
- Overview of command sources and generation
- Philosophy behind agentic code review

## Quick Reference

```bash
# Build marketplace
make

# Clean
make clean

# Sync generated commands from topics
make sync-generated

# Build legacy structure (backwards compatibility)
make legacy
```

## Structure

```
review/
├── static_commands/        # Hand-written slash commands
├── generated_commands/     # Copied from generated_agentic_operations/
├── generated_commands.yaml # Mapping: source → target filename
├── galaxy-plugins/         # Output marketplace
│   ├── .claude-plugin/
│   │   └── marketplace.json
│   ├── plugins/
│   │   └── gx-arch-review/
│   │       ├── commands/   # Final commands (static + generated)
│   │       └── README.md
│   └── README.md
├── gx-arch-review/         # Legacy output (deprecated)
└── Makefile
```

## Workflow

1. **Static commands**: Edit in `static_commands/`
2. **Generated commands**: Run `/generate-agentic-op <topic> <operation>`, add mapping to `generated_commands.yaml`
3. **Build**: `make` syncs generated commands and builds `galaxy-plugins/`
4. **Publish**: Commit and push `galaxy-plugins/`

## Command Format

```markdown
---
description: Brief description for command listing
---

# Command Title

Review criteria and patterns...
```

## Plugin Usage

See [galaxy-plugins/plugins/gx-arch-review/README.md](galaxy-plugins/plugins/gx-arch-review/README.md) for installation and command reference.
