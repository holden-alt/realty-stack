# Security Policy

## Reporting a vulnerability

If you find a security issue in Realty Stack — especially anything in the future `fub-mcp-server` that touches a realtor's FUB API key, contact data, or local credentials — please disclose privately first.

**Email:** holden@holdengr.com

Include:
- Description of the issue
- Steps to reproduce
- The version of Realty Stack you found it in
- Your suggested fix if you have one

We aim to respond within 48 business hours and to publish a patched release within 7 days of confirmation for anything that exposes credentials or contact data.

## What's in scope

- Anything in this repository that handles user credentials (FUB API keys, future MLS keys, etc.)
- The `fub-mcp-server` (when it lands in v0.3)
- Skill prompts that could exfiltrate contact data
- Plugin manifests that could be hijacked to load malicious skills

## What's out of scope

- Vulnerabilities in Claude itself or in MCP servers we don't ship
- Vulnerabilities in FUB's API (report to Follow Up Boss directly)
- Issues that only apply if the realtor explicitly disables a built-in safety check (e.g., disabling T18 "show before do" enforcement)

## What we won't do

- We won't bury or delay disclosure of confirmed issues to make ourselves look good.
- We won't punish or thank-but-shame researchers who follow this policy.
- We won't ship telemetry to detect "abuse" of the skill bundle, because the bundle is private-first.

## Credit

If you'd like public credit for a disclosure, we'll list you in the release notes for the fix. If you'd prefer to stay anonymous, we'll respect that.
