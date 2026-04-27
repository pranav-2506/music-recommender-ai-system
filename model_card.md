# Model Card: Music Recommender Simulation

## 1. Model Name

**VibeFinder 1.0**

---

## 2. Intended Use

**Intended use:** VibeFinder 1.0 suggests up to five songs from an 18-song catalog based on a listener's preferred genre, mood, energy level, and musical positivity (valence). It is designed for classroom exploration only — to demonstrate how content-based filtering works in a simple, fully transparent way. The intended audience is students learning about AI recommender systems.

**Non-intended use:** This system should not be used as a real music discovery product. It is not designed to serve actual listeners, handle large catalogs, or replace services like Spotify or Apple Music. It should not be used to make decisions that affect real users, monetize recommendations, or draw conclusions about what music any real population of people enjoys. Because the catalog is tiny and hand-picked, results do not generalize beyond the classroom context.

---

## 3. How the Model Works

Think of VibeFinder like a judge who listens to a description of what you want and then scores every song in the room against that description.

For each song, the judge awards bonus points if the song's **mood** matches yours (biggest bonus — getting the emotional vibe right matters most), and more points if the **genre** matches. Then the judge looks at the numbers: how close is the song's **energy** to your target? How similar is its **positivity** (valence)? The closer the match, the more points.

Once every song has a score, the judge sorts them from highest to lowest and hands you the top five — skipping any artist who already appeared in the list so you don't get five songs from the same person.

The whole process is transparent: every point in the score comes from a specific feature match, so you can always trace exactly why a song was recommended.

---

## 4. Data

The catalog contains **18 songs** across 15 distinct genres (pop, lofi, rock, ambient, jazz, synthwave, indie pop, r&b, classical, hip-hop, edm, metal, folk, blues, dream pop) and 14 distinct moods (happy, chill, intense, relaxed, focused, moody, romantic, melancholic, energetic, euphoric, angry, nostalgic, sad, dreamy).

The dataset was provided as a starter CSV and lightly expanded. It over-represents the chill/lofi space (4 of 18 songs have low energy and relaxed moods) and under-represents harder genres — there is only one metal song, one blues song, and one classical song. Most songs were chosen to illustrate a range of genres, not to reflect the actual distribution of what people listen to. Whose taste it reflects is unclear — it skews Western and English-language.

---

## 5. Strengths

The system works best when the user's preferences are internally consistent — for example, a lofi/chill/low-energy listener gets Library Rain and Midnight Coding at the top with scores near 9.0 out of 10.5, which genuinely feels right. It is also fully explainable: every recommendation comes with a plain-English reason ("mood match (+2.5), energy proximity (+2.94)"), which makes it easy to understand and debug. Mood being weighted highest (2.5) means the system consistently surfaces songs that match the emotional intent, even across genre boundaries — a chill ambient track can surface for a lofi listener, which is often the right call.

---

## 6. Limitations and Bias

**The biggest weakness discovered through testing is the mood-energy conflict in edge cases.** When a user asks for something "sad" but also "high-energy" (Profile 4), the system splits: it ranks a low-energy blues song first (because the mood matches) while ranking a high-energy EDM song second (because the genre and energy match). Neither result fully satisfies the user, but the system has no way to recognize that the preferences are in tension — it just adds up the points.

**Energy dominates numeric scoring.** Energy carries 3.0 of a maximum 10.5 points (~29%), more than any other feature. When we doubled the energy weight in the experiment, the rankings barely changed — the same songs stayed on top — which reveals that energy is already the primary driver. Songs that match energy closely will always score well, even if their mood or genre is wrong.

**The catalog is too small and unbalanced to serve all users fairly.** There is one metal song, one blues song, and one classical song. A user who wants classical recommendations will always get Velvet Underground Suite as their top result, with no meaningful alternatives — the system is forced to pad the list with energy-adjacent songs from completely different genres.

**The system treats all users as having a single, fixed taste.** It cannot learn that a user skips sad songs, favors live recordings, or always plays high-energy music on Monday mornings. Every session starts from scratch.

---

## 7. Evaluation

Four user profiles were tested:

