# Product design

TRC currently has no end-user UI. The first implementation is library/application contracts; REST/CLI and a Review/Correction UI are later interfaces over the same use cases.

## Future review workflow

1. Show page image and recognized structure without altering raw evidence.
2. Highlight low-confidence regions/tokens and explain `REVIEW_REQUIRED`.
3. Let the user compare alternatives, edit text/layout, mark correct/uncertain/ignored and rerun a selected scope.
4. Preview the new revision and provenance before commit.
5. Expose revision history, diff and rollback; clearly distinguish raw, current and selected historical view.
6. Ask separately for training/export consent; never bundle it with correction acceptance.

## Required states

- loading/progress with page and pipeline stage;
- empty/no recognized content without fabricated text;
- review-required with count and navigation;
- partial/fallback warning with usable output;
- fatal safe error with retryability/correlation ID;
- cancellation pending/cancelled;
- revision conflict with refresh/compare rather than silent overwrite;
- offline/privacy indicator showing enforced mode.

## Interaction constraints

Coordinates and provenance must allow bidirectional selection between text and source image. Keyboard navigation, focus visibility, semantic labels, zoom and non-color confidence cues are mandatory when UI work starts. Responsive layout must keep image/text comparison usable; exact visual tokens are intentionally undecided until a UI stage and must not be invented here.

The UI must not expose vendor-engine controls as required application concepts. Advanced engine selection may be an optional diagnostic control governed by capabilities and privacy policy.
