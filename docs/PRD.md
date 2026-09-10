# Product Requirements Document

## Brand-Aware 3D Product Design Agent

**Document version:** 1.0  
**Status:** Hackathon MVP definition  
**Primary users:** Product designers and 3D artists  
**Primary platform:** Web review workspace connected to Blender  
**Model:** GPT-6 Astra  

---

## 1. Product Summary

### Slogan

> **Your brand, built into every product.**

### Product Pitch

An AI review agent that turns brand guidelines into actionable product-design rules, then reviews, revises, and rerenders 3D concepts until they are unmistakably on-brand.

### Product Vision

Make brand understanding an active part of the product-design workflow rather than a static document designers must repeatedly interpret.

The product helps a designer move from a brand guideline and product brief to an editable 3D concept, then evaluates whether the concept expresses the brand through its form, proportions, colors, materials, surface details, and final presentation. It provides object-level evidence, proposes controlled revisions, rerenders the concept, and verifies whether the revision improved brand alignment.

### Core Loop

```text
Brand context + Product brief
              ↓
      Generate 3D concept
              ↓
            Review
              ↓
           Evidence
              ↓
            Revise
              ↓
           Rerender
              ↓
            Verify
              ↓
       Designer approval
```

### Human Role

The designer retains approval and creative control throughout the workflow.

The system may generate, evaluate, and propose or apply bounded revisions, but it must not silently overwrite the designer's work or present subjective judgments as objective facts.

---

## 2. Problem Statement

AI can generate product concepts and 3D renders quickly, but it does not reliably understand what makes a product belong to a specific brand.

Brand guidelines are usually stored in static documents, mood boards, reference images, and the experience of senior designers. Product designers and 3D artists must manually translate these abstract principles into decisions about form, proportions, colors, materials, surface details, lighting, composition, and presentation.

As teams create more AI-generated concepts and variations, this process becomes difficult to scale. Designs may look polished while still feeling inconsistent with the brand, leading to repetitive reviews, subjective feedback, and costly revisions.

The product transforms brand guidelines and past design references into actionable review criteria. It evaluates editable 3D product scenes and final renders, identifies off-brand elements with object-level evidence, recommends or applies controlled changes, and rerenders the design to verify improvement while keeping the designer in control.

### Current Workflow Problems

1. **Brand knowledge is fragmented.** Relevant information is spread across PDFs, logos, color palettes, reference images, mood boards, and individual team members.
2. **Brand principles are difficult to operationalize.** Statements such as “quiet confidence,” “friendly precision,” or “organic minimalism” do not directly specify geometry, materials, or proportions.
3. **AI-generated concepts are inconsistent.** Different prompts or iterations may produce unrelated visual languages.
4. **Review feedback is subjective.** Comments such as “this does not feel like us” provide little evidence or implementation guidance.
5. **Revisions are repetitive.** Designers must manually identify objects, change the scene, rerender, and request another review.
6. **There is no verification loop.** A modification may address one comment while creating another inconsistency.

### Product Opportunity

AI makes concept generation faster, which increases the number of concepts teams can create. As generation becomes abundant, review, consistency, and trust become the bottleneck.

The product becomes the brand-governance layer between AI-assisted creation and designer approval.

---

## 3. Target Users

### Primary Persona: Product Designer

**Responsibilities**

- Translate a product brief into form and interaction concepts.
- Explore multiple design directions.
- Maintain coherence across a product family.
- Present concepts to design leads and stakeholders.

**Pain points**

- Spends significant time interpreting broad brand principles.
- Receives subjective feedback that is difficult to act on.
- Must repeatedly compare new concepts with previous products.
- Needs rapid iteration without losing authorship.

**Desired outcome**

Generate a credible branded starting point and receive specific, evidence-based feedback that can be selectively applied.

### Primary Persona: 3D Artist

**Responsibilities**

- Convert product concepts into editable 3D scenes.
- Apply materials, lighting, cameras, and render settings.
- Produce presentation-ready renders and variations.

**Pain points**

- Brand intent may be lost during the transition from concept to render.
- Review comments often require repeated scene edits and rerenders.
- Small material, detail, or presentation inconsistencies are discovered late.

**Desired outcome**

Identify exact objects and properties that need attention, apply controlled changes, and verify the result without rebuilding the scene.

### Secondary Persona: Design Lead or Brand Owner

**Responsibilities**

- Protect the brand's product language.
- Review and approve product concepts.
- Guide multiple internal and external designers.

**Desired outcome**

Review a consistent, traceable explanation of why a concept does or does not align with the brand.

### Jobs to Be Done

