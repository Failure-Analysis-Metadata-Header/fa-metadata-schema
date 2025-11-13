# Schema v2.0 - Change Log & Migration Guide

**Date:** November 13, 2025  
**Version:** 2.0  
**Previous Version:** 1.0

## Executive Summary

Version 2.0 represents a major overhaul of the FA Metadata Header schema with focus on:
- **Simplicity** - Reduced required fields from 26+ to 5 core fields
- **Usability** - Proper naming conventions and consistent structure
- **Flexibility** - More optional fields for easier implementation

## Breaking Changes

### 1. Property Naming Convention Change

**Changed from:** Spaces in property names  
**Changed to:** camelCase without spaces

| Old (v1.0) | New (v2.0) |
|------------|------------|
| `"General Section"` | `"generalSection"` |
| `"File Name"` | `"fileName"` |
| `"Time Stamp"` | `"timeStamp"` |
| `"Image Width"` | `"imageWidth"` |
| `"Pixel Width"` | `"pixelWidth"` |
| `"Method Specific"` | `"methodSpecific"` |
| `"Customer Specific"` | `"customerSpecific"` |
| `"Tool Specific"` | `"toolSpecific"` |
| `"Data Evaluation"` | `"dataEvaluation"` |
| `"Signal Type(s)"` | `"signalTypes"` |
| `"Detector(s)"` | `"detectors"` |
| `"ROI (Region of Interest)"` | `"regionsOfInterest"` |
| `"POI"` | `"pointsOfInterest"` |
| `"Scanning Electron Microscopy"` | `"scanningElectronMicroscopy"` |
| `"Focused Ion Beam"` | `"focusedIonBeam"` |
| `"Optical Microscopy"` | `"opticalMicroscopy"` |

**Reason:** Property names with spaces require bracket notation in code (`json["File Name"]`) instead of dot notation (`json.fileName`). This makes programmatic access cumbersome and error-prone. CamelCase is the JSON standard.

### 2. Drastically Reduced Required Fields

**General Section**

OLD (26 required):
```
"File Name", "File Size", "File Format", "File Path", "Logfile Path", 
"Previous Header File", "Header Type", "Version", "Time Stamp", 
"Manufacturer", "Tool Name", "Serial Number", "Method", "Image Width", 
"Image Height", "Pixel Width", "Pixel Height", "Bit Depth", "Color Mode", 
"Customer", "Sample Holder", "Tool Calibrated", "Compressed Bits/Pixel", 
"Coordinates Sub Section", "Alignment Marks Sub Section"
```

NEW (5 required):
```
"fileName", "timeStamp", "manufacturer", "toolName", "method"
```

**Reason:** Many fields are not available via tool APIs or don't apply to all scenarios:
- `logfilePath` - Not all tools generate log files
- `previousHeaderFile` - Makes first file in workflow impossible
- `compressedBitsPerPixel` - Not applicable to uncompressed images
- Entire subsections as required - Only needed when using specific features

**SEM Method**

OLD (21 required):
```
"Accelerating Voltage", "Decelerating Voltage", "Working Distance", 
"Magnification", "Signal Mixing", "Signal Type(s)", "Detector(s)", 
"Signal Proportion", "Aperture Alignment X Y", "Stigmator Alignment X Y", 
"Brightness", "Contrast", "Emission Current", "Probe Current", 
"High Current Mode", "Tilt Correction Mode", "Corrected Tilt Angle", 
"Beam Shift X", "Beam Shift Y", "Scan Rotation Mode", "Scan Rotation"
```

NEW (3 required):
```
"acceleratingVoltage", "workingDistance", "signalTypes"
```

**Reason:** Settings like aperture alignment, stigmator, brightness are often not accessible via API and are operator adjustments, not critical metadata.

### 3. Fixed Structural Issues

#### Added Proper Schema Declarations
```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "...",
  "description": "..."
}
```

**Reason:** Enables validation tools to properly validate JSON files against the schema.

#### Fixed Schema Root Structure

OLD:
```json
{
  "General Section": {
    "type": "object",
    "properties": { ... }
  }
}
```

