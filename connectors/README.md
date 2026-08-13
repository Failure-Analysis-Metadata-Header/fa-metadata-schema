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
| `transform` | no | Optional transform invocation. Can be a string ID for a simple one-input transform or an object that names the primary input, binds additional inputs, and passes parameters. |

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

### Transform invocation

When a mapping includes a transform, the top-level `source` still provides the main value for the mapping. In the object form, `transform.primaryInput` names which transform input receives that source value.

Use the string shorthand when the transform only needs that one primary input:

```json
{
  "source": { "type": "tiff-tag", "id": 306, "name": "DateTime" },
  "transform": "datetime-tiff-to-iso8601",
  "target": "/General Section/Time Stamp"
}
```

Use the object form when the transform needs more than one runtime input or when you want to pass transform parameters:

```json
{
  "source": { "type": "tiff-tag", "id": 282, "name": "XResolution" },
  "transform": {
    "id": "resolution-to-nm-per-px",
    "primaryInput": "resolution",
    "inputs": {
      "resolution_unit": { "type": "tiff-tag", "id": 296, "name": "ResolutionUnit" }
    }
  },
  "target": "/General Section/Pixel Width/Value"
}
```

If a transform definition declares optional parameters, pass them through `transform.parameters`:

```json
{
  "source": { "type": "tiff-tag", "id": 306, "name": "DateTime" },
  "transform": {
    "id": "datetime-tiff-to-iso8601",
    "primaryInput": "value",
    "parameters": {
      "timezone_offset": "+01:00"
    }
  },
  "target": "/General Section/Time Stamp"
}
```

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

> **Tool support may still be partial.** The connector schema now defines how transform invocations are expressed, but consuming tools may not yet implement every transform or invocation feature.

Transform definitions live in [`transforms/`](transforms/) and are validated against [`transforms/transform-schema.json`](transforms/transform-schema.json). Each file describes:

- The runtime input set (`inputs`), including type and optional format hints
- The output type and format
- Any configurable parameters
- Optional `appliesTo` scope for source-format-specific assumptions (for example TIFF)
- Optional `behavior` rules for missing, invalid, or unknown values
- Optional worked `examples`
- Implementation notes and edge cases

### Available transform definitions

| Transform ID | File | Description |
|---|---|---|
| `datetime-tiff-to-iso8601` | [transforms/datetime-tiff-to-iso8601.json](transforms/datetime-tiff-to-iso8601.json) | Convert TIFF `DateTime` (`"YYYY:MM:DD HH:MM:SS"`) to ISO 8601 (`"YYYY-MM-DDTHH:MM:SS+HH:MM"`) |
| `rational-to-float` | [transforms/rational-to-float.json](transforms/rational-to-float.json) | Convert TIFF rational string `"N/D"` to a floating-point number |
| `resolution-to-nm-per-px` | [transforms/resolution-to-nm-per-px.json](transforms/resolution-to-nm-per-px.json) | Convert XResolution/YResolution + ResolutionUnit to nm/px |
| `photometric-to-color-mode` | [transforms/photometric-to-color-mode.json](transforms/photometric-to-color-mode.json) | Map `PhotometricInterpretation` integer to FAMH Color Mode string |

The current transform catalog intentionally mixes generic transforms and TIFF-specific transforms:

- `rational-to-float` is generic for any extractor that represents fractions as strings like `"N/D"`.
- `datetime-tiff-to-iso8601`, `resolution-to-nm-per-px`, and `photometric-to-color-mode` are explicitly TIFF-specific and mark that via `appliesTo.sourceFormat` and TIFF-oriented `format` hints.

### Using a transform in a mapping

Simple one-input transforms can use the string shorthand:

```json
{
  "source": { "type": "tiff-tag", "id": 306, "name": "DateTime" },
  "transform": "datetime-tiff-to-iso8601",
  "target": "/General Section/Time Stamp"
}
```

Transforms with multiple runtime inputs should use the object form:

```json
{
  "source": { "type": "tiff-tag", "id": 282, "name": "XResolution" },
  "transform": {
    "id": "resolution-to-nm-per-px",
    "primaryInput": "resolution",
    "inputs": {
      "resolution_unit": { "type": "tiff-tag", "id": 296, "name": "ResolutionUnit" }
    }
  },
  "target": "/General Section/Pixel Width/Value"
}
```

---

## Available Connectors

