# FA Metadata Header Standard

**Version 1.1** | December 2025

## What is this?

A lightweight JSON schema for storing metadata alongside semiconductor failure analysis images. Enables seamless data exchange between different analysis tools (SEM, FIB, Optical microscopes, etc.) and supports automation and ML analysis.

## Quick Links

- **[Quick Start Guide](QUICK_START.md)** - For equipment manufacturers implementing the standard
- **[Change Log v1.1](changelog/CHANGELOG_v1.1.md)** - What changed from v1.0 and why
- **[Versioning Strategy](documentation/VERSIONING.md)** - How we manage schema versions
- **[Schema Files](schema/v1.1/)** - JSON Schema definitions
- **[Examples](schema/v1.1/examples/)** - Sample implementations
- **[FA40 Documentation](documentation/fa40_description.md)** - Documentation from the FA4.0 Project

## Why Version 1.1?

Version 1.1 is a **non-breaking update** focused on **ease of implementation**:

- ✅ **80% fewer required fields** (5 instead of 26+ core fields)
- ✅ **Backward compatible** with v1.0 (no migration needed)
- ✅ **Better schema quality** (proper JSON Schema format, fixed validation bugs)
- ✅ **Clearer documentation** (concise, action-oriented)

**What didn't change:** All property names remain identical to v1.0 for full backward compatibility.

See [CHANGELOG_v1.1.md](changelog/CHANGELOG_v1.1.md) for complete details.

## Core Concept

Each analysis image gets a companion JSON file with standardized metadata:

```
measurement_001.tiff    ← Your image file
measurement_001.json    ← Metadata file
```

**Minimal example (SEM):**
```json
{
  "General Section": {
    "File Name": "measurement_001.tiff",
    "Time Stamp": "2025-12-09T14:30:00+01:00",
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

That's it! Just 8 fields minimum for SEM, 6 for Optical. Add more as available.

## Schema Structure

### Individual Section Schemas

Six modular schemas that define the structure:

| Section | Schema File | Required? | Purpose |
|---------|-------------|-----------|---------|
| **General** | `v1.1/General Section.json` | ✅ Yes | Core metadata (file, tool, timestamp) |
| **Method Specific** | `v1.1/Method Specific.json` | ✅ Yes | Analysis method parameters (SEM/FIB/Optical) |
| **Data Evaluation** | `v1.1/Data Evaluation.json` | Optional | Marked features (POIs, ROIs) |
| **Customer** | `v1.1/Customer Section.json` | Optional | Your organization's custom fields |
| **Tool Specific** | `v1.1/Tool Specific.json` | Optional | Vendor-specific parameters |
| **History** | `v1.1/History.json` | Optional | Previous workflow steps |

### Validation

Validate your JSON files using any JSON Schema validator:

```python
import jsonschema
import json

# Load schema
with open('schema/v1.1/General Section.json') as f:
    general_schema = json.load(f)

# Load your metadata
with open('measurement.json') as f:
    metadata = json.load(f)

# Validate
jsonschema.validate(
    instance=metadata["General Section"],
    schema=general_schema["General Section"]
)
```

## Minimum Required Fields

### General Section (5 fields)

```json
{
  "General Section": {
    "File Name": "measurement.tiff",
    "Time Stamp": "2025-12-09T14:30:00+01:00",
    "Manufacturer": "ZEISS",
    "Tool Name": "GeminiSEM 500",
    "Method": "SEM"
  }
}
```

### Method-Specific Sections

**SEM (3 fields):**
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

**FIB (3 fields):**
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

**Optical (1 field):**
```json
{
  "Method Specific": {
    "Optical Microscopy": {
      "Objective Lens Magnification": { "Value": 50, "Unit": "x" }
    }
  }
}
```

## Optional Sections

Add these sections when you have the data:

### Data Evaluation
Mark important features in your images:
```json
{
  "Data Evaluation": {
    "POI": [
      {
        "Name": "Defect 1",
        "Coordinates": { "Value": [1024, 768], "Unit": "pixel" }
      }
    ]
  }
}
```

### Customer Specific
Add your organization's fields:
```json
{
  "Customer Specific": {
    "Project ID": "PROJ-2025-123",
    "Sample ID": "WAFER-456"
  }
}
```

### Tool Specific
Add vendor-specific parameters not in Method Specific:
```json
{
  "Tool Specific": {
    "Zeiss SmartSEM": {
      "Auto Brightness": true,
      "Auto Contrast": true
    }
  }
}
```

### History
Link to previous analysis steps:
```json
{
  "History": {
    "Previous Files": [
      "overview_image_001.json",
      "zoom_image_002.json"
    ]
  }
}
```

## For Equipment Manufacturers

**Implementing this standard:**

1. When saving an image, generate a companion JSON file
2. Populate the 5 required General Section fields
3. Populate the 1-3 required Method Specific fields for your tool type
4. Add any optional fields your tool can provide
5. Save JSON file with same base name as image

See [QUICK_START.md](QUICK_START.md) for detailed implementation guide.

## For Data Scientists

**Reading metadata:**

```python
import json

# Load metadata
with open('measurement_001.json') as f:
    metadata = json.load(f)

# Access fields
filename = metadata["General Section"]["File Name"]
voltage = metadata["Method Specific"]["Scanning Electron Microscopy"]["Accelerating Voltage"]["Value"]
timestamp = metadata["General Section"]["Time Stamp"]

# Check optional sections
if "Data Evaluation" in metadata:
    pois = metadata["Data Evaluation"].get("POI", [])
    for poi in pois:
        print(f"Found POI: {poi['Name']} at {poi['Coordinates']['Value']}")
```

## Version Information

### Current Version: 1.1 (Stable)
- **Location:** `schema/v1.1/`
- **Status:** Production-ready
- **Compatibility:** Fully backward compatible with v1.0
- **Use for:** All new implementations

### Legacy Version: 1.0
- **Location:** `schema/v1/`
- **Status:** Superseded by v1.1
- **Note:** v1.0 files work with v1.1 validators

### Future Version: 2.0-draft (Experimental)
- **Location:** `schema/v2-draft/`
- **Status:** ⚠️ **NOT FOR PRODUCTION USE**
- **Note:** Contains breaking changes (camelCase property names). Postponed after stakeholder consultation. See [FUTURE_V2_MIGRATION.md](documentation/FUTURE_V2_MIGRATION.md)

## Resources

- **Schema Files:** [schema/v1.1/](schema/v1.1/)
- **Examples:** [schema/v1.1/examples/](schema/v1.1/examples/)
- **Changelog:** [CHANGELOG_v1.1.md](changelog/CHANGELOG_v1.1.md)
- **Versioning:** [VERSIONING.md](documentation/VERSIONING.md)
- **Future v2.0:** [FUTURE_V2_MIGRATION.md](documentation/FUTURE_V2_MIGRATION.md)

## Contributing

This standard is maintained by the Failure Analysis Metadata Header Initiative. For questions, suggestions, or to report issues:

- **Website:** https://failure-analysis-metadata-header.github.io/
- **GitHub:** https://github.com/Failure-Analysis-Metadata-Header/fa-metadata-schema

## License

The schema files and documentation are provided for use in the semiconductor failure analysis community.

---

**Last Updated:** December 9, 2025  
**Schema Version:** 1.1  
**Status:** Stable
