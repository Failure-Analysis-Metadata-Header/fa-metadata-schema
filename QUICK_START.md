# FA Metadata Header - Quick Start Guide

## Overview

The FA Metadata Header is a standardized JSON schema for storing metadata alongside failure analysis images. It enables seamless data exchange between different analysis tools and supports automation and ML-based analysis.

## Key Principles

- **Minimal required fields** - Easy to implement for equipment manufacturers
- **Modular structure** - Six independent sections that can be combined
- **Extensible** - Tool and customer-specific sections for custom data

## Schema Structure

```json
{
  "generalSection": { },      // Core metadata (5 required fields)
  "methodSpecific": { },      // Analysis method data (3-4 required per method)
  "dataEvaluation": { },      // POIs, ROIs (optional)
  "customerSpecific": { },    // Your organization's fields (optional)
  "toolSpecific": { },        // Vendor-specific data (optional)
  "history": { }              // Workflow links (optional)
}
```

## Required Fields - Absolute Minimum

### General Section (5 required)
- `fileName` - Name of the measurement file
- `timeStamp` - ISO8601 format (e.g., "2025-11-13T16:05:25+01:00")
- `manufacturer` - Tool manufacturer name
- `toolName` - Tool model/name
- `method` - Analysis method ("SEM", "FIB", "Optical", etc.)

### Method-Specific Section (varies by method)

**SEM:** 3 required fields
- `acceleratingVoltage` - Beam voltage
- `workingDistance` - Lens-to-sample distance
- `signalTypes` - Array of signal types used (e.g., ["SE2"])

**FIB:** 3 required fields  
- `acceleratingVoltage`
- `workingDistance`
- `signalTypes`

**Optical:** 1 required field
- `objectiveMagnification` - Objective lens magnification

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
  "generalSection": {
    "fileName": "sem_sample_001.tiff",
    "timeStamp": "2025-11-13T14:30:00+01:00",
    "manufacturer": "ZEISS",
    "toolName": "GeminiSEM 500",
    "method": "SEM"
  },
  "methodSpecific": {
    "scanningElectronMicroscopy": {
      "acceleratingVoltage": {
        "value": 5.0,
        "unit": "kV"
      },
      "workingDistance": {
        "value": 8.5,
        "unit": "mm"
      },
      "signalTypes": ["SE2"]
    }
  }
}
```

### 3. Add Optional Fields as Available

Include additional fields if your tool can provide them:

```json
{
  "generalSection": {
    "fileName": "sem_sample_001.tiff",
    "timeStamp": "2025-11-13T14:30:00+01:00",
    "manufacturer": "ZEISS",
    "toolName": "GeminiSEM 500",
    "method": "SEM",
    "imageWidth": { "value": 1024, "unit": "px" },
    "imageHeight": { "value": 1024, "unit": "px" },
    "pixelWidth": { "value": 50.2, "unit": "nm" },
    "serialNumber": "12345-ABC"
  },
  "methodSpecific": {
    "scanningElectronMicroscopy": {
      "acceleratingVoltage": { "value": 5.0, "unit": "kV" },
      "workingDistance": { "value": 8.5, "unit": "mm" },
      "signalTypes": ["SE2", "BSE"],
      "signalMixing": true,
      "signalProportion": [0.7, 0.3],
      "magnification": "5000x",
      "detectors": ["Everhart-Thornley", "Backscatter"]
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

All schema files are in `/schema/v2/`:

**Root Schema (recommended for validation):**
- `famSchema.json` - Complete schema combining all sections

**Individual Section Schemas:**
- `generalSection.json` - Core metadata
- `methodSpecific.json` - SEM, FIB, Optical methods
- `dataEvaluation.json` - POIs and ROIs
- `customerSection.json` - Organization-specific fields
- `toolSpecific.json` - Vendor-specific fields
- `historySection.json` - Workflow tracking

## Value Format Convention

Numeric values with units use this structure:
```json
{
  "value": 5.0,
  "unit": "kV"
}
```

## Common Pitfalls

❌ **Don't** use spaces in property names  
✅ **Do** use camelCase: `fileName` not `"File Name"`

❌ **Don't** make fields required if they're not always available  
✅ **Do** mark optional fields as nullable: `"type": ["string", "null"]`

❌ **Don't** include fields with no value  
✅ **Do** omit optional fields if data is unavailable

## Support & Validation

- Validate your JSON against `schema/v2/famSchema.json` using any JSON Schema validator
- Schema version: 2.0 (Nov 2025)
- Standard: JSON Schema Draft 2020-12

**Example validation (Python):**
```python
import json
from jsonschema import validate

with open('schema/v2/famSchema.json') as schema_file:
    schema = json.load(schema_file)

with open('your_metadata.json') as data_file:
    data = json.load(data_file)

validate(instance=data, schema=schema)
```

## Examples

See `/schema/v2/examples/` for complete implementation examples from different tool vendors.
