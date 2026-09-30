---
type: "Template"
title: "Utkal Blueprint — role and JD standard"
---

# Utkal Blueprint — role and JD standard

**UTB-TPL-003 · Draft v0.1 · 27 September 2026 · For Founder review**

This shared standard applies to every adopting organization. A role describes a responsibility; a JD defines its duties and limits; an assignment identifies who performs it in a particular project. A person or persona may hold several assignments, recorded separately. A shared role does not confer access across projects.

**Founder-directed naming requirement:** everyone has a full profile name including a surname; an everyday short name may also be recorded. Human names must be supplied by the person, not inferred. AI names require approval and remain explicitly labelled as AI. See the initial naming review. This requirement is confirmed; the remaining standard and proposed names retain their review states.

## Required JD and assignment fields

| Field | Required content |
|---|---|
| Identity and type | Stable identity; explicitly human or AI persona. Proposed machine field: `kind: human` or `kind: persona` |
| Project and role | Project code, stable JD ID, version, title and purpose |
| Duties and outputs | Concrete responsibilities, expected artifacts and what lies outside the remit |
| Accountability | Human manager or AI supervisor; top accountable human has no invented superior |
| Decision authority | Decisions the role may make, reserved decisions and delegation reference, if any |
| Access | Actual permitted records, tools and actions; record none or pending when not granted |
| Quality evidence | How completion and useful performance will be assessed |
| Working arrangements | Availability or bounded run, reporting recipient, decision home and handover expectations |
| Lifecycle | Proposed/approved/active/ended status, actual approval, start/end when known, and JML references |
| Credit and review | Accurate contributor credit; relevant AI runtime when known; whether review is independent |

The table proposes the minimum information, not a new software schema. Optional fields and technical validation can follow practical use. Missing information is recorded honestly rather than filled with invented dates, permissions or credentials.

## Common authority boundary

Humans report only to humans. AI assignments have zero human reports and no final approval authority. AI may choose ordinary research or implementation steps within its authorized task. It may recommend decisions outside that scope but cannot make them on behalf of a human.

A JD is not a standing instruction to run agents, spend, contact people, publish, expand access or monitor in the background. Existing task authorization remains valid within its scope. Starting or changing an assignment follows the adopted JML process.

## One role, several contexts

Each project records its own assignment, even when it uses a familiar persona. UTP research access does not become UTC membership access. Supporting Blueprint development likewise needs an explicit UTB assignment or bounded brief; a UTP title alone does not grant it.

Initial UTP responsibilities are proposed in the team and JD review. External adopters choose their own people, persona names and role combinations using this same standard. They are not required to inherit the UTP roster.

**Review decision: pending.** Approval would accept this role/JD standard and the two proposed identity labels; the wider member schema, runtime configuration, actual appointments and permissions remain separately scoped.


---
Internal planning references not included in this repository appear as reference labels. The approved package and actual human decision are recorded in records/batch-approval.json. Application evidence is recorded separately; this statement does not claim project adoption or runtime enforcement.


Status update: the Founder approved this document as part of batch UTB-DEC-005. Earlier candidate/review notices describe its review history; actual application, adoption and activation are recorded separately.
