# Product Requirements Document

## Attune

**Brand-Aware 3D Product Design Agent**

**Status:** Hackathon MVP  
**Users:** Product designers and 3D artists  
**Platform:** Web review workspace connected to Blender  
**Model:** GPT-6 Astra  

---

## 1. Product Summary

### Slogan

> **Every brand has its own frequency.**

### Concept

Every brand has its own frequency.

It can be found in the softness of a curve, the weight of a form, the finish of a material, or the way a product is presented. Brand guidelines attempt to document this language, but translating those principles into every new product still depends on the judgment of experienced designers.

This becomes harder as teams generate more concepts with AI. A design may look polished and functional, yet somehow feel out of tune with the brand.

That is why we built Attune.

Like tuning an instrument to a reference note, Attune uses a company’s existing brand guidelines as its reference. It reviews an initial 3D concept, examines its form, proportions, colors, materials, details, and presentation, and identifies where the design falls out of alignment.

Attune then explains the mismatch, modifies and rerenders the concept, and reviews the new result again until the product and the brand speak the same visual language.

Attune does not replace the designer or invent the brand.

The brand provides the frequency.  
The designer sets the creative direction.  
Attune helps every product stay in tune.

### Core Loop

```text
Frontend: designer uploads guidelines
              ↓
Backend: connect to Blender scene
              ↓
Agent: review design in Blender
              ↓
Agent: analyze against guidelines
              ↓
Agent: revise → rerender → re-review
              ↓
        Stay in tune
```

---

## 2. Problem

AI can generate polished 3D concepts quickly, but it does not reliably keep them on-brand. Guidelines stay in PDFs and senior designers’ judgment, while review feedback stays subjective (“this does not feel like us”) and revisions stay manual.

Attune turns brand guidelines into reviewable rules, finds off-brand choices with object-level evidence, applies focused fixes in Blender, and verifies the result.

---

## 3. Users

**Product designer** — provides the creative requirements and brand guidelines, then reviews the generated result.

**3D artist** — needs exact objects and properties called out, controlled edits, and verification without rebuilding the scene.

---

## 4. Principles

1. **Evidence before opinion.** Every finding names the brand rule, scene object, observation, and evidence.
2. **Brand-specific, not generically attractive.** Attune checks whether the concept matches this brand’s frequency—not whether it looks “good.”
3. **Agent-operated.** The Agent may generate and revise the Blender scene automatically within allowlisted operations.
4. **Editable outputs.** Primary output is an editable Blender scene, not only a render.
5. **Verify after fix.** A finding becomes PASS only after a new review of the revised scene.

---

## 5. MVP Goals

1. Accept brand inputs and a product brief.
2. Convert brand inputs into an editable Brand Design Profile.
3. Generate one editable 3D smart-speaker concept in Blender.
4. Produce three product renders (three-quarter, front, detail).
5. Review the concept against brand-design rules.
6. Connect findings to stable object IDs and visual evidence.
7. Let the Agent apply at least two controlled revisions.
8. Rerender and verify the revised concept.
9. Show a clear before-and-after explanation.

---

## 6. MVP Scope

### Product category

> **Compact desktop smart speaker**

### Inputs

1. **Product requirements (textbox)**
   - Product type and purpose
   - Required components and functions
   - Target user and context
   - Size or design constraints
   - Desired character
2. **Brand Guidelines (PDF)**
   - One PDF containing the brand's form, color, material, detail, and presentation guidance

### Outputs

- Brand Design Profile
- One editable Blender scene with persistent object IDs
- Three review renders
- Structured brand-review findings
- At least two Agent-applied revisions
- Before-and-after verification summary

### Environment

- Blender (`.blend`) + Blender Python API
- Stable custom object IDs
- Fixed review cameras and render settings

---

## 7. Brand Design Profile

Machine-readable bridge between brand materials and generation/review. The Agent creates it automatically from the PDF.

Covers:

