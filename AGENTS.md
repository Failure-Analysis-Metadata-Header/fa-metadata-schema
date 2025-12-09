# AGENTS.md - AI Assistant Guide

**Repository:** FA Metadata Header Standard  
**Version:** 1.1 (December 2025) - Current Stable  
**Purpose:** Standardized JSON schema for semiconductor failure analysis metadata

---

## ⚠️ Important Version Information (December 2025)

**Current Stable Version: 1.1**
- Location: `schema/v1.1/`
- Status: Production-ready
- Property names: **WITH SPACES** (e.g., `"File Name"`, `"General Section"`)
- Only 5-8 required fields total
- Fully backward compatible with v1.0

**Experimental Draft: v2.0-draft** 
- Location: `schema/v2-draft/`
- Status: ⚠️ **NOT FOR PRODUCTION USE**
- Property names: camelCase (e.g., `"fileName"`, `"generalSection"`)
- Contains breaking changes, postponed after stakeholder consultation
- See `documentation/FUTURE_V2_MIGRATION.md` for details

**When helping users:** Always use v1.1 (with spaces in property names) unless they explicitly ask about v2.0-draft.

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
│   ├── v1/                    # Legacy v1.0 (preserved for reference)
│   ├── v1.1/                  # Current stable version (December 2025)
│   │   ├── General Section.json       # Core metadata (5 required fields)
│   │   ├── Method Specific.json       # SEM/FIB/Optical parameters
│   │   ├── Data Evaluation.json       # POIs/ROIs (optional)
│   │   ├── Customer Section.json      # Custom fields (optional)
│   │   ├── Tool Specific.json         # Vendor-specific (optional)
│   │   ├── History.json               # Workflow links (optional)
│   │   └── examples/
│   │       ├── minimal_example_sem.json
│   │       ├── minimal_example_fib.json
│   │       └── minimal_example_optical.json
│   └── v2-draft/              # Experimental (NOT for production)
│       ├── famSchema.json     # ⚠️ DRAFT - camelCase names
│       ├── generalSection.json
│       └── ... (all with camelCase)
├── documentation/
│   ├── fa40_description.md            # Original FA4.0 project docs
│   ├── VERSIONING.md                  # Version strategy
│   ├── MIGRATION_REFERENCE.md         # v1 → v2 mapping (for future)
│   └── FUTURE_V2_MIGRATION.md         # v2.0-draft migration plan
├── changelog/
│   ├── CHANGELOG_v1.1.md              # v1.1 changes (current)
│   └── CHANGELOG_v2.md                # v2.0-draft reference
├── README.md                          # Main documentation (v1.1)
└── QUICK_START.md                     # Implementation guide (v1.1)
```

---

## Schema Architecture

### Modular Design
The schema consists of **6 independent sections** that can be combined:

| Section | File | Required? | Purpose |
|---------|------|-----------|---------|
| **General** | `General Section.json` | ✅ Yes | Core metadata (file, tool, timestamp) |
| **Method Specific** | `Method Specific.json` | ✅ Yes | Analysis parameters (SEM/FIB/Optical) |
| **Data Evaluation** | `Data Evaluation.json` | Optional | Marked features (POIs, ROIs) |
| **Customer** | `Customer Section.json` | Optional | Custom organizational fields |
| **Tool Specific** | `Tool Specific.json` | Optional | Vendor-specific parameters |
| **History** | `History.json` | Optional | Previous workflow steps |

### Note on v1.1 Structure
Unlike v2.0-draft which has a root `famSchema.json`, v1.1 uses individual section schemas. Validate each section separately against its corresponding schema file.

---

## Required Fields (Absolute Minimum)

### General Section (5 required)
```json
{
  "General Section": {
    "File Name": "measurement.tiff",           // Name of measurement file
    "Time Stamp": "2025-12-09T14:30:00+01:00", // ISO8601 format
    "Manufacturer": "ZEISS",                   // Tool manufacturer
    "Tool Name": "GeminiSEM 500",              // Tool model/name
    "Method": "SEM"                            // "SEM", "FIB", or "Optical"
  }
}
```

### Method-Specific Section (varies by method)

**SEM: 3 required fields**
```json
{
  "Method Specific": {
    "Scanning Electron Microscopy": {
      "Accelerating Voltage": { "Value": 5.0, "Unit": "kV" },
      "Working Distance": { "Value": 8.5, "Unit": "mm" },
      "Signal Type(s)": ["SE2"]
    }
  }
}
```

**FIB: 3 required fields** (same as SEM)
```json
{
  "Method Specific": {
    "Focused Ion Beam": {
      "Accelerating Voltage": { "Value": 30.0, "Unit": "kV" },
      "Working Distance": { "Value": 4.0, "Unit": "mm" },
      "Signal Type(s)": ["SE"]
    }
  }
}
```

**Optical: 1 required field**
```json
{
  "Method Specific": {
    "Optical Microscopy": {
      "Objective Lens Magnification": { "Value": 50, "Unit": "x" }
    }
  }
}
```
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

## v1.1 Key Changes from v1.0

### Major Improvements (Non-Breaking)
1. **80% fewer required fields** - Down from 26+ to just 5 core fields
2. **Same property naming** - Kept `"File Name"`, `"General Section"` etc. for backward compatibility
3. **Proper JSON Schema** - Added `$schema`, fixed validation bugs
4. **Better documentation** - Clear examples, fixed spelling errors

### What Changed
- **Dramatically reduced requirements** - Only 5-8 fields needed now
- **Fixed array validation bugs** - Proper `minItems` placement
- **Added schema metadata** - `$schema`, `title`, `version` fields
- **Corrected spelling** - Fixed typos in descriptions
- **All property names UNCHANGED** - Full backward compatibility with v1.0

### What About v2.0?
- **v2.0-draft exists** in `schema/v2-draft/` but is **NOT for production**
- Contains breaking changes (camelCase naming like `"fileName"`, `"generalSection"`)
- Postponed after stakeholder feedback prioritized backward compatibility
- See `documentation/FUTURE_V2_MIGRATION.md` for future migration plans

---

## Common Use Cases & Tasks

### For Equipment Manufacturers
**Task:** Implement metadata export in analysis tools

**Implementation Steps:**
1. When saving an image, generate companion JSON file with same base name
2. Populate required fields (5 in General + 1-3 in Method Specific)
3. Add optional fields as available from tool
4. Validate against v1.1 schemas
5. Save JSON file alongside image

**Validation:**
```python
import jsonschema
import json