- When I begin a new product concept, help me translate the brand into a useful design direction.
- When I review an AI-generated concept, show me which parts support or contradict the brand language.
- When feedback identifies a problem, connect it to the exact 3D object and property that should change.
- When the system proposes a revision, let me preview and approve it.
- When a revision is applied, rerender and verify whether it improved the design.

---

## 4. Product Principles

### 4.1 Evidence Before Opinion

Every finding must identify the relevant brand rule, scene object, observed design choice, and supporting evidence.

### 4.2 Brand-Specific, Not Generically Attractive

The system evaluates whether a concept belongs to the provided brand. It does not attempt to define universally “good” or “beautiful” design.

### 4.3 Designer-Controlled Automation

The system may automatically apply only low-risk, reversible changes approved by the designer.

### 4.4 Editable Outputs

The primary output must remain an editable 3D scene. A rendered image alone is insufficient.

### 4.5 Separate Facts From Interpretation

Exact scene properties such as material IDs, dimensions, and object names are treated as facts. Visual or stylistic judgments are presented with reasoning and confidence.

### 4.6 Verification Is a New Review

A finding changes to `PASS` only after the updated scene is measured or visually reviewed again.

---

## 5. Goals and Non-Goals

### MVP Goals

1. Accept a structured set of brand inputs and a product brief.
2. Convert brand inputs into an editable Brand Design Profile.
3. Generate one editable 3D product concept in Blender.
4. Produce a set of consistent product renders.
5. Review the concept against explicit brand-design rules.
6. Connect findings to stable object IDs and visual evidence.
7. Let the designer approve at least two types of controlled revisions.
8. Rerender and verify the revised concept.
9. Show a clear before-and-after explanation of the improvement.

### MVP Non-Goals

- Support every kind of physical product.
- Train or fine-tune a proprietary 3D generation model.
- Replace industrial designers or brand-design leads.
- Guarantee manufacturing feasibility.
- Validate engineering, structural, electrical, thermal, or safety requirements.
- Provide legal or regulatory certification.
- Learn a complete enterprise design system from historical data automatically.
- Support multiple 3D applications in the first release.
- Generate production-ready CAD or manufacturing files.
- Apply irreversible scene changes without designer approval.

---

## 6. MVP Scope

### Demonstration Product Category

The MVP supports one bounded product category:

> **Compact desktop smart speaker**

This category is selected because it allows the system to demonstrate:

- Recognizable product form and proportions.
- Multiple independently editable components.
- Color, material, and finish decisions.
- Brand accent and logo placement.
- Product-family consistency.
- Studio lighting and presentation rules.
- Safe, visible revisions within a hackathon timeframe.

The architecture should allow additional categories in the future, but category generalization is not required for MVP acceptance.

### Supported 3D Environment

- Blender scene format (`.blend`).
- Blender Python API for scene creation, inspection, editing, and rendering.
- Stable custom object IDs stored as Blender custom properties.
- A fixed set of review cameras and render settings.

### Supported Brand Inputs

- One brand-guideline document in PDF, Markdown, or plain text.
- One logo file.
- A defined color palette.
- Optional typography guidance for rendered presentation.
- Three to six existing product or mood-board reference images.
- Optional written brand principles.

### Supported Product Brief Inputs

- Product type.
- Functional requirements.
- Target user.
- Required components.
- Design constraints.
- Desired brand attributes.
- Optional deadline or effort constraint.

### MVP Outputs

- A Brand Design Profile.
- A generated design rationale.
- One editable Blender product scene.
- Three product renders: three-quarter, front, and detail view.
- A structured brand-review report.
- Object-level findings.
- At least two designer-approved revisions.
- A new render set after revision.
- A before-and-after verification summary.

---

## 7. Star Feature: Brand-Aware 3D Product Generation

### Feature Statement

The user does not simply ask the system to generate a product. The user asks it to generate a product for a specific brand.

The system must understand why the product should look like the brand and express that understanding through editable design decisions.

### User Provides

#### Brand Context

- Brand guidelines.
- Logo.
- Colors.
- Typography.
- Existing product images.
- Mood board and references.
- Written brand principles.

#### Product Brief

- Product type.
- Functional requirements.
- Target user.
- Required components.
- Design constraints.
- Desired product character.

#### Project Constraints

- Deadline.
- Optional effort constraint.
- Optional rendering-quality target.

### System Produces

> **An editable 3D product concept that follows the brand's visual language.**

```text
Brand guidelines
       +
Product brief
       +
References
       ↓
GPT-6 Astra
       ↓
Brand understanding
       ↓
Brand Design Profile
       ↓
3D build plan
       ↓
Editable Blender concept
       ↓
Product renders
```

### Required Brand Understanding

