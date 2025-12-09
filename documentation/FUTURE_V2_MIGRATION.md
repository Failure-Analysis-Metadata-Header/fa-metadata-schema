# Future Migration to v2.0 - Planning Document

**Status:** 🚧 DRAFT - Not for production use  
**Date:** December 9, 2025  
**Current Version:** 1.1 (stable)  
**Draft Version:** 2.0-draft (experimental)

---

## Executive Summary

A **v2.0-draft** schema exists in `schema/v2-draft/` that implements significant improvements through **breaking changes**, primarily property name standardization (camelCase). After stakeholder consultation in December 2025, it was decided to **postpone** these breaking changes and instead release **v1.1** with non-breaking improvements first.

This document explains:
1. What v2.0-draft offers
2. Why it was postponed
3. Migration strategy for when stakeholders are ready
4. Decision criteria for future v2.0 release

---

## What v2.0-Draft Offers

### 1. Modern Property Naming (camelCase)

**Current (v1.x):** Property names with spaces  
**v2.0-draft:** Standard camelCase without spaces

**Examples:**
- `"File Name"` → `"fileName"`
- `"Time Stamp"` → `"timeStamp"`
- `"General Section"` → `"generalSection"`
- `"Method Specific"` → `"methodSpecific"`
- `"Signal Type(s)"` → `"signalTypes"`
- `"ROI (Region of Interest)"` → `"regionsOfInterest"`

**Benefits:**
- ✅ **Better code integration** - Enables dot notation (`json.fileName`) instead of bracket notation (`json["File Name"]`)
- ✅ **Industry standard** - Follows JSON and JavaScript conventions
- ✅ **Cleaner parsing** - No escaping needed for property names
- ✅ **Better IDE support** - Auto-completion works better with camelCase

**Trade-off:**
- ❌ **Breaking change** - Requires migration of existing data and code

### 2. Cleaner Property Names

**Current (v1.x):** Inconsistent naming with parentheses, hyphens, spaces  
**v2.0-draft:** Consistent camelCase throughout

**Examples:**
- `"Signal Type(s)"` → `"signalTypes"` (removed parentheses)
- `"FIB-SEM Intersection Point"` → `"fibSemIntersectionPoint"` (removed hyphens)
- `"Coordinates Sub Section"` → `"coordinates"` (removed redundancy)
- `"ROI-Polygon"` → `"polygons"` (simplified)
- `"Value"` / `"Unit"` → `"value"` / `"unit"` (lowercase for consistency)

### 3. Improved Enum Values

**Current (v1.x):** Enum values with spaces  
**v2.0-draft:** camelCase enum values

**Example:**
```json
// v1.x
"Stage Coordinate System Orientation": {
  "enum": ["right handed", "left handed"]
}

// v2.0-draft
"stageCoordinateSystem": {
  "enum": ["rightHanded", "leftHanded"]
}
```

### 4. Restructured Data Evaluation

**Current (v1.x):**
```json
"ROI (Region of Interest)": {
  "ROI-Polygon": [...],
  "ROI-Polyline": [...]
}
```

**v2.0-draft:**
```json
"regionsOfInterest": {
  "polygons": [...],
  "polylines": [...]
}
```

**Benefits:** Removes "ROI" redundancy and simplifies structure.

### 5. All v1.1 Improvements Included

v2.0-draft also includes all the non-breaking improvements from v1.1:
- ✅ Reduced required fields (26 → 5 in General, 21 → 3 in SEM, etc.)
- ✅ Fixed array validation bugs
- ✅ Proper JSON Schema structure
- ✅ Corrected spelling errors
- ✅ Added missing type definitions

---

## Why v2.0 Was Postponed

### Stakeholder Concerns (December 2025)

After presenting the v2.0 changes, stakeholders raised valid concerns:

1. **Existing Implementations** 
   - Several tool manufacturers have already implemented v1.0
   - Migration would require code changes in multiple organizations
   - Testing burden for manufacturers

