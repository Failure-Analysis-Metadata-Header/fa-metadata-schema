# Versioning Strategy

**Last Updated:** November 13, 2025  
**Current Version:** 2.0

## Overview

The FA Metadata Header standard uses a hybrid versioning approach that balances stability with evolution:

- **Major versions** (breaking changes) → Separate folders
- **Minor versions** (non-breaking changes) → Schema version field

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
├── v1/          # Version 1.x schemas
│   ├── General Section.json
│   └── ...
├── v2/          # Version 2.x schemas
│   ├── generalSection.json
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

### Version 2.0 (November 2025)
**Status:** Current  
**Type:** Major (breaking changes)  
**Location:** `schema/v2/`

**Key Changes:**
- Property names converted to camelCase (breaking)
- Required fields reduced from 26 to 5 (breaking)
- Proper JSON Schema Draft 07 structure
- Fixed naming inconsistencies
- Comprehensive documentation

**Migration Required:** Yes - see [CHANGELOG_v2.md](CHANGELOG_v2.md)

### Version 1.0 (Pre-2025)
**Status:** Legacy (preserved)  
**Type:** Initial release  
**Location:** `schema/v1/`

**Preserved For:**
- Backward compatibility reference
- Migration assistance
- Historical documentation

## Version Numbering

We follow **semantic versioning** principles:

**X.Y format**
- **X** (Major): Breaking changes, requires migration
- **Y** (Minor): Non-breaking additions/clarifications

**Examples:**
- `1.0` → `2.0`: Breaking changes (property renaming)
- `2.0` → `2.1`: Added optional fields
- `2.1` → `2.2`: Clarified descriptions, fixed typos

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
  "generalSection": {
    "headerType": "FA4.0 Metadata Header",
    "version": "2.0",
    "fileName": "...",
    ...
  }
}
```

**Reading Different Versions:**

Tools should detect and handle multiple versions:

```python
def load_metadata(json_file):
    data = json.load(json_file)
    
    # Detect version
    version = data.get("generalSection", {}).get("version", "1.0")
    
    if version.startswith("1."):
        return normalize_v1(data)  # Convert v1 to internal format
    elif version.startswith("2."):
        return normalize_v2(data)  # Use v2 directly
    else:
        raise ValueError(f"Unsupported version: {version}")
```

### For Schema Maintainers

**Adding Optional Field (Minor Version):**

```json
// In schema/v2/generalSection.json
{
  "version": "2.1",  // Increment from 2.0
  "properties": {
    "generalSection": {
      "properties": {
        "newOptionalField": {  // New field
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
# 1. Create new version directory
mkdir schema/v3

# 2. Copy v2 schemas as starting point
cp schema/v2/*.json schema/v3/

# 3. Make breaking changes in v3 files
# 4. Update version fields to "3.0"
# 5. Create CHANGELOG_v3.md
# 6. Update README.md to reference v3 as current
```

## Deprecation Policy

When creating a new major version:

1. **Previous major version remains available** for at least 2 years
2. **Clear migration documentation** must be provided
3. **Both versions coexist** in the repository
4. **README indicates current version** but links to legacy versions

**Example:**
- v2.0 released November 2025
- v1.0 remains in `schema/v1/` until at least November 2027
- New implementations should use v2.0
- Existing v1.0 implementations can migrate at their own pace

## FAQ

**Q: Can I use v1.0 for new implementations?**  
A: No, please use the current version (v2.0). v1.0 is preserved only for backward compatibility.

**Q: Will my v1.0 files stop working?**  
A: No, v1.0 schemas remain in the repository. However, new tools may only support v2.0+.

**Q: How do I migrate from v1.0 to v2.0?**  
A: See [CHANGELOG_v2.md](CHANGELOG_v2.md) for complete migration guide including property mapping tables.

**Q: What if I find a bug in a schema?**  
A: Report it as an issue. Bug fixes are released as minor version updates (e.g., 2.0 → 2.1).

**Q: Can minor versions add required fields?**  
A: No, adding required fields is a breaking change and requires a new major version.

**Q: How do I know which version a JSON file uses?**  
A: Check the `version` field in the `generalSection`. If missing, assume v1.0.

## Resources

- **Current Version:** [schema/v2/](schema/v2/) - Version 2.0
- **Legacy Version:** [schema/v1/](schema/v1/) - Version 1.0
- **Migration Guide:** [CHANGELOG_v2.md](CHANGELOG_v2.md)
- **Quick Start:** [QUICK_START.md](QUICK_START.md)
- **Implementation Summary:** [IMPLEMENTATION_SUMMARY.md](IMPLEMENTATION_SUMMARY.md)

---

**Note:** This versioning strategy may be refined based on community feedback and real-world usage patterns.
