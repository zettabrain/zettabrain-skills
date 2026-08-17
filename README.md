# 3RVA Claude Team Build Package

Scaffolding for the six SOW line items. Everything marked `<<FILL: ...>>` requires
information only 3RVA can give you — those slots are the discovery deliverable.

## Build order (this order matters)

1. **Discovery** → `discovery/QUESTIONNAIRE.md`
   Nothing below can be written until this is filled in. Run it as the paid engagement.

2. **Corpus** → `corpus/CORPUS-SPEC.md`
   Can run in parallel with discovery — it doesn't depend on 3RVA's answers.

3. **Compliance Response Skill** → `compliance-response/`
   Build second. It depends only on the corpus, not on Mike's business logic.
   Ship this first so they see value while you're still writing the rest.

4. **Quote Generation Skill** → `quote-generation/`
   Build third. Fully dependent on discovery output.

5. **Recovery Documentation Skill** → `recovery-documentation/`
   Build fourth. Depends on discovery plus a sample of their existing job tickets.

6. **Workspace config + training** → last. Don't configure sharing until the
   content is stable, or you'll retrain people on a moving target.

## How a Skill is structured

```
skill-name/
├── SKILL.md          (required — YAML frontmatter + instructions)
└── references/       (optional — loaded only when needed)
```

The `description` in the frontmatter is the trigger. Claude reads only the name and
description until it decides the Skill is relevant, then loads the body. Keep the body
under ~500 lines; push detail into `references/` and point to it from the body.

Write descriptions slightly pushy. Skills tend to under-trigger — a description that
only says what the Skill does will get skipped on requests that should have hit it.
Name the situations, not just the capability.

## The one design rule that matters most here

3RVA is a regulated business. **Every Skill in this package must answer from the
corpus, never from the model's own recollection of regulation.** Regulatory detail
recalled from training data is the single biggest liability in this deployment — it
will be confident, plausible, and occasionally wrong, and Mike has no way to tell.

Every Skill below enforces this the same way: cite the corpus document, or say the
corpus doesn't cover it. Do not soften this when you edit them.

## Testing before you hand over

For each Skill, write 3–5 prompts in the words Mike's people would actually use, run
them with the Skill installed, and have Mike read the outputs. He is the only person
who can tell you the quote terms are wrong. Budget half a day for this — it is the
difference between a deployment that gets used and one that gets abandoned in week
three.
