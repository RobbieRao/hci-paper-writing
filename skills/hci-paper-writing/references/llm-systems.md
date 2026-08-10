# LLM-Integrated HCI Systems

Apply these questions when an LLM or generative model is part of an interactive
system. Verify current community guidance before treating any item as policy.

## Framing

- Is the LLM central to the HCI contribution or an implementation choice?
- Why is an LLM appropriate for the interaction and affected people?
- Would model progress make the claimed contribution obsolete?
- Does the contribution concern interaction, workflow, human understanding,
  design knowledge, or system engineering rather than novelty by API use?

## Reporting

- Identify model, version or date, configuration, prompts, retrieval context,
  guardrails, sampling, and components that materially affect claims.
- Separate implemented behavior from conceptual or future behavior.
- Describe development iteration without overwhelming the interaction story.
- Report costs, latency, reliability, and data handling when they affect use.

## Evaluation

- Include technical evaluation when model behavior is central to a human-facing
  claim.
- Test meaningful variation, failure modes, and robustness rather than only best
  examples.
- Match human evaluators to the claim and distinguish preferences from correctness.
- Examine agency, delegation, accountability, uncertainty, and recovery from
  failure where relevant.

Starting reference: the 2026 guidelines for reporting LLM-integrated systems in
HCI, derived from author and reviewer interviews:
https://ianarawjo.github.io/Guidelines-for-Reporting-LLM-Integrated-Systems-in-HCI/

