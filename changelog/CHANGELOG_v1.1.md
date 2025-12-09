# Schema v1.1 - Change Log

**Date:** December 9, 2025  
**Version:** 1.1  
**Previous Version:** 1.0  
**Compatibility:** ✅ **BACKWARD COMPATIBLE** with v1.0

## Executive Summary

Version 1.1 represents a **non-breaking update** to the FA Metadata Header schema with focus on:
- **Ease of Implementation** - Reduced required fields from 26+ to 5 core fields
- **Schema Quality** - Fixed validation bugs and added proper JSON Schema structure
- **Clarity** - Corrected spelling errors and improved documentation

**Important:** All property names, structure, and data formats remain identical to v1.0. Existing v1.0 JSON files are fully compatible with v1.1 validators.

## What Changed in v1.1

### 1. Dramatically Reduced Required Fields ✅ Non-Breaking

Making fields optional doesn't break existing implementations - files with all fields still validate.

#### General Section
**Before (v1.0):** 26 required fields  
**After (v1.1):** 5 required fields

**New required fields (v1.1):**
```json
[
  "File Name",
  "Time Stamp", 
  "Manufacturer",
  "Tool Name",
  "Method"
]
```

**Now optional (previously required):**
- `"File Size"`, `"File Format"`, `"File Path"`, `"Logfile Path"`
- `"Previous Header File"`, `"Header Type"`, `"Version"`, `"Serial Number"`
- `"Image Width"`, `"Image Height"`, `"Pixel Width"`, `"Pixel Height"`
- `"Bit Depth"`, `"Color Mode"`, `"Customer"`, `"Sample Holder"`
- `"Tool Calibrated"`, `"Compressed Bits/Pixel"`
- `"Coordinates Sub Section"`, `"Alignment Marks Sub Section"`

**Reason:** Many fields are not available via tool APIs or don't apply to all scenarios:
- `"Logfile Path"` - Not all tools generate log files
- `"Previous Header File"` - Makes first file in workflow impossible
- `"Compressed Bits/Pixel"` - Not applicable to uncompressed images
- Entire subsections - Only needed when using specific features

#### SEM Method (in Method Specific Section)
**Before (v1.0):** 21 required fields  
**After (v1.1):** 3 required fields

**New required fields (v1.1):**
```json
[
  "Accelerating Voltage",
  "Working Distance",
  "Signal Type(s)"
]
```

**Now optional (previously required):**
- `"Decelerating Voltage"`, `"Magnification"`, `"Signal Mixing"`
- `"Detector(s)"`, `"Signal Proportion"`, `"Aperture Alignment X Y"`
- `"Stigmator Alignment X Y"`, `"Brightness"`, `"Contrast"`
- `"Emission Current"`, `"Probe Current"`, `"High Current Mode"`
- `"Tilt Correction Mode"`, `"Corrected Tilt Angle"`
- `"Beam Shift X"`, `"Beam Shift Y"`, `"Scan Rotation Mode"`, `"Scan Rotation"`

**Reason:** Settings like aperture alignment, stigmator, brightness are often not accessible via API and are operator adjustments, not critical metadata.

#### FIB Method (in Method Specific Section)
**Before (v1.0):** 23 required fields (all SEM fields + FIB-specific)  
**After (v1.1):** 3 required fields

**New required fields (v1.1):**
```json
[
  "Accelerating Voltage",
  "Working Distance",
  "Signal Type(s)"
]
```

**Now optional (previously required):**
- All SEM fields listed above
- FIB-specific fields: `"FIB-SEM Intersection Point"`, `"FIB Tilt Angle"`

#### Optical Method (in Method Specific Section)
**Before (v1.0):** 6 required fields  
**After (v1.1):** 1 required field

**New required field (v1.1):**
```json
[
  "Objective Lens Magnification"
]
```

**Now optional (previously required):**
- `"Optical Zoom"`, `"Digital Zoom"`, `"Contrast Method"`
- `"HDR Mode"`, `"Exposure Time"`

### 2. Added Proper JSON Schema Structure ✅ Non-Breaking

Added standard JSON Schema declarations to enable proper validation. This doesn't affect data format.

**Added to all schema files:**
```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "FA Metadata - [Section Name]",
  "version": "1.1",
  "description": "..."
}
```

**Benefit:** Validation tools can now properly identify and validate JSON files against the schema.

### 3. Fixed Array Validation Bugs ✅ Non-Breaking

Corrected JSON Schema syntax for array validation. This fixes schema validation errors without changing valid data format.

**Before (v1.0) - Incorrect:**
```json
"Signal Type(s)": {
  "type": "array",
  "items": {
    "type": "string",
    "minItems": 1  // ❌ Wrong location
  }
}
```

**After (v1.1) - Correct:**
```json
"Signal Type(s)": {
  "type": "array",
  "items": {
    "type": "string"
  },
  "minItems": 1  // ✅ Correct location
}
```

**Affected fields:**
- `"Signal Type(s)"` (SEM, FIB)
- `"Detector(s)"` (SEM, FIB)
- All array fields with `minItems`/`maxItems` constraints

**Reason:** `minItems` and `maxItems` belong at the array level, not inside the `items` definition, per JSON Schema specification.

### 4. Corrected Spelling Errors ✅ Non-Breaking

Fixed typos in field descriptions. This doesn't affect property names or data.

**Corrections:**
- "ommitted" → "omitted"
- "Deccelerating" → "Decelerating"
- "neccessary" → "necessary"
- "preferable" → "preferably"

**Location:** Only in `"description"` fields, not in property names.

### 5. Added Missing Type Definitions ✅ Non-Breaking

Added `"type"` specification to fields that were missing it.

**Example - Version field:**

**Before (v1.0):**
```json
"Version": {
  "description": "The version of the standard header type.",
  "example": "v1.0"
}
```

