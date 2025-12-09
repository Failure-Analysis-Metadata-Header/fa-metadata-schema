# Versioning Strategy

**Last Updated:** December 9, 2025  
**Current Version:** 1.1 (stable)  
**Draft Version:** 2.0-draft (experimental, not for production)

## Overview

The FA Metadata Header standard uses a hybrid versioning approach that balances stability with evolution:

- **Major versions** (breaking changes) → Separate folders
- **Minor versions** (non-breaking changes) → Schema version field

### December 2025 Update

After stakeholder consultation, we decided to **postpone v2.0's breaking changes** and instead release **v1.1** with non-breaking improvements. The primary concern was property naming changes (spaces to camelCase) affecting existing implementations. v1.1 delivers the most requested feature (reduced required fields) while maintaining full backward compatibility.

## Version Structure

### Major Versions (X.0)

Major versions introduce **breaking changes** that require migration:
- Property name changes
- Required field modifications
- Structural reorganization
- Incompatible enum value changes

**Location:** Separate directories (`schema/v1/`, `schema/v2/`, etc.)

**Example:**
```
schema/
├── v1/          # Version 1.0 schemas (legacy)
│   ├── General Section.json
│   └── ...
├── v1.1/        # Version 1.1 schemas (current stable)
│   ├── General Section.json
│   └── ...
├── v2-draft/    # Version 2.0-draft (experimental, breaking changes)
│   ├── generalSection.json  # ⚠️ Different naming!
│   └── ...
```

**Benefits:**
- ✅ Multiple versions coexist
- ✅ Old implementations continue working
- ✅ Clear migration path
- ✅ Easy version comparison in Git

### Minor Versions (x.Y)

Minor versions introduce **non-breaking changes**:
- New optional fields
- Additional enum values
- Clarified descriptions
- Bug fixes in schema definitions

**Location:** Updated in place within version folder

**Tracking:** Each schema file contains a `"version"` field:
```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "FA Metadata - General Section",
  "version": "2.1",
  "description": "...",
  ...
}
```

## Version History

### Version 1.1 (December 2025)
**Status:** Current stable  
**Type:** Minor (non-breaking improvements)  
**Location:** `schema/v1.1/`

**Key Changes:**
- Required fields reduced from 26 to 5 in General Section
- Required fields reduced from 21 to 3 in SEM method
- Required fields reduced from 23 to 3 in FIB method
- Required fields reduced from 6 to 1 in Optical method
- Added proper JSON Schema structure ($schema, title, version fields)
- Fixed array validation bugs (minItems placement)
- Corrected spelling errors in descriptions
- Added missing type definitions

**Migration Required:** No - fully backward compatible with v1.0

**See:** [CHANGELOG_v1.1.md](../changelog/CHANGELOG_v1.1.md)

### Version 2.0-draft (November 2025)
**Status:** Experimental (NOT FOR PRODUCTION)  
**Type:** Major (breaking changes)  
**Location:** `schema/v2-draft/`

**Key Changes:**
- Property names converted to camelCase (BREAKING)
- All v1.1 improvements included
- Restructured data evaluation section
- Consistent enum value formatting

**Status:** Postponed after stakeholder consultation in December 2025. Breaking changes (especially property naming) were deemed premature given limited v1.0 adoption. Focus shifted to v1.1 non-breaking improvements.

**See:** [FUTURE_V2_MIGRATION.md](FUTURE_V2_MIGRATION.md) for details on future migration path

### Version 1.0 (Pre-2025)
**Status:** Legacy (superseded by v1.1)  
**Type:** Initial release  
**Location:** `schema/v1/`

**Notes:**
- 26 required fields in General Section
- 21 required fields in SEM method
- Difficult for manufacturers to implement

**Preserved For:**
- Backward compatibility reference
- Historical documentation
- Comparison with v1.1 improvements

## Version Numbering

We follow **semantic versioning** principles:

**X.Y format**
- **X** (Major): Breaking changes, requires migration
- **Y** (Minor): Non-breaking additions/clarifications

**Examples:**
- `1.0` → `1.1`: Reduced required fields (non-breaking)
- `1.1` → `2.0`: Property renaming (breaking - when ready)
- `2.0` → `2.1`: Added optional fields (non-breaking)
- `2.1` → `2.2`: Clarified descriptions, fixed typos (non-breaking)

## When to Increment Versions

### Create New Major Version (X.0) When:

❌ **Breaking Changes:**
- Renaming existing properties
- Removing fields
- Changing required field list
- Modifying enum values
- Restructuring nested objects
- Changing data types

**Process:**
1. Create new version folder (`schema/vX/`)
2. Copy existing schemas as starting point
3. Make breaking changes
4. Update all schema `"version"` fields to `X.0`
5. Create CHANGELOG_vX.md documenting changes
6. Update README to point to new version as current

### Increment Minor Version (x.Y) When:

✅ **Non-Breaking Changes:**
- Adding optional properties
- Adding new enum values (if field is optional or has defaults)
- Improving descriptions
- Adding examples
- Fixing documentation errors
- Clarifying validation rules without changing behavior