The system must translate source materials into the following categories:

#### Form Language

- Dominant geometry: rounded, rectilinear, faceted, organic, or hybrid.
- Edge treatment and corner behavior.
- Symmetry or asymmetry.
- Visual weight and stance.
- Relationship between primary and secondary volumes.

#### Proportion Language

- Preferred width-to-height ranges.
- Base-to-body relationships.
- Component scale and visual hierarchy.
- Perceived compactness, stability, or lightness.

#### Color, Material, and Finish

- Approved primary and secondary colors.
- Approved materials.
- Surface gloss or roughness ranges.
- Accent-color usage.
- Material transitions and separation lines.

#### Signature Details

- Brand-specific seams, rings, buttons, perforations, or textures.
- Logo placement and clear space.
- Repeated motifs from previous products.

#### Presentation Language

- Preferred camera angles.
- Background color and environment.
- Lighting softness and contrast.
- Product orientation and crop.
- Acceptable use of typography or graphic elements.

### Generation Requirements

| ID | Requirement | Priority | Acceptance criterion |
|---|---|---:|---|
| GEN-01 | Create a structured Brand Design Profile from the provided inputs. | P0 | Profile includes form, proportion, CMF, signature-detail, and presentation rules. |
| GEN-02 | Explain which source supports each generated brand rule. | P0 | Every rule includes a source reference or is marked as an inference. |
| GEN-03 | Generate a product concept plan before modifying Blender. | P0 | Plan lists required objects, dimensions, materials, and intended brand rationale. |
| GEN-04 | Build the concept as an editable Blender scene. | P0 | Required product parts are separate named objects. |
| GEN-05 | Assign a stable ID to every reviewable object. | P0 | IDs persist across review, revision, and rerender. |
| GEN-06 | Produce three consistent review renders. | P0 | Three-quarter, front, and detail views render successfully. |
| GEN-07 | Generate multiple product concepts. | P1 | User can request up to three variants from the same Brand Design Profile. |

### Why This Is the Star Feature

Generic generation answers:

> “What could a smart speaker look like?”

Brand-aware generation answers:

> “What should a smart speaker look like if it belongs to this brand, and which design decisions make that relationship legible?”

The second question requires multimodal understanding, long-context synthesis, design reasoning, 3D planning, tool use, and iterative visual evaluation. This is where GPT-6 Astra becomes central to the experience rather than an interchangeable text interface.

---

## 8. Brand Design Profile

### Purpose

The Brand Design Profile is the machine-readable bridge between static brand material and product generation or review.

It is editable by the designer before generation begins.

### Example Structure

```json
{
  "brand_id": "vela",
  "profile_version": "1.0",
  "principles": [
    "quiet confidence",
    "warm precision",
    "technology that belongs in the home"
  ],
  "form_language": {
    "primary_geometry": "soft rounded volumes",
    "edge_behavior": "continuous radii without sharp transitions",
    "visual_weight": "grounded but not heavy"
  },
  "proportion_rules": [
    {
      "rule_id": "PROP-01",
      "description": "Main body width-to-height ratio",
      "minimum": 0.68,
      "maximum": 0.76,
      "source": "existing product family"
    }
  ],
  "cmf": {
    "primary_materials": ["warm matte ceramic", "charcoal acoustic textile"],
    "accent_colors": ["muted amber"],
    "forbidden_finishes": ["mirror chrome", "high-gloss plastic"]
  },
  "signature_details": [
    {
      "rule_id": "DETAIL-01",
      "description": "Use one restrained illuminated control ring",
      "maximum_thickness_mm": 12
    }
  ],
  "presentation": {
    "background": "dark neutral studio",
    "lighting": "soft directional key with controlled rim light",
    "required_views": ["three-quarter", "front", "detail"]
  }
}
```

### Profile Confidence

Each generated rule must include one of the following confidence types:

- **Explicit:** Directly stated in the brand guideline.
- **Observed:** Repeated across supplied product references.
- **Inferred:** Derived by Astra from the overall brand language.
- **Designer-defined:** Added or modified by the designer.

Only explicit, observed, and designer-defined rules may create blocking `FAIL` findings in the MVP. Inferred rules create `REVIEW` findings.

---

## 9. Brand Review and QA

### Review Categories

#### 9.1 Form

- Primary silhouette matches the intended geometry.
- Edge language is consistent.
- Primary and secondary volumes have the expected relationship.
- Product stance communicates the intended brand character.

#### 9.2 Proportions

- Width-to-height ratio.
- Base-to-body ratio.
- Relative scale of controls, seams, and accents.
- Visual balance across the product.

#### 9.3 Color, Material, and Finish

