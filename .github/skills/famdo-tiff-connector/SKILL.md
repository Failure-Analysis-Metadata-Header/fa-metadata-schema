---
name: famdo-tiff-connector
description: 'Use when creating or updating a FAMH connector or mapping JSON from a TIFF file with famdo. Extract TIFF metadata with the famdo CLI, map tags to FAMH connector fields using tag IDs, add transform invocations when needed, validate the connector JSON, and write unresolved or ambiguous tags to a sidecar .unresolved.json file instead of guessing.'
argument-hint: 'Path to the TIFF file and desired connector or mapping file name'
user-invocable: true
disable-model-invocation: false
---

# Famdo TIFF Connector

Create a conservative connector or mapping JSON for the FA Metadata Header (FAMH) schema from TIFF metadata extracted with the `famdo` CLI.

This skill builds files such as `connectors/mappings/my-tool.json` from a real TIFF
sample. It prioritizes a schema-valid connector over aggressive guessing. When a
tag, transform, required FAMH field, or contextual decision cannot be resolved
confidently, keep the connector free of speculative mappings and write a
machine-readable `.unresolved.json` sidecar for human review.

## When to Use

- Build a new connector from a TIFF file
- Update an existing connector after inspecting a new tool's TIFF metadata
- Convert `famdo extract` output into `connectors/mappings/*.json`
- Identify which TIFF tags can map directly to FAMH and which need transforms or user decisions

## Preconditions

- A TIFF file is available for inspection
- `famdo` is installed or a local checkout is available
- The target connector should follow `connectors/connector-schema.json`
- The target mappings should default to FAMH `v1.1` unless the user explicitly asks for another version
- `famdo map` supports connector target versions `1` and `1.1`; target version `2` requires a separately designed connector mapping

## Procedure

1. Confirm the sample TIFF path and decide the connector output path.

   Preferred output location: `connectors/mappings/<name>.json`

   Preferred unresolved sidecar path: `connectors/mappings/<name>.unresolved.json`

2. Run metadata extraction with `famdo`.

   Preferred command:

   ```bash
   famdo extract <path-to-image.tif> -o <extracted-json>
   ```

   If `famdo` is not on `PATH` but a local checkout exists, use the local binary or
   `cargo run -- extract` from that repo.

   The command may return status `1` when it writes metadata with extraction
   diagnostics. Do not ignore those diagnostics: retain the extracted JSON for
   inspection and record each blocking issue in the unresolved sidecar.

3. Inspect the extracted metadata.

   For mappings, use `ifds[0].tags` (or the compatible top-level `tags` array):

   - tag `id`
   - tag `name`
   - sample `value`
   - TIFF value `type`

   Also inspect:

   - `diagnostics`: tag-read or unsupported-value problems that block mapping
   - `ifds`: additional image directories; `famdo map` currently reads IFD 0 only

   Do not infer that a tag in another IFD applies to IFD 0. If multi-IFD
   semantics matter for the connector, create an unresolved review item.

4. Build the connector skeleton.

   Start with:

   ```json
   {
     "$schema": "../connector-schema.json",
     "name": "<Connector Name>",
     "version": "1.0.0",
     "targetSchemaVersion": "1.1",
     "mappings": []
   }
   ```

5. Add direct mappings first.

   Use direct mappings only when the TIFF value can be copied into the FAMH
   target without conversion and its extracted JSON type matches the target
   field. Do not add a placeholder value just to satisfy a required FAMH field.

   Typical baseline mappings when present:

   - `ImageWidth` (256) -> `/General Section/Image Width/Value`
   - `ImageLength` (257) -> `/General Section/Image Height/Value`
   - constant `"px"` -> `/General Section/Image Width/Unit`
   - constant `"px"` -> `/General Section/Image Height/Unit`
   - `BitsPerSample` (258) -> `/General Section/Bit Depth` when the extracted
     value has the shape expected by the target schema
   - `Make` (271) -> `/General Section/Manufacturer`
   - `Model` (272) -> `/General Section/Tool Name`

   Do not copy the extracted `filename` into a connector constant for a
   reusable connector. It identifies the sample path, not a TIFF tag. If the
   target FAMH version requires `/General Section/File Name` and no runtime
   source is available, record that target as unresolved instead of baking the
   sample filename into every mapped output.

6. Add transform-based mappings where a transform definition already exists.

   Rules:

   - Use tag IDs as the canonical identifier in every `tiff-tag` source.
   - Keep `name` for readability when available.
   - Use the string `transform` shorthand only for simple one-input transforms.
   - Use the object `transform` form when the transform requires extra named inputs or parameters.
   - Bind additional transform inputs through `transform.inputs`.
   - Bind optional transform parameters through `transform.parameters`.
   - Check the transform definition in `connectors/transforms/` before using it.

   Current standard examples:

   - `DateTime` (306) + `datetime-tiff-to-iso8601`; provide an explicit
     `timezone_offset`, or leave it unresolved rather than guessing
   - `XResolution` (282) + `ResolutionUnit` (296) + `resolution-to-nm-per-px`
   - `YResolution` (283) + `ResolutionUnit` (296) + `resolution-to-nm-per-px`
   - `PhotometricInterpretation` (262) + `photometric-to-color-mode`

