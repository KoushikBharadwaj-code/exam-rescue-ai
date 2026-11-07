# Exam Rescue AI

**A multi-agent study workflow powered by Switch, Codex, and Telegram**  
**Hackathon:** Flip the Switch 2026 · **Track 02:** Best Personal or Creative Workflow

> **Project status:** The existing live Telegram workflow was demonstrated by the builder on November 7, 2026. This repository is a reproducible *configuration and documentation* package, not a hosted application. The included templates are structurally validated but have **not** been import-tested on a second Switch installation.

## The problem

Students facing an exam often switch between asking for explanations, finding practice questions, grading answers, and deciding what to revise. A single chat assistant can do some of that, but the learner has to orchestrate every step. Exam Rescue AI places **two differently instructed Codex agents** in the *same* group conversation so they share context and hand work to each other while the student remains involved.

## How it works

```text
                  Telegram group (student)
                           |
                   Switch Telegram bridge
                           |
                       Switch room
                     /             \
              Study Coach        Quiz Master
              Explain topic      Ask 5 MCQs one by one
              Simple examples    Grade real answers
              Targeted revision  Report score/weaknesses
                     \             /
                 Contextual agent handoff
                           |
            Revision -> follow-up quiz -> feedback
```

Switch is **central**, not just a notification relay: the bridge connects the existing Telegram group, Switch maps it to a shared room, agents participate under distinct names, and each can read the conversation and explicitly address the other for a task handoff. The AI models come from the user's own Codex provider; Switch itself doesn't ship a model.

## Demonstrated working functionality

The builder's November 7, 2026 Telegram and Switch screenshots show:

- **Study Coach** answering a K-means clustering question with a straightforward example.
- **Quiz Master** asking five MCQs sequentially, checking responses, updating the score, and reporting **5/5** on the completed test.
- Quiz Master explicitly asking Study Coach to recap the completed test, with Study Coach reading the shared room context and publishing a five-point revision lesson.
- Quiz Master then reading that lesson and starting a *new* five-question follow-up quiz.
- Telegram routing working through the shared bot after its group access and agent invitations were configured.

These are **observations from the builder's supplied screenshots**, not independently replayed automated tests. The follow-up quiz was started, but its final grading and dynamically changing difficulty were **not** independently verified. PDF uploads and syllabus extraction are **not implemented** in this package.

## Tech stack

- **Switch Console:** observed v0.40.1 running a local Switch server on Windows.
- **AI runtime:** Codex CLI, observed v0.167.0; the builder successfully used the `gpt-6-luna` model with their ChatGPT sign-in.
- **Chat app:** Telegram bot and a real Telegram **group** bridged into Switch.
- **Application implementation:** Switch YAML templates plus agent instructions (no bespoke web app or backend is required for this demonstrated workflow).

Your account may expose different Codex models; select a model that you have tested with `codex` rather than assuming `gpt-6-luna` works on every account.

## Quick start for a NEW installation (Telegram)

This is the reproduction path, not an instruction to recreate or disrupt the builder's already working setup.

1. Install **Switch Console**, start a local server, install/sign in to Codex or another supported provider, and confirm the built-in assistant replies. Official quickstart: https://docs.switchagents.ai/switch-rooms/getting-started
2. In Telegram, create a bot through the official `@BotFather`, and keep its **bot token private**. Use Switch Console **Home → Messaging apps → Connect → Telegram** to connect the bot. Supply the actual bot username and token only in Switch.
3. Create a **Telegram group** and add your bot. Telegram group creation takes place **in Telegram**, not Switch. To let it receive ordinary group messages, grant the bot administrator status with the minimum necessary rights, or disable its group privacy mode through BotFather (re-adding the bot may be required). Verify Switch discovers a new room corresponding to the group, **not** the numeric private-chat lobby. Link your Telegram user account to Switch if owner-only agents do not recognize you.
4. Go to **Switch Console → Templates → Import** and load **`exam-rescue-telegram.template.yaml`**. Select the **existing Telegram group room** in the form. Choose your working AI provider, machine, and a supported model ID. Choose fresh agent names/prefixes to avoid clashes. Run the template **only in a clean demo environment**; the current setup already has working agents.
5. In **Your Rooms**, confirm the Telegram group room contains both generated agents. If the import doesn't automatically attach them in your Console version, invite them from the Telegram group with `!invite-agent @<exact-agent-name>` (for the prefixed template, the names are `<prefix>-study-coach` and `<prefix>-quiz-master`). These are **Switch mentions**, not separate Telegram bot accounts.
6. Send a message addressing Study Coach, then ask Quiz Master for a five-question quiz. Read the handoff messages and check the real score. If an agent is silent, confirm it is in the **group** room, the Telegram bot can read the group messages, and the user's account is linked or the agent addressing policy permits them.

