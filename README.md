# Stack-chan Educational Task Assistant – Roll-out Plan  
_Last updated : 2025-04-30_

## 0. Why this file?
We want a single, living plan that shows **what to buy, when to buy it, and what to build next**.  
Copy / edit dates freely as velocity changes.

---

## 1. Shopping list & timing

| When to order | Part | Notes | Rough cost (JPY) |
|---------------|------|-------|------------------|
| **Week 1** (today) | **Raspberry Pi 5 (8 GB)** | Core dev host; long delivery lead-time. | ¥15 000 |
| Week 1 | 32 GB micro-SD + USB-C 30 W PSU | Boot + head-room for images. | ¥3 000 |
| Week 3 | Active cooling HAT for Pi 5 | Keeps Whisper/TTS fast. | ¥2 000 |
| **Week 4** (after Phase 2 works) | **Stack-chan kit** (M5Stack Core 3 + Servo Pack) | Firmware supports MQTT out-of-box. | ¥14 000 |
| Week 4 | Small external speaker (3 W USB) | Louder voice if needed. | ¥1 000 |
| Optional (Week 6+) | Presence sensor of choice<br>  • Pi Camera v3 **or**<br>  • Velostat pressure pad kit | Enables “child is at desk” feature. | ¥3 000–6 000 |
| Optional (Week 6+) | USB M.2 SSD (128 GB) | Faster swap if you try 13 B models. | ¥6 000 |

*Add parts as rows when new concepts arise.*

---

## 2. Development calendar (first 8 weeks)

| Week | Phase / Milestone | Key deliverables |
|------|------------------|------------------|
| **1** | **Phase 0 – Repo skeleton** | `poetry init`, pre-commit, `.env.example`, CI green. |
| 1–2 | **Phase 1 – Trello ☞ SQLite sync** | FastAPI `/trello`, unit tests passing. |
| 2–3 | **Phase 2 – Scheduler** | APScheduler fires console reminders on Mac. |
| 3 | **Phase 3 – Slack outbound** | Slack DM shows reminders; Pi 5 should have arrived – flash OS & deploy. |
| **4** | **Phase 4 – Stack-chan bridge** | Order Stack-chan; MQTT loop proven with `mosquitto_pub`. |
| 4–5 | Stack-chan assembly & firmware flash | Robot says “Hello World” from Pi. |
| 5 | End-to-end demo | Trello → Robot → Button → Slack ✅ |
| **6** | **Presence sensor POC (optional)** | One method (camera _or_ seat pad) publishes `presence/desk`. |
| 6–7 | **/plan add** Slack command + Plan table | Robot can talk about weekend zoo trip. |
| 7–8 | Daily summariser for friend mentions | Vector search returns top-k facts to dialog manager. |

_If hardware shipping slips, keep coding phases unblocked on laptop._

---

## 3. Weekly checklist template

Copy this into GitHub Issues (milestone = week **n**) or into ChatGPT when you need focus.

### Week <N> goals
- [ ] Finish <phase / module>
- [ ] Write / update unit tests
- [ ] Manual test: <scenario>
- [ ] Update README progress bar
- [ ] Decide if BOM changes are required

## 4. Progress badge (markdown copy-paste)

**Roadmap status**  
Phase 0 ███░░░░░░  
Phase 1 ██████████
Phase 2 ██░░░░░░░  
Phase 3 ░░░░░░░░░  
Phase 4 ░░░░░░░░░  
Update the blocks █ each Friday.

## 5. Next decisions list
Which presence sensor—camera (software-only) or pressure pad (hardware)?

Local Llama 8 B vs cloud GPT for dialog fallback?

Long-term store: stick with SQLite or migrate to Postgres once Phase 6 lands?


6. LLM + MQTT Based Task Assistant Design (Without Stack-chan)

Focusing on LLM (Llama3 8B via Ollama) and MQTT (Mosquitto), we will build a task assistant that combines
instructions to Stack-chan, voice file conversion, and facial expression control.

    * Components:
        * MQTT Broker (Mosquitto)
        * LLM (Llama3 8B via Ollama)
        * NLU Module
        * DM Module
        * NLG Module
        * TTS Module
        * Task Management Module
        * Client

    * Message Flow: (Add details later)

    * MQTT Topic Design: (Add details later)

Tip for future ChatGPT prompts
Paste a single checklist or table row above and say
“Expand Week 5 checklist into step-by-step shell commands and sample code.”
That keeps the assistant focused on the exact sub-task.
```

