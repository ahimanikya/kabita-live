---
type: "Project record"
title: "Joiner–Mover–Leaver lifecycle"
---

# Joiner–Mover–Leaver lifecycle

**UTB-GOV-004 · v0.1 · 27 September 2026 · JML process adopted by the Founder; technical implementation pending**

The Founder directed: **“Yes, it has a strong JML flow, which we also adopt.”** This adopts the Joiner–Mover–Leaver process into Utkal Blueprint. It covers approved entry, role changes with access review, and departure with handover and access removal. The operating checklists below adapt that flow to our confirmed human-authority model; each assignment still requires its own human approval and scoped access.

The process applies to humans and AI personas in every Blueprint instance. A particular appointment, role change, activation or revocation still has its own actual human decision and scope. Adopting this process has not appointed anyone, activated an agent or changed live access.

## Shared lifecycle, distinct identities

Identity, role and assignment are different records. The proposed `kind: human | persona` field identifies the actor; a project-scoped assignment identifies the JD, reporting/supervision, access and lifecycle state. One actor can have assignments in several projects. A move or departure in one project must not silently change other assignments.

Humans report only to humans. AI assignments have named human supervisors and never acquire authority over people. Internal reserved decisions belong to the Founder; an external Blueprint adopter uses its own authorized human leadership. Disha can prepare and coordinate JML records under an approved remit, but cannot appoint, dismiss, promote or authorize access.

## Joiner — establish a valid assignment

| Step | Human member | AI persona |
|---|---|---|
| Define the need | Purpose, role, project, expected contribution and named human manager | Purpose, role, project, bounded tasks and named human supervisor |
| Prepare the record | Personal JD, responsibilities, availability, working agreement, data boundaries and proposed access | JD/role configuration, task and tool boundaries, permitted data, execution mode, stop conditions and proposed access |
| Human decision | Record actual appointment and scoped access authorization | Record actual assignment/activation and scoped access authorization; a template file is insufficient |
| Orient | Person reads relevant charter, agreement and safety/privacy guidance; acknowledges the versions | Load the approved brief/context; verify role, project, authority and next task against the source records |
| Provision and verify | Grant only approved access; verify it supports the role | Configure only approved tools/runtime; verify permissions and supervisor; no inferred grants from persona name |
| Start and follow up | Begin a bounded first contribution with agreed feedback | Begin a bounded first assignment; record outputs and limits with human oversight |

Record the approval, acknowledgement or configuration verification, actual access, effective date and first assignment separately. Do not mark active merely because a name appears in a roster. A human’s acknowledgement cannot be fabricated by AI, and an AI’s claim that it read instructions is not evidence of actual permissions.

## Mover — change responsibilities without accumulating access

1. Record the requested change, reason, affected projects, old/new JD versions, reporting or supervision and proposed effective date.
2. Obtain the authorized human decision; keep the old assignment record and identify what is superseded.
3. Transfer or explicitly park open work, decisions, deadlines, maintenance ownership and dependencies. Capture context a successor cannot recover from task titles alone.
4. Review the full access delta: **what is added, what is removed, what stays and why**. Record “none” where a category has no change. Remove obsolete privileges through the authorized access process; do not merely append new ones.
5. Update roster, JD, org/reporting chart and scoped integrations consistently. Verify that every human reporting target is human. A move cannot bypass the human-only rule.
6. Complete any new orientation, human acknowledgement or AI configuration verification required by the changed scope. Record actual access and the transition outcome before claiming the move is complete.

A human changing projects or responsibilities follows this flow. An AI receiving a new role, supervisor, tool scope or materially changed operating brief also follows it. Routine session replacement within an unchanged authorized assignment requires a handover and context/permission verification, not an invented new appointment. A role/template update does not automatically expand an existing assignment.

## Leaver — close the assignment and its access

1. Record the authorized end or retirement decision, affected assignment(s), effective date, accountable human and closure owner.
2. Inventory open work, maintained documents, pending decisions, dependencies and organization-held resources. Reassign or park work; preserve the necessary handover context.
3. Remove the assignment’s access at the authorized effective point. Check relevant repositories, accounts, tokens, sessions, connectors, shared folders and scheduled jobs. For an AI, terminate authorized execution and revoke its task-specific grants; deleting its prompt or source files is not proof of revocation.
4. Verify the access changes and record evidence. If verification is incomplete, keep closure visibly incomplete and escalate to the accountable human. Access removal must not wait for the departing person or agent to provide a perfect handover.
5. Handle organization data and copies under the agreed retention, return or deletion requirements. Do not claim that externally held copies were erased without evidence. Preserve an appropriate historical record without retaining sensitive data unnecessarily in public history.
6. Mark the assignment ended or retired, with dates and successors. Preserve original authorship and contribution credit; current maintenance ownership can transfer. Record lessons and outstanding obligations.

Ending one AI session is different from retiring its role. Session handover preserves current work and reconciles actual state before resumption; persona retirement closes all affected assignments and their permissions. A project-specific departure does not justify removing unrelated authorized access in another project. An organization-wide departure requires an explicit inventory of all affected assignments.

## Proposed common event record

Use existing project-prefixed records rather than inventing a new ID prefix: a `WORK` item tracks the JML action, a `DEC` record references the human decision, a `JD` identifies the role and a `REV` can capture verification.

Minimum fields: actor ID and kind; project/organization; event (join/move/leave); current and target assignment; JD version; named accountable human; actual decision reference; scope and effective date; handover; access added/removed/retained; acknowledgement or configuration verification; evidence; outstanding obligations; state and closure reference. Private identity/access details remain in approved restricted storage, with safe references in public records.

Suggested event states are **proposed → authorized → in progress → verified complete**, with blocked or cancelled recorded honestly. The member’s assignment state is separate from the event state and the project’s lifecycle. A decision to end access and a completed revocation are different facts. Detailed schema and validators remain implementation work.

## Completion evidence and practical checks

- Join: a real human decision, scoped JD, valid human reporting/supervision, relevant acknowledgement/verification and approved access actually recorded.
- Move: old/new responsibilities and both sides of the access change are accounted for; no orphaned work or silent reporting change.
- Leave: affected access is verified closed, work is transferred or parked, and remaining data/contract obligations are assigned. Record incomplete evidence rather than overstating closure.
- All events: typed identity, project scope, traceable human authorization and zero human-to-AI reporting relationships.

These checks must be built and exercised with permitted test records as part of UTB development. A schema validator can check structure, references and required evidence pointers; it cannot by itself prove a human approved something or that a third-party system revoked access.

## Rollout

UTB packages this lifecycle and its record templates. UTP uses it first through its own reviewed adoption and specific appointments; UTC and UTU follow. BAL and BAC remain deferred. Existing Founder accountability is recorded as existing context, not invented retrospective onboarding evidence. No member event has been executed by adopting this document.

The [human-authority rule](../reference/human-authority.md) and project-specific decisions govern this lifecycle.


---
Internal planning references not included in this repository appear as reference labels. The approved package and actual human decision are recorded in records/batch-approval.json. Application evidence is recorded separately; this statement does not claim project adoption or runtime enforcement.


Status update: the Founder approved this document as part of batch UTB-DEC-005. Earlier candidate/review notices describe its review history; actual application, adoption and activation are recorded separately.
