# AGENTS.md - AI Assistant Guide

**Repository:** FA Metadata Header Standard  
**Version:** 2.0 (November 2025)  
**Purpose:** Standardized JSON schema for semiconductor failure analysis metadata

---

## Repository Overview

This repository defines a **lightweight JSON schema standard** for storing metadata alongside semiconductor failure analysis (FA) images. It enables seamless data exchange between different analysis tools (SEM, FIB, Optical microscopes, etc.) and supports automation and ML-based analysis.

### Core Concept
Each analysis image gets a companion JSON file with standardized metadata:
```
measurement_001.tiff    ← Image file
measurement_001.json    ← Metadata file (following this schema)
```

### Key Stakeholders
- **Equipment manufacturers** (ZEISS, FEI, etc.) - Implement schema in their tools
- **Failure analysis labs** - Use metadata for automation and data exchange
- **Software developers** - Integrate schema validation and processing
- **Researchers** - Use standardized data for ML analysis

---

## Repository Structure

```
fa-metadata-schema/
├── schema/
│   ├── v1/                    # Legacy version (preserved for reference)
│   └── v2/                    # Current version (2.0)
│       ├── famSchema.json     # Root schema (validates complete files)
│       ├── generalSection.json        # Core metadata (5 required fields)
│       ├── methodSpecific.json        # SEM/FIB/Optical parameters
│       ├── dataEvaluation.json        # POIs/ROIs (optional)
│       ├── customerSection.json       # Custom fields (optional)
│       ├── toolSpecific.json          # Vendor-specific (optional)
│       ├── historySection.json        # Workflow links (optional)
│       └── examples/
│           ├── minimal_example_fib.json
│           ├── minimal_example_optical.json
│           └── complete_example_v2.json
├── documentation/
│   ├── fa40_description.md            # Original FA4.0 project docs
│   ├── VERSIONING.md                  # Version strategy
│   └── MIGRATION_REFERENCE.md         # v1 → v2 migration
├── changelog/
│   └── CHANGELOG_v2.md                # Detailed v2.0 changes
├── README.md                          # Main documentation
└── QUICK_START.md                     # Implementation guide
```

---

## Schema Architecture

### Modular Design
The schema consists of **6 independent sections** that can be combined:

| Section | File | Required? | Purpose |
|---------|------|-----------|---------|
| **General** | `generalSection.json` | ✅ Yes | Core metadata (file, tool, timestamp) |
| **Method Specific** | `methodSpecific.json` | ✅ Yes | Analysis parameters (SEM/FIB/Optical) |
| **Data Evaluation** | `dataEvaluation.json` | Optional | Marked features (POIs, ROIs) |
| **Customer** | `customerSection.json` | Optional | Custom organizational fields |
| **Tool Specific** | `toolSpecific.json` | Optional | Vendor-specific parameters |
| **History** | `historySection.json` | Optional | Previous workflow steps |

### Root Schema (`famSchema.json`)
Combines all sections into a single validation schema. Use this to validate complete metadata files.

---

## Required Fields (Absolute Minimum)

### General Section (5 required)
```json
{
  "generalSection": {
    "fileName": "measurement.tiff",           // Name of measurement file
    "timeStamp": "2025-11-26T14:30:00+01:00", // ISO8601 format
    "manufacturer": "ZEISS",                   // Tool manufacturer
    "toolName": "GeminiSEM 500",               // Tool model/name
    "method": "SEM"                            // "SEM", "FIB", or "Optical"
  }
}
```

### Method-Specific Section (varies by method)

**SEM: 3 required fields**
```json
{
  "methodSpecific": {
    "scanningElectronMicroscopy": {
      "acceleratingVoltage": { "value": 5.0, "unit": "kV" },
      "workingDistance": { "value": 8.5, "unit": "mm" },
      "signalTypes": ["SE2"]
    }
  }
}
```

**FIB: 3 required fields** (same as SEM)
```json
{
  "methodSpecific": {
    "focusedIonBeam": {
      "acceleratingVoltage": { "value": 30.0, "unit": "kV" },
      "workingDistance": { "value": 4.0, "unit": "mm" },
      "signalTypes": ["SE"]
    }
  }
}
```

**Optical: 1 required field**
```json
{
  "methodSpecific": {
    "opticalMicroscopy": {
      "objectiveMagnification": { "value": 50, "unit": "x" }
    }
  }
}
```

---

## Version 2.0 Key Changes

### Major Improvements (Breaking Changes)
1. **80% fewer required fields** - Down from 26+ to just 5 core fields
2. **camelCase naming** - Changed from `"File Name"` to `"fileName"` for better code integration
3. **Proper JSON Schema** - Follows JSON Schema Draft 07 standard
4. **Better structure** - Clear separation of required vs optional fields