**Process:**
1. Update schema files in place (e.g., `schema/v2/generalSection.json`)
2. Increment `"version"` field (e.g., `"2.0"` → `"2.1"`)
3. Document changes in CHANGELOG
4. No folder changes needed

## Implementation Guidelines

### For Tool Manufacturers

**Specifying Version in Metadata:**

Include version in your generated metadata files:

```json
{
  "General Section": {
    "Header Type": "FA4.0 Metadata Header",
    "Version": "1.1",
    "File Name": "...",
    ...
  }
}
```

**Reading Different Versions:**

Tools should detect and handle multiple versions:

```python
def load_metadata(json_file):
    data = json.load(json_file)
    
    # Detect version by checking structure
    if "General Section" in data:
        # v1.x format (v1.0 or v1.1)
        version = data.get("General Section", {}).get("Version", "1.0")
        return normalize_v1(data)  # Both v1.0 and v1.1 use same structure
    elif "generalSection" in data:
        # v2.x format (camelCase)
        version = data.get("generalSection", {}).get("version", "2.0")
        return normalize_v2(data)
    else:
        raise ValueError("Unknown metadata format")
```

### For Schema Maintainers

**Adding Optional Field (Minor Version):**

```json
// In schema/v1.1/General Section.json
{
  "version": "1.2",  // Increment from 1.1
  "properties": {
    "General Section": {
      "properties": {
        "New Optional Field": {  // New field
          "type": "string",
          "description": "New optional parameter"
        }
      }
    }
  }
}
```

**Creating New Major Version:**

```bash
# Example: When v2.0 is ready for release
# 1. Rename v2-draft to v2
mv schema/v2-draft schema/v2

# 2. Update all schema version fields to "2.0" (from "2.0-draft")
# 3. Remove DRAFT warnings from schema files
# 4. Rename CHANGELOG_v2.md to final version
# 5. Update README.md to reference v2 as current
# 6. Provide migration tooling (v1-to-v2 converter)
```

## Deprecation Policy

When creating a new major version:

1. **Previous major version remains available** for at least 2 years
2. **Clear migration documentation** must be provided
3. **Both versions coexist** in the repository
4. **README indicates current version** but links to legacy versions
5. **Migration tooling provided** for automated conversion (when applicable)

**Example:**
- v1.1 released December 2025 (current stable)
- v1.0 remains in `schema/v1/` for reference
- v2.0-draft exists in `schema/v2-draft/` but NOT for production use
- v2.0 official release: TBD (earliest Q3 2026)
- When v2.0 is released, v1.1 remains supported until at least Q3 2028

## FAQ

**Q: Can I use v1.0 for new implementations?**  
A: Use v1.1 instead - it's backward compatible with v1.0 but has much fewer required fields (5 instead of 26).

**Q: What's the difference between v1.0 and v1.1?**  
A: v1.1 dramatically reduces required fields but keeps all property names identical. v1.0 files work with v1.1 validators, and v1.1 files work with v1.0 parsers (if they include the formerly required fields).

**Q: Should I use v2.0-draft?**  
A: No! It's experimental and marked as NOT FOR PRODUCTION. Use v1.1 for all production work.

**Q: Will my v1.0 files stop working?**  
A: No, v1.0 files are valid v1.1 files. The schemas are backward compatible.

**Q: When will v2.0 be officially released?**  
A: TBD, depends on v1.1 adoption and stakeholder readiness. Earliest realistic date is Q3 2026. See [FUTURE_V2_MIGRATION.md](FUTURE_V2_MIGRATION.md).

**Q: How do I migrate from v1.0 to v1.1?**  
A: No migration needed! Just update your schema references. v1.1 is fully backward compatible.

**Q: How do I migrate from v1.1 to v2.0 (when it's released)?**  
A: Automated migration tools will be provided. See [FUTURE_V2_MIGRATION.md](FUTURE_V2_MIGRATION.md) for the planned migration strategy.

**Q: What if I find a bug in a schema?**  
A: Report it as an issue. Bug fixes are released as minor version updates (e.g., 1.1 → 1.2).

**Q: Can minor versions add required fields?**  
A: No, adding required fields is a breaking change and requires a new major version.

**Q: How do I know which version a JSON file uses?**  
A: Check the "Version" field in "General Section". If missing, assume v1.0. You can also detect structure: v1.x uses "General Section", v2.x uses "generalSection".

## Resources

- **Current Stable Version:** [schema/v1.1/](../schema/v1.1/) - Version 1.1
- **Legacy Version:** [schema/v1/](../schema/v1/) - Version 1.0
- **Draft Version (NOT FOR PRODUCTION):** [schema/v2-draft/](../schema/v2-draft/) - Version 2.0-draft
- **v1.1 Changes:** [CHANGELOG_v1.1.md](../changelog/CHANGELOG_v1.1.md)
- **Future v2.0 Migration:** [FUTURE_V2_MIGRATION.md](FUTURE_V2_MIGRATION.md)
- **Quick Start:** [QUICK_START.md](../QUICK_START.md)
- **Main Documentation:** [README.md](../README.md)

---

**Note:** This versioning strategy prioritizes stability and backward compatibility. Breaking changes (v2.0) will only be released when the ecosystem is ready and proper migration tooling is available.