- Materials belong to the approved palette.
- Surface roughness and reflectivity are appropriate.
- Accent colors are approved and used with restraint.
- Material transitions follow the brand pattern.

#### 9.4 Signature Details

- Required brand motifs are present.
- Detail thickness and scale are appropriate.
- Logo placement and clear space match the profile.
- Controls and seams are consistent with the product family.

#### 9.5 Product-Family Consistency

- The concept shares recognizable attributes with existing products.
- New elements do not contradict established patterns without explanation.
- The concept remains distinct enough to fulfill the new product brief.

#### 9.6 Rendering and Presentation

- Required camera views are present.
- Background and lighting follow the presentation profile.
- Product shape and materials remain legible.
- Crop, orientation, and visual hierarchy are consistent.

### Finding Statuses

- **PASS:** Evidence confirms that the rule is satisfied.
- **FAIL:** A measurable or explicit brand rule is violated.
- **WARNING:** The concept is close to violating a rule or may create inconsistency.
- **REVIEW:** The judgment is subjective, inferred, or requires human interpretation.

### Finding Requirements

Every finding must contain:

```json
{
  "finding_id": "finding_0042",
  "review_run_id": "review_0007",
  "status": "fail",
  "severity": "major",
  "category": "cmf",
  "rule_id": "CMF-03",
  "rule_source": "Brand Design Profile 1.0",
  "object_ids": ["body_shell_01"],
  "observation": "Main shell uses polished chrome.",
  "expectation": "Main shell must use a warm matte finish.",
  "evidence": {
    "scene_property": "material_id=chrome_polished_02",
    "render_view": "three_quarter_before.png"
  },
  "reasoning": "The reflective finish creates a technical and high-contrast expression that conflicts with the brand's warm, domestic product language.",
  "recommended_change": "Replace with ceramic_matte_warm_01.",
  "auto_fixable": true,
  "confidence": 0.98
}
```

### Review Requirements

| ID | Requirement | Priority | Acceptance criterion |
|---|---|---:|---|
| REV-01 | Review the editable scene and rendered views together. | P0 | Review request contains both scene manifest and renders. |
| REV-02 | Evaluate the concept against the active Brand Design Profile. | P0 | Findings reference valid profile rule IDs. |
| REV-03 | Attach each actionable finding to one or more object IDs. | P0 | Selecting a finding identifies the correct Blender object. |
| REV-04 | Separate deterministic findings from visual interpretation. | P0 | Each finding records its evidence type. |
| REV-05 | Explain why the issue matters to the brand. | P0 | Finding contains a concise brand-specific rationale. |
| REV-06 | Allow the designer to filter by category and status. | P1 | Filters update the visible findings. |
| REV-07 | Compare the new product with previous product references. | P1 | Review includes product-family consistency findings. |

---

## 10. Revision and Auto-Fix

### MVP Safe Fix Types

The MVP supports the following bounded changes:

1. Replace an object's material with an approved material.
2. Change an approved accent color.
3. Adjust the scale or thickness of a non-structural detail.
4. Move the logo or non-functional visual detail within a defined range.
5. Adjust lighting intensity or background color.
6. Adjust a review camera to a defined presentation preset.

### Human Approval Flow

```text
Select finding
      ↓
View evidence and recommendation
      ↓
Preview exact scene changes
      ↓
Designer approves or rejects
      ↓
System saves a backup
      ↓
Apply bounded modification
      ↓
Rerender affected views
      ↓
Run verification review
```

### Changes That Require Manual Editing

- Major silhouette redesign.
- Functional component relocation.
- Structural geometry changes.
- Changes that affect manufacturing assumptions.
- Conflicting brand rules.
- Low-confidence or inferred stylistic recommendations.

### Revision Requirements

| ID | Requirement | Priority | Acceptance criterion |
|---|---|---:|---|
| FIX-01 | Preview the exact proposed changes. | P0 | UI displays target object and before/after property values. |
| FIX-02 | Require designer approval before applying a change. | P0 | No scene mutation occurs before approval. |
| FIX-03 | Save a restorable scene version. | P0 | Designer can reopen the pre-fix scene. |
| FIX-04 | Restrict edits to an allowlist of properties and objects. | P0 | Attempts outside the allowlist are rejected. |
| FIX-05 | Support material replacement. | P0 | Approved material is applied to the correct object. |
| FIX-06 | Support one geometric-detail adjustment. | P0 | Selected detail changes without modifying unrelated objects. |
| FIX-07 | Support natural-language revision requests. | P1 | Designer can request a bounded change in conversation. |

---

## 11. Rerender and Verification

### Purpose