7. Add required companion mappings for transformed targets when needed.

   Example:

   - If mapping `Pixel Width/Value` or `Pixel Height/Value`, also add the corresponding `Unit` mapping, typically constant `"nm"`.

8. Do not guess when the semantics are unclear.

   A tag should be left out of the connector if any of the following is true:

   - multiple FAMH targets are plausible
   - the meaning depends on vendor-specific knowledge that is not present
   - the extracted value is insufficient to derive the target confidently
   - no transform definition exists for the required conversion

9. Write unresolved items outside the connector JSON.

   Keep the connector file schema-valid. Do not insert `_note`, `todo`, or comment-like properties into the JSON.

    If unresolved items remain, create a sidecar JSON file next to the connector file using the same base name with the suffix `.unresolved.json`.

   Validate the sidecar against [`connectors/unresolved-schema.json`](../../../connectors/unresolved-schema.json).
   For a connector under `connectors/mappings/`, use `../unresolved-schema.json`
   in the sidecar's `$schema` field.

   Structure:

   ```json
   {
     "$schema": "../unresolved-schema.json",
     "version": "1.0.0",
     "status": "needs-review",
     "sourceImage": "<path-to-image.tif>",
     "connectorPath": "connectors/mappings/<name>.json",
     "unresolved": [
       {
         "kind": "vendor-specific-tag",
         "id": 34682,
         "name": "Unknown(34682)",
         "sampleValue": "...",
         "candidateTargets": [
           "/Tool Specific/..."
         ],
         "reason": "Meaning depends on vendor-specific knowledge not available from the sample."
       },
       {
         "kind": "missing-context",
         "id": 306,
         "name": "DateTime",
         "sampleValue": "2025:12:09 14:30:00",
         "target": "/General Section/Time Stamp",
         "question": "Which timezone applies to this acquisition?",
         "reason": "TIFF DateTime has no timezone and famdo map will not guess one."
       }
     ]
   }
   ```

   Each unresolved entry should capture:

   - a `kind` describing the review category
   - TIFF tag `id` and `name`, when applicable
   - sample value, when available
   - likely candidate FAMH target path or paths, if any
   - transform ID or a concrete reviewer `question`, when applicable
   - reason the mapping was not added

   If there are no unresolved items, do not create the sidecar file.

10. Validate the connector and sample mapping before finishing.

   At minimum:

   - validate JSON syntax
   - validate against `connectors/connector-schema.json`
   - validate any `.unresolved.json` sidecar against `connectors/unresolved-schema.json`
   - check that multi-input transform bindings are present when required
   - check that transformed numeric value fields also have appropriate unit mappings when needed
   - run `famdo map <image> <connector> --out <candidate-output>`

   `famdo map` validates the mapped FAMH document before writing it. Treat the
   outcomes as follows:

   - **Ready:** map succeeds and writes the candidate output. No unresolved
     sidecar is needed.
   - **Needs review:** the connector is schema-valid but map reports missing
     required FAMH fields, ambiguous values, extraction diagnostics, or an
     unsupported transform. Keep the connector, record every blocking issue in
     the sidecar, and do not claim that the connector produces a complete FAMH
     document.

## Decision Rules

- Default to FAMH `v1.1`
- Prefer exact schema field names and valid JSON Pointers
- Prefer direct mappings over transforms when no conversion is needed
- Prefer existing transform definitions over inventing new conversions ad hoc
- Prefer omission plus explicit review notes over speculative mappings
- Prefer tool-agnostic standard TIFF tags first, then vendor-specific tags only when the meaning is clear

## Completion Criteria

The task is complete when all of the following are true:

- The connector JSON is valid against `connectors/connector-schema.json`
- Every `tiff-tag` mapping uses numeric `id`
- Every transform invocation matches the transform definition shape as closely as the connector schema allows
- Directly mappable baseline TIFF tags have been included when present
- Ambiguous or unresolved tags are written to `<name>.unresolved.json` when any exist
- A successful sample mapping was written and validated, or the connector is explicitly marked as needing review with a schema-valid sidecar
- The final response states what was created, what was validated, and what still needs a decision

## Final Response Format

Include:

- the created or updated connector path
- the unresolved sidecar path, if one was created
- whether connector-schema validation passed
- whether unresolved-schema validation passed, if a sidecar was created
- a short summary of direct mappings and transform-based mappings added
- a short summary of unresolved tags needing user input

## Notes

- This skill is intentionally conservative. A smaller valid connector plus a clean unresolved sidecar file is better than an overfit connector with wrong mappings.
- Keep the unresolved sidecar machine-readable. Do not mix prose paragraphs into the JSON file.
- A schema-valid connector is not necessarily complete: `famdo map` must also
  succeed for the sample before the connector is presented as production-ready.
