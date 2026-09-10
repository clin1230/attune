# Product Requirements Document

## Attune: Collaborative 3D Concept Prototyping

**Version:** 2.1  
**Status:** MVP  
**Primary user:** Product designer  
**MVP category:** Compact desktop speaker

## 1. Product Summary

Attune helps designers turn product requirements and brand guidelines into a high-level 3D concept. The designer can publish the concept for team feedback, choose which comments should be considered, and ask the agent to create a new version from the accepted comments.

The product has two goals:

1. Help designers brainstorm and prototype ideas quickly without needing advanced Blender skills.
2. Make team feedback easier to collect, evaluate, and use in the next design iteration.

### Core Workflow

```text
Product requirements + Brand guidelines
                    ↓
       Generate and validate 3D concept
                    ↓
          Publish concept to team
                    ↓
             Collect feedback
                    ↓
     Designer accepts or removes comments
                    ↓
        Designer clicks “Redesign”
                    ↓
        Generate and validate new version
```

## 2. Problems

### Slow 3D Prototyping

Blender and similar tools have a steep learning curve. Designers may spend too much time learning 3D software or waiting for 3D support before they can visualize and discuss an early idea.

Attune creates an editable first concept from the designer's requirements and brand guidance so the team can evaluate the idea sooner.

### Fragmented Team Feedback

Feedback is often spread across meetings, messages, screenshots, and documents. The designer must organize the comments and manually translate them into design changes.

Attune keeps feedback with the correct design version. The designer decides which comments matter, and the agent uses only those comments to prepare the next version.

## 3. Users

### Designer

- Provides product requirements and brand guidelines.
- Reviews and publishes the generated concept.
- Accepts or removes team comments.
- Starts and approves a redesign.
- Retains final control over the design.

### Team Reviewer

- Views a published 3D concept and its renders.
- Leaves feedback on that version.
- Cannot modify the model or approve a redesign.

For the local MVP, reviewers use selectable local identities. Remote accounts and authentication are not included.

## 4. Feature 1: Generate the First 3D Concept

### Input

- Product description and functional requirements in the textbox.
- Designer can upload the Brand guideline pdf file.

### Flow

1. The agent converts the inputs into a structured 3D generation plan.
2. The designer reviews and approves the plan.
3. Blender generates a file.
4. The system creates a GLB preview and front, three-quarter, and detail renders.
5. The system measures the scene and validates the output.

### Validation

The generated version is valid when:

- Required product components exist.
- Reviewable objects have stable IDs.
- The Blender scene and GLB preview can be opened.
- Required renders exist.
- Scene dimensions and materials can be measured.

Validation must use fresh measurements and renders. A successful command alone does not prove that the model is valid.

## 5. Feature 2: Publish and Gather Feedback

### Flow

1. The designer publishes a validated design version.
2. The team opens the published 3D preview and renders.
3. Each reviewer selects a local identity and leaves comments.
4. Comments may optionally reference a render view or model object.

### Rules

- A publication is a fixed snapshot of one design version.
- Later changes must not alter an older publication.
- Every comment records its reviewer, time, and design version.
- Reviewers can comment but cannot change the model.
- The interface shows whether reviewers are viewing the latest version.

## 6. Feature 3: Evaluate Feedback and Redesign

### Comment Decisions

The designer marks each comment as:

- **Accepted:** include it in the next redesign.
- **Removed:** keep it in the history, but do not use it in the redesign.

### Redesign Flow

1. The designer evaluates the comments.
2. The designer clicks **Redesign**.
3. The agent uses only accepted comments to create a redesign plan.
4. The system identifies conflicting or unsupported requests.
5. The designer reviews and approves the proposed changes.
6. Blender applies only the approved changes to a new scene version.
7. The system creates fresh measurements, previews, and renders.
8. The designer compares the original and redesigned versions.

The agent cannot treat comments as permission to edit. No model change occurs until the designer approves the redesign plan.

### Supported MVP Changes

- Change an approved material or color.
- Adjust supported product proportions.
- Adjust the size or position of a non-structural detail.
- Adjust lighting or review-camera settings.

Unsupported changes are clearly labeled and require manual editing.

## 7. Required Screens

### Project Setup

- Product requirements.
- Brand guidelines and references.
- Generate action.

### Concept Workspace

- 3D preview and renders.
- Validation status and version number.
- Publish button.

### Team Review