Verification proves whether an approved revision improved the concept. The system must not assume that applying a command resolved the finding.

### Verification Process

1. Create a new scene version.
2. Rerender only the affected views when possible.
3. Recheck the original rule.
4. Check whether the change introduced a related violation.
5. Compare before and after evidence.
6. Assign a new status.
7. Present the result for designer approval.

### Verification Requirements

| ID | Requirement | Priority | Acceptance criterion |
|---|---|---:|---|
| VER-01 | Create a new review run after revision. | P0 | Verification has a unique review-run ID. |
| VER-02 | Use fresh scene and render evidence. | P0 | Evidence references the revised scene version. |
| VER-03 | Show before-and-after comparison. | P0 | Designer can view both renders and property changes. |
| VER-04 | Preserve unresolved or new findings. | P0 | Only confirmed resolved findings become PASS. |
| VER-05 | Show overall brand-alignment change. | P1 | Summary explains which categories improved or regressed. |

---

## 12. End-to-End User Experience

### Step 1: Create Project

The designer creates a project and selects the supported product category.

**Required fields**

- Project name.
- Product category.
- Brand profile.
- Product brief.

### Step 2: Add Brand Context

The designer uploads or selects brand materials.

The system extracts a draft Brand Design Profile and shows:

- Extracted principles.
- Product-design rules.
- Rule sources.
- Confidence type.
- Editable thresholds and notes.

The designer approves the profile before generation.

### Step 3: Define Product Brief

The designer provides:

- Product description.
- Required functional elements.
- Target user and context.
- Desired character.
- Hard constraints.

### Step 4: Review Generation Plan

Astra creates a concise product rationale and 3D build plan.

The designer can edit or approve the plan.

### Step 5: Generate Concept

The system builds an editable Blender scene and renders three views.

The interface displays generation stages:

- Planning product architecture.
- Creating primary form.
- Adding components.
- Applying materials.
- Placing signature details.
- Lighting and rendering.

### Step 6: Run Brand Review

The system displays:

- Overall review status.
- Category scores.
- PASS, FAIL, WARNING, and REVIEW findings.
- Object-level evidence.
- Recommended actions.

### Step 7: Revise

The designer chooses a finding and selects one of the following:

- Preview suggested fix.
- Apply safe fix.
- Edit manually.
- Dismiss with reason.
- Save as an intentional exception.

### Step 8: Rerender and Verify

The system generates updated views and compares them with the original concept.

### Step 9: Approve

The designer approves the concept or begins another iteration.

---

## 13. Required MVP Screens

### 13.1 Project Setup

- Brand context upload.
- Product brief form.
- Product category selection.
- Demo project shortcut.

### 13.2 Brand Design Profile Review

- Brand principles.
- Form rules.
- Proportion rules.
- Color, material, and finish rules.
- Signature details.
- Presentation rules.
- Source and confidence indicators.
- Approve and edit actions.

### 13.3 Generation Workspace

- Current generation stage.
- Product build plan.
- Blender connection status.
- Generated render previews.
- Generated object list.

### 13.4 Review Workspace

- Large 3D render or viewport.
- View selector.
- Object tree.
- Brand-alignment summary.
- Finding list and filters.
- Finding-detail panel.

### 13.5 Fix Preview

- Target object.
- Current and proposed values.
- Affected brand rule.
- Before-and-after visual preview when available.
- Approve, reject, or edit controls.

### 13.6 Verification Result

- Before-and-after render comparison.
- Resolved findings.
- Remaining findings.
- Newly introduced findings.
- Approve concept or continue iteration.

---

## 14. System Architecture

```text
┌───────────────────────────────────────────────┐
│                 Designer UI                   │
│ Inputs · Profile · Renders · Findings · Fixes │
└───────────────────────┬───────────────────────┘
                        │
                        ▼
┌───────────────────────────────────────────────┐
│             GPT-6 Astra Agent Core            │
│ Understand · Plan · Orchestrate · Explain     │
└──────────────┬─────────────────┬──────────────┘
               │                 │
               ▼                 ▼
┌──────────────────────┐  ┌─────────────────────┐
│ Brand Context Engine │  │ Blender Scene Tools │
│ Profile + Rule Pack  │  │ Build/Edit/Render   │
└──────────────┬───────┘  └──────────┬──────────┘
               │                     │
               └──────────┬──────────┘
                          ▼
┌───────────────────────────────────────────────┐
│                Review Engine                  │
│ Scene facts + renders + brand rules + history │
└───────────────────────┬───────────────────────┘
                        ▼
┌───────────────────────────────────────────────┐
│          Findings and Verification Log        │
└───────────────────────────────────────────────┘
```

