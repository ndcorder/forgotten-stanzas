# The Annotation

**Domain:** annotation  
**ID:** 0010  
**Mean rating:** 4.3

## Proposal

ideas:
  - title: The Annotation
    domain: annotation
    pitch: "A single page of a physics textbook — dense, correct, unremarkable —
      heavily annotated in pencil by an unknown student who is slowly realizing
      something the textbook isn't saying. The footnotes, margins, and
      interlinear comments start as clarifications, become questions, then
      become something else entirely: a second argument running parallel to the
      official text, written by someone who understands the equations better
      than the author did. The PDF is the artifact; the annotations are the
      story."
    complexity: M
    why: Annotation domain is untouched — this is narrative through scholarly
      apparatus, a ghost story told in margins.
    project_id: null
    stimulus_ref: "speculative-design.md — 'Artifacts from alternate presents'
      transformed: the present is a used textbook, the alternate reality is what
      someone found in the equations"
    xl_mode: null
    project: null


## Critic Review

The CSS for "The Annotation" is a masterclass in restrained atmospheric design — a stylesheet that makes you feel graphite on paper without a single rendered element to test it against. The five-stage progression system (opacity climbing from 0.75 to 0.94, weight from normal to 800, rotation tightening from -1.5deg to -4.2deg) encodes an entire psychological arc in font-size increments. The pencil texture via inline SVG feTurbulence with mix-blend-mode multiply is a genuinely lovely detail — the stylesheet cares about how graphite catches paper grain. The z-index layering (toner specks at 1, text at 2, annotations at 10, controls at 100) reveals clear architectural thinking about what sits on top of what in a reader's attention. The fraction typesetting system with .math-frac/.num/.den and bottom borders is the kind of craft that separates "CSS that works" from "CSS that typesets." The wavy red underline for disagreement, the vertical marginal text, the scrawl class for "WAIT" and "NO" — each utility class is a tiny narrative device. This stylesheet doesn't just support a story about marginalia; it *is* marginalia rendered as architecture. Ships with enthusiasm.


## Ratings

| Dimension | Score |
|---|---|
| originality | 4 |
| specificity | 4 |
| craft | 5 |
| surprise | 3 |
| coherence | 5 |
| portfolio_fit | 4 |
| technical_quality | 5 |

## Tester Report

**Verdict:** pass
**Summary:** Well-structured CSS file that supports all elements described in the proposal (textbook page, pencil annotations with progression, controls, responsive layout). No bugs or structural problems detected.
**Tests:** 10/10 passed
