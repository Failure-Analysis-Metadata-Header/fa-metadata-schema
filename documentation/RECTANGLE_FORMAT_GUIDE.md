# ROI-Rectangle Format Guide

## Overview

The ROI-Rectangle type provides a guaranteed rectangular shape representation for bounding boxes, suitable for ML annotation workflows and integration with popular annotation formats like COCO and YOLO.

## Format Specification

### v1.1 (Production)

```json
{
  "ROI (Region of Interest)": {
    "ROI-Rectangle": [
      {
        "Name": "Defect Region 1",
        "Label": "Delamination",
        "ID": "rect_001",
        "Center Coordinates": {
          "Value": [2500.0, 3000.0],
          "Unit": "µm"
        },
        "Width": {
          "Value": 500.0,
          "Unit": "µm"
        },
        "Height": {
          "Value": 300.0,
          "Unit": "µm"
        },
        "Rotation Angle": {
          "Value": 15.0,
          "Unit": "deg"
        },
        "Area": {
          "Value": 150000.0,
          "Unit": "µm²"
        },
        "FillColor": [1.0, 0.0, 0.0, 0.3],
        "StrokeColor": [1.0, 0.0, 0.0],
        "StrokeWidth": {
          "Value": 2,
          "Unit": "px"
        }
      }
    ]
  }
}
```

### v2-draft (Experimental)

```json
{
  "regionsOfInterest": {
    "rectangles": [
      {
        "name": "Defect Region 1",
        "label": "Delamination",
        "id": "rect_001",
        "centerCoordinates": {
          "value": [2500.0, 3000.0],
          "unit": "µm"
        },
        "width": {
          "value": 500.0,
          "unit": "µm"
        },
        "height": {
          "value": 300.0,
          "unit": "µm"
        },
        "rotationAngle": {
          "value": 15.0,
          "unit": "deg"
        },
        "area": {
          "value": 150000.0,
          "unit": "µm²"
        },
        "fillColor": [1.0, 0.0, 0.0, 0.3],
        "strokeColor": [1.0, 0.0, 0.0],
        "strokeWidth": {
          "value": 2,
          "unit": "px"
        }
      }
    ]
  }
}
```

## Coordinate System

- **Center Coordinates**: `[centerX, centerY]` - The center point of the rectangle
- **Width**: Measured along the rectangle's local x-axis (before rotation)
- **Height**: Measured along the rectangle's local y-axis (before rotation)
- **Rotation Angle**: (Optional) Counter-clockwise rotation from positive x-axis
  - Default: 0° (axis-aligned rectangle)
  - Units: "deg" (degrees) or "rad" (radians)

## Required vs. Optional Fields

### v1.1 Required Fields
- `Name`, `Label`, `ID`
- `Center Coordinates`, `Width`, `Height`
- `Area`, `FillColor`, `StrokeColor`, `StrokeWidth`

### v1.1 Optional Fields
- `Rotation Angle` (defaults to 0° if omitted)

### v2-draft Required Fields
- `name`, `centerCoordinates`, `width`, `height`

### v2-draft Optional Fields
- `label`, `id`, `rotationAngle`, `area`, `fillColor`, `strokeColor`, `strokeWidth`

## Format Conversions

### Converting to COCO Format

COCO uses `[x, y, width, height]` where `(x, y)` is the **top-left corner** of an axis-aligned bounding box.

**For axis-aligned rectangles (rotation = 0°):**

```python
def fa_to_coco(center_x, center_y, width, height):
    """Convert FA metadata rectangle to COCO bbox format."""
    x = center_x - width / 2
    y = center_y - height / 2
    return [x, y, width, height]

# Example:
# Center: [2500, 3000], Width: 500, Height: 300
# COCO: [2250, 2850, 500, 300]
```

**For rotated rectangles:**

COCO also supports segmentation format with polygon points:

```python
import math

def fa_rotated_to_coco_segmentation(center_x, center_y, width, height, angle_deg):
    """Convert rotated FA rectangle to COCO segmentation format."""
    angle_rad = math.radians(angle_deg)
    cos_a = math.cos(angle_rad)
    sin_a = math.sin(angle_rad)
    
    # Half dimensions
    hw = width / 2
    hh = height / 2
    
    # Four corners in local coordinates
    corners_local = [
        (-hw, -hh),  # Top-left
        (hw, -hh),   # Top-right
        (hw, hh),    # Bottom-right
        (-hw, hh)    # Bottom-left
    ]
    
    # Rotate and translate to global coordinates
    segmentation = []
    for lx, ly in corners_local:
        gx = center_x + lx * cos_a - ly * sin_a
        gy = center_y + lx * sin_a + ly * cos_a
        segmentation.extend([gx, gy])
    
    return segmentation

# Example:
# Center: [2500, 3000], Width: 500, Height: 300, Rotation: 15°
# COCO segmentation: [x1, y1, x2, y2, x3, y3, x4, y4]
```

