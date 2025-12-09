# FA Metadata Header - Quick Start Guide

**Version 1.1** | December 2025

## Overview

The FA Metadata Header is a standardized JSON schema for storing metadata alongside failure analysis images. It enables seamless data exchange between different analysis tools and supports automation and ML-based analysis.

## Key Principles

- **Minimal required fields** - Easy to implement for equipment manufacturers (only 5-8 fields!)
- **Modular structure** - Six independent sections that can be combined
- **Extensible** - Tool and customer-specific sections for custom data
- **Backward compatible** - v1.1 works with v1.0 implementations

## Schema Structure

```json
{
  "General Section": { },      // Core metadata (5 required fields)
  "Method Specific": { },      // Analysis method data (1-3 required per method)
  "Data Evaluation": { },      // POIs, ROIs (optional)
  "Customer Specific": { },    // Your organization's fields (optional)
  "Tool Specific": { },        // Vendor-specific data (optional)
  "History": { }               // Workflow links (optional)
}
```

## Required Fields - Absolute Minimum

### General Section (5 required)
- `"File Name"` - Name of the measurement file
- `"Time Stamp"` - ISO8601 format (e.g., "2025-12-09T16:05:25+01:00")
- `"Manufacturer"` - Tool manufacturer name
- `"Tool Name"` - Tool model/name
- `"Method"` - Analysis method ("SEM", "FIB", or "Optical")

### Method-Specific Section (varies by method)

**SEM:** 3 required fields
- `"Accelerating Voltage"` - Beam voltage
- `"Working Distance"` - Lens-to-sample distance
- `"Signal Type(s)"` - Array of signal types used (e.g., ["SE2"])

**FIB:** 3 required fields  
- `"Accelerating Voltage"`
- `"Working Distance"`
- `"Signal Type(s)"`

**Optical:** 1 required field
- `"Objective Lens Magnification"` - Objective lens magnification

## Implementation for Manufacturers

### 1. Generate Metadata on Image Save

When your tool saves an image, create a companion JSON file with the same base name:

```
my_image.tiff       → Measurement file
my_image.json       → Metadata file
```

### 2. Minimal Example (SEM)

```json
{
  "General Section": {
    "File Name": "sem_sample_001.tiff",
    "Time Stamp": "2025-12-09T14:30:00+01:00",
    "Manufacturer": "ZEISS",
    "Tool Name": "GeminiSEM 500",
    "Method": "SEM"
  },
  "Method Specific": {
    "Scanning Electron Microscopy": {
      "Accelerating Voltage": {
        "Value": 5.0,
        "Unit": "kV"
      },
      "Working Distance": {
        "Value": 8.5,
        "Unit": "mm"
      },
      "Signal Type(s)": ["SE2"]
    }
  }
}
```

### 3. Add Optional Fields as Available

Include additional fields if your tool can provide them:

```json
{
  "General Section": {
    "File Name": "sem_sample_001.tiff",
    "Time Stamp": "2025-12-09T14:30:00+01:00",
    "Manufacturer": "ZEISS",
    "Tool Name": "GeminiSEM 500",
    "Method": "SEM",
    "Image Width": { "Value": 1024, "Unit": "px" },
    "Image Height": { "Value": 1024, "Unit": "px" },
    "Pixel Width": { "Value": 50.2, "Unit": "nm" },
    "Serial Number": "12345-ABC"
  },
  "Method Specific": {
    "Scanning Electron Microscopy": {
      "Accelerating Voltage": { "Value": 5.0, "Unit": "kV" },
      "Working Distance": { "Value": 8.5, "Unit": "mm" },
      "Signal Type(s)": ["SE2", "BSE"],
      "Signal Mixing": true,
      "Signal Proportion": [0.7, 0.3],
      "Magnification": "5000x",
      "Detector(s)": ["Everhart-Thornley", "Backscatter"]
    }
  }
}
```

### 4. Reading Metadata from Other Tools

Load the JSON file to access:
- Sample positioning (coordinates)
- Previous analysis steps (history)
- Marked regions of interest (POIs/ROIs)
- Customer sample identifiers

## Schema Files

All schema files are in `schema/v1.1/`:

**Individual Section Schemas:**
- `General Section.json` - Core metadata (5 required fields)
- `Method Specific.json` - SEM, FIB, Optical methods (1-3 required fields each)
- `Data Evaluation.json` - POIs and ROIs (all optional)
- `Customer Section.json` - Organization-specific fields (all optional)
- `Tool Specific.json` - Vendor-specific fields (all optional)
- `History.json` - Workflow tracking (all optional)

**Examples:**
- `examples/minimal_example_sem.json` - SEM with only 8 fields
- `examples/minimal_example_fib.json` - FIB with only 8 fields
- `examples/minimal_example_optical.json` - Optical with only 6 fields

## Value Format Convention

Numeric values with units use this structure:
```json
{
  "Value": 5.0,
  "Unit": "kV"
}
```

## Important Notes

✅ **Use property names with spaces** - This is v1.1, not v2.0-draft  
Examples: `"File Name"`, `"Time Stamp"`, `"General Section"`

✅ **Capitalize Value and Unit** - Use `"Value"` and `"Unit"`, not lowercase

✅ **Only 5-8 required fields total** - v1.1 dramatically reduced requirements from v1.0

⚠️ **v2.0-draft exists but is NOT for production** - It uses camelCase names and is experimental

## Compatibility

- **v1.1 is fully backward compatible with v1.0** - No migration needed
- **v1.0 files validate against v1.1 schemas** - Old implementations still work
- **v1.1 uses same property names as v1.0** - Only requirement counts changed

## Support & Validation

- Validate your JSON against `schema/v1.1/General Section.json` and `schema/v1.1/Method Specific.json`
- Schema version: 1.1 (December 2025)
- Standard: JSON Schema Draft 07

**Example validation (Python):**
```python
import json
from jsonschema import validate

# Load schemas
with open('schema/v1.1/General Section.json') as f:
    general_schema = json.load(f)

with open('schema/v1.1/Method Specific.json') as f:
    method_schema = json.load(f)

# Load your metadata
with open('your_metadata.json') as f:
    data = json.load(f)

# Validate each section
validate(instance=data["General Section"], 
         schema=general_schema["General Section"])
validate(instance=data["Method Specific"], 
         schema=method_schema["Method Specific"])

print("✓ Validation successful!")
```

## Examples

See `schema/v1.1/examples/` for minimal implementation examples:
- `minimal_example_sem.json` - Only 8 fields (5 General + 3 SEM)
- `minimal_example_fib.json` - Only 8 fields (5 General + 3 FIB)
- `minimal_example_optical.json` - Only 6 fields (5 General + 1 Optical)

## Additional Resources

- **[README.md](README.md)** - Main documentation
- **[CHANGELOG_v1.1.md](changelog/CHANGELOG_v1.1.md)** - What changed from v1.0
- **[VERSIONING.md](documentation/VERSIONING.md)** - Version strategy
- **[FUTURE_V2_MIGRATION.md](documentation/FUTURE_V2_MIGRATION.md)** - About v2.0-draft