2. **Data Migration**
   - Existing v1.0 JSON files would need conversion
   - Risk of data loss or corruption during migration
   - No immediate tooling for automated migration

3. **Fragmentation Risk**
   - If adoption is slow, ecosystem splits between v1.x and v2.x
   - Some tools supporting only v1, others only v2
   - Users caught in the middle

4. **Cost vs. Benefit**
   - **Biggest pain point was "too many required fields"** ✅ Fixed in v1.1 (non-breaking)
   - Property naming is "nice to have" but not blocking adoption
   - Can wait until more implementations exist

### Decision: Focus on v1.1 First

**Strategy:**
1. ✅ Release v1.1 with non-breaking improvements (especially reduced requirements)
2. ✅ Get more tool manufacturers to adopt v1.1 (easier than v1.0)
3. ⏳ Monitor adoption and gather feedback
4. ⏳ Revisit v2.0 breaking changes when ecosystem is more mature
5. ⏳ Provide migration tooling before releasing v2.0

---

## Migration Strategy for Future v2.0

When stakeholders are ready for v2.0, here's the planned migration path:

### Phase 1: Preparation (Before v2.0 Release)

1. **Create Automated Migration Tool**
   ```python
   # Proposed tool: v1-to-v2-converter
   python convert_metadata.py --input v1_file.json --output v2_file.json
   ```
   
   Features:
   - Convert all property names to camelCase
   - Restructure ROI sections
   - Update enum values
   - Validate output against v2 schema

2. **Bi-Directional Support Library**
   ```python
   # Proposed library: fa-metadata-compat
   metadata = FAMetadata.load('file.json')  # Auto-detects v1 or v2
   metadata.save('output.json', version='2.0')  # Can convert on save
   ```

3. **Comprehensive Testing**
   - Test migration tool with real-world v1 files
   - Validate round-trip conversion (v1 → v2 → data integrity check)
   - Performance testing with large datasets

### Phase 2: Parallel Support (First 12 Months After v2.0)

1. **Tools Support Both Versions**
   - Manufacturers update software to read both v1.x and v2.0
   - Export preference setting (default: v1.1, option: v2.0)
   - Version detection from file content

2. **Migration Assistance**
   - Document migration in QUICK_START.md
   - Provide code examples in Python, JavaScript, C++
   - Webinars/tutorials for manufacturers

3. **Deprecation Warnings**
   - v1.x schemas marked as "legacy" in documentation
   - Clear timeline for v1.x end-of-support (e.g., 2027)

### Phase 3: v2.0 Primary (12-24 Months After Release)

1. **New Implementations Use v2.0**
   - Documentation primarily shows v2.0 examples
   - v1.x support maintained but not featured

2. **Data Migration Campaigns**
   - Organizations convert their historical data
   - Migration tool integrated into analysis software

3. **v1.x Legacy Support**
   - Schemas still available but not actively developed
   - Only critical bug fixes, no new features

### Phase 4: v1.x End-of-Life (24+ Months)

1. **v2.0 Required for New Tools**
   - Certification/compliance requires v2.0 support

2. **v1.x Deprecated**
   - Schemas moved to `schema/legacy/v1/`
   - Still available for historical data but not recommended

---

## Automated Migration Example

Here's what the migration tool would do:

