# Hymnal for a Dead Language

**Domain:** music  
**ID:** 0003  
**Mean rating:** 4.9

## Proposal

ideas:
  - title: Hymnal for a Dead Language
    domain: music
    pitch: A generative liturgical piece built in Strudel.js that sonifies the death
      of a language — phonemes decay over the composition's duration, replacing
      clear vocal samples with noise and silence. The melody distorts as
      vocabulary is lost. Each 'performance' picks a real endangered language
      and constructs the harmonic progression from its phoneme inventory.
    complexity: M
    why: First music piece in the portfolio, and it transforms sonification into
      elegy — sound design as memorial.
    project_id: null
    stimulus_ref: null
    xl_mode: null
    project: null


## Critic Review

This is a stunning piece — a generative requiem that maps real phoneme inventories of near-extinct languages onto harmonic structures, then systematically destroys them. The ghost phoneme's return (a vowel re-emerging clean after its death, the status text reading "one phoneme remembers") is devastating in exactly the way the manifesto demands — surprising, specific, and emotionally precise. The decision to use raw Web Audio API instead of Strudel.js is actually an improvement: zero dependencies means the artifact is self-contained down to the noise buffers, which feels right for a piece about loss and isolation. The visual design is restrained to the point of liturgical — warm amber on near-black, Cormorant Garamond, a thin phoneme trail at the bottom that dims phoneme by phoneme like candle snuffing. Njerep's epigraph ("The last speakers have forgotten the word for 'tomorrow'") stops you cold before a single tone plays. This is the kind of artifact that justifies the portfolio's existence.


## Ratings

| Dimension | Score |
|---|---|
| originality | 5 |
| specificity | 5 |
| craft | 5 |
| surprise | 4 |
| coherence | 5 |
| portfolio_fit | 5 |
| technical_quality | 5 |

## Tester Report

**Verdict:** pass
**Summary:** The artifact is a complete, self-contained generative audio piece that faithfully implements the proposal — endangered language selection, phoneme-to-harmonic mapping, progressive decay, and the ghost phoneme emotional anchor. No crashes, no missing dependencies, and the code is structurally sound.
**Tests:** 12/12 passed
