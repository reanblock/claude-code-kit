---
name: story-to-video
description: "Convert a narrated story or prose document into a structured, tool-agnostic shooting script for AI text-to-video movie generators. Takes a third-person narrated story (a short story, chapter, scene, or any narrative prose) and produces a complete Markdown spec containing an Asset Bible (characters, locations/rooms, props, wardrobe) plus per-scene blocks with setting, camera direction, blocking/action, dialogue, music, and ambient sound. Use this skill whenever a user wants to turn a story, narrative, screenplay treatment, novel excerpt, or written scene into input for an AI video/movie generator. Triggers include: 'turn this story into a video script', 'convert to a film/movie spec', 'make this into a shooting script', 'prep this for Sora/Runway/Veo/Pika/Kling', 'storyboard this', 'generate scenes from this narrative', or any request to adapt narrated prose into directable, asset-rich scene descriptions for AI video generation. Do NOT use for live-action production scheduling, call sheets, or non-narrative content."
---

# Story-to-Video Script Skill

## Purpose

Convert a document written as a narrated, third-person story into a complete, **tool-agnostic Markdown shooting script** that can be fed into a state-of-the-art AI text-to-video movie generator (Sora, Runway, Veo, Pika, Kling, etc.).

Narrated prose leaves most of the screen unspecified: it implies what characters look like, where they are, how the camera sees them, and what the scene sounds like. An AI video generator needs all of that made explicit and **consistent across every shot**. This skill bridges that gap by producing two things:

1. An **Asset Bible** — canonical, reusable descriptions of every character, location, prop, and wardrobe item, so the generator renders the same dog, the same kitchen, and the same red coat every time they appear.
2. A sequence of **Scene Blocks** — each scene fully described with setting, camera, action, dialogue, music, and ambient sound.

The output is one Markdown file. It is human-readable and editable, and works as input for any AI video tool.

## Workflow

1. **Read the source story** the user provides (pasted text, a file path, or a description). If it's a file, read it in full.
2. **Extract the asset inventory** — every named or implied character, location, significant prop, and notable wardrobe item.
3. **Segment the narrative into scenes.** A new scene begins on a change of location, a significant time jump, or a hard shift in dramatic beat.
4. **Write the Asset Bible** with canonical descriptions (see rules below).
5. **Write each Scene Block** following the exact template below, breaking long scenes into numbered shots.
6. **Save the file** and present it to the user.

## Asset Extraction Rules

Before writing scenes, build the inventory. Scan the whole story and list:

- **Characters** — anyone who appears on screen, named or not ("the bartender", "a child"). Even background figures that recur.
- **Locations / Rooms / Sets** — every distinct place the action happens.
- **Props** — objects that matter to the action or are handled by characters (a letter, a revolver, a birthday cake).
- **Wardrobe** — clothing that is described, recurring, or dramatically meaningful.

For anything the prose leaves unspecified, **invent a concrete, plausible description and commit to it** — AI generators need specifics, and consistency matters more than fidelity to gaps in the source. Note invented details so the user can adjust them.

### Canonical description rules

- Give each asset a **stable ID/name in CAPS** (e.g. `MARIA`, `THE OLD KITCHEN`, `BRASS KEY`) and reference that exact ID everywhere it appears.
- Descriptions must be **visual and specific**: age, build, hair, distinguishing features, skin tone, default wardrobe for characters; architecture, materials, lighting, era, scale, mood for locations.
- Keep each canonical description **self-contained** — the generator may see it in isolation, so don't rely on context from elsewhere in the document.
- Once defined, refer back by ID rather than re-describing, so the asset stays consistent shot to shot.

## Scene Segmentation Rules

- Start a new scene on a **location change**, a **time jump**, or a **major dramatic shift**.
- Within a scene, break the action into **numbered shots** when the camera, framing, or focus changes — this gives the generator digestible, single-action clips rather than one impossibly long instruction.
- Keep each shot's action to **one continuous, generatable beat** (roughly what could be a 3–10 second clip). Don't pack a whole conversation or a montage into a single shot.
- **Hard 15-second limit per shot.** AI video generators produce a maximum of ~15 seconds per continuous clip, so every shot must describe an amount of action that can plausibly play out in **15 seconds or less**. You don't need to print a duration in the shot, but the instructions you write must respect it: if a beat would take longer to perform than 15 seconds (a long speech, a slow walk across a room, multiple sequential actions), split it into two or more numbered shots. When in doubt, err toward shorter — a shot that overruns 15 seconds cannot be generated as a single clip.
- Convert narration into **what is seen and heard**. Internal thoughts, backstory, and authorial commentary must be translated into visible action, expression, dialogue, or an explicit on-screen device (voiceover, text on screen) — never left as un-filmable prose.

## Output Format

Produce a single Markdown file with this exact top-level structure. Begin the file with a **YAML frontmatter block** carrying the generation settings the AI video platform reads, then the human-readable header:

