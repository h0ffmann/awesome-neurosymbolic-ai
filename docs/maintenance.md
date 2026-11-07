# Maintainer notes

Internal notes on how this repository is set up and maintained. Contributors don't need this file; see [contributing.md](../contributing.md) instead.

## One-time setup after creating the repo

1. Replace `OWNER` with your GitHub username in `.github/ISSUE_TEMPLATE/config.yml`.
2. Repo settings:
   - Description: `A curated list of neurosymbolic AI frameworks, reasoners, papers, courses, and benchmarks.`
   - Topics: `awesome`, `awesome-list`, `neurosymbolic-ai`, `neuro-symbolic`, `symbolic-ai`, `logic-programming`, `machine-learning`, `reasoning`.
   - Enable "Automatically delete head branches".
3. Branch protection on `main`: require the `awesome-lint`, `List structure check`, and `Check links` status checks to pass.
4. Create the labels used by automation: `broken-link`, `automated`, `suggestion`.
5. Confirm GitHub detected the license as CC0-1.0 (shown in the repo sidebar).

## Automation overview

| Workflow | Trigger | What it does |
|---|---|---|
| `lint.yml` | push to main, PRs | Runs [awesome-lint](https://github.com/sindresorhus/awesome-lint) plus `scripts/check_list.py` (entry format, duplicate URLs, ToC consistency). |
| `links.yml` | weekly cron, PRs touching the markdown, manual | Runs [lychee](https://github.com/lycheeverse/lychee) with `lychee.toml`. Fails PRs on broken links; on the weekly run it opens an issue with the report instead. |
| `dependabot.yml` | monthly | Keeps the pinned GitHub Actions up to date, grouped into one PR. |

Run the checks locally:

```sh
npx awesome-lint
python scripts/check_list.py README.md
lychee --config lychee.toml README.md   # needs the lychee binary
```

## Curation policy (summary)

- Quality over quantity; every entry should be defensible in one sentence.
- Software: maintained within ~2 years, documented, open source preferred.
- Papers: surveys and genuinely landmark work only — this is not a rolling paper feed (the related LLM-era paper lists cover that).
- Review removals as eagerly as additions; link rot and abandonware erode trust in the list.

## Submitting to sindresorhus/awesome (later)

The list must be **at least 30 days old** with the readme polished before submitting. Requirements already handled: repo name, title case heading, awesome badge, `## Contents` ToC, CC0 license, contributing.md, entry format, no trailing slashes. When the time comes, follow the current `pull_request_template.md` of [sindresorhus/awesome](https://github.com/sindresorhus/awesome) — it requires reviewing 2 other open PRs first.