### Astra Responsibilities

- Interpret documents and visual references.
- Create the Brand Design Profile.
- Identify ambiguity and ask focused questions.
- Plan the product concept.
- Generate or call Blender-building operations.
- Decide which review tools to invoke.
- Compare the concept with brand rules and references.
- Produce structured findings.
- Explain brand-specific reasoning.
- Propose bounded revisions.
- Coordinate rerendering and verification.

### Blender Responsibilities

- Store editable scene geometry.
- Store stable object IDs.
- Provide exact transforms, dimensions, and material assignments.
- Execute approved generation and modification scripts.
- Render fixed review views.
- Save versioned scene files.

### Deterministic Review Responsibilities

- Read exact dimensions and ratios.
- Validate material IDs against approved lists.
- Check whether required objects exist.
- Validate logo position against defined ranges.
- Validate camera and render settings.
- Compare known numeric thresholds.

### Visual Review Responsibilities

- Judge overall form-language alignment.
- Evaluate perceived visual weight and character.
- Compare the concept with reference products.
- Evaluate material appearance in the final render.
- Identify presentation choices that weaken brand recognition.
- Mark ambiguous judgments for human review.

---

## 15. Core Tool Contracts

| Tool | Purpose | Input | Output |
|---|---|---|---|
| `extract_brand_profile` | Transform brand materials into structured rules. | Documents, images, palette, logo | Draft Brand Design Profile |
| `create_product_plan` | Plan the branded concept before modeling. | Brand profile, product brief | Object plan, dimensions, materials, rationale |
| `build_blender_scene` | Create editable 3D scene. | Approved product plan | Blender scene version and object manifest |
| `extract_scene_manifest` | Read scene facts. | Blender scene | Objects, IDs, dimensions, transforms, materials |
| `render_review_views` | Produce consistent evidence. | Scene, camera presets | Review renders |
| `run_rule_checks` | Evaluate deterministic rules. | Scene manifest, rule pack | Measurements and violations |
| `review_visual_alignment` | Evaluate visual brand alignment. | Renders, references, brand profile | Visual findings |
| `preview_revision` | Show exact proposed scene changes. | Finding, proposed operation | Change preview |
| `apply_revision` | Execute approved bounded changes. | Approved preview ID | New scene version and change log |
| `verify_revision` | Recheck revised concept. | New scene, prior findings | Updated findings and comparison |

---

## 16. Data Model

### Project

```json
{
  "project_id": "project_001",
  "name": "Vela Desktop Speaker",
  "product_category": "smart_speaker",
  "brand_profile_id": "brand_profile_001",
  "brief_id": "brief_001",
  "current_scene_version": "scene_003",
  "status": "in_review"
}
```

### Scene Object

```json
{
  "object_id": "body_shell_01",
  "display_name": "Main body shell",
  "blender_object_name": "Speaker_BodyShell",
  "object_type": "mesh",
  "dimensions_mm": {
    "width": 168,
    "depth": 154,
    "height": 262
  },
  "material_ids": ["chrome_polished_02"],
  "editable_properties": ["material", "scale", "detail_radius"],
  "read_only": false
}
```

### Revision Record

```json
{
  "revision_id": "revision_0012",
  "finding_id": "finding_0042",
  "approved_by": "designer",
  "target_object_id": "body_shell_01",
  "operation": "replace_material",
  "before": "chrome_polished_02",
  "after": "ceramic_matte_warm_01",
  "source_scene_version": "scene_002",
  "result_scene_version": "scene_003"
}
```

---

## 17. MVP Demo Scenario

### Demo Brand

**Brand:** Vela  
**Principles:** Quiet confidence, warm precision, domestic technology  
**Form language:** Soft continuous volumes, restrained details  
**CMF:** Warm matte ceramic, charcoal textile, muted amber accent  
**Presentation:** Dark neutral studio, soft directional lighting

### Product Brief

> Design a compact desktop smart speaker for home offices. It must include an acoustic front surface, top controls, a status light, and subtle Vela branding. The product should feel calm, approachable, and premium.

### Initial Concept Issues

The first generated or prepared concept intentionally includes:

1. A polished chrome main shell instead of a warm matte finish.
2. A bright cyan control ring that conflicts with the muted amber accent palette.
3. A control ring thickness above the approved detail range.
4. A logo positioned too close to the base edge.
5. A width-to-height ratio outside the preferred product-family range.
6. A render with overly dramatic contrast.

### Live Demo Flow