- Form language
- Proportion rules
- Color, material, and finish (CMF)
- Signature details
- Presentation (camera, lighting, background)

Each rule records a source and confidence:

| Confidence | Meaning | MVP finding status |
|---|---|---|
| Explicit | Stated in the guideline | May `FAIL` |
| Observed | Repeated in references | May `FAIL` |
| Designer-defined | Added by the designer | May `FAIL` |
| Inferred | Derived by Astra | `REVIEW` only |

---

## 8. Review

### Categories

Form · Proportions · CMF · Signature details · Product-family consistency · Presentation

### Finding statuses

- **PASS** — rule satisfied  
- **FAIL** — explicit/measurable rule violated  
- **WARNING** — near violation or risk of inconsistency  
- **REVIEW** — subjective, inferred, or needs human judgment  

### Every finding includes

Rule ID · category · status · object IDs · observation · expectation · evidence · brand rationale · recommended change · whether auto-fixable

---

## 9. Revision and Verification

### Safe fixes (MVP)

1. Replace material with a brand-specified material  
2. Change to a brand-specified accent color  
3. Adjust scale/thickness of a non-structural detail  
4. Move logo or non-functional detail within a defined range  
5. Adjust lighting intensity or background color  
6. Adjust camera to a presentation preset  

### Flow

```text
Find issue → Create bounded change → Backup scene
→ Apply fix → Rerender → Verify
```

Major silhouette, structural, or functional changes require manual editing.

Verification creates a new review run with fresh evidence. Only confirmed resolutions become PASS.

---

## 10. User Flow

1. Designer enters the **product requirements** in a textbox.
2. Designer uploads the **Brand Guidelines PDF**.
3. Agent turns both inputs into:
   - Brand Design Profile
   - 3D generation plan
4. Backend connects to Blender.
5. Agent instructs Blender to generate the editable 3D model.
6. Blender returns the scene data and renders.
7. Agent reviews the model against the Brand Guidelines.
8. Agent applies bounded revisions through the backend.
9. Blender rerenders and the Agent repeats the review.
10. Designer views the final result.

---

## 11. Screens

1. **Project setup** — brand upload, brief, demo shortcut  
2. **Brand Design Profile** — extracted rules, sources, confidence  
3. **Generation** — plan, Blender status, renders, object list  
4. **Review** — renders, object tree, findings, evidence  
5. **Revision log** — before/after properties and applied changes  
6. **Verification** — before/after renders, resolved and remaining findings  

---

## 12. System Structure

Attune has four parts: **Frontend**, **Backend**, **Agent**, and **Blender**.

```text
Designer
   ↓
Frontend
   ├── Product requirements textbox
   └── Brand Guidelines PDF upload
   ↓
Backend API
   ├── stores project inputs
   ├── sends inputs to Agent
   └── connects Agent tools to Blender
   ↓
Attune Agent
   ├── extracts brand rules
   ├── creates a 3D generation plan
   ├── requests Blender operations
   └── reviews and revises the result
   ↓
Blender
   ├── generates editable objects
   ├── assigns materials and stable object IDs
   └── saves the scene and renders review views
```

### Frontend

- Product requirements textbox
- Brand Guidelines PDF upload
- Generated Brand Design Profile and 3D plan
- Blender generation status
- Render, finding, and revision review

### Backend

- Validate and store the textbox input and PDF
- Extract PDF text with page references
- Manage project state and revision history
- Connect to Blender through controlled tools
- Send generation commands to Blender
- Return scene data, renders, findings, and progress to the frontend
- Save scene versions before every revision

### Agent (GPT-6 Astra)

1. Read the product requirements.
2. Extract brand rules from the PDF with page references.
3. Resolve both inputs into a structured 3D generation plan:
   - Objects and components
   - Dimensions and proportions
   - Form language
   - Colors, materials, and finishes
   - Signature details
   - Camera, lighting, and presentation