| File | Target version | Source | Description |
|---|---|---|---|
| [mappings/tiff-standard.json](mappings/tiff-standard.json) | v1.1 | Standard TIFF tags | Maps baseline TIFF 6.0 tags (ImageWidth, ImageLength, BitsPerSample, Make, Model) to FAMH fields. Tool-agnostic, but not sufficient by itself for every required FAMH field. |

> Vendor-specific connectors (ZEISS, FEI/Thermo Fisher, Tescan, …) will be added to this directory as they are developed. Vendor tools typically embed rich acquisition parameters in private TIFF tags or in structured text within the `ImageDescription` tag (256), which will require an additional source type (`tiff-embedded-text`) and vendor-specific transform definitions.

---

## Writing a New Connector

### 1 – Extract metadata from your image

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
    { "id": 256, "tag": "ImageWidth", "value": 1024, "type": "Short" },
    { "id": 271, "tag": "Make", "value": "ZEISS", "type": "ASCII" },
    { "id": 306, "tag": "DateTime", "value": "2025:12:09 14:30:00", "type": "ASCII" }
  ],
  "ifds": [
    {
      "index": 0,
      "dimensions": { "width": 1024, "height": 768 },
      "tags": [
        { "id": 256, "tag": "ImageWidth", "value": 1024, "type": "Short" },
        { "id": 271, "tag": "Make", "value": "ZEISS", "type": "ASCII" },
        { "id": 306, "tag": "DateTime", "value": "2025:12:09 14:30:00", "type": "ASCII" }
      ]
    }
  ],
  "diagnostics": []
}
```

The top-level `dimensions` and `tags` fields are the compatible IFD 0 view.
The `ifds` array contains every image directory. `famdo map` currently reads
IFD 0 only, so do not map tags from another IFD without confirming the intended
semantics. Treat non-empty `diagnostics` as review items rather than guessing.

The connector should use the numeric TIFF tag ID as the canonical identifier and
may keep the human-readable `tag` value as `name`.

### 2 – Create the connector file

Create `connectors/mappings/my-tool.json` from the repository root, referencing
the schema in the parent `connectors` directory:

```json
{
  "$schema": "../connector-schema.json",
  "name": "My Tool",
  "version": "1.0.0",
  "targetSchemaVersion": "1.1",
  "mappings": [...]
}
```

Map each extracted tag to the appropriate JSON Pointer target. For tags whose values need conversion, use a `transform` entry and bind any additional transform inputs or parameters that the transform definition requires.

### 3 – Validate the connector and sample mapping

Validate your connector against the schema using any JSON Schema Draft 07 validator, for example:

```bash
python3 -c "
import json, jsonschema
schema = json.load(open('connectors/connector-schema.json'))
data   = json.load(open('connectors/mappings/my-tool.json'))
jsonschema.validate(data, schema)
print('Valid')
"
```

Then apply it to the sample TIFF:

```bash
famdo map my_image.tif mappings/my-tool.json -o mapped.json
```

`famdo map` validates the connector and the resulting FAMH document before it
writes `mapped.json`. It reads TIFF tags from IFD 0 and does not guess missing
context such as a timezone. The extracted sample filename is also not a
connector source; do not turn it into a constant unless the connector is
intentionally limited to that one image.

### 4 – Record unresolved review items

If the connector is schema-valid but the sample cannot produce a complete FAMH
document, do not add placeholder mappings. Create
`mappings/my-tool.unresolved.json` and validate it against
[unresolved-schema.json](unresolved-schema.json):

```json
{
  "$schema": "../unresolved-schema.json",
  "version": "1.0.0",
  "status": "needs-review",
  "sourceImage": "my_image.tif",
  "connectorPath": "mappings/my-tool.json",
  "unresolved": [
    {
      "kind": "missing-required-target",
      "target": "/General Section/Method",
      "candidateTargets": [
        "/General Section/Method"
      ],
      "question": "Which acquisition method should be recorded?",
      "reason": "The sample TIFF does not contain enough information to determine the FAMH method."
    }
  ]
}
```

Sidecars are required only when unresolved items exist. A connector is
production-ready only after the connector schema passes and `famdo map`
succeeds for the representative sample; otherwise the sidecar is the handoff
for human review.

The repository also provides an agent workflow for this process in
[`famdo-tiff-connector`](../.github/skills/famdo-tiff-connector/SKILL.md).
