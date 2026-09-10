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

Attune then explains the mismatch, proposes focused revisions, and—with the designer’s approval—modifies and rerenders the concept. The new result is reviewed again until the product and the brand speak the same visual language.

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
Designer approves revisions
              ↓
Agent: revise → rerender → re-review
              ↓
        Stay in tune
```

---

## 2. Problem

AI can generate polished 3D concepts quickly, but it does not reliably keep them on-brand. Guidelines stay in PDFs and senior designers’ judgment, while review feedback stays subjective (“this does not feel like us”) and revisions stay manual.

Attune turns brand guidelines into reviewable rules, finds off-brand choices with object-level evidence, applies designer-approved fixes, and verifies the result.

---

## 3. Users

**Product designer** — needs a branded starting point and specific, evidence-based feedback they can approve selectively.

**3D artist** — needs exact objects and properties called out, controlled edits, and verification without rebuilding the scene.

---

## 4. Principles

1. **Evidence before opinion.** Every finding names the brand rule, scene object, observation, and evidence.
2. **Brand-specific, not generically attractive.** Attune checks whether the concept matches this brand’s frequency—not whether it looks “good.”
3. **Designer-controlled.** No scene mutation without approval.
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
7. Let the designer approve at least two controlled revisions.
8. Rerender and verify the revised concept.
9. Show a clear before-and-after explanation.

---

## 6. MVP Scope

### Product category

> **Compact desktop smart speaker**

### Inputs

- Brand guideline (PDF, Markdown, or text)
- Logo, color palette, 3–6 reference images
- Optional written brand principles
- Product brief (type, functions, target user, constraints, desired character)

### Outputs

- Brand Design Profile
- One editable Blender scene with persistent object IDs
- Three review renders
- Structured brand-review findings
- At least two designer-approved revisions
- Before-and-after verification summary

### Environment

- Blender (`.blend`) + Blender Python API
- Stable custom object IDs
- Fixed review cameras and render settings

---

## 7. Brand Design Profile

Machine-readable bridge between brand materials and generation/review. Designer edits and approves it before generation.

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

1. Replace material with an approved material  
2. Change an approved accent color  
3. Adjust scale/thickness of a non-structural detail  
4. Move logo or non-functional detail within a defined range  
5. Adjust lighting intensity or background color  
6. Adjust camera to a presentation preset  

### Flow

```text
Select finding → Preview change → Designer approves
→ Backup scene → Apply fix → Rerender → Verify
```

Major silhouette, structural, or functional changes require manual editing.

Verification creates a new review run with fresh evidence. Only confirmed resolutions become PASS.

---

## 10. User Flow

1. **Frontend** — designer uploads guidelines and product brief  
2. **Agent** — builds Brand Design Profile; designer reviews/approves  
3. **Backend** — connects to the Blender scene (demo concept or generated)  
4. **Agent** — reviews the design in Blender against the guidelines  
5. **Frontend** — designer sees findings, evidence, and proposed fixes  
6. **Designer approves** → **Backend** applies the fix in Blender  
7. **Agent** — rerenders, re-reviews, and iterates until the design is in tune  
8. **Frontend** — designer approves the final concept

---

## 11. Screens

1. **Project setup** — brand upload, brief, demo shortcut  
2. **Brand Design Profile** — rules, sources, confidence, approve/edit  
3. **Generation** — plan, Blender status, renders, object list  
4. **Review** — renders, object tree, findings, evidence  
5. **Fix preview** — before/after properties, approve/reject  
6. **Verification** — before/after renders, resolved and remaining findings  

---

## 12. System Structure

Attune has three layers: **Frontend**, **Backend**, and **Agent**. The designer feeds guidelines in the frontend; the backend connects those guidelines to Blender; the agent reviews the live design, analyzes it against the guidelines, and re-iterates until the product stays in tune.

```text
┌─────────────────────────────────────────────────────────┐
│                      FRONTEND                           │
│  Designer uploads guidelines · reviews findings ·       │
│  approves revisions · sees before/after                 │
└───────────────────────────┬─────────────────────────────┘
                            │ guidelines + approvals
                            ▼