# Load schemas
with open('schema/v1.1/General Section.json') as f:
    general_schema = json.load(f)

# Validate metadata
with open('measurement.json') as f:
    metadata = json.load(f)
    
jsonschema.validate(
    instance=metadata["General Section"], 
    schema=general_schema["General Section"]
)
```

### For Data Scientists
**Task:** Read and process FA metadata for ML analysis

**Key Fields to Extract:**
- `metadata["General Section"]["Method"]` - Analysis type
- `metadata["General Section"]["Time Stamp"]` - When captured
- `metadata["Method Specific"]["Scanning Electron Microscopy"]["Accelerating Voltage"]` - SEM parameters
- `metadata["Data Evaluation"]["POI"]` - Marked features
- `metadata["Data Evaluation"]["ROI (Region of Interest)"]` - Marked regions

### For Lab Automation
**Task:** Chain multiple analysis tools together

**Workflow:**
1. Tool A creates image + metadata JSON
2. Tool B reads metadata to:
   - Locate sample position (`"General Section"` → `"Coordinates Sub Section"`)
   - Access previous results (`"Data Evaluation"` → `"POI"`)
   - Continue workflow (`"History"` section)
3. Tool B adds its own metadata and saves updated JSON

---

## Important Naming Conventions (v1.1)

### Property Naming Rules
- **Use spaces in names** - `"File Name"`, `"Time Stamp"`, `"Accelerating Voltage"`
- **Capitalize properly** - Section names: `"General Section"`, `"Method Specific"`
- **Capitalize Value/Unit** - Always `{ "Value": 5.0, "Unit": "kV" }`
- **Arrays use parentheses** - `"Signal Type(s)"`, `"Detector(s)"`

### Section Names (exact spelling required)
```json
{
  "General Section": {},      // WITH spaces, NOT "generalSection"
  "Method Specific": {},      // WITH spaces, NOT "methodSpecific"
  "Data Evaluation": {},      // WITH spaces, NOT "dataEvaluation"
  "Customer Specific": {},    // WITH spaces, NOT "customerSpecific"
  "Tool Specific": {},        // WITH spaces, NOT "toolSpecific"
  "History": {}               // Just "History"
}
```

### Method Names (in Method Specific)
```json
{
  "Method Specific": {
    "Scanning Electron Microscopy": {},  // WITH spaces, NOT "scanningElectronMicroscopy"
    "Focused Ion Beam": {},              // WITH spaces, NOT "focusedIonBeam"
    "Optical Microscopy": {}             // WITH spaces, NOT "opticalMicroscopy"
  }
}
```

---

## File Locations & References

### Current Version Files (v1.1)
- **Schema files:** `schema/v1.1/General Section.json`, `Method Specific.json`, etc.
- **Examples:** `schema/v1.1/examples/`
- **Documentation:** `README.md`, `QUICK_START.md`

### Historical/Reference Files
- **v1.0 schemas:** `schema/v1/` (preserved for reference)
- **v2.0-draft schemas:** `schema/v2-draft/` (experimental, not for production)
- **Migration guide:** `documentation/MIGRATION_REFERENCE.md` (v1 to v2 field mapping, for future)
- **Future migration:** `documentation/FUTURE_V2_MIGRATION.md`
- **Changelog v1.1:** `changelog/CHANGELOG_v1.1.md`
- **Changelog v2-draft:** `changelog/CHANGELOG_v2.md`
- **FA4.0 project docs:** `documentation/fa40_description.md`

### Validation Scripts
- `schema/examples/validate_examples.py` - Python validation example

---

## Versioning Strategy

### Version Format: X.Y
- **X (Major):** Breaking changes, new folder (`schema/v1/`, `schema/v2/`)
- **Y (Minor):** Non-breaking additions, updated in-place

### Current Status
- **Version 1.1:** Current stable (December 2025) - `schema/v1.1/`
- **Version 1.0:** Legacy (preserved) - `schema/v1/`
- **Version 2.0-draft:** Experimental (NOT for production) - `schema/v2-draft/`

### Backward Compatibility
- v1.1 is fully backward compatible with v1.0
- Multiple versions coexist in separate folders
- Old implementations continue working
- Migration guides provided for major versions (when released)

---

## Common Questions

### Q: What are the absolute minimum fields needed?
**A:** Only 5 in `"General Section"` + 1-3 in `"Method Specific"` (varies by method). That's 6-8 fields total.

### Q: Can I add custom fields?
**A:** Yes! Use `"Customer Specific"` section for organizational fields, or `"Tool Specific"` for vendor-specific data.

### Q: Do field names have spaces?
**A:** YES! In v1.1 (current version), use `"File Name"`, `"General Section"`, etc. with spaces. v2.0-draft uses camelCase but is NOT for production yet.

### Q: How do I validate my JSON?
**A:** Use `schema/v1.1/General Section.json` and `schema/v1.1/Method Specific.json` with any JSON Schema validator (Python: jsonschema, JavaScript: ajv, etc.). You can also use the `famdo` tool (https://github.com/Failure-Analysis-Metadata-Header/famdo) directly with your JSON files.

### Q: What's the difference between POI and ROI?
**A:** POI (Point of Interest) is a single coordinate. ROI (Region of Interest) is a polygon or polyline with multiple points.

### Q: Can I use both SEM and FIB in one file?
**A:** No. Pick one method per file. If you have both SEM and FIB images of the same area, create two separate image+metadata file pairs.

### Q: What timestamp format should I use?
**A:** ISO8601 with timezone: `"2025-12-09T14:30:00+01:00"`

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
### Data Types
- **Strings:** `"File Name": "measurement.tiff"`
- **Numbers:** `"Value": 5.0`
- **Arrays:** `"Signal Type(s)": ["SE2", "BSE"]`
- **Objects:** `{ "Value": 5.0, "Unit": "kV" }`
- **Booleans:** `"Tool Calibrated": true`
- **Nullable:** `"Value": [number, null]` allows null values

### Unit Convention
Quantities with units ALWAYS use object format:
```json
{
  "Accelerating Voltage": {
    "Value": 5.0,
    "Unit": "kV"
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

with open('schema/v1.1/General Section.json') as f:
    general_schema = json.load(f)

with open('my_metadata.json') as f:
    data = json.load(f)

jsonschema.validate(
    instance=data["General Section"], 
    schema=general_schema["General Section"]
)
print("✓ Valid!")
```

### Generate minimal metadata (Python example)
```python
import json
from datetime import datetime

metadata = {
    "General Section": {
        "File Name": "sem_image_001.tiff",
        "Time Stamp": datetime.now().astimezone().isoformat(),
        "Manufacturer": "ZEISS",
        "Tool Name": "GeminiSEM 500",
        "Method": "SEM"
    },
    "Method Specific": {
        "Scanning Electron Microscopy": {
            "Accelerating Voltage": {"Value": 5.0, "Unit": "kV"},
            "Working Distance": {"Value": 8.5, "Unit": "mm"},
            "Signal Type(s)": ["SE2"]
        }
    }
}

with open('sem_image_001.json', 'w') as f:
    json.dump(metadata, f, indent=2)
```

---

## Tips for AI Assistants

### When helping users with this repository:

1. **Always use v1.1 schemas** unless explicitly asked about v2.0-draft
2. **Check property names carefully** - they must have spaces: `"File Name"`, `"General Section"`
3. **Remember the minimal requirements** - only 5-8 fields needed total
4. **Validate against individual section schemas** - `General Section.json`, `Method Specific.json`
5. **Use examples** in `schema/v1.1/examples/` as reference
6. **For v2 migration questions** - refer to `FUTURE_V2_MIGRATION.md`
7. **For version questions** - refer to `VERSIONING.md`

### Common user intents:
- "How do I implement this?" → Point to `QUICK_START.md`
- "What changed in v1.1?" → Point to `CHANGELOG_v1.1.md`
- "What fields are required?" → Show minimal example (6-8 fields total)
- "Can I add custom fields?" → Yes, use `"Customer Specific"` or `"Tool Specific"`
- "What about v2.0?" → Explain v2.0-draft is experimental, use v1.1 for production

### Code generation best practices:
- Always use property names with spaces
- Capitalize `"Value"` and `"Unit"` in value/unit objects
- Use ISO8601 for timestamps
- Validate generated JSON against v1.1 schemas
- Provide working, minimal examples first, then expand

---

**Last Updated:** December 9, 2025  
**Schema Version:** 1.1  
**Maintainer:** Failure Analysis Metadata Header Initiative
