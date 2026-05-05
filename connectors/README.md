# Connectors

Connector files map metadata from image files (e.g. TIFF tags) to fields in the [FA Metadata Header (FAMH)](../README.md) schema. A connector is a plain JSON file that a tool such as [`famdo`](https://github.com/Failure-Analysis-Metadata-Header/famdo) can read to automatically populate an FAMH output document from image metadata.

---

## Connector File Format

Each connector is a JSON object validated against [connector-schema.json](connector-schema.json).

### Top-level fields

| Field | Required | Description |
|---|---|---|
| `$schema` | recommended | URI to `connector-schema.json` |
| `name` | yes | Human-readable connector name |
| `version` | yes | Version string (e.g. `"1.0.0"`) |
| `description` | no | What the connector does and which tool it targets |
| `targetSchemaVersion` | yes | FAMH schema version: `"1"`, `"1.1"`, or `"2"` |
| `mappings` | yes | Array of mapping objects (see below) |

### Mapping objects

Each entry in `mappings` has the following fields:

| Field | Required | Description |
|---|---|---|
| `source` | yes | Where to read the value from (see Source types) |
| `target` | yes | JSON Pointer (RFC 6901) to the field in the FAMH output document |
| `description` | no | Human-readable annotation |
| `required` | no | If `true`, the tool should error when the source value is absent (default: `false`) |
| `transform` | no | **Reserved, not yet implemented.** ID of a transform from `transforms/` to apply to the source value before writing to the target (e.g. `"datetime-tiff-to-iso8601"`) |

### Source types

#### `tiff-tag`
Reads the value of a TIFF tag from the image file.

```json
{ "type": "tiff-tag", "id": 256, "name": "ImageWidth" }
```

- `id` is the canonical TIFF tag ID and should be used for matching across tools. Standard tags keep the same numeric ID regardless of extractor.
- `name` is optional and is kept for readability and documentation. Tools should treat it as informational.
- When a tool exposes both numeric IDs and human-readable names, connector authors should include both.

#### `constant`
Injects a fixed literal value into the target field, regardless of the image content. Useful for units and other fields that are always the same for a given source format.

```json
{ "type": "constant", "value": "px" }
```

`value` may be any JSON type: string, number, boolean, array, or object.

### Target paths

`target` is a [JSON Pointer (RFC 6901)](https://datatracker.ietf.org/doc/html/rfc6901) into the FAMH output document. For FAMH v1.1 (which uses spaces in property names) the paths look like:

```
/General Section/File Name
/General Section/Image Width/Value
/General Section/Image Width/Unit
/General Section/Manufacturer
/General Section/Tool Name
/General Section/Bit Depth
/Method Specific/Scanning Electron Microscopy/Accelerating Voltage/Value
/Data Evaluation/POI/0/Name
```

> **Note:** Spaces in property names do **not** need to be escaped in JSON Pointer — only `/` (as `~1`) and `~` (as `~0`) require escaping.

### Minimal connector example

```json
{
  "$schema": "./connector-schema.json",
  "name": "My Tool Connector",
  "version": "1.0.0",
  "targetSchemaVersion": "1.1",
  "mappings": [
    {
      "source": { "type": "tiff-tag", "id": 256, "name": "ImageWidth" },
      "target": "/General Section/Image Width/Value"
    },
    {
      "source": { "type": "constant", "value": "px" },
      "target": "/General Section/Image Width/Unit"
    },
    {
      "source": { "type": "tiff-tag", "id": 271, "name": "Make" },
      "target": "/General Section/Manufacturer"
    }
  ]
}
```

---

## Transforms

Some source values cannot be written directly to the FAMH target because their format differs from what the schema expects. In these cases a **transform** is needed to convert the value first.

> **Transforms are not yet implemented.** The `transform` field is reserved in the connector schema. The transform definitions below document the planned conversions so that implementations are consistent once support is added.

Transform definitions live in [`transforms/`](transforms/) and are validated against [`transforms/transform-schema.json`](transforms/transform-schema.json). Each file describes:

- The input type and format
- The output type and format
- Any configurable parameters
- Implementation notes and edge cases

### Available transform definitions

| Transform ID | File | Description |
|---|---|---|
| `datetime-tiff-to-iso8601` | [transforms/datetime-tiff-to-iso8601.json](transforms/datetime-tiff-to-iso8601.json) | Convert TIFF `DateTime` (`"YYYY:MM:DD HH:MM:SS"`) to ISO 8601 (`"YYYY-MM-DDTHH:MM:SS+HH:MM"`) |
| `rational-to-float` | [transforms/rational-to-float.json](transforms/rational-to-float.json) | Convert TIFF rational string `"N/D"` to a floating-point number |
| `resolution-to-nm-per-px` | [transforms/resolution-to-nm-per-px.json](transforms/resolution-to-nm-per-px.json) | Convert XResolution/YResolution + ResolutionUnit to nm/px |
| `photometric-to-color-mode` | [transforms/photometric-to-color-mode.json](transforms/photometric-to-color-mode.json) | Map `PhotometricInterpretation` integer to FAMH Color Mode string |

### Using a transform in a mapping (future syntax)

Once implemented, transforms will be referenced by ID in the mapping object:

```json
{
  "source": { "type": "tiff-tag", "id": 306, "name": "DateTime" },
  "transform": "datetime-tiff-to-iso8601",
  "target": "/General Section/Time Stamp"
}
```

---

## Available Connectors

| File | Target version | Source | Description |
|---|---|---|---|
| [tiff-standard.json](tiff-standard.json) | v1.1 | Standard TIFF tags | Maps baseline TIFF 6.0 tags (ImageWidth, ImageLength, BitsPerSample, Make, Model) to FAMH fields. Tool-agnostic. |

> Vendor-specific connectors (ZEISS, FEI/Thermo Fisher, Tescan, …) will be added to this directory as they are developed. Vendor tools typically embed rich acquisition parameters in private TIFF tags or in structured text within the `ImageDescription` tag (256), which will require an additional source type (`tiff-embedded-text`) and vendor-specific transform definitions.

---

## Writing a New Connector

### 1 – Extract tag names from your image

Use `famdo extract` to see what tags are present in a sample image and what values they contain. `famdo` is a convenient reference extractor, but other TIFF tools can be used too as long as they expose the raw TIFF tag IDs:

```bash
famdo extract my_image.tif -o extracted.json
```

The output JSON has the structure:

```json
{
  "filename": "my_image.tif",
  "dimensions": { "width": 1024, "height": 768 },
  "tags": [
    { "tag": "ImageWidth",  "value": 1024,   "type": "Short" },
    { "tag": "Make",        "value": "ZEISS", "type": "ASCII" },
    { "tag": "DateTime",    "value": "2025:12:09 14:30:00", "type": "ASCII" }
  ]
}
```

Use the `tag` string values directly as `name` in `tiff-tag` source objects.

The connector should still use the numeric TIFF tag ID as the canonical identifier. If your extractor reports IDs separately, copy those into `id` and keep the human-readable name in `name`. If your extractor reports only names, you should look up the corresponding TIFF tag IDs before finalizing the connector.

### 2 – Create the connector file

Create a new JSON file in this directory (e.g. `my-tool.json`) referencing `connector-schema.json`:

```json
{
  "$schema": "./connector-schema.json",
  "name": "My Tool",
  "version": "1.0.0",
  "targetSchemaVersion": "1.1",
  "mappings": [...]
}
```

Map each extracted tag to the appropriate JSON Pointer target. For tags whose values need conversion, document them in `_pendingMappings` (like `tiff-standard.json`) until transform support is available.

### 3 – Validate the connector

Validate your connector against the schema using any JSON Schema Draft 07 validator, for example:

```bash
python3 -c "
import json, jsonschema
schema = json.load(open('connector-schema.json'))
data   = json.load(open('my-tool.json'))
jsonschema.validate(data, schema)
print('Valid')
"
```