1. Show the brand inputs and product brief.
2. Show the Brand Design Profile created by Astra.
3. Generate or open the editable Blender product concept.
4. Show three product renders.
5. Run Brand Review.
6. Open the polished-chrome finding.
7. Show the exact object, material ID, brand rule, and visual reasoning.
8. Preview replacement with the approved warm matte material.
9. Approve and apply the revision.
10. Adjust the control-ring accent and thickness.
11. Rerender the product.
12. Verify the updated concept.
13. Show before-and-after evidence and improved findings.
14. End with designer approval.

### Demo Success Statement

> The system did not simply make the speaker more attractive. It explained which decisions made it inconsistent with Vela, changed only the approved objects, and verified the result against the same brand rules.

---

## 18. Success Metrics

### Hackathon MVP Metrics

| Metric | Target |
|---|---:|
| Brand profile generation | Completes from the prepared input set |
| Editable 3D concept | One valid Blender scene |
| Required render views | Three |
| Seeded issues detected | At least five of six |
| Findings with rule and object evidence | 100% of actionable findings |
| Supported Auto-fix types | At least two |
| Fixes followed by new verification | 100% |
| Unapproved scene mutations | Zero |
| End-to-end demo duration | Under three minutes |

### Future Product Metrics

- Time from product brief to first reviewable concept.
- Reduction in review rounds.
- Percentage of findings accepted by designers.
- Percentage of recommended fixes approved.
- Brand-review agreement between the agent and design leads.
- Frequency of false positive and false negative findings.
- Consistency across concepts generated from the same Brand Design Profile.
- Time saved per concept iteration.

---

## 19. Evaluation Plan

### Test Set

Create a small evaluation set containing:

- Five Vela-compliant concept renders.
- Five intentionally non-compliant concept renders.
- A scene manifest for each concept.
- Expert labels for applicable brand rules.
- Expected object-level findings.

### Evaluation Dimensions

1. **Rule extraction accuracy:** Does the Brand Design Profile reflect the supplied sources?
2. **Finding precision:** Are reported violations genuine?
3. **Finding recall:** Does the system detect the known violations?
4. **Object grounding:** Is each finding attached to the correct scene object?
5. **Explanation quality:** Does the rationale connect the design choice to the brand?
6. **Revision accuracy:** Does the fix change only the intended property?
7. **Verification integrity:** Does the system use new evidence after revision?

### Required Human Review

At least one product designer should review:

- The Brand Design Profile.
- The original concept.
- The findings.
- The proposed changes.
- The revised concept.

The evaluator should record whether each finding is correct, useful, and actionable.

---

## 20. Safety, Trust, and Control

### Required Controls

- Designer approval before every scene mutation.
- Scene backup before applying a revision.
- Allowlisted operations and editable properties.
- Clear distinction between measured and inferred findings.
- Rule source and confidence shown in the interface.
- Complete revision history.
- Ability to dismiss a finding or record an intentional exception.
- Ability to restore the previous scene version.

### Prohibited MVP Behavior

- Claim that a product is legally compliant or safe to manufacture.
- Modify functional geometry based only on a rendered image.
- Present an inferred aesthetic preference as an explicit brand requirement.
- Remove designer-created elements without approval.
- Use unrelated reference material that was not supplied or approved.
- Mark a finding resolved without running verification.

### Privacy Considerations

Brand guidelines and unreleased product concepts may be confidential. A production version must support:

- Clear data-retention controls.
- Project-level access boundaries.
- Encrypted storage and transport.
- Audit logs.
- Deletion of uploaded assets and derived profiles.
- Configurable model-data policies for enterprise customers.

These enterprise controls are outside the hackathon MVP.

---

## 21. Failure and Edge States

| Scenario | Required behavior |
|---|---|
| Brand guideline contains conflicting principles | Show the conflict and ask the designer to choose or prioritize. |
| Reference images contradict the written guideline | Keep both sources visible and mark derived rules for review. |
| Brand evidence is insufficient | Generate fewer rules and identify missing context. |
| Blender is unavailable | Preserve the approved plan and show connection recovery instructions. |
| Scene generation fails | Keep the last valid scene version and report the failed stage. |
| Object ID is missing | Assign a new persistent ID before review. |
| Finding cannot be linked to an object | Mark it as a scene-level REVIEW finding. |
| Proposed change affects a read-only object | Block Auto-fix and require manual editing. |
| Rerender fails | Keep the revision unverified and do not mark the finding PASS. |
| Revision introduces a new violation | Show both resolved and newly created findings. |
| Astra confidence is low | Ask a focused question or route the finding to human review. |

---

## 22. Hackathon Implementation Plan

### Workstream A: Blender and Scene Engine

- Prepare the demo smart-speaker scene.
- Create procedural or scripted scene generation.
- Assign persistent object IDs.
- Export the scene manifest.
- Implement material replacement.
- Implement one geometric-detail adjustment.
- Set up three render cameras.
- Save scene versions and rerender.

