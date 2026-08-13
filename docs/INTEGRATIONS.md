# Application integrations

Application integration is an anti-corruption layer around stable TRC contracts. It has two directions:

```text
Consumer request/profile → RecognitionRequest hints
RecognitionResult        → consumer-owned projection
```

Neither direction mutates Core domain or imports consumer business services into it. Every derived field carries provenance to source Region/Line/Token IDs and revision.

## Common adapter contract

```text
ApplicationProfile
  name/version
  required/optional capabilities
  allowed privacy modes
  default language/mode hints

ApplicationProjector[T]
  project(result, revision_id) -> ProjectionResult[T]
  validate_provenance(projection) -> ValidationReport
```

Projection warnings distinguish missing source, low confidence and ambiguous mapping. A projector is deterministic for the same result, revision and adapter version.

## Personal Chronicle

Inputs: `MIXED/HTR`, Ukrainian/Russian/English hints, `LOCAL_ONLY` allowed/expected, layout and uncertain fragments required.

Output concept (consumer-owned): document ID, probable date candidates, entry candidates, uncertain fragments and source references. TRC does not create timeline events, embeddings, RAG, summaries or answers about the diary.

Acceptance: raw page layout remains recoverable; every entry/uncertain fragment references source IDs; no network adapter is selected under `LOCAL_ONLY`.

## Receipt Scanner

Inputs: OCR + layout, country `UA`, currency hint `UAH`, receipt capability optional until supported.

Output concept: merchant/timestamp/items/subtotal/discount/total/currency with confidence and source references for every populated field. Parsing/extraction belongs to integration package; expense categories and analytics belong to Receipt Scanner.

Acceptance: total/item fields link to tokens/regions; ambiguous amounts are warnings, not fabricated values; arithmetic validation cannot overwrite raw text.

## Tutor

Inputs: MIXED, layout, handwriting; future `MATH`, `TABLE`, `DIAGRAM`, `ANSWER_REGION`, `TEACHER_COMMENT` capabilities.

Output concept: printed assignment/handwritten answer/teacher comment region candidates with provenance. Student, lesson, grading and solution generation stay in Tutor.

Acceptance: unsupported required math capability is explicit; optional future capability degrades with warning; printed and handwritten regions can route to different engines.

## New consumer onboarding

1. Define a consumer-owned projection SPEC.
2. Select existing capabilities and privacy modes; new Core capability requires separate review.
3. Implement input profile and projector outside Core domain.
4. Add contract/fixture tests with synthetic or approved data.
5. Prove no direct OCR SDK dependency in the consumer.

Success means the consumer connects through existing TRC API without copying pipeline or correction logic.
