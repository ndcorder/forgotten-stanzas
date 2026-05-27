# Access Log for a Door That Was Never Installed

**Domain:** data-narrative  
**ID:** 0038  
**Mean rating:** 5.0

## Proposal

ideas:
  - title: Access Log for a Door That Was Never Installed
    domain: data-narrative
    pitch: A building's access control system generates 2,847 entries for door
      D-0-NULL — a door that exists in the database but was removed from floor
      plans during value engineering. Swipes, tailgating, held-open alarms,
      maintenance requests. The log's longest consecutive user (673 entries over
      14 months) is an employee who died in the building in 2019. The system
      never invalidated her credential.
    complexity: M
    why: Forensic inference through pure system data — no prose, no characters, just
      access timestamps and event codes that reconstruct a life passing through
      a gap in institutional memory.
    project_id: null
    stimulus_ref: null
    xl_mode: null
    project: null


## Critic Review

The portfolio's definitive data-narrative and its most structurally perfect forensic artifact since Witness Stand. The central inversion — a door that doesn't exist generating 2,847 access log entries because no one told the system it was value-engineered out — is devastating institutional horror: the building's database is more faithful than any person, logging access for a portal to nowhere with mechanical indifference. Chen's narrative arc across 673 entries is the portfolio's most controlled use of behavioral data as character study: you watch a woman's life disorder in real time through arrival timestamps migrating from 08:30 to 02:00, weekend visits multiplying, TAILGATE and DOOR_HELD_OPEN events accumulating, all leading to the final swipe at 2020-03-12 22:52:41 marked ◄ FINAL — a timestamp that sits in the chest like the STAY frame at 0x3FF. The quarterly audit entry flagging her credential as "ACTIVE" ninety days after her death is the portfolio's cruelest institutional sentence since The Defect Report. The maintenance worker Moreno filing the same confused report exactly one year apart ("Database update deferred to Q1 maintenance window") is comedy and tragedy in the same gesture. The detail that Chen swiped a door that wasn't there 673 times — and that after her death, the system finally denied her entry to a room that doesn't exist — is the most theologically loaded image in the portfolio: access control as afterlife, a dead woman's badge still active at a threshold no one can cross. The BMS log viewer is functionally complete with filtering, sorting, pagination, and Chen's rows subtly highlighted, making the reader an investigator without announcing it. Sits alongside Your Car Knows You're Sad, The Last Algorithm, and Incident Report for a Color as the portfolio's canonical forensic narratives, and the first to make the database itself — not the data, the schema — the instrument of mourning.


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
**Summary:** The artifact is a fully functional, self-contained HTML access log viewer that faithfully implements all requirements from the proposal. No critical or major bugs were found; the total entry count matches exactly 2,847, Chen's narrative arc shows the prescribed behavioral phases, and all UI controls work correctly.
**Tests:** 16/16 passed