**Input (v1.1):**
```json
{
  "General Section": {
    "File Name": "measurement.tiff",
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

**Output (v2.0):**
```json
{
  "generalSection": {
    "fileName": "measurement.tiff",
    "timeStamp": "2025-12-09T10:30:00+01:00",
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

**Mapping Table:**
See `changelog/CHANGELOG_v2.md` (currently references v2.0-draft) for complete property name mappings.

---

## Decision Criteria for v2.0 Release

v2.0 should be released when:

### Adoption Metrics
- [ ] At least 5 tool manufacturers have implemented v1.1
- [ ] At least 3 analysis software tools support v1.1 reading
- [ ] Community feedback indicates naming is a pain point

### Tooling Ready
- [ ] Automated migration tool tested and released
- [ ] Bi-directional support library available in Python
- [ ] Example code available in major languages (Python, JavaScript, C++)

### Documentation Complete
- [ ] Migration guide with step-by-step instructions
- [ ] Video tutorials for manufacturers
- [ ] FAQ addressing common migration issues

### Stakeholder Agreement
- [ ] Major tool manufacturers agree on timeline
- [ ] Industry group (FA4.0 or equivalent) endorses v2.0
- [ ] Migration support commitment (12+ months parallel support)

### Timeline
**Earliest realistic date:** Q3 2026 (18 months from now)
- Assumes strong v1.1 adoption in 2025-2026
- Allows time for tooling development
- Provides migration window

---

## Current v2.0-Draft Status

**Location:** `schema/v2-draft/`

**Files:**
- `famSchema.json` - Root schema combining all sections
- `generalSection.json` - General metadata
- `methodSpecific.json` - SEM/FIB/Optical parameters
- `dataEvaluation.json` - POIs/ROIs
- `customerSection.json` - Custom fields
- `toolSpecific.json` - Vendor-specific
- `historySection.json` - Workflow tracking
- `examples/` - Complete examples in v2 format

**Status:** 
- ⚠️ **Clearly marked as DRAFT** with warnings in schema files
- ⚠️ **Not for production use**
- ⚠️ **May change before official v2.0 release**

**Purpose:**
- Reference implementation for future v2.0
- Discussion basis for naming conventions
- Testing ground for schema improvements

---

## Recommendations

### For Tool Manufacturers (Now)
1. ✅ **Implement v1.1** - Get the benefits of reduced requirements without breaking changes
2. ⏸️ **Don't implement v2.0-draft** - It may change before official release
3. 📋 **Provide feedback** - Help shape what v2.0 should include

### For Analysis Software Developers (Now)
1. ✅ **Support v1.1 reading** - Current stable version
2. ✅ **Detect version** - Check for "Version" field or property naming style
3. 📋 **Prepare for future** - Design code to handle multiple schema versions

### For Data Scientists (Now)
1. ✅ **Use v1.1 for new projects** - Current stable version
2. ✅ **Accept v1.0 and v1.1** - They're compatible
3. ⏸️ **Wait for v2.0** - Don't use v2.0-draft data yet

---

## Questions & Answers

### Q: Can I use v2.0-draft now?
**A:** Not recommended. It's experimental and may change. Use v1.1 for production.

### Q: Will v2.0 definitely happen?
**A:** Likely, but timing depends on v1.1 adoption and stakeholder readiness. It's not on a fixed timeline.

### Q: What if I've already implemented v2.0-draft?
**A:** Migrate back to v1.1 for now, or maintain both versions. When v2.0 is officially released, you'll need to verify compatibility with the final spec.

### Q: How long will v1.x be supported?
**A:** At minimum until 2027, possibly longer. v1.1 is the current stable version and will be supported for years.

### Q: Can I influence what goes into v2.0?
**A:** Yes! Provide feedback through GitHub issues or contact the maintainers. Community input will shape the final v2.0.

### Q: Will there be a v3.0 someday?
**A:** Hopefully not needed! The goal is for v2.0 to be stable long-term. Major versions should be rare.

---

## References

- **Current stable version:** `schema/v1.1/` + `changelog/CHANGELOG_v1.1.md`
- **Legacy version:** `schema/v1/`
- **Draft version:** `schema/v2-draft/` + `changelog/CHANGELOG_v2.md`
- **Version strategy:** `documentation/VERSIONING.md`
- **Main docs:** `README.md`, `QUICK_START.md`

---

**Document Status:** Living document - will be updated as decisions are made  
**Next Review:** Q2 2026 (evaluate v1.1 adoption and readiness for v2.0)  
**Maintainer:** FA Metadata Header Initiative