### Migration from v1.0
- **All property names changed** to camelCase (e.g., `"Time Stamp"` → `"timeStamp"`)
- **Section names changed** (e.g., `"General Section"` → `"generalSection"`)
- **Most fields now optional** - Only 5 required in General, 1-3 in Method Specific
- See `MIGRATION_REFERENCE.md` for complete mapping table

---

## Common Use Cases & Tasks

### For Equipment Manufacturers
**Task:** Implement metadata export in analysis tools

**Implementation Steps:**
1. When saving an image, generate companion JSON file with same base name
2. Populate required fields (5 in General + 1-3 in Method Specific)
3. Add optional fields as available from tool
4. Validate against `famSchema.json`
5. Save JSON file alongside image

**Validation:**
```python
import jsonschema
import json

# Load schema
with open('schema/v2/famSchema.json') as f:
    schema = json.load(f)

# Validate metadata
with open('measurement.json') as f:
    metadata = json.load(f)
    
jsonschema.validate(instance=metadata, schema=schema)
```

### For Data Scientists
**Task:** Read and process FA metadata for ML analysis

**Key Fields to Extract:**
- `generalSection.method` - Analysis type
- `generalSection.timeStamp` - When captured
- `methodSpecific.scanningElectronMicroscopy.acceleratingVoltage` - SEM parameters
- `dataEvaluation.pointsOfInterest` - Marked features
- `dataEvaluation.regionsOfInterest` - Marked regions

### For Lab Automation
**Task:** Chain multiple analysis tools together

**Workflow:**
1. Tool A creates image + metadata JSON
2. Tool B reads metadata to:
   - Locate sample position (`generalSection.coordinates`)
   - Access previous results (`dataEvaluation.pointsOfInterest`)
   - Continue workflow (`history` section)
3. Tool B adds its own metadata and saves updated JSON

---

## Important Naming Conventions

### Property Naming Rules
- **Always camelCase** - `fileName`, `timeStamp`, `acceleratingVoltage`
- **No spaces** - Use camelCase, not `"File Name"`
- **Arrays are plural** - `signalTypes`, `detectors`, `pointsOfInterest`
- **Objects for units** - Always `{ "value": 5.0, "unit": "kV" }`

### Section Names (exact spelling required)
```json
{
  "generalSection": {},      // NOT "General Section"
  "methodSpecific": {},      // NOT "Method Specific"
  "dataEvaluation": {},      // NOT "Data Evaluation"
  "customerSpecific": {},    // NOT "Customer Specific"
  "toolSpecific": {},        // NOT "Tool Specific"
  "history": {}              // NOT "History"
}
```

### Method Names (in methodSpecific)
```json
{
  "methodSpecific": {
    "scanningElectronMicroscopy": {},  // NOT "Scanning Electron Microscopy"
    "focusedIonBeam": {},              // NOT "Focused Ion Beam"
    "opticalMicroscopy": {}            // NOT "Optical Microscopy"
  }
}
```

---

## File Locations & References

### Current Version Files
- **Main schema:** `schema/v2/famSchema.json`
- **Examples:** `schema/v2/examples/`
- **Documentation:** `README.md`, `QUICK_START.md`

### Historical/Reference Files
- **v1.0 schemas:** `schema/v1/` (preserved for migration reference)
- **Migration guide:** `documentation/MIGRATION_REFERENCE.md`
- **Changelog:** `changelog/CHANGELOG_v2.md`
- **FA4.0 project docs:** `documentation/fa40_description.md`

### Validation Scripts
- `schema/examples/validate_examples.py` - Python validation example

---

## Versioning Strategy

### Version Format: X.Y
- **X (Major):** Breaking changes, new folder (`schema/v1/`, `schema/v2/`)
- **Y (Minor):** Non-breaking additions, updated in-place

### Current Status
- **Version 2.0:** Current (November 2025) - `schema/v2/`
- **Version 1.0:** Legacy (preserved) - `schema/v1/`

### Backward Compatibility
- Multiple versions coexist in separate folders
- Old implementations continue working
- Migration guides provided for major versions

---

## Common Questions

### Q: What are the absolute minimum fields needed?
**A:** Only 5 in `generalSection` + 1-3 in `methodSpecific` (varies by method). That's 6-8 fields total.

### Q: Can I add custom fields?
**A:** Yes! Use `customerSpecific` section for organizational fields, or `toolSpecific` for vendor-specific data.

### Q: Do field names have spaces?
**A:** NO! Version 2.0 uses camelCase. `fileName`, not `"File Name"`. This is a breaking change from v1.0.

