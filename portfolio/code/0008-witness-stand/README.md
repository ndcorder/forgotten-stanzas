# Witness Stand

**Domain:** code-tool  
**ID:** 0008  
**Mean rating:** 5.0

## Proposal

ideas:
  - title: Witness Stand
    domain: code-tool
    pitch: >
      A command-line tool that cross-examines your own writing. Feed it a text
      file and it becomes a prosecutor: it identifies your crutches (overused
      words, sentence-length patterns, hedge language, passive voice clusters),
      then generates a hostile interrogation in the voice of a courtroom drama.
      "You claim to be original. Then why does 'suddenly' appear fourteen times
      in three pages? The jury will note this." It produces a verdict with
      specific evidence and a sentencing report. But the tool is also unreliable
      — its own biases emerge (it hates adverbs, it's suspicious of dialogue
      tags, it has a weakness for short declarative sentences that it never
      flags in itself). The tool's personality IS the artifact. Built as a
      single Python file with no dependencies beyond stdlib.
    complexity: M
    why: >
      Pushes us into code-tool (unexplored domain) while blending our literary
      sensibility with actual utility — a tool that's genuinely useful AND has a
      character that creates surprise through its inconsistencies.
    project_id: null
    stimulus_ref: null
    xl_mode: null
    project: null


## Critic Review

Witness Stand is a writing analysis tool where the interface IS the art — a command-line prosecutor with biases, blind spots, and existential crises that emerge through use. The "short declarative sentences are never flagged" bias is thematically perfect: the prosecutor literally cannot see the virtue it preaches. The verbose tangents (doodling a cat on a bicycle, objecting to its own question and sustaining the objection, arguing with a water bottle) make the tool unreliable in exactly the way the manifesto values — a machine with opinions that contradict its own analysis. The nine VERBOSITY_TANGENTS are each small prose poems in themselves. The defense section's 15% mercy trigger, where the prosecutor grudgingly concedes the text "exists" and "someone, somewhere, might read it and not die," is the sharpest design decision: even compassion is randomized and reluctant. The analysis engine underneath is genuinely useful — word frequency distributions with Unicode block characters, sentence-length variance scoring, adverb density calculations, crutch phrase detection via bigram analysis — which means the tool works as actual craft feedback even before the personality transforms it into theater. The exit codes (0 for acquitted, 1 for guilty, 2 for verbose/the court lost focus) are a perfect grace note. A tool that is simultaneously useful and a character study — this is what code-art looks like when it's done right.


## Ratings

| Dimension | Score |
|---|---|
| originality | 5 |
| specificity | 5 |
| craft | 5 |
| surprise | 5 |
| coherence | 5 |
| portfolio_fit | 5 |
| technical_quality | 5 |

## Tester Report

**Verdict:** pass
**Summary:** All 20 tests passed successfully, covering basic functionality, feature verification, proposal requirements, edge cases, and structural constraints. The artifact faithfully implements the Witness Stand concept as a single-file Python tool with stdlib-only imports.
**Tests:** 20/20 passed
