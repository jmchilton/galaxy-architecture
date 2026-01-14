# New marketplace structure
MARKETPLACE := galaxy-plugins
PLUGIN_DIR := $(MARKETPLACE)/plugins/gx-arch-review
PLUGIN_COMMANDS_DIR := $(PLUGIN_DIR)/commands

# Legacy structure (preserved for now)
SUBREPO := gx-arch-review
COMMANDS_DIR := $(SUBREPO)/commands

.PHONY: all clean sync-generated legacy

all: sync-generated $(PLUGIN_COMMANDS_DIR)
	@echo "Copying static commands to marketplace..."
	cp -r static_commands/* $(PLUGIN_COMMANDS_DIR)/
	@if [ -n "$$(ls -A generated_commands 2>/dev/null)" ]; then \
		echo "Copying generated commands to marketplace..."; \
		cp -r generated_commands/* $(PLUGIN_COMMANDS_DIR)/; \
	fi
	@echo "Done. Commands copied to $(PLUGIN_COMMANDS_DIR)/"

# Build legacy structure (for backwards compatibility)
legacy: sync-generated $(COMMANDS_DIR)
	@echo "Copying static commands to legacy location..."
	cp -r static_commands/* $(COMMANDS_DIR)/
	@if [ -n "$$(ls -A generated_commands 2>/dev/null)" ]; then \
		echo "Copying generated commands to legacy location..."; \
		cp -r generated_commands/* $(COMMANDS_DIR)/; \
	fi
	@echo "Done. Commands copied to $(COMMANDS_DIR)/"

sync-generated:
	@echo "Syncing generated agentic operations..."
	python sync_generated.py

$(PLUGIN_COMMANDS_DIR):
	mkdir -p $(PLUGIN_COMMANDS_DIR)

$(COMMANDS_DIR):
	mkdir -p $(COMMANDS_DIR)

clean:
	rm -rf $(PLUGIN_COMMANDS_DIR)/*
	rm -rf $(COMMANDS_DIR)/*
	rm -rf generated_commands/*