**Existing setup note:** On the builder's laptop, agents were named `study-coach` and `quiz-master`. A new template run generates names using `{project}`. Therefore commands and mentions must use the actual names created, not assume both environments use the same handles.

### Alternative: a new room on an app that supports channel creation

`exam-rescue-new-room.template.yaml` provisions both agents **and** describes a new room with a configurable `{bridge}` parameter. Use it only when your messaging platform and Switch connection support Switch-driven channel creation. It is **not** the recommended Telegram path because Telegram groups must be created in Telegram first.

### Existing installation: do not overwrite

**Don't run either template against the already-working Exam Rescue Group just to prepare the submission.** These templates describe a way for a new user to reproduce the workflow. They are not an exact export of the builder's live agent instructions. If needed, use `docs/LOCAL_EXPORT_PROMPT.md` to ask Switch Buddy for a read-only, sanitized export of the real configuration. Keep the live system untouched.

## Example user prompts (live group)

Use the *actual* agent names installed in your room. The builder's demonstrated names were `study-coach` and `quiz-master`.

**Teach:** `@study-coach Explain K-means clustering in simple terms with a student-based example.`

**Quiz:** `@quiz-master Ask me 5 multiple-choice questions about K-means, one at a time. Check my answers and show my final score.`

**Handoff:** `@quiz-master Share my actual quiz performance with @study-coach. Ask for a targeted revision lesson. Do not invent weak areas if I got 5/5.`

**Retest:** `@quiz-master Read Study Coach's lesson and start a fresh five-question follow-up quiz, with feedback after each response.`

> The student's answers must be real. A correct result is not evidence of adaptive difficulty unless the agent demonstrably changes difficulty in response to the answers.

## Security and privacy

The code repository contains **no Telegram bot token, provider credential, personal chat history, private user IDs, session secrets, or Windows home directory details**. Never commit `.env`, provider credentials, or exported Switch state with embedded secrets. The included templates use normal permission approval (`auto_mode: true`) and keep bypass permissions **off** (`auto_approve: false`). Anyone allowed to address the agents in the selected group can request responses; use a trusted group and review agent permissions.

## Validation and limitations

- Templates parse as YAML and pass a basic repository structural check (`python scripts/validate_templates.py`, requiring `PyYAML`). See `TEST_REPORT.md` for what is and is not verified.
- **Not validated:** actual import in this assistant's environment, provider authorization for other accounts, new Telegram group setup on an independent machine, adaptive difficulty end-to-end, PDF extraction, persistence across computer restarts, or final grading of the follow-up test.
- Telegram *private bot conversations* appear as a Switch lobby and do **not** work like a group room. The user's earlier troubleshooting showed that distinction clearly.
- The project is an agent-orchestration **workflow template**, not an autonomous website or custom Telegram bot backend. Reproduction requires a configured Switch server, a logged-in agent provider, and a real messaging bridge.

## Demo, evidence and submission

- See [`DEMO_SCRIPT.md`](DEMO_SCRIPT.md) for a truthful ~2–3 minute recording plan.
- See [`TEST_REPORT.md`](TEST_REPORT.md) for the test/evidence matrix and limitations.
- See [`SUBMISSION_CHECKLIST.md`](SUBMISSION_CHECKLIST.md) to finish GitHub publication and the hackathon form.
- See [`docs/GITHUB_UPLOAD_WINDOWS.md`](docs/GITHUB_UPLOAD_WINDOWS.md) for no-terminal GitHub upload steps.

**Demo video URL:** `TODO: paste actual public/unlisted video URL here before submitting`

**Repository URL:** `TODO: paste actual public GitHub repository URL here`

Do not substitute the original source repository of Switch for *your own* project repository. The official deadline is **November 7, 2026, 11:59 PM IST**.

## Official resources

- [Flip the Switch Hackathon](https://www.wemakedevs.org/hackathons/switch)
- [Official Switch repository](https://github.com/sandbox-quantum/switch)
- [Official Switch template language](https://github.com/sandbox-quantum/switch/blob/main/docs/TEMPLATES.md)
- [Switch quickstart](https://docs.switchagents.ai/switch-rooms/getting-started)

## Future work (NOT currently implemented)

PDF upload and extraction with trustworthy source-grounded Q&A; evidence-backed per-topic mastery tracking; truly adaptive difficulty with repeatable rules; downloadable study reports; and better long-term retention insights.