### Converting to YOLO Format

YOLO uses normalized `[center_x, center_y, width, height]` where all values are normalized by image dimensions (0.0 to 1.0).

**For axis-aligned rectangles:**

```python
def fa_to_yolo(center_x, center_y, width, height, image_width, image_height):
    """Convert FA metadata rectangle to YOLO format (normalized)."""
    norm_cx = center_x / image_width
    norm_cy = center_y / image_height
    norm_w = width / image_width
    norm_h = height / image_height
    return [norm_cx, norm_cy, norm_w, norm_h]

# Example:
# Center: [2500, 3000], Width: 500, Height: 300
# Image: 5000 x 6000 pixels
# YOLO: [0.5, 0.5, 0.1, 0.05]
```

**For rotated rectangles:**

YOLO v8+ supports oriented bounding boxes (OBB) with rotation:

```python
def fa_to_yolo_obb(center_x, center_y, width, height, angle_deg, image_width, image_height):
    """Convert rotated FA rectangle to YOLO OBB format."""
    norm_cx = center_x / image_width
    norm_cy = center_y / image_height
    norm_w = width / image_width
    norm_h = height / image_height
    angle_rad = math.radians(angle_deg)
    
    return [norm_cx, norm_cy, norm_w, norm_h, angle_rad]

# Example:
# Center: [2500, 3000], Width: 500, Height: 300, Rotation: 15°
# Image: 5000 x 6000 pixels
# YOLO OBB: [0.5, 0.5, 0.1, 0.05, 0.2618]  # 15° = 0.2618 rad
```

### Converting FROM COCO to FA

```python
def coco_to_fa(x, y, width, height, unit="px"):
    """Convert COCO bbox to FA metadata rectangle format."""
    center_x = x + width / 2
    center_y = y + height / 2
    
    return {
        "Center Coordinates": {
            "Value": [center_x, center_y],
            "Unit": unit
        },
        "Width": {"Value": width, "Unit": unit},
        "Height": {"Value": height, "Unit": unit},
        "Area": {"Value": width * height, "Unit": f"{unit}²"}
    }
```

### Converting FROM YOLO to FA

```python
def yolo_to_fa(norm_cx, norm_cy, norm_w, norm_h, image_width, image_height, unit="px"):
    """Convert YOLO normalized bbox to FA metadata rectangle format."""
    center_x = norm_cx * image_width
    center_y = norm_cy * image_height
    width = norm_w * image_width
    height = norm_h * image_height
    
    return {
        "Center Coordinates": {
            "Value": [center_x, center_y],
            "Unit": unit
        },
        "Width": {"Value": width, "Unit": unit},
        "Height": {"Value": height, "Unit": unit},
        "Area": {"Value": width * height, "Unit": f"{unit}²"}
    }
```

## Use Cases

### 1. Axis-Aligned Bounding Boxes
For simple rectangular regions without rotation:
- Set `Rotation Angle` to 0° or omit it (v2-draft)
- Direct conversion to/from COCO and YOLO formats

### 2. Oriented Bounding Boxes
For rotated rectangular regions:
- Specify `Rotation Angle` in degrees or radians
- Use COCO segmentation or YOLO v8+ OBB format
- Useful for rotated chips, angled defects

### 3. ML Annotation Workflows
- Export FA metadata to COCO/YOLO for training
- Import ML predictions back to FA metadata format
- Maintain traceability with unique IDs

### 4. Comparison with Polygons

**Use ROI-Rectangle when:**
- You need guaranteed rectangular shapes
- Converting to/from ML annotation formats
- Defining bounding boxes around features
- Rotation support is needed

**Use ROI-Polygon when:**
- Arbitrary shapes are needed
- Segmentation masks with irregular boundaries
- Tracing exact contours of defects

## Complete Example

See `schema/v1.1/examples/rectangle_example_sem.json` for a complete working example with multiple rectangles, including both axis-aligned and rotated variants.

## Validation

Both v1.1 and v2-draft schemas include proper JSON Schema validation for rectangles:
- Coordinate arrays have exactly 2 elements
- Color arrays have correct dimensions (RGB: 3, RGBA: 4)
- Units are specified for all numeric values
- Required fields are enforced (varies by version)