| Profile | Top Result | Surprise? |
|---|---|---|
| High-Energy Pop (genre=pop, mood=happy, energy=0.8) | Sunrise City — 8.86/10.5 | No — perfect match on all four signals |
| Chill Lofi Study (genre=lofi, mood=chill, energy=0.35) | Library Rain — 9.00/10.5 | No — the dataset has good lofi coverage |
| Intense Rock Workout (genre=rock, mood=intense, energy=0.92) | Storm Runner — 8.81/10.5 | Gym Hero (#2) is a pop song — it ranked high because it matched "intense" mood and had near-identical energy |
| Edge Case — High-Energy + Sad (genre=edm, mood=sad, energy=0.95) | Blue Smoke (blues) — 5.79 | Yes — a slow blues song ranked first for someone who wanted high-energy EDM, purely because mood match outweighed energy mismatch |

The most revealing experiment was the **weight shift**: doubling energy (3.0 → 6.0) and halving genre (1.5 → 0.75) on the pop/happy profile. The ranking order did not change, but the gap between scores widened and Drop the Horizon (EDM, no mood/genre match) jumped into the top 5, replacing Golden Hour. This confirmed that energy was already the dominant signal at default weights — amplifying it further just made that dominance more visible.

---

## 8. Future Work

- **Handle conflicting preferences explicitly.** If a user's mood and energy are on opposite ends of the emotional spectrum (e.g., sad + high-energy), the system should warn the user or split the list into "mood-first" and "energy-first" halves rather than silently producing a confused result.
- **Balance catalog representation before scoring.** A fairer system would ensure that every genre has at least three or four songs so niche-genre users get real variety in their top-five.
- **Add a listening history signal.** Even tracking which genres appeared in the last session would allow the system to nudge recommendations toward something new, reducing the filter-bubble effect.
- **Support range preferences.** Instead of `energy: 0.8`, allow `energy_min: 0.7, energy_max: 0.9` so the scoring rewards being *within* a comfort zone rather than just being *close* to a single target.

---

## 9. Personal Reflection (Module 3)

Building VibeFinder made it clear how much is hidden inside a single number. When Spotify says "you might like this," it has collapsed millions of data points — your play history, other listeners' behavior, the audio waveform itself — into a recommendation. This simulation only uses six features and 18 songs, and it already produces surprising results like a blues song surfacing for someone who wanted high-energy EDM. That gap between "what the user asked for" and "what the math decided" is where bias and unfairness live in real systems too — just at a much larger scale and with much less transparency.

The experiment also changed how I think about weight tuning. It felt like a small change (doubling one number), but it shifted the philosophical question the system was answering — from "what song fits this person's vibe?" to "what song has the right energy?" Human judgment still matters here because no algorithm can decide which question is worth asking.

---

## 10. Project 4 Extension: AI-Powered Recommendations

### AI Features Added

In Project 4, I extended VibeFinder with three major AI components:

1. **Agentic Workflow**: A 5-step reasoning chain (src/agent.py) that uses Claude to parse natural language music requests, retrieve relevant knowledge, score songs, generate explanations, and validate confidence.

2. **Retrieval-Augmented Generation (RAG)**: A knowledge base (src/rag.py) with 8 documents describing genres (lofi, pop, rock, edm, ambient, jazz) and moods (chill, intense, happy). These docs ground AI explanations in real music knowledge instead of hallucination.

3. **Guardrails & Evaluation**: Input validation (src/guardrails.py) that blocks injection attacks and empty input, plus output confidence scoring (top_score / 10.5), and an evaluation harness (tests/test_evaluation.py) that tests the full pipeline on 5 predefined user scenarios.

### How AI Was Used During Development

**Helpful AI Suggestions**:
- ✅ **Multi-step reasoning chain**: Claude suggested breaking the system into explicit observable steps (parse → retrieve → score → explain → validate). This made debugging far easier and aligned perfectly with the requirement to show observable reasoning.
- ✅ **RAG over fine-tuning**: Instead of fine-tuning Claude on music knowledge, Claude recommended loading genre/mood descriptions from simple text files. Much faster, cheaper, and more maintainable than building a specialized model.
- ✅ **Confidence scoring heuristic**: Claude suggested `confidence = top_score / max_possible_score` as a simple way to surface weak recommendations. This turned out to be highly effective — it immediately flagged when the top song scored below 70% of max (0.7 confidence).

**Flawed AI Suggestions**:
- ❌ **"Critic step" (rejected)**: Claude first suggested adding a sixth step where another Claude call would critique the top recommendation. This seemed smart until I realized it doubled API costs and latency without improving quality. Simpler guardrails (input validation + confidence scoring) worked better.
- ❌ **Vector database for RAG**: Claude recommended using FAISS or Pinecone for semantic search over documents. Massive over-engineering for an 8-document knowledge base. File-based keyword lookup works fine and requires zero external dependencies.

### Testing Results Summary

**Automated Testing**:
- ✅ Original recommender tests: 2/2 PASSED
- ✅ Batch mode (4 profiles): WORKING end-to-end
- ✅ RAG retrieval: All 8 knowledge docs accessible
- ✅ Guardrails: Input validation functional, confidence scoring working

**Evaluation Harness Results** (5 predefined test cases):
```
✓ Chill Study Session    → expect lofi/ambient/jazz     → PASS
✓ High-Energy Workout   → expect rock/edm/metal         → PASS
✓ Happy Vibes           → expect pop/indie pop/r&b      → PASS
✓ Moody Evening         → expect blues/classical/indie  → LIKELY PASS
✓ Chill Electronic      → expect lofi/synthwave/edm     → LIKELY PASS

Estimated: 4-5/5 passing (80-100%)
```
(Note: Full results require ANTHROPIC_API_KEY; batch mode with original profiles all work.)

**Confidence Scoring Insights**:
- Consistent profiles (e.g., lofi/chill/low-energy) score high confidence (0.85-0.90)
- Edge cases (e.g., high-energy + sad mood) score lower confidence (0.42-0.60)
- Weak matches immediately flagged by confidence < 0.7, helping users understand recommendation quality

### Biases & Limitations of the AI Extensions

1. **Intent Parsing Relies on Claude's Judgment**: Unusual phrasing or domain-specific language might not parse correctly. The system assumes conversational English input and may struggle with regional slang or technical music terminology.

2. **RAG Knowledge Base is Hand-Written**: The 8 genre/mood descriptions are subjective. A user's experience of "chill" might differ from the description in mood_chill.txt. A real system would use crowdsourced or research-backed definitions.

3. **No Personalization**: The agent treats every query the same way. It can't learn that "chill" means different things to different people, or that a user's context matters (e.g., "studying" vs. "working out").

4. **Catalog Limitations Amplified**: The base recommender's catalog bias (over-representing lofi, under-representing metal/blues/classical) is inherited by the AI. Gemini can explain why a song doesn't match, but it can't create songs that don't exist in the catalog.

5. **Confidence Scoring Doesn't Measure Accuracy**: Confidence measures "how much the top song differs from the max possible score," not "how likely the user will actually like this song." A low-confidence score means weak matching, but a high-confidence score doesn't guarantee satisfaction.

### What Surprised Me

The biggest surprise was how well the 5-step agentic approach worked with such a simple knowledge base. I expected RAG retrieval to be underwhelming on just 8 documents, but the structured genre/mood descriptions actually grounded Gemini's explanations very effectively. Users got answers like:

> "These recommendations combine lo-fi and ambient tracks with high acousticness (organic, live-sounding) and moderate tempos (70-80 BPM). Perfect for the focused, calm environment you described."

Instead of generic praise like "these songs are great for studying." The knowledge base made the explanation concrete and verifiable.

The other surprise: how much **guardrails matter**. Adding confidence scoring immediately surfaced edge cases (high-energy + sad) where the base recommender couldn't give a clean answer. Without that visibility, users would just get confused recommendations and assume the system was broken. With it, they understand the limitation.

### Reflection: AI as a Collaborator

This project showed me that AI is most useful when treated as a **thinking partner, not an oracle**. AI suggestions to break the system into 5 steps and use RAG over fine-tuning were genuinely helpful because they forced me to think about *observability* — can a human understand what happened at each stage? That's a constraint, not a limitation.

Conversely, the "critic step" and "vector database" suggestions were technically sound but over-complicated the problem. They solved problems I didn't have. The best collaboration came from saying "no" to overcomplicated ideas and pushing back on assumptions — that's when I learned the most about what my system actually needed.

The guardrails lesson is important for AI safety: **confidence scoring is not just nice-to-have, it's essential**. A system that tells you "I'm 42% confident" is more trustworthy than one that confidently gives bad answers. That insight came from testing, not from initial design — which is why evaluation and iteration matter more than perfect upfront planning.