4. Call allowlisted Blender tools to build the model.
5. Review the generated scene data and renders against the extracted rules.
6. Explain mismatches and propose object-level revisions.
7. Request bounded Blender changes and review again automatically.

The Agent must not execute arbitrary Blender code. All Blender actions must use backend-validated, allowlisted operations.

### Blender

- Create separate, editable objects from the generation plan
- Assign stable object IDs
- Apply dimensions, materials, lights, and cameras
- Save a `.blend` scene
- Produce fixed review renders
- Apply only backend-validated revisions

### Iteration loop

```text
Product requirements + Brand Guidelines PDF
        ↓
Brand rules + 3D generation plan
        ↓
Blender generates editable 3D model
        ↓
Agent reviews model against guidelines
        ↓
Agent revises through bounded Blender tools
        ↓
Blender updates + rerenders
        ↓
Agent re-reviews → repeat
```

### Core tools

`extract_brand_profile` · `extract_scene_manifest` · `render_review_views` · `run_rule_checks` · `review_visual_alignment` · `preview_revision` · `apply_revision` · `verify_revision`

---

## 13. Demo Scenario

**Brand:** Vela — quiet confidence, warm precision, domestic technology  
**Form:** soft continuous volumes, restrained details  
**CMF:** warm matte ceramic, charcoal textile, muted amber  
**Presentation:** dark neutral studio, soft directional light  

**Brief:** Compact desktop smart speaker for home offices—acoustic front, top controls, status light, subtle Vela branding. Calm, approachable, premium.

**Seeded issues:** polished chrome shell · bright cyan control ring · ring too thick · logo too close to base · off-family proportions · overly dramatic render contrast  

**Demo flow:** brand inputs → profile → concept → three renders → review → fix chrome material → adjust ring → rerender → verify → final result  

> Attune did not simply make the speaker more attractive. It explained which decisions made it out of tune with Vela, changed only allowlisted objects and properties, and verified the result until the product and the brand spoke the same visual language.

---

## 14. Success Metrics

| Metric | Target |
|---|---:|
| Brand profile from prepared inputs | Completes |
| Editable Blender concept | One valid scene |
| Review renders | Three |
| Seeded issues detected | ≥ 5 of 6 |
| Findings with rule + object evidence | 100% actionable |
| Supported Auto-fix types | ≥ 2 |
| Fixes followed by verification | 100% |
| Changes outside allowlist | Zero |
| End-to-end demo | Under 3 minutes |

---

## 15. Safety Controls

- Scene backup before revision  
- Allowlisted operations only  
- Designer can stop the iteration or restore the previous scene
- Distinguish measured vs inferred findings  
- Show rule source and confidence  
- Dismiss finding or restore previous scene  
- Never mark PASS without verification  
- Never claim legal, safety, or manufacturing compliance  

---

## 16. Acceptance Criteria

- [ ] Designer can provide prepared brand context  
- [ ] Astra produces a Brand Design Profile from the PDF  
- [ ] Editable Blender smart-speaker scene with persistent object IDs  
- [ ] Three review renders  
- [ ] At least five prepared brand inconsistencies detected  
- [ ] Every actionable finding references a brand rule and correct object ID  
- [ ] Agent applies revisions only through allowlisted operations  
- [ ] Material replacement and one detail/proportion adjustment work  
- [ ] Original scene remains recoverable  
- [ ] Rerender + new verification run; PASS only after new evidence  
- [ ] UI shows before-and-after renders and property changes  
- [ ] Full demo under three minutes  

---

## 17. Final Definition

> A product designer gives Attune Vela’s brand context and a smart-speaker brief. Astra turns that into explicit product-design rules, builds an editable Blender concept, and renders three views. Attune finds where the design falls out of alignment—form, proportions, colors, materials, details, presentation—with rule- and object-level evidence. Attune then modifies, rerenders, and reviews again automatically until the product and the brand speak the same visual language.

The brand provides the frequency.  
The designer sets the creative direction.  
Attune helps every product stay in tune.
