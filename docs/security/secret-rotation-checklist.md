# Secret Rotation Checklist

Operational checklist for rotating repo-related secrets without exposing `.env` contents to agents.

## Hard rules

- Do not paste `.env` into chat tools.
- Do not ask Codex or other agents to read, print, diff, or summarize `.env`.
- Rotate provider-side credentials first, then update local and hosted environments.

## Scope

Use this checklist when rotating any secret used by this repo, including:

- EUR-Lex or Publications Office credentials
- API keys used by local ingestion scripts
- CI/CD or hosted environment secrets
- Any private output path credentials or storage tokens added later

## Pre-rotation prep

1. Pick an owner and a maintenance window.
2. Inventory which environments need the new value:
   - local machine
   - CI/CD
   - hosted preview / production environments
3. Record the provider console pages or secret managers you will update.
4. Identify the smallest smoke test that proves the rotated secret works.

## Rotation flow

1. Create the replacement credential in the provider console.
2. Update the secret where it is actually consumed:
   - local `.env`
   - shell profile or secure keychain entries
   - CI/CD secret store
   - platform-specific env vars
3. Restart any shells, dev servers, or scheduled jobs that cache environment variables.
4. Run a smoke test that exercises the rotated integration.
5. Only after the new credential works, revoke the old one.

## Repo-specific verification ideas

- If EUR-Lex or ingestion credentials changed, run the smallest safe fetch or connectivity check you normally use for legislation collection.
- If only local document generation changed, verify generators still write to `$GDPR_EXPERT_PRIVATE_DIR`.
- Re-run `python3 scripts/audit_prompt_injection.py --root library` after large ingestion batches to confirm the sanitized pipeline still behaves as expected.

## Rotation log template

Capture this in your own private ops notes, not in `.env`:

- Date:
- Owner:
- Secret / provider:
- Environments updated:
- Smoke test run:
- Old credential revoked:
- Follow-up needed:
