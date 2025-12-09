# Quick Reference: v1.0 vs v2.0

## Property Name Changes - Quick Lookup

### Section Names
| v1.0 | v2.0 |
|------|------|
| `"General Section"` | `"generalSection"` |
| `"Method Specific"` | `"methodSpecific"` |
| `"Customer Specific"` | `"customerSpecific"` |
| `"Tool Specific"` | `"toolSpecific"` |
| `"Data Evaluation"` | `"dataEvaluation"` |
| `"History"` | `"history"` |

### General Section Properties
| v1.0 | v2.0 |
|------|------|
| `"File Path"` | `"filePath"` |
| `"File Name"` | `"fileName"` |
| `"File Format"` | `"fileFormat"` |
| `"File Size"` | `"fileSize"` |
| `"Logfile Path"` | `"logfilePath"` |
| `"Previous Header File"` | `"previousHeaderFile"` |
| `"Header Type"` | `"headerType"` |
| `"Version"` | `"version"` |
| `"Time Stamp"` | `"timeStamp"` |
| `"Manufacturer"` | `"manufacturer"` |
| `"Tool Name"` | `"toolName"` |
| `"Serial Number"` | `"serialNumber"` |
| `"Method"` | `"method"` |
| `"Image Width"` | `"imageWidth"` |
| `"Image Height"` | `"imageHeight"` |
| `"Pixel Width"` | `"pixelWidth"` |
| `"Pixel Height"` | `"pixelHeight"` |
| `"Bit Depth"` | `"bitDepth"` |
| `"Compressed Bits/Pixel"` | `"compressedBitsPerPixel"` |
| `"Color Mode"` | `"colorMode"` |
| `"Customer"` | `"customer"` |
| `"Sample Holder"` | `"sampleHolder"` |
| `"Tool Calibrated"` | `"toolCalibrated"` |
| `"Coordinates Sub Section"` | `"coordinates"` |
| `"Alignment Marks Sub Section"` | `"alignmentMarks"` |

### Method Section Properties
| v1.0 | v2.0 |
|------|------|
| `"Scanning Electron Microscopy"` | `"scanningElectronMicroscopy"` |
| `"Focused Ion Beam"` | `"focusedIonBeam"` |
| `"Optical Microscopy"` | `"opticalMicroscopy"` |
| `"Accelerating Voltage"` | `"acceleratingVoltage"` |
| `"Decelerating Voltage"` | `"deceleratingVoltage"` |
| `"Working Distance"` | `"workingDistance"` |
| `"Magnification"` | `"magnification"` |
| `"Signal Mixing"` | `"signalMixing"` |
| `"Signal Type(s)"` | `"signalTypes"` |
| `"Detector(s)"` | `"detectors"` |
| `"Signal Proportion"` | `"signalProportion"` |
| `"Aperture Size"` | `"apertureSize"` |
| `"Aperture Alignment X Y"` | `"apertureAlignment"` |
| `"Stigmator Alignment X Y"` | `"stigmatorAlignment"` |
| `"Brightness"` | `"brightness"` |
| `"Contrast"` | `"contrast"` |
| `"Emission Current"` | `"emissionCurrent"` |
| `"Probe Current"` | `"probeCurrent"` |
| `"High Current Mode"` | `"highCurrentMode"` |
| `"Tilt Correction Mode"` | `"tiltCorrectionMode"` |
| `"Corrected Tilt Angle"` | `"correctedTiltAngle"` |
| `"Beam Shift X"` / `"Beam Shift Y"` | `"beamShift"` (array) |
| `"Scan Rotation Mode"` | `"scanRotationMode"` |
| `"Scan Rotation"` | `"scanRotation"` |
| `"FIB-SEM Intersection Point"` | `"fibSemIntersectionPoint"` |
| `"FIB Tilt Angle"` | `"fibTiltAngle"` |
| `"Objective Lens Magnification"` | `"objectiveMagnification"` |
| `"Optical Zoom"` | `"opticalZoom"` |
| `"Digital Zoom"` | `"digitalZoom"` |
| `"Contrast Method"` | `"contrastMethod"` |
| `"HDR Mode"` | `"hdrMode"` |
| `"Exposure Time"` | `"exposureTime"` |

