---
name: famdo-tiff-connector
description: 'Use when creating or updating a FAMH connector or mapping JSON from a TIFF file with famdo. Extract TIFF metadata with the famdo CLI, map tags to FAMH connector fields using tag IDs, add transform invocations when needed, validate the connector JSON, and write unresolved or ambiguous tags to a sidecar .unresolved.json file instead of guessing.'
argument-hint: 'Path to the TIFF file and desired connector or mapping file name'
user-invocable: true
disable-model-invocation: false
---

# Famdo TIFF Connector

Create a valid connector or mapping JSON for the FA Metadata Header (FAMH) schema from TIFF metadata extracted with the `famdo` CLI.

This skill is for building files such as `connectors/mappings/my-tool.json` from a real TIFF sample. It prioritizes a valid connector file over aggressive guessing. When a tag cannot be mapped confidently, keep the connector valid and write the unresolved item to a sidecar `.unresolved.json` file for user review.

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

## Procedure

1. Confirm the sample TIFF path and decide the connector output path.

   Preferred output location: `connectors/mappings/<name>.json`

   Preferred unresolved sidecar path: `connectors/mappings/<name>.unresolved.json`

2. Run metadata extraction with `famdo`.

   Preferred command:

   ```bash
   famdo extract <path-to-image.tif> -o <extracted-json>
   ```

   If `famdo` is not on `PATH` but a local checkout exists, use the local binary or `cargo run` from that repo.

3. Inspect the extracted tag list.

   Focus on:

   - tag `id`
   - tag `name`
   - sample `value`
   - TIFF value `type`

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

   Use direct mappings only when the TIFF value can be copied into the FAMH target without conversion.

   Typical baseline mappings when present:

   - `ImageWidth` (256) -> `/General Section/Image Width/Value`
   - `ImageLength` (257) -> `/General Section/Image Height/Value`
   - constant `"px"` -> `/General Section/Image Width/Unit`
   - constant `"px"` -> `/General Section/Image Height/Unit`
   - `BitsPerSample` (258) -> `/General Section/Bit Depth`
   - `Make` (271) -> `/General Section/Manufacturer`
   - `Model` (272) -> `/General Section/Tool Name`

6. Add transform-based mappings where a transform definition already exists.

   Rules:

   - Use tag IDs as the canonical identifier in every `tiff-tag` source.
   - Keep `name` for readability when available.
   - Use the string `transform` shorthand only for simple one-input transforms.
   - Use the object `transform` form when the transform requires extra named inputs or parameters.
   - Bind additional transform inputs through `transform.inputs`.
   - Bind optional transform parameters through `transform.parameters`.

   Current standard examples:

   - `DateTime` (306) + `datetime-tiff-to-iso8601`
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

    Recommended structure:

    ```json
    {
       "sourceImage": "<path-to-image.tif>",
       "connectorPath": "connectors/mappings/<name>.json",
       "unresolved": [
          {
             "id": 34682,
             "name": "Unknown(34682)",
             "sampleValue": "...",
             "candidateTargets": [
                "/Tool Specific/..."
             ],
             "reason": "Meaning depends on vendor-specific knowledge not available from the sample."
          }
       ]
    }
    ```

    Each unresolved entry should capture:

   - TIFF tag ID and name
   - sample value
    - likely candidate FAMH target path or paths, if any
   - reason the mapping was not added

    If there are no unresolved items, do not create the sidecar file.

10. Validate the connector before finishing.

    At minimum:

    - validate JSON syntax
    - validate against `connectors/connector-schema.json`
    - check that multi-input transform bindings are present when required
    - check that transformed numeric value fields also have appropriate unit mappings when needed

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
- The final response states what was created, what was validated, and what still needs a decision

## Final Response Format

Include:

- the created or updated connector path
- the unresolved sidecar path, if one was created
- whether connector-schema validation passed
- a short summary of direct mappings and transform-based mappings added
- a short summary of unresolved tags needing user input

## Notes

- This skill is intentionally conservative. A smaller valid connector plus a clean unresolved sidecar file is better than an overfit connector with wrong mappings.
- Keep the unresolved sidecar machine-readable. Do not mix prose paragraphs into the JSON file.