```markdown
---
# Video generation settings — read by the AI video platform
image_model: Nano Banana Pro
video_model: Seedance 2.0 Fast
music_model: Suno 5
narration_model: MiniMax Speech 2.8 HD
length: 5 min                 # target total runtime (5 min or less)
aspect_ratio: "16:9"          # 16:9 landscape
resolution: 720p
visual_style: cinematic realism
---

# [Title] — Video Generation Script

> ## ⚠️ STRICT COMPLIANCE — READ FIRST (for the AI video generator)
> **This script is the single source of truth. Follow it EXACTLY. Do NOT change, reinterpret, embellish, or "improve" anything.**
> - **Do not alter the assets.** Every character, location, prop, and wardrobe item must match its Asset Bible description exactly — same appearance, same wardrobe, same details, every time it appears.
> - **Do not alter the scenes or storyboard.** Render the scenes and shots in the exact order given, with the exact framing, camera, blocking, and action specified. Do not add, remove, reorder, merge, or split shots.
> - **Do not alter the dialogue.** Speak every line verbatim, attributed to the specified character, with the given delivery. Do not paraphrase, rewrite, add, or cut lines.
> - **Do not alter music, ambient sound, on-screen text, or timing.** Use exactly what each shot specifies.
> - **Invent nothing that isn't written here, and drop nothing that is.** If a detail seems missing, render only what is specified rather than improvising.
> - **Honor the generation settings** in the frontmatter (models, length, aspect ratio, resolution, visual style) without deviation.

> **Source:** [brief note on the source story]
> **Logline:** [one-sentence summary of the story]
> **Visual style:** [overall look — e.g. "warm naturalistic 35mm, shallow depth of field, muted autumn palette"]
> **Aspect ratio / format:** [e.g. 16:9 cinematic]
> **Tone & pacing:** [e.g. "slow, melancholic; long held shots"]

---

## Asset Bible

### Characters

**MARIA** — [age, build, hair, skin tone, face, distinguishing features]. Default wardrobe: [...]. Demeanor: [...].

**[NEXT CHARACTER]** — [...]

### Locations

**THE OLD KITCHEN** — [architecture, era, materials, furnishings, lighting quality, time-of-day default, mood]. [...]

**[NEXT LOCATION]** — [...]

### Props

**BRASS KEY** — [size, material, condition, any markings]. [...]

### Wardrobe (recurring / significant)

**MARIA'S RED COAT** — [...]

---

## Scenes

### SCENE 1 — [LOCATION], [TIME OF DAY]

**Setting:** [Which Asset Bible location, dressed for this moment — weather, time, what's changed since we last saw it.]
**Characters present:** [list by ID]
**Mood / lighting:** [emotional tone + concrete lighting description]

#### Shot 1.1 — [shot type, e.g. "Wide establishing"]
- **Camera:** [framing + movement — e.g. "slow dolly-in from doorway, eye level, shallow focus"]
- **Action / blocking:** [what the characters do, by ID; one continuous beat]
- **Dialogue:**
  - **MARIA:** "[line]" *(delivery note: e.g. whispered, trembling)*
- **Music:** [cue, instrumentation, intensity, or "none / continues from previous"]
- **Ambient SFX:** [diegetic sounds beyond the obvious — e.g. "a dog barking offscreen in the distance, kettle starting to whistle"]
- **On-screen text / VO:** [only if needed]

#### Shot 1.2 — [...]
- [same fields]

### SCENE 2 — [...]
```

## Frontmatter Guidance

The YAML frontmatter at the top of the file carries the generation settings the AI video platform reads. Always include it, and keep these defaults unless the user specifies otherwise:

- **image_model** — the model used for image generation. Default: `Nano Banana Pro`.
- **video_model** — the model used for video generation. Default: `Seedance 2.0 Fast`.
- **music_model** — the model used for music generation. Default: `Suno 5`.
- **narration_model** — the model used for narration / voiceover (text-to-speech). Default: `MiniMax Speech 2.8 HD`.
- **length** — target total runtime, `5 min` or less.
- **aspect_ratio** — default `"16:9"` (landscape). Keep the value quoted so YAML doesn't parse it as a sexagesimal number.
- **resolution** — default `720p`.
- **visual_style** — short style descriptor (default `cinematic realism`); keep it consistent with the `Visual style` noted in the human-readable header below.

If the user names a different image, video, music, or narration model, runtime, aspect ratio, resolution, or style, override the corresponding field with their choice.

## Strict Compliance Banner

Every generated script **must** include the **⚠️ STRICT COMPLIANCE — READ FIRST** banner directly under the title, exactly as shown in the template (above the Source/Logline header). This banner is a direct, non-negotiable instruction to the downstream AI video generator telling it to follow the script verbatim — assets, scenes, storyboard, dialogue, music, sound, and generation settings — and to change, add, or drop nothing. Never omit, soften, or shorten it. Keep its wording emphatic and unambiguous so the video tool cannot treat the script as a loose suggestion.

## Field Guidance

Fill every field on every shot. If a field genuinely doesn't apply, write `—` rather than omitting it, so the structure stays predictable for downstream parsing.