### Workstream B: Astra Agent and Product Experience

- Parse the prepared brand inputs.
- Generate the Brand Design Profile.
- Define structured outputs for rules and findings.
- Orchestrate Blender tools.
- Build the review workspace.
- Display findings and evidence.
- Implement approval and verification states.
- Prepare the pitch and demo fallback.

### Suggested Build Order

1. Freeze the demo brand, brief, and expected violations.
2. Build and validate the editable Blender scene.
3. Implement scene manifest extraction.
4. Implement two deterministic review rules.
5. Connect Astra to the brand sources and renders.
6. Normalize all results into the finding schema.
7. Build the review interface.
8. Implement material replacement and detail adjustment.
9. Implement rerender and verification.
10. Add before-and-after comparison.
11. Create a cached fallback review result.
12. Rehearse the complete demo.

### Demo Fallbacks

- Keep a valid pre-generated Blender scene.
- Keep the original and revised render sets.
- Cache one valid Brand Design Profile.
- Cache one valid structured review response.
- Preserve the live object-selection and revision actions even if model access fails.

---

## 23. MVP Acceptance Criteria

The MVP is complete when all of the following are true:

- [ ] A designer can view or provide the prepared brand context.
- [ ] Astra produces a structured Brand Design Profile.
- [ ] The designer can review and approve the profile.
- [ ] The system creates or opens an editable Blender smart-speaker scene.
- [ ] Every reviewable Blender object has a persistent ID.
- [ ] The system produces three required review renders.
- [ ] The system detects at least five prepared brand inconsistencies.
- [ ] Every actionable finding references a valid brand rule.
- [ ] Every object-level finding references the correct object ID.
- [ ] The designer can preview an exact proposed change.
- [ ] The designer must approve before a revision is applied.
- [ ] The system supports material replacement.
- [ ] The system supports one detail or proportion adjustment.
- [ ] The original scene remains recoverable.
- [ ] The system rerenders the modified concept.
- [ ] The system creates a new verification run.
- [ ] A finding becomes PASS only after new evidence confirms the result.
- [ ] The UI shows before-and-after renders and property changes.
- [ ] The designer can approve the final concept or continue iterating.
- [ ] The complete demo can be shown in under three minutes.

---

## 24. Post-MVP Roadmap

### Phase 1: More Product Categories

- Seating and furniture.
- Lighting products.
- Small appliances.
- Consumer electronics.
- Packaging and retail-display objects.

### Phase 2: Design Memory

- Learn from accepted and rejected findings.
- Store intentional brand exceptions.
- Build product-family pattern libraries.
- Track how brand language evolves over time.
- Recommend new rules from repeated design decisions.

### Phase 3: Team Governance

- Design-lead approval workflows.
- Project and organization rule packs.
- Version history and audit reports.
- Role-based permissions.
- Review gates before asset delivery.

### Phase 4: Tool Integrations

- Rhino.
- Fusion 360.
- SolidWorks.
- KeyShot.
- Cinema 4D.
- Unreal Engine.
- Figma for guideline and presentation assets.

### Phase 5: Engineering and Manufacturing Review

Possible future integrations may evaluate manufacturing or engineering constraints, but these must use appropriate deterministic tools and professional review. They are not extensions of visual brand judgment alone.

---

## 25. Open Product Questions

1. Should the Brand Design Profile be approved once per brand or once per project?
2. Which rules should be allowed to block approval?
3. How should designers resolve conflicts between innovation and product-family consistency?
4. Should dismissed findings become project exceptions or organization-wide memory?
5. Which revision types are trusted enough for Auto-fix?
6. How should the system express uncertainty in visual judgments?
7. What level of Blender integration can be completed reliably during the hackathon?
8. Should concept generation start from procedural geometry, existing assets, or both?
9. How should the product measure improvement without reducing design diversity?
10. Which first commercial segment has the strongest repeated need: design studios, consumer brands, or 3D visualization teams?

---

## 26. Final MVP Definition

The hackathon MVP is a focused demonstration of brand-aware creation and closed-loop review:

> A product designer gives the agent Vela's brand context and a smart-speaker brief. Astra converts that context into explicit product-design rules, creates an editable Blender concept, and renders it from three views. The agent then identifies brand inconsistencies with rule-level and object-level evidence. The designer approves controlled material and detail changes. The system modifies the scene, rerenders the concept, and verifies whether the product now expresses Vela's visual language more clearly.

The MVP succeeds when the audience can see that the system understands not only **what product to generate**, but **why that product belongs to the brand**.
