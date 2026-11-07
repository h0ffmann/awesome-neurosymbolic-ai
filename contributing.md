# Contribution Guidelines

Thank you for helping curate Awesome Neurosymbolic AI! This is a *curated* list, not a comprehensive index — quality over quantity. When in doubt, leave it out.

## What belongs here

An entry should meet all of these:

- **Relevant.** It is about neurosymbolic AI, a symbolic engine that neurosymbolic systems actually build on, or LLM + symbolic-reasoner integration.
- **Awesome.** It is something you would recommend to a colleague: actively maintained software, a widely cited paper or survey, or a genuinely useful learning resource. Not merely "exists".
- **Alive.** Software entries should have activity (commits, releases, or issue triage) within the last ~2 years, unless the project is historically foundational.
- **Documented.** A README that explains what the project does and how to use it.
- **Open.** Prefer open-source software and openly accessible papers (arXiv, open-access venues, author pages).

What does **not** belong here:

- Self-promotion of unproven projects (give your project ~30 days and some users first).
- Blog posts, individual tweets/threads, or marketing pages.
- Paywalled content when no open version exists.
- Duplicates — check the list and open pull requests before submitting.

## Entry format

Entries follow the [awesome-lint](https://github.com/sindresorhus/awesome-lint) conventions:

```markdown
- [Name](https://example.com/link) - Description that starts with a capital letter and ends with a period.
```

- Use the project's own capitalization for its name.
- Link to the canonical home (usually the GitHub repository; otherwise the project website).
- No trailing slash in URLs.
- Keep the description to one sentence: what it is and why it matters. No superlatives like "best" or "amazing".
- Add the entry to the most specific fitting section, at the bottom of that section unless it clearly belongs elsewhere.
- If you add a new section, update the `## Contents` table accordingly.

## How to submit

1. Fork the repository and create a branch: `git checkout -b add-project-name`.
2. Make your change. **One entry (or one tightly related group of changes) per pull request.**
3. Run the checks locally (optional but appreciated):

   ```sh
   npx awesome-lint
   python scripts/check_list.py README.md
   ```

4. Open a pull request with the title `Add Project Name` and fill in the template, including a line on **why** the entry is awesome.

Pull requests are also welcome for *removing* entries that have become unmaintained or broken, and for fixing descriptions and links.

## Review process

- CI runs `awesome-lint`, a structural check (`scripts/check_list.py`), and a link check on every pull request; all must pass.
- A maintainer reviews for relevance and quality. We may ask questions or suggest a different section.
- Maintainers' decisions on curation are final, but you are always welcome to make the case for an entry in the pull request thread.

## Reporting problems

- **Broken link or dead project?** Open an issue with the "Broken link" template (the weekly link-check workflow also files these automatically).
- **Resource suggestion without a PR?** Open an issue with the "Suggest a resource" template.

By contributing, you agree that your contributions are dedicated to the public domain under the [CC0 1.0](license) waiver that covers this repository, and you agree to follow the [code of conduct](code-of-conduct.md).