**After (v1.1):**
```json
"Version": {
  "description": "The version of the standard header type.",
  "type": "string",
  "examples": ["1.1", "1.0"]
}
```

**Changes:**
- Added `"type": "string"`
- Changed `"example"` to `"examples"` (JSON Schema Draft 07 convention)

## Minimal Example Files

New minimal examples demonstrate the reduced requirements:

### SEM Example (`minimal_example_sem.json`)
```json
{
  "General Section": {
    "File Name": "sem_measurement_001.tiff",
    "Time Stamp": "2025-12-09T10:30:00+01:00",
    "Manufacturer": "ZEISS",
    "Tool Name": "GeminiSEM 500",
    "Method": "SEM"
  },
  "Method Specific": {
    "Scanning Electron Microscopy": {
      "Accelerating Voltage": { "Value": 5.0, "Unit": "kV" },
      "Working Distance": { "Value": 8.5, "Unit": "mm" },
      "Signal Type(s)": ["SE2"]
    }
  }
}
```

**Only 8 total fields required!** (5 in General + 3 in SEM)

### FIB Example (`minimal_example_fib.json`)
```json
{
  "General Section": {
    "File Name": "fib_measurement_001.tiff",
    "Time Stamp": "2025-12-09T11:15:00+01:00",
    "Manufacturer": "FEI",
    "Tool Name": "Helios G4 UX",
    "Method": "FIB"
  },
  "Method Specific": {
    "Focused Ion Beam": {
      "Accelerating Voltage": { "Value": 30.0, "Unit": "kV" },
      "Working Distance": { "Value": 4.0, "Unit": "mm" },
      "Signal Type(s)": ["SE"]
    }
  }
}
```

**Only 8 total fields required!** (5 in General + 3 in FIB)

### Optical Example (`minimal_example_optical.json`)
```json
{
  "General Section": {
    "File Name": "optical_measurement_001.tiff",
    "Time Stamp": "2025-12-09T14:20:00+01:00",
    "Manufacturer": "Leica",
    "Tool Name": "DM6 M",
    "Method": "Optical"
  },
  "Method Specific": {
    "Optical Microscopy": {
      "Objective Lens Magnification": { "Value": 50, "Unit": "x" }
    }
  }
}
```

**Only 6 total fields required!** (5 in General + 1 in Optical)

## Migration from v1.0 to v1.1

### For Tool Manufacturers

**Good news:** No code changes required! Your v1.0 implementation will validate against v1.1.

**To take advantage of v1.1:**
1. Update schema file references to point to `schema/v1.1/` files
2. Optionally reduce the number of fields you populate (now only 5-8 fields minimum)
3. Test validation against v1.1 schemas

**Example Python validation:**
```python
import jsonschema
import json

# Load v1.1 schema
with open('schema/v1.1/General Section.json') as f:
    schema = json.load(f)

# Your existing v1.0 or v1.1 metadata
with open('measurement.json') as f:
    metadata = json.load(f)
    
# This will validate successfully for both v1.0 and v1.1 files
jsonschema.validate(instance=metadata, schema=schema)
```

### For Analysis Software

**No changes required!** Your v1.0 parser will work with v1.1 files because:
- All property names are unchanged
- All structure is unchanged
- v1.1 files are valid v1.0 files (possibly with fewer fields)

**Optional enhancement:**
Update to v1.1 schemas for better error messages when validating incomplete files.

## Backward Compatibility

✅ **v1.1 is FULLY backward compatible with v1.0**

- **v1.0 files validate against v1.1 schemas** - All v1.0 files are valid v1.1 files
- **v1.1 files validate against v1.0 schemas** - If they include all v1.0 required fields
- **No property name changes** - All field names identical
- **No structural changes** - Object hierarchy unchanged
- **No enum changes** - All allowed values identical

## Benefits Summary

### For Manufacturers
- ✅ **80% fewer required fields** - Much easier to implement
- ✅ **Zero breaking changes** - Existing v1.0 code works unchanged
- ✅ **Better schema quality** - Proper JSON Schema structure

### For Users
- ✅ **More tool compatibility** - Lower barrier to entry means more tools will adopt it
- ✅ **Existing workflows continue** - No migration needed
- ✅ **Better validation** - Fixed schema bugs enable proper validation

### For the Standard
- ✅ **Maintains compatibility** - No fragmentation of implementations
- ✅ **Easier adoption** - Reduced requirements lower barriers
- ✅ **Professional quality** - Follows JSON Schema best practices

## What Didn't Change

To maintain backward compatibility, v1.1 keeps:

- ✅ All property names (including spaces: `"File Name"`, `"Time Stamp"`)
- ✅ All section names (`"General Section"`, `"Method Specific"`)
- ✅ All capitalization (`"Value"`, `"Unit"`, `"Scanning Electron Microscopy"`)
- ✅ All enum values (`"right handed"`, `"left handed"`)
- ✅ All structure and nesting
- ✅ All data types

## Future: v2.0-draft

A draft version 2.0 exists in `schema/v2-draft/` with breaking changes (camelCase property names). However, after stakeholder consultation, it was decided to postpone these breaking changes and focus on non-breaking improvements in v1.1 first.

See `documentation/FUTURE_V2_MIGRATION.md` for details about what v2.0-draft offers and the migration path when stakeholders are ready.

## Questions?

For implementation questions, please refer to:
- `README.md` - Main documentation
- `QUICK_START.md` - Implementation guide
- `schema/v1.1/examples/` - Minimal working examples

---

**Schema Files:**
- Current stable: `schema/v1.1/` (use this for production)
- Legacy: `schema/v1/` (still valid, but v1.1 recommended)
- Future draft: `schema/v2-draft/` (breaking changes, not for production)