### Data Evaluation Properties
| v1.0 | v2.0 |
|------|------|
| `"Image Label"` | `"imageLabel"` |
| `"Image ID"` | `"imageId"` |
| `"POI"` | `"pointsOfInterest"` |
| `"ROI (Region of Interest)"` | `"regionsOfInterest"` |
| `"ROI-Polygon"` | `"polygons"` |
| `"ROI-Polyline"` | `"polylines"` |
| `"Name"` | `"name"` |
| `"Label"` | `"label"` |
| `"ID"` | `"id"` |
| `"Coordinates"` | `"coordinates"` |
| `"Area"` | `"area"` |
| `"FillColor"` | `"fillColor"` |
| `"StrokeColor"` | `"strokeColor"` |
| `"StrokeWidth"` | `"strokeWidth"` |

### Coordinates Properties
| v1.0 | v2.0 |
|------|------|
| `"Stage Coordinate System Orientation"` | `"stageCoordinateSystem"` |
| `"global or local frame movement"` | `"globalOrLocalFrame"` |
| `"Relative Orientation to screens coordinate frame"` | `"relativeOrientation"` |
| `"Stage Coordinates X Y Z"` | `"stagePosition"` |
| `"Stage Rotation Rx"` | `"stageRotationRx"` |
| `"Stage Rotation Ry"` | `"stageRotationRy"` |
| `"Stage Rotation Rz"` | `"stageRotationRz"` |

### Alignment Marks Properties
| v1.0 | v2.0 |
|------|------|
| `"Offset(x y z)"` | `"offset"` |
| `"Position of the Fiducials"` | `"fiducialPositions"` |
| `"Mark1"` | `"mark1"` |
| `"Mark2"` | `"mark2"` |
| `"Mark3"` | `"mark3"` |
| `"Type of Fiducials"` | `"fiducialType"` |
| `"Fiducial Size"` | `"fiducialSize"` |

### Value Properties (within objects)
| v1.0 | v2.0 |
|------|------|
| `"Value"` | `"value"` |
| `"Unit"` | `"unit"` |

## Required Fields Comparison

### General Section
| v1.0 | v2.0 | Change |
|------|------|--------|
| 26 fields required | 5 fields required | **↓ 80%** |

**v2.0 Required:** `fileName`, `timeStamp`, `manufacturer`, `toolName`, `method`

### SEM Method
| v1.0 | v2.0 | Change |
|------|------|--------|
| 21 fields required | 3 fields required | **↓ 86%** |

**v2.0 Required:** `acceleratingVoltage`, `workingDistance`, `signalTypes`

### FIB Method
| v1.0 | v2.0 | Change |
|------|------|--------|
| 22 fields required | 3 fields required | **↓ 86%** |

**v2.0 Required:** `acceleratingVoltage`, `workingDistance`, `signalTypes`

### Optical Method
| v1.0 | v2.0 | Change |
|------|------|--------|
| 6 fields required | 1 field required | **↓ 83%** |

**v2.0 Required:** `objectiveMagnification`

## File Names

| v1.0 | v2.0 |
|------|------|
| `General Section.json` | `generalSection.json` |
| `Method Specific.json` | `methodSpecific.json` |
| `Customer Section.json` | `customerSection.json` |
| `Tool Specific.json` | `toolSpecific.json` |
| `Data Evaluation.json` | `dataEvaluation.json` |
| `History.json` | `historySection.json` |

## Enum Value Changes

| v1.0 | v2.0 |
|------|------|
| `"right handed"` | `"right-handed"` |
| `"left handed"` | `"left-handed"` |

## Schema Format Changes

### v1.0 Structure
```json
{
  "General Section": {
    "type": "object",
    "properties": { ... }
  }
}
```

### v2.0 Structure
```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "...",
  "type": "object",
  "properties": {
    "generalSection": {
      "type": "object",
      "required": [...],
      "properties": { ... }
    }
  }
}
```

## Quick Migration Script Pattern

```python
# Python example for converting v1.0 to v2.0 property names
v1_to_v2_mapping = {
    "General Section": "generalSection",
    "File Name": "fileName",
    "Time Stamp": "timeStamp",
    "Image Width": "imageWidth",
    # ... add all mappings from table above
}

def convert_metadata(v1_data):
    v2_data = {}
    for old_key, value in v1_data.items():
        new_key = v1_to_v2_mapping.get(old_key, old_key)
        if isinstance(value, dict):
            v2_data[new_key] = convert_metadata(value)
        else:
            v2_data[new_key] = value
    return v2_data
```

## Quick Validation

```bash
# Validate a JSON file against v2.0 schema
ajv validate -s schema/generalSection.json -d your_metadata.json
```

---

**Note:** All v1.0 schema files are preserved in the repository for reference and backward compatibility. Use v2.0 files (camelCase names without spaces) for new implementations.
