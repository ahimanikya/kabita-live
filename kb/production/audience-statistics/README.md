---
type: "Project record"
title: "Aggregate readership implementation and activation"
---

# Kabita Live aggregate readership — activated 27 October 2026

Owner direction: capture useful aggregate readership whether Google Analytics is accepted or declined. This changes the project's consent-only analytics assumption for this separate audience counter; it does not authorize identifying visitors or overriding a specific aggregate-statistics opt-out. Samanta implementation and Drishti self-review are by the same assistant, not independent review.

## What is prepared

A public HTTP counter accepts exactly an allowlisted public path and a fixed metric enum. Daily totals use the server's India date. No event log, browser ID, user ID, sessions, exact client times, URL parameters, fragments, arbitrary referrers, search terms, author details or stored IP addresses are in application records. Referral categories are direct/unknown, internal, search, social or other. Screen width is grouped small/medium/large, not asserted as a device identity. Reading milestones and visible-time thresholds are indications, not proof of reading. Language and share actions are capped to once per page/content/value; reloads count again.

Google's consent adapter remains unchanged in authority: no Google tag without opt-in. The aggregate counter has a separate visible privacy notice/control linked from every footer and honours GPC/DNT plus a stored local opt-out. Local storage holds only that opt-out preference, never an analytics identifier. If preference storage is unavailable, the choice applies to the current page. No anti-adblock or fingerprinting fallback. Private/editor/submission/proof/search routes are not in either end's aggregate allowlist. Counters begin at activation, never backfill inferred historical visits. No cross-site tracking, remarketing, individual journeys or unique/returning-reader estimates.

The browser sends directly to our Google Cloud-hosted endpoint. The provider necessarily handles network addresses and may keep infrastructure logs. Do not describe this as zero personal-data processing or as a universally established consent exemption. Application payload minimisation does not itself settle provider logging, contracts, international transfer or local statutory requirements.

## Regulatory assessment and activation gates

Reviewed official CNIL audience measurement guidance and ICO statistical-purpose exception guidance on 26 October 2026. Both describe bounded conditions, not a general cookie-free exemption. This implementation limits purpose to aggregate publication/service improvement, separates Google, avoids linkage, informs readers and offers a simple objection. National rules vary; `policyReviewed` remains false until the operator has confirmed the applicable deployment basis and provider configuration. No assumption that declining GA authorises unrelated tracking of a person.

Sources:
- https://www.cnil.fr/fr/cookies-et-autres-traceurs/regles/cookies-solutions-pour-les-outils-de-mesure-daudience
- https://www.cnil.fr/fr/node/677
- https://ico.org.uk/for-organisations/direct-marketing-and-privacy-and-electronic-communications/guidance-on-the-use-of-storage-and-access-technologies/what-are-the-exceptions/

## Deployment scope

1. Create a separate Firestore database named `audience` in the existing billed Kabita Live project. Deploy the deny-all browser rules and disable indexing for the `pages` counter map. Keep default database and submissions unchanged.
2. Create `audience-counter@kabita-live.iam.gserviceaccount.com` with database-conditioned read/create/update access to `audience` only; no default-database, Gmail, deletion or administration access. Give the existing editorial account read/write access to the aggregate database for reports/cache only. Confirm named-database IAM conditions before granting; never substitute project-wide data access.
3. Deploy only `audienceCount` and the updated `editorialAction`. Counter has zero minimum and one maximum instance, ten concurrent requests and ten-second timeout. A transactional 50,000-event/day cap bounds stored counters, not total invocation/network charges. Origin/body checks reduce accidental misuse but are not bot authentication. Identifiers/CAPTCHA are deliberately absent; automated traffic can inflate or exhaust counts.
4. Inspect logging: exclude this endpoint's automatic request logs from retained application sinks, audit other sinks and provider retention, and do not log payloads/headers/IPs. Keep security/admin audit logging. No credentials or site change should be called anonymous before these operational checks.
5. Validate the backend route/title manifest against the new public export; refresh it from `runtime.audience.publicPages` before each release that adds public pages. Keep all private routes excluded.
6. With runtime still off, run controlled invalid-route/payload and access checks. Set `audienceSettings/current` in the named database to `{enabled:true, policyReviewed:true, startedOn:"YYYY-MM-DD"}` only after policy/configuration acceptance. Set `KBL_AUDIENCE_DATABASE=audience` on editorialAction. Report reads remain behind existing editor authentication; it never adds GA numbers to aggregate counts.
7. Prepare final website configuration with enabled true and policyReviewed true, publish ONLY with owner approval of that release, then verify one controlled visit with GA denied, opt-out suppression, real counter receipt and authenticated Studio report. Save the exact activation date and evidence. No genuine reader activity can be recovered retroactively.

Kill switch: audienceSettings/current.enabled=false stops writes immediately. Website audience.enabled=false stops sending after publication. A paused aggregate source is not silently replaced with GA totals once editorialAction uses the aggregate database.

## Reporting and limits

Dashboard ranges: 7 days, 28 days or since activation. Reports cache for 15 minutes; the maximum query is 4,000 daily documents, with an explicit error instead of a silently truncated lifetime report. Each edition totals its page plus its published poem pages. A poem appearing in multiple editions contributes to each membership; sums across editions are not unique site visits. Counts exclude clients that block, opt out or do not run the script. Collection capacity warnings are shown. Daily counters need future archival aggregation before 4,000 days. Aggregate totals are retained; there is no per-visitor record to reconstruct.

Modern Web Guidance: calculate-total-foreground-time retrieved. Visibility performance entries are used when available. Its elapsed-navigation fallback would overcount hidden time; Safari/Firefox instead use visibilitychange accumulation, verified by tests. Core operation uses established browser APIs and optional MutationObserver.

## Activation checkpoint — 27 October 2026

Owner approved this runtime and exact release, then separately approved the counter-only HTTP request-log exclusion. Named database, restrictive browser rules, database-conditioned counter account and both functions are deployed. The editor function uses KBL_AUDIENCE_DATABASE=audience. A controlled count succeeded and was removed before publication; private paths and extra payload fields were rejected. The only retained-log exclusion targets audiencecount routine Cloud Run request logs. Required security/admin audit logging remains unchanged. Owner impersonation was unavailable, so negative service-account API probes are not claimed; IAM policy and the successful named-database write were verified. Website release 40387579465 succeeded at commit 9c15b673f39d5e78a6040084c3d167a4a5b4fa6d. Live Google-declined browser visit counted, aggregate opt-out suppressed a second visit, and authenticated Studio displayed the count. November issue49 draft was preserved. Six synthetic request logs were retained during initial exclusion propagation; a fresh post-propagation probe left no retained request logs before public collection began.