NEW:
```json
{
  "$schema": "...",
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

**Reason:** Proper JSON Schema structure with schema declaration and consistent hierarchy.

#### Fixed Array Validation

OLD:
```json
"items": {
  "type": "string",
  "minItems": 1
}
```

NEW:
```json
"items": {
  "type": "string"
},
"minItems": 1
```

**Reason:** `minItems` belongs at array level, not inside `items` definition.

#### Removed Parentheses from Property Names

OLD: `"Signal Type(s)"`, `"Detector(s)"`, `"ROI (Region of Interest)"`  
NEW: `"signalTypes"`, `"detectors"`, `"regionsOfInterest"`

**Reason:** Parentheses in property names are non-standard and complicate parsing.

### 4. Improved Naming Consistency

#### Subsection Naming

OLD:
- `"Coordinates Sub Section"`
- `"Alignment Marks Sub Section"`

NEW:
- `"coordinates"`
- `"alignmentMarks"`

**Reason:** Remove redundant "Sub Section" suffix. Nesting already indicates it's a subsection.

#### Hyphen Usage Standardization

OLD: Mix of hyphens, spaces, and camelCase
- `"FIB-SEM Intersection Point"`
- `"Stage Rotation Rx"`

NEW: Consistent camelCase
- `"fibSemIntersectionPoint"`
- `"stageRotationRx"`

**Reason:** Consistent naming convention throughout the schema.

#### Enum Value Formatting

OLD: `"right handed"`, `"left handed"`  
NEW: `"right-handed"`, `"left-handed"`

**Reason:** Hyphenated compound adjectives are correct English and avoid space parsing issues.

### 5. Corrected Spelling Errors

- "ommitted" → "omitted"
- "Deccelerating" → "Decelerating"
- "neccessary" → "necessary"
- "preferable" → "preferably"

### 6. Fixed Type Definitions

**Version field:**
```json
OLD: "Version": { "example": "v1.0" }
NEW: "version": { "type": "string", "examples": ["2.0", "1.0"] }
```

**Reason:** Missing type definition. Also changed from `example` to `examples` (JSON Schema Draft 07 convention).

### 7. Restructured Data Evaluation

OLD:
```json
"ROI (Region of Interest)": {
  "ROI-Polygon": [ ... ],
  "ROI-Polyline": [ ... ]
}
```

NEW:
```json
"regionsOfInterest": {
  "polygons": [ ... ],
  "polylines": [ ... ]
}
```

**Reason:** Removed "ROI" redundancy and simplified naming.

## New File Naming

Schema files renamed to match their content property:

| Old Filename | New Filename |
|--------------|--------------||
| `v1/General Section.json` | `v2/generalSection.json` |
| `v1/Method Specific.json` | `v2/methodSpecific.json` |
| `v1/Customer Section.json` | `v2/customerSection.json` |
| `v1/Tool Specific.json` | `v2/toolSpecific.json` |
| `v1/Data Evaluation.json` | `v2/dataEvaluation.json` |
| `v1/History.json` | `v2/historySection.json` |

**Reason:** Consistent with camelCase convention and removes spaces from filenames. Versions separated into folders.

## Migration Guide

### For Tool Manufacturers

If you've already implemented v1.0:

1. **Update property names** - Use find/replace to convert spaces to camelCase:
   ```python
   # Example Python conversion
   old_keys = ["File Name", "Time Stamp", "Image Width"]
   new_keys = ["fileName", "timeStamp", "imageWidth"]
   ```

2. **Remove excess required fields** - Only populate the 5 core general section fields and 3 method-specific fields as minimum

3. **Update schema file references** - Point to new schema file names

4. **Test with validator** - Validate your JSON against new schema files

### For Analysis Software

If your software reads v1.0 metadata:

1. **Support both versions** - Detect version from `headerType` or `version` field
2. **Add compatibility layer**:
   ```python
   def normalize_metadata(data):
       if "General Section" in data:  # v1.0
           return convert_v1_to_v2(data)
       return data  # v2.0
   ```

3. **Update parsers** to handle camelCase properties

### Backward Compatibility Note

**v2.0 is NOT backward compatible with v1.0** due to property name changes. However, automated conversion is straightforward using the mapping table above.

## Benefits Summary

### For Manufacturers
- ✅ **80% fewer required fields** - Much easier to implement
- ✅ **Standard JSON naming** - Works better with all programming languages
- ✅ **Clear validation** - Proper JSON Schema structure

### For Users
- ✅ **More tool compatibility** - Lower barrier to entry means more tools will support it
- ✅ **Cleaner code** - `json.fileName` instead of `json["File Name"]`
- ✅ **Better documentation** - Clearer, more concise guide

### For the Standard
- ✅ **Professional quality** - Follows JSON Schema best practices
- ✅ **Maintainable** - Consistent conventions throughout
- ✅ **Extensible** - Easier to add new methods and fields

## Questions?

For implementation questions or migration support, please refer to `QUICK_START.md` or open an issue in the repository.

---

**Note:** Old schema files (v1.0) are preserved in the repository at:
- `schema/v1/General Section.json`
- `schema/v1/Method Specific.json`
- `schema/v1/Customer Section.json`
- `schema/v1/Tool Specific.json`
- `schema/v1/Data Evaluation.json`
- `schema/v1/History.json`

New v2.0 files are in `schema/v2/` with camelCase naming.
