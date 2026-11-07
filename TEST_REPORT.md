# Exam Rescue AI — evidence and validation report

## Scope of this report

The assistant examined screenshots and chat history the builder supplied during November 7, 2026. It did **not** connect to the builder's Windows machine or its Switch server. Live agent instructions and room configuration were inferred only where visible, not exported. Newly generated templates are a reproducible **proposal**, not an exact snapshot of the live environment.

## Observed from supplied screens

| Item | Observation | Confidence |
|---|---|---|
| Local Switch server | Green running indicator in Switch Console | Demonstrated |
| Codex installed/authenticated | CLI `0.167.0` worked; signed-in state shown | Demonstrated |
| Compatible model | `gpt-6-luna` answered a real Codex prompt, then a Switch chat | Demonstrated for that login |
| Two study agents | `Study Coach` and `Quiz Master` seen running in Switch | Demonstrated |
| Telegram group connection | Telegram bot delivered room activity and both agents' messages | Demonstrated |
| Teaching | Coach explained K-means with a practical example | Demonstrated |
| Five-question quiz | Quiz Master asked, graded and scored a completed 5/5 quiz | Demonstrated |
| Agent handoff | Quiz Master requested review from Study Coach; Coach responded using shared room context | Demonstrated |
| Follow-up quiz | Quiz Master acknowledged Coach's lesson and started another quiz | Demonstrated start only |
| Personalized evaluation of weak topics | None demonstrated on perfect 5/5 initial quiz | Not verified |
| Dynamic difficulty changes | Promised by agent for follow-up quiz but not independently observed | Not verified |
| PDF extraction | No working demo or code verified | Not implemented / not verified |
| Exact original local agent instructions | Not supplied as export | Unknown |
| Importing supplied templates into Switch | No live import performed by assistant | Not verified |

## Static tests of repository files

Run `python scripts/validate_templates.py` after `pip install PyYAML`. This checks YAML syntax, expected Switch top-level keys, required managed-agent fields, the room-vs-existing-room arrangement, non-bypass permissions, and user-editable params. It is a **smoke check only**; Switch Console is the authority for full template validity and model/bridge compatibility.

## Remaining risks

1. Telegram requires a **real group**. Private bot chats are lobby rooms and do not route agent mentions as a study group.
2. Switch's Telegram mapping/permissions are environment-specific. On the live setup, a bot's ability to read group messages and the group room's agent membership needed explicit configuration.
3. The demo uses one person's actual Codex sign-in and supported model; other accounts may need a different model.
4. The templates create or attach agents; do **not** execute them against a working installation without reviewing every field.
5. No public GitHub URL or playable demo URL was provided when this package was assembled.

## Integrity statement

No synthetic demo recording, simulated tool logs, or fabricated test pass has been added. Build evidence may be demonstrated using the builder's authentic Telegram and Switch screen captures, with private details redacted before publication.