┌─────────────────────────────────────────────────────────┐
│                      BACKEND                            │
│  Stores brand context · connects to Blender ·           │
│  runs scene tools · returns renders and scene facts     │
└───────────────┬─────────────────────────┬───────────────┘
                │                         │
                ▼                         ▼
        ┌───────────────┐         ┌───────────────┐
        │    Blender    │         │  Attune Agent │
        │  live scene   │◄───────►│  (GPT-6 Astra)│
        │  inspect/edit │         │ review · fix  │
        │  render       │         │ re-iterate    │
        └───────────────┘         └───────────────┘
```

### Frontend

Where the designer works.

- Upload brand guidelines, logo, palette, and references
- Provide the product brief
- Review the Brand Design Profile
- View Blender renders and review findings
- Approve or reject proposed revisions
- Compare before/after and continue the loop

### Backend

The bridge between the frontend, Blender, and the agent.

- Persist project data, guidelines, and Brand Design Profile
- Connect to Blender over the Blender Python API
- Expose scene tools: inspect objects, read materials/dimensions, apply approved edits, render views
- Send scene facts and renders to the agent
- Return findings and verification results to the frontend

### Agent (GPT-6 Astra)

The brand-aware reviewer that operates on the Blender design.

1. **Read guidelines** from the frontend (via the Brand Design Profile)
2. **Review the design in Blender** — inspect form, proportions, colors, materials, details, and presentation
3. **Analyze against guidelines** — produce object-level findings with evidence
4. **Propose revisions** — suggest focused, allowlisted changes
5. **Re-iterate** — after designer approval, apply changes in Blender, rerender, and review again

### Iteration loop

```text
Guidelines (frontend)
        ↓
Backend opens / updates Blender scene
        ↓
Agent reviews scene + renders
        ↓
Agent analyzes vs guidelines → findings
        ↓
Designer approves in frontend
        ↓
Backend applies fix in Blender
        ↓
Agent re-reviews → repeat until in tune
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

**Demo flow:** brand inputs → profile → concept → three renders → review → fix chrome material → adjust ring → rerender → verify → approve  

> Attune did not simply make the speaker more attractive. It explained which decisions made it out of tune with Vela, changed only the approved objects, and verified the result until the product and the brand spoke the same visual language.

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
| Unapproved scene mutations | Zero |
| End-to-end demo | Under 3 minutes |

---

## 15. Safety Controls

- Designer approval before every scene mutation  
- Scene backup before revision  
- Allowlisted operations only  
- Distinguish measured vs inferred findings  
- Show rule source and confidence  
- Dismiss finding or restore previous scene  
- Never mark PASS without verification  
- Never claim legal, safety, or manufacturing compliance  

---

## 16. Acceptance Criteria

- [ ] Designer can provide prepared brand context  
- [ ] Astra produces a Brand Design Profile; designer can approve it  
- [ ] Editable Blender smart-speaker scene with persistent object IDs  
- [ ] Three review renders  
- [ ] At least five prepared brand inconsistencies detected  
- [ ] Every actionable finding references a brand rule and correct object ID  
- [ ] Designer previews and must approve before a revision applies  
- [ ] Material replacement and one detail/proportion adjustment work  
- [ ] Original scene remains recoverable  
- [ ] Rerender + new verification run; PASS only after new evidence  
- [ ] UI shows before-and-after renders and property changes  
- [ ] Full demo under three minutes  

---

## 17. Final Definition

> A product designer gives Attune Vela’s brand context and a smart-speaker brief. Astra turns that into explicit product-design rules, builds an editable Blender concept, and renders three views. Attune finds where the design falls out of alignment—form, proportions, colors, materials, details, presentation—with rule- and object-level evidence. The designer approves controlled fixes. Attune modifies, rerenders, and reviews again until the product and the brand speak the same visual language.

The brand provides the frequency.  
The designer sets the creative direction.  
Attune helps every product stay in tune.
