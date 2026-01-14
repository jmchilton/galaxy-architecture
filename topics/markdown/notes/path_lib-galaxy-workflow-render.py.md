# Code Path: lib/galaxy/workflow/render.py

## Role in Architecture

Renders Galaxy workflows as SVG visualizations for documentation and display. Converts workflow step metadata into interactive SVG diagrams showing execution flow with input/output connections.

## Core Purpose

The `WorkflowCanvas` class serves as a diagram builder that:
- Visualizes workflow steps as connected boxes
- Displays input/output ports and data connections
- Renders as SVG suitable for embedding in HTML
- Handles layout positioning and connection drawing

## Key Components

### WorkflowCanvas Class

**Initialization:**
```python
self.canvas = svgwrite.Drawing(profile="full")
self.connectors = []  # Connection lines between steps
self.boxes = []       # Step rectangles
self.text = []        # Labels and text
self.in_pos = {}      # Input port positions
self.out_pos = {}     # Output port positions
self.widths = {}      # Width of each step box
self.max_x, self.max_y, self.max_width  # Canvas dimensions
self.data = []        # Step metadata
```

Maintains separate collections for structure (connectors, boxes), rendering (text), and layout tracking (positions, dimensions).

### Key Methods

**`populate_data_for_step(step, module_name, module_data_inputs, module_data_outputs, tool_errors=None)`**
- Prepares step metadata for rendering
- Builds input connection mapping
- Stores step position, inputs, outputs, error state

**`add_text(module_data_inputs, module_data_outputs, step, module_name)`**
- Renders step name and port labels
- Maps port names to SVG coordinates
- Calculates box width based on label length
- Tracks canvas bounds

**`add_boxes(step_dict, width, name_fill)`**
- Draws main step rectangle with configurable fill color
- Draws data section with input/output ports
- Adds visual separator between inputs and outputs
- Colors: `#EBD9B2` (default), `#EBBCB2` (tool error highlight)

**`add_connection(step_dict, conn, output_dict)`**
- Draws connector line from upstream output to current input
- Adds connection endpoint circles on output ports
- Creates SVG arrow markers pointing into input ports
- Uses coordinate lookup for positioning

**`add_steps(highlight_errors=False)`**
- Orchestrates rendering all workflow steps
- Conditionally highlights steps with tool errors
- Processes input connections for each step

**`finish(for_embed=False)`**
- Assembles SVG layers: boxes, connectors, text
- Applies font styling to all text elements
- Sets SVG viewbox for responsive embedding
- Returns final `svgwrite.Drawing` object

## Design Patterns

### Separation of Concerns
- Data collection → layout calculation → SVG rendering
- Text/labels separate from geometry for styled application

### Two-Pass Rendering
1. **First pass:** `populate_data_for_step()` + `add_text()` → builds coordinate map
2. **Second pass:** `add_steps()` → draws connectors using coordinates from pass 1

### Position Tracking
Stores positions by step order_index: `in_pos[step_id][port_name] = (x, y)`
Enables flexible connection routing without recalculation.

### Resilient Connection Lookup
Gracefully handles missing expected outputs by using any available port—important for workflows with variable outputs.

## Layout System

- **MARGIN:** 5px padding/offset
- **LINE_SPACING:** 15px vertical spacing per port
- **Box dimensions:** Width varies by content; height from port count
- **Coordinates:** Uses step position dict with "left"/"top" keys
- **Canvas bounds:** Tracked as maximum extents for viewbox

## Connection Semantics

A connection represents data flow from one step's output to another step's input:

```python
input_conn_dict[conn.input_name] = {
    "id": conn.output_step.order_index,
    "output_name": conn.output_name
}
```

Rendered as directed arrow from output step → input step.

## SVG Output Features

- **Responsive embedding:** Uses viewBox + fit() for HTML embedding
- **Standalone format:** Optional DOCTYPE wrapper for standalone SVG files
- **Font stack:** Helvetica/Arial fallback for consistent rendering
- **Arrow markers:** SVG path-based arrowheads on connection lines
- **Color coding:** Tool error states highlighted visually

## Example Rendering Flow

```
1. Workflow step 1: create_input
   - Outputs: {"file": output_port_position}

2. Workflow step 2: transform
   - Inputs: {"input_file"}
   - Connection from step 1
   - Arrow from step 1 output → step 2 input

3. Workflow step 3: analyze
   - Inputs: {"data"}
   - Connection from step 2
   - Draws connection chain
```

## Constants & Configuration

```python
MARGIN = 5                    # Box padding
LINE_SPACING = 15             # Vertical port spacing
STANDALONE_SVG_TEMPLATE       # DOCTYPE wrapper
COLORS:
  - "#EBD9B2"               # Normal step (tan)
  - "#EBBCB2"               # Tool error (light red)
  - "#ffffff"               # Port backgrounds
  - "#000000"               # Borders/text
```

## Documentation Highlights

**For training:**
- Rendering with varying input/output port counts
- Tool error highlighting behavior
- Connection routing with missing outputs (fallback)
- SVG embedding vs. standalone output
- Canvas bounds calculation for layout shapes