- Published concept and version.
- Reviewer identity selector.
- Comment form and comment list.

### Feedback and Redesign

- Accepted and removed comment controls.
- Redesign button.
- Proposed changes and conflicts.
- Approve or cancel controls.
- Before-and-after comparison.

## 8. System Architecture

```text
┌──────────────────────────────────────────────┐
│               Local React App                │
│ Concept · Publish · Feedback · Redesign     │
└──────────────────────┬───────────────────────┘
                       │ Local HTTP
                       ▼
┌──────────────────────────────────────────────┐
│               FastAPI Backend                │
│ Projects · Versions · Comments · Approvals  │
└──────────────┬──────────────────┬────────────┘
               │                  │
               ▼                  ▼
┌──────────────────────┐  ┌────────────────────┐
│ Agent                │  │ SQLite             │
│ Generation and       │  │ Project state and  │
│ redesign planning    │  │ feedback history   │
└───────────┬──────────┘  └────────────────────┘
            │ Validated plan
            ▼
┌──────────────────────────────────────────────┐
│         Allowlisted Blender Worker           │
│ Generate · Edit · Measure · Render          │
└──────────────────────┬───────────────────────┘
                       ▼
┌──────────────────────────────────────────────┐
│             Versioned Artifacts              │
│ .blend · GLB · manifest · renders           │
└──────────────────────────────────────────────┘
```

### Responsibilities

**React app**

- Provides the designer workspace and team review interface.
- Prevents reviewers from accessing model-edit actions.

**FastAPI backend**

- Validates inputs and agent outputs.
- Stores projects, versions, publications, comments, and approvals.
- Uses only accepted comments for redesign.
- Rejects stale redesign requests.
- Preserves the last valid version when a job fails.

**Agent**

- Creates generation plans from requirements and brand guidelines.
- Creates redesign plans from accepted comments.
- Identifies conflicts and unsupported requests.
- Produces validated data, not arbitrary Blender code.

**Blender worker**

- Generates the editable scene.
- Applies approved, allowlisted changes.
- Maintains stable object IDs.
- Saves a new version instead of overwriting the old one.
- Produces fresh measurements and renders.

**Storage**

- SQLite stores project state, publications, comments, decisions, and approvals.
- The local filesystem stores versioned Blender scenes, GLB previews, manifests, and renders.

### MVP Boundary

The MVP runs on one local machine. “Publish to the team” means publishing to a local review workspace with simulated reviewer identities.

Remote collaboration, accounts, invitations, notifications, and public links are outside the MVP.

## 9. Core Requirements

| ID | Requirement |
|---|---|
| GEN-01 | Generate an editable 3D concept from product requirements and brand guidelines. |
| GEN-02 | Validate the concept with fresh scene measurements and renders. |
| PUB-01 | Let the designer publish an immutable design version. |
| COM-01 | Let reviewers leave version-specific comments. |
| COM-02 | Prevent reviewers from modifying the model. |
| REV-01 | Let the designer accept or remove comments. |
| REV-02 | Use only accepted comments in a redesign plan. |
| REV-03 | Require designer approval before changing the model. |
| REV-04 | Create a new version without overwriting the old one. |
| REV-05 | Change only approved objects and properties. |
| REV-06 | Validate the redesigned version with fresh evidence. |
| REV-07 | Show which accepted comments caused each change. |

## 10. MVP Acceptance Criteria

- [ ] A designer can provide product requirements and brand guidelines.
- [ ] The system generates an editable compact speaker concept.
- [ ] The system validates the model and produces a GLB preview and three renders.
- [ ] The designer can publish the validated version.
- [ ] Reviewers can add comments to that version.
- [ ] The designer can accept or remove comments.
- [ ] Clicking Redesign creates a plan from accepted comments only.
- [ ] The designer must approve the plan before model changes.
- [ ] The redesign creates and validates a new version.
- [ ] The original version remains available.
- [ ] The designer can see which comments caused each change.

## 11. Final MVP Definition

> A designer provides product requirements and brand guidelines. Attune generates and validates an editable 3D concept. The designer publishes it to a local team review workspace, where teammates leave feedback. The designer accepts or removes comments and clicks Redesign. Attune creates a plan from only the accepted comments, asks for approval, produces a new model version, and validates the result.

Attune succeeds when it helps designers prototype ideas faster, gather feedback more easily, and iterate without losing control of the design.
