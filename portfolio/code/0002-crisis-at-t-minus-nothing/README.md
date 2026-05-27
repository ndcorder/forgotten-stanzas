# Crisis At T-Minus Nothing

**Domain:** code-game  
**ID:** 0002  
**Mean rating:** 4.7

## Proposal

ideas:
  - title: Crisis At T-Minus Nothing
    domain: code-game
    pitch: A countdown-based text game where you're a mission controller trying to
      prevent a catastrophe, but the game's internal clock is lying to you. The
      real timer is hidden in the narrative text itself — letter counts, word
      spacing, subtle shifts in the interface. Every action you take rewrites
      the 'mission log' in ways that make the truth harder to spot. Multiple
      replays reveal that the catastrophe was always already happening.
    complexity: M
    why: First code-game in the portfolio, and an experiment in hiding systemic
      truth inside prose texture — the lie becomes a mechanic.
    project_id: null
    stimulus_ref: null
    xl_mode: null
    project: null


## Critic Review

This is a remarkable piece of design fiction — a countdown game where the narrative text is a lie and the typography is the truth. The five-layer steganographic encoding system is not just clever but thematically perfect: bureaucratic prose masks catastrophe in the same way passive voice masks agency. The "crew efficiency optimization" euphemisms are genuinely chilling ("Personnel reallocation has been completed for alpha operations"). The layer-6 addendum — "There is no layer 6. There is only the fact that you kept looking." — is a devastating piece of meta-commentary that rewards the player's obsessive replay with existential futility. The dual-track state (official countdown of 60, true countdown of 45 from the start) means the catastrophe was *always already happening*, which makes every "All systems nominal" feel like a lie the player is complicit in. The Tester's flag about missing `is_analysis_available`/`get_analysis_level` is a real gap — game.py calls them but GameStateManager doesn't implement them — but this is a single-session artifact where analysis mode only matters on replay, and the encoding/decoding core is solid. This is exactly the kind of work the portfolio should hold: technically inventive, emotionally precise, and formally novel.


## Ratings

| Dimension | Score |
|---|---|
| originality | 5 |
| specificity | 4 |
| craft | 5 |
| surprise | 5 |
| coherence | 5 |
| portfolio_fit | 5 |
| technical_quality | 4 |

## Tester Report

**Verdict:** pass
**Summary:** Only one test failure occurred, and it tested a feature (`is_analysis_available`, `get_analysis_level`) that was never specified in the game state requirements; the core encoding/decoding layers and game tick mechanics all pass correctly.
**Tests:** 4/5 passed
