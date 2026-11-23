# 12 Working agreement

How the three of us work together. Change anything the team does not like, then treat it
as the rule.

## Talking

- **One team channel.** A decision made in a call gets one line in the channel, then a row
  in [11_DECISIONS.md](11_DECISIONS.md).
- **One list of work:** the GitHub issues. Every piece of work is an issue.
- **Core hours:** agreed by the team, for example 10:00 to 16:00 on working days. Outside
  them nobody waits for an answer.
- **Stuck for more than 60 minutes?** Say so in the channel. Asking early is part of the job.

## Standup: 15 minutes, every working day, same time

Each person answers three things: what I finished, what I do today, what blocks me.
Problems are solved after the standup by the people involved, not during it.

## Taking work

1. Pick an open issue in your lane, from the nearest milestone.
2. Assign yourself.
3. When you open a pull request, write "Closes #number" in it, so the issue closes when it merges.

## Git and pull requests

- `main` is protected. Every change goes through a pull request, with the automatic checks
  green and one approval from someone in another lane. If GitHub cannot protect the branch
  on our plan, the checks are the gate and the rule holds by agreement.
- Branch names start with the lane: `a/parser-grouped-cells`, `b/ledger-validity`,
  `c/case-page`.
- Keep pull requests small. Below 400 changed lines is normal. A larger one says why.
- One-line commit messages that say what changed. Squash when merging.
- A reviewer answers within one working day. If you cannot, say who should.
- Never push a secret. `.env` stays on your laptop. Keys for the automatic checks live in
  GitHub Actions secrets.
- Nobody edits another person's open branch without asking.

## Done means

1. The code is merged and the automatic checks are green.
2. There are tests for the new behaviour, including one for the hardest case the issue names.
3. Public functions and API shapes are typed. A new setting is in `.env.example`.
4. It can be shown at the next Friday review.
5. If it changes a number in the results table, the report says so and why.
6. No number on screen comes from free model text.

## Changing a frozen data shape (after Thu 26 Nov)

- Open a pull request with the label `schema-change`. Say what changes, why, and who must adapt.
- All three approve. Example files and their tests change in the same pull request.

## Evaluation integrity: not up for discussion

- Nobody grades their own homework. See [10_EVALUATION.md](10_EVALUATION.md).
- Only the exam keeper and the co-labeller open the sealed exam before the run. If anyone
  else sees an exam act or answer by accident, say so at once. The act is replaced and the
  incident is logged.
- After the freeze tag, nothing the exam uses may change before the run.
- Results are reported as they come out. A missed bar is a finding, not a failure.

## AI coding assistants

Follow the bootcamp's rules. Whatever the tool, the person who opens a pull request can
explain every line in it. In the final presentation each person answers questions on their
own lane.

## Deciding and disagreeing

- Inside a lane, the lane owner decides after listening.
- Across lanes, the team decides. No agreement within a day? The majority decides, and the
  other view is written down with the decision.
- A change of scope always needs all three.
- If something goes wrong between people, raise it in the Friday retro or in private.
  Never in a pull request comment.

## Fairness

- Each lane has one model piece with its own line in the results table.
- If a lane falls behind, the Friday review moves work. Nobody quietly works nights.
- Everyone tells the team their course days, appointments and days off.
