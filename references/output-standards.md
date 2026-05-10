# Output Standards

Use this reference for responses, review notes, and diagnostic reports.

## Working Updates

- Give short progress updates while exploring, editing, or simulating.
- Explain what context is being gathered and what has been learned.
- Before edits, state what will be changed and why.
- Mention concrete block paths, signal names, and validation targets.

## Final Response

Lead with the answer. Then give the most important evidence.

For a completed fix, include:

- root cause
- model or file areas changed
- verification simulations or checks run
- key numerical results
- anything intentionally left unchanged

Avoid generic power-electronics theory unless it helps explain the specific model behavior.

## Review Mode

When asked to review, lead with findings ordered by severity. Use block paths, signal names, and measured behavior. Put summaries after findings.

## Data Standard

Prefer concrete numbers:

- simulation stop time
- analysis window
- phase RMS
- line RMS
- current RMS
- state or duty counts
- gate mismatch sample count
- solver diagnostics

When a result is inferred from logs or topology, say it is inferred.

## Safety Standard

- Do not use destructive file or git commands without explicit user approval.
- Do not revert unrelated user changes.
- Treat generated artifacts as generated unless the user specifically asks about them.
- For real hardware implications, mention shoot-through, overvoltage, overcurrent, and measurement-polarity risks.
