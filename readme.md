# FA Metadata Header Standard

**Version 2.0** | November 2025

## What is this?

A lightweight JSON schema for storing metadata alongside semiconductor failure analysis images. Enables seamless data exchange between different analysis tools (SEM, FIB, Optical microscopes, etc.) and supports automation and ML analysis.

## Quick Links

- **[Quick Start Guide](QUICK_START.md)** - For equipment manufacturers implementing the standard
- **[Change Log v2.0]()** - What changed from v1.0 and why
- **[Versioning Strategy](documentation/VERSIONING.md)** - How we manage schema versions
- **[Schema Files](schema/v2/)** - JSON Schema definitions
- **[Examples](schema/v2/examples/)** - Sample implementations

## Why Version 2.0?

Version 2.0 is a major simplification focused on **ease of implementation**:

- ✅ **80% fewer required fields** (5 instead of 26+ core fields)
- ✅ **Standard JSON naming** (camelCase, no spaces)
- ✅ **Better structure** (proper JSON Schema format)
- ✅ **Clearer documentation** (concise, action-oriented)

See [CHANGELOG_v2.md](changelog/CHANGELOG_v2.md) for complete details.

## Core Concept

Each analysis image gets a companion JSON file with standardized metadata:

```
measurement_001.tiff    ← Your image file
measurement_001.json    ← Metadata file
```

**Minimal example:**
```json
{
  "generalSection": {
    "fileName": "measurement_001.tiff",
    "timeStamp": "2025-11-13T14:30:00+01:00",
    "manufacturer": "ZEISS",
    "toolName": "GeminiSEM 500",
    "method": "SEM"
  },
  "methodSpecific": {
    "scanningElectronMicroscopy": {
      "acceleratingVoltage": { "value": 5.0, "unit": "kV" },
      "workingDistance": { "value": 8.5, "unit": "mm" },
      "signalTypes": ["SE2"]
    }
  }
}
```

That's it! Just 8 fields minimum. Add more as available.

## Schema Structure

Six modular sections that can be combined as needed:

| Section | Schema File | Required? | Purpose |
|---------|-------------|-----------|---------||
| **General** | `v2/generalSection.json` | ✅ Yes | Core metadata (file, tool, timestamp) |
| **Method Specific** | `v2/methodSpecific.json` | ✅ Yes | Analysis method parameters (SEM/FIB/Optical) |
| **Data Evaluation** | `v2/dataEvaluation.json` | Optional | Marked features (POIs, ROIs) |
| **Customer** | `v2/customerSection.json` | Optional | Your organization's custom fields |
| **Tool Specific** | `v2/toolSpecific.json` | Optional | Vendor-specific parameters |
| **History** | `v2/historySection.json` | Optional | Previous analysis steps in workflow |

### Section Details

**General Section** - 5 required fields, ~25 optional  
Core information about the measurement file and tool. Only `fileName`, `timeStamp`, `manufacturer`, `toolName`, and `method` are required. Everything else (image dimensions, stage coordinates, alignment marks) is optional.

**Method Specific** - 1-3 required fields per method  
Method-specific settings. Requirements vary:
- **SEM:** 3 required (`acceleratingVoltage`, `workingDistance`, `signalTypes`)
- **FIB:** 3 required (same as SEM)
- **Optical:** 1 required (`objectiveMagnification`)

**Data Evaluation** - All optional  
Points of interest (POIs) and regions of interest (ROIs) marked during analysis. Supports polygons and polylines with styling information.

**Customer Section** - Fully customizable  
Define your own fields for sample tracking, order numbers, project IDs, etc. Completely flexible schema.

**Tool Specific** - Fully customizable  
Vendor-defined fields for tool-specific parameters not covered in the standard method section.

**History** - All optional  
Links to previous measurements and workflow tracking.

## For Equipment Manufacturers

### Implementation Checklist

1. ✅ Generate JSON file when saving measurement images
2. ✅ Populate 5 required general fields
3. ✅ Populate 1-3 required method-specific fields
4. ✅ Add optional fields as available from your tool API
5. ✅ Validate against schema files

### Reading Metadata

Your tool should be able to:
- Load JSON metadata files
- Extract customer sample IDs
- Read stage coordinates and alignment marks
- Access POIs/ROIs from previous steps

This enables workflow automation and data exchange between tools.

See **[QUICK_START.md](QUICK_START.md)** for detailed implementation guide.

## Example Workflow

**Scenario:** Transfer POIs between SAM (acoustic microscope) and FIB tools

1. **SAM Analysis**
   - Sample mounted on Universal Sample Holder
   - Alignment marks scanned automatically
   - Delaminations identified and saved with JSON metadata
   - POIs marked on defects

2. **Data Transfer**
   - JSON file contains: POIs, alignment marks, stage coordinates
   - File loaded into FIB tool

3. **FIB Navigation**
   - Alignment marks scanned on FIB
   - Coordinate transformation applied using alignment marks
   - FIB automatically navigates to POIs from SAM
   - Cross-section performed at exact location

**Result:** Seamless handoff between tools without manual coordinate conversion.

## Schema Files

### Current Version (v2.0)
- `schema/v2/generalSection.json`
- `schema/v2/methodSpecific.json`
- `schema/v2/dataEvaluation.json`
- `schema/v2/customerSection.json`
- `schema/v2/toolSpecific.json`
- `schema/v2/historySection.json`

### Legacy (v1.0 - preserved for reference)
- `schema/v1/General Section.json`
- `schema/v1/Method Specific.json`
- `schema/v1/Data Evaluation.json`
- `schema/v1/Customer Section.json`
- `schema/v1/Tool Specific.json`
- `schema/v1/History.json`

## Resources

- **Documentation Website:** [Failure Analysis Metadata Header Documentation](https://failure-analysis-metadata-header.github.io/)
- **Quick Start:** [QUICK_START.md](QUICK_START.md)
- **Migration Guide:** [CHANGELOG_v2.md](CHANGELOG_v2.md)
- **Examples:** [schema/examples/](schema/examples/)

## Contributing

This is an open standard. Feedback and contributions welcome:
- Open issues for suggestions
- Submit pull requests for improvements
- Share implementation experiences

## License

This schema is provided as-is for use in the semiconductor failure analysis community.