- **Camera** — Specify both **framing** (wide / medium / close-up / over-the-shoulder / POV / aerial) and **movement** (static, pan, tilt, dolly, tracking, crane, handheld, zoom). Add lens feel where it matters (shallow vs deep focus, wide-angle vs telephoto). Keep moves achievable in a single clip.
- **Action / blocking** — Reference characters and props by their Asset Bible ID. Describe observable behavior and expression, not interior states. One beat per shot. **Spell out the physical micro-actions in order** — see *Specify the physical sequence* below. Video models don't reason about cause and effect; they continue the most common action pattern unless you state exactly what the body does at each beat, especially where a character stops short of, avoids, or reverses an expected action.
- **Dialogue** — Attribute every line to a character ID. Add a short parenthetical delivery note (tone, volume, emotion) when it isn't obvious. Keep lines as the characters would actually say them.
- **Music** — Describe the **emotional function and instrumentation** ("sparse solo cello, mournful, low volume"), not a copyrighted track. Note when a cue starts, swells, or cuts. Use "continues" to maintain continuity across shots.
- **Ambient SFX** — This is the **non-obvious** sound layer. The generator will usually infer obvious sounds (a door closing, footsteps). Call out atmosphere and off-screen sounds that set the scene: a dog barking somewhere unseen, distant traffic, rain on a tin roof, a clock ticking, murmuring crowd. Mark whether a source is **on-screen** or **offscreen**.
- **On-screen text / VO** — Use for titles, location/time cards, or when narration must be preserved as voiceover because it can't be made visual.

## Writing Principles

- **Consistency over novelty.** The same asset must be described identically everywhere — reuse IDs, don't re-improvise. This is the single most important rule for coherent generated video.
- **Show, don't narrate.** Every line of the source must become something seeable or hearable. If you can't film it, convert it (to action, expression, dialogue, or VO).
- **Be concrete and visual.** Replace vague prose ("she felt uneasy") with directable specifics ("MARIA's hand stills on the cup; her eyes flick to the window").
- **Specify the physical sequence — don't let the model fill the gaps.** Video generators don't reason about narrative logic or real-world cause-and-effect. They render the described action, and where the description is underspecified they default to the *most common* action pattern — which is often plausible but wrong. A shot that says "DARA walks to the restroom door past an out-of-order sign" will likely show him opening the door and going through, because that's what people usually do at doors. What you wanted — he notices the sign and turns away — never gets rendered, because you never said his body stops.

  Whenever the **stopping point, hesitation, avoidance, or decision is the point of the shot**, write the micro-actions explicitly, beat by beat, in order. State where the body is at each step, the exact moment it stops, and what the hands/eyes/feet do:

  > ❌ Vague: "DARA walks to the restroom door; there's an out-of-order sign."
  > ✅ Explicit: "DARA approaches the restroom door and raises his hand toward the handle. **Before touching it**, his eyes catch the OUT-OF-ORDER SIGN taped at eye level. His hand stops mid-air and pulls back. He pauses, takes half a step back, then turns away from the door and walks off toward the elevator. He never touches the handle; the door stays shut."

  Name what does **not** happen when an expected action is being avoided ("he never touches the handle," "the cup is never lifted," "she does not sit"). The more "what-actually-happens" detail you give — body position, the precise stop, hand reaching/pausing/withdrawing, gaze shifts, weight changes — the less the model has to invent. Split the sequence across numbered shots if a single beat can't hold it (still respecting the 15-second cap).
- **One beat per shot, max 15 seconds.** Generators handle short, single-action clips far better than long, multi-action instructions — and they cap out at ~15 seconds per clip. Every shot must be performable within 15 seconds; if it can't, split it.
- **Commit to invented detail.** Where the source is silent, decide and state it. Flag invented choices so the user can override.
- **Stay tool-agnostic.** Use plain, descriptive film language any generator can interpret; don't assume a specific product's parameters.

## Output

- Save as a Markdown file named `<story-slug>-video-script.md`.
- Save it next to the source document if a path was given, otherwise in the current working directory (or `./output/` if that convention is in use).
- Present the file to the user and give a brief summary: number of scenes, number of shots, and any significant details you invented to fill gaps in the source.

## Example

**Input:** A two-page short story narrating an old woman who returns to her childhood home, finds a brass key in a kitchen drawer, and remembers her late sister while a neighbor's dog barks outside.

**Output:** A Markdown script with:
- An **Asset Bible** defining `AGATHA` (the woman), `THE SISTER` (seen in memory), `THE CHILDHOOD KITCHEN`, `THE DRAWER`, `THE BRASS KEY`, and `AGATHA'S GREY SHAWL`.
- **Scene 1** (kitchen, present day, overcast afternoon) broken into shots: a wide establishing dolly-in, a medium of Agatha crossing to the drawer, an insert close-up of the brass key, a close-up of her face. Music: sparse piano entering on the key reveal. Ambient SFX: a dog barking offscreen in a neighboring yard, wind against the windowpane.
- **Scene 2** (memory flashback, same kitchen, warm sunlit, decades earlier) with the sister present, color-graded warmer, music swelling, then cutting abruptly back to present.
