---
name: famdo-tiff-connector
description: 'Use when creating or updating a FAMH connector or mapping JSON from one or more TIFF files with famdo. Extract and compare TIFF metadata, map stable tags to FAMH connector fields, validate every sample output, and write unresolved or ambiguous decisions to a sidecar instead of guessing.'
argument-hint: 'One or more TIFF paths, optional tool context, and a connector output path'
user-invocable: true
disable-model-invocation: false
---

# Famdo TIFF Connector

Create a conservative connector or mapping JSON for the FA Metadata Header (FAMH)
schema from one or more TIFF samples extracted with the `famdo` CLI.

This skill builds files such as `connectors/mappings/my-tool.json` from one or
more representative TIFF samples. It prioritizes a schema-valid connector over
aggressive guessing. When a tag, transform, required FAMH field, or contextual
decision cannot be resolved confidently, keep the connector free of speculative
mappings and write a machine-readable `.unresolved.json` sidecar for human review.

The skill is self-contained. The user only needs to provide the TIFF path(s),
any known vendor/instrument/method context, and the desired connector output
path. Do not ask the user to repeat the extraction, mapping, validation, or
review procedure described below.

## When to Use

- Build a new connector from one or more TIFF files
- Update an existing connector after inspecting a new tool's TIFF metadata
- Convert `famdo extract` output into `connectors/mappings/*.json`
- Identify which TIFF tags can map directly to FAMH and which need transforms or user decisions

## Preconditions

- One or more representative TIFF files are available for inspection
- `famdo` is installed or a local checkout is available
- The target connector should follow `connectors/connector-schema.json`
- The target mappings should default to FAMH `v1.1` unless the user explicitly asks for another version
- `famdo map` supports connector target versions `1` and `1.1`; target version `2` requires a separately designed connector mapping

## Minimal Invocation

An invocation can be as short as:

```text
Use the famdo-tiff-connector skill for these TIFFs:
- /path/to/sample-1.tiff
- /path/to/sample-2.tiff

Known context: <vendor, instrument, and method if known>
Create the connector at: connectors/mappings/<name>.json
```

Treat all other steps in this skill as required implementation work. If known
context is absent, continue conservatively and create unresolved review items
for the missing decisions.

## Procedure

1. Collect the TIFF samples, known context, and connector output path.

   Preferred output location: `connectors/mappings/<name>.json`

   Preferred unresolved sidecar path: `connectors/mappings/<name>.unresolved.json`

   When multiple samples are provided, treat them as one connector family
   candidate and compare them before adding mappings.

2. Run metadata extraction with `famdo` for every sample.

   Preferred command:

   ```bash
   famdo extract <path-to-image.tif> -o <extracted-json>
   ```

   If `famdo` is not on `PATH` but a local checkout exists, use the local binary or
   `cargo run -- extract` from that repo.

   Use a separate output JSON for each input. The command may return status `1`
   when it writes metadata with extraction diagnostics. Continue to inspect that
   output, but record every extraction diagnostic in the unresolved sidecar.

3. Inspect and compare the extracted metadata.

   For mappings, use `ifds[0].tags` (or the compatible top-level `tags` array):

   - tag `id`
   - tag `name`
   - sample `value`
   - TIFF value `type`

   Also inspect:

   - `diagnostics`: tag-read or unsupported-value problems that block mapping
   - `ifds`: additional image directories; `famdo map` currently reads IFD 0 only

   Across multiple samples, distinguish:

   - stable tags and value types that can become connector mappings;
   - optional tags that are absent from some samples;
   - values that vary per image and must not become constants;
   - vendor-specific tags whose meaning needs human confirmation.

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

   Use the `runtime` source for generated FAMH metadata instead of copying
   sample context into constants:

   ```json
   {
     "source": { "type": "runtime", "field": "image-file-name" },
     "target": "/General Section/File Name"
   }
   ```

   Use `{ "type": "runtime", "field": "mapping-timestamp" }` for
   `/General Section/Time Stamp`. These values describe the current mapping
   invocation and do not require sample-specific constants.

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

   If the target schema has no established method-specific subsection, a
   connector may materialize a provisional subsection under
   `/Method Specific/<Method Name>/...` using descriptive field names. Keep
   those fields conservative, preserve raw vendor values when useful, and
   record the provisional structure as a `human-decision` item in the review
   sidecar. A successful schema validation does not make the subsection an
   official FAMH vocabulary.

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
   - run `famdo map <image> <connector> --out <candidate-output>` for every sample
   - run `famdo validate --version v1` (or the selected supported version) for every mapped output

   `famdo map` validates the mapped FAMH document before writing it. Treat the
   outcomes as follows:

   - **Ready:** map and validate succeed for every sample and no unresolved
     sidecar is needed.
   - **Needs review:** the connector is schema-valid but any sample fails
     mapping/validation, or the sidecar contains provisional mappings,
     ambiguous values, extraction diagnostics, or human decisions. Keep the
     connector, record every blocking issue in the sidecar, and do not claim
     production readiness merely because the JSON schema accepts the output.

## Decision Rules

- Default to FAMH `v1.1`
- Prefer exact schema field names and valid JSON Pointers
- Use runtime sources for the generated FAMH filename and mapping timestamp
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
- A mapped and validated output was produced for every representative sample, or the connector is explicitly marked as needing review with a schema-valid sidecar
- The final response states what was created, what was validated, and what still needs a decision

## Final Response Format

Include:

- the created or updated connector path
- the unresolved sidecar path, if one was created
- whether connector-schema validation passed
- whether unresolved-schema validation passed, if a sidecar was created
- a short summary of direct mappings and transform-based mappings added
- the mapped and validated output path for each representative sample
- a short summary of unresolved tags needing user input

## Notes

- This skill is intentionally conservative. A smaller valid connector plus a clean unresolved sidecar file is better than an overfit connector with wrong mappings.
- Keep the unresolved sidecar machine-readable. Do not mix prose paragraphs into the JSON file.
- A schema-valid connector is not necessarily complete: `famdo map` must also
  succeed for the sample before the connector is presented as production-ready.