### Q: How do I validate my JSON?
**A:** Use `schema/v2/famSchema.json` with any JSON Schema validator (Python: jsonschema, JavaScript: ajv, etc.). You can also use the `famdo`[https://github.com/Failure-Analysis-Metadata-Header/famdo] directly with your JSON files.

### Q: What's the difference between POI and ROI?
**A:** POI (Point of Interest) is a single coordinate. ROI (Region of Interest) is a polygon or polyline with multiple points.

### Q: Can I use both SEM and FIB in one file?
**A:** No. Pick one method per file. If you have both SEM and FIB images of the same area, create two separate image+metadata file pairs.

### Q: What timestamp format should I use?
**A:** ISO8601 with timezone: `"2025-11-26T14:30:00+01:00"`

---

## Working with This Repository

### Making Schema Changes
1. **Non-breaking changes** (new optional fields):
   - Edit schema files in `schema/v2/` directly
   - Update `version` field in schema file (e.g., 2.0 → 2.1)
   - Update examples if relevant
   - Document in changelog

2. **Breaking changes** (renamed fields, new requirements):
   - Create new major version folder `schema/v3/`
   - Copy v2 schemas as starting point
   - Make changes
   - Create migration guide
   - Update README with new version

### Testing Changes
1. Validate example files against schema
2. Run `schema/examples/validate_examples.py`
3. Check that old examples still validate (if non-breaking)

### Documentation Updates
- **README.md** - Main entry point, keep concise
- **QUICK_START.md** - Implementation guide for manufacturers
- **CHANGELOG_v2.md** - Detailed change documentation
- **MIGRATION_REFERENCE.md** - v1 to v2 field mapping

---

## Technical Details

### JSON Schema Specification
- **Standard:** JSON Schema Draft 07
- **Validation:** All schemas include `$schema` property
- **References:** Uses `$ref` for modular composition

### Data Types
- **Strings:** `"fileName": "measurement.tiff"`
- **Numbers:** `"value": 5.0`
- **Arrays:** `"signalTypes": ["SE2", "BSE"]`
- **Objects:** `{ "value": 5.0, "unit": "kV" }`
- **Booleans:** `"toolCalibrated": true`
- **Nullable:** `"value": [number, null]` allows null values

### Unit Convention
Quantities with units ALWAYS use object format:
```json
{
  "acceleratingVoltage": {
    "value": 5.0,
    "unit": "kV"
  }
}
```

---

## External Resources

### Related Projects
- **FA4.0 Initiative:** Original semiconductor industry project that created this standard
- **Website:** https://failure-analysis-metadata-header.github.io/

### JSON Schema Tools
- **Python:** `jsonschema` library
- **JavaScript:** `ajv` (Another JSON Schema Validator)
- **Online validators:** jsonschemavalidator.net

### Standards Referenced
- **ISO8601:** Timestamp format
- **JSON Schema Draft 07:** Schema specification standard

---

## Quick Command Reference

### Validate a metadata file (Python)
```python
import jsonschema
import json

with open('schema/v2/famSchema.json') as f:
    schema = json.load(f)

with open('my_metadata.json') as f:
    data = json.load(f)

jsonschema.validate(instance=data, schema=schema)
print("✓ Valid!")
```

### Generate minimal metadata (Python example)
```python
import json
from datetime import datetime

metadata = {
    "generalSection": {
        "fileName": "sem_image_001.tiff",
        "timeStamp": datetime.now().astimezone().isoformat(),
        "manufacturer": "ZEISS",
        "toolName": "GeminiSEM 500",
        "method": "SEM"
    },
    "methodSpecific": {
        "scanningElectronMicroscopy": {
            "acceleratingVoltage": {"value": 5.0, "unit": "kV"},
            "workingDistance": {"value": 8.5, "unit": "mm"},
            "signalTypes": ["SE2"]
        }
    }
}

with open('sem_image_001.json', 'w') as f:
    json.dump(metadata, f, indent=2)
```

---

## Tips for AI Assistants

### When helping users with this repository:

1. **Always use v2.0 schemas** unless explicitly asked about v1.0
2. **Check property names carefully** - they must be camelCase without spaces
3. **Remember the minimal requirements** - only 5-8 fields needed total
4. **Validate against famSchema.json** - this is the root schema
5. **Use examples** in `schema/v2/examples/` as reference
6. **For migration questions** - refer to `MIGRATION_REFERENCE.md`
7. **For version questions** - refer to `VERSIONING.md`

### Common user intents:
- "How do I implement this?" → Point to `QUICK_START.md`
- "What changed in v2?" → Point to `CHANGELOG_v2.md`
- "How do I migrate?" → Point to `MIGRATION_REFERENCE.md`
- "What fields are required?" → Show minimal example (8 fields total)
- "Can I add custom fields?" → Yes, use `customerSpecific` or `toolSpecific`

### Code generation best practices:
- Always use proper camelCase property names
- Include unit objects for all quantities
- Use ISO8601 for timestamps
- Validate generated JSON against schema
- Provide working, minimal examples first, then expand

---

**Last Updated:** November 26, 2025  
**Schema Version:** 2.0  
**Maintainer:** Failure Analysis Metadata Header Initiative
