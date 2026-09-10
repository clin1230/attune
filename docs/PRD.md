# Attune — Product Requirements Document

**Version:** 3.0 · **Updated:** 2026-09-10
**Status:** Implementation-aligned local MVP
**Primary user:** Product designer

This document describes the current code, with future capabilities explicitly separated. It supersedes earlier speaker-only and publish-to-team specifications. The product intent remains faster concept prototyping with brand context and designer-controlled iteration.

## 1. Product and problem

Attune helps designers create a product **for a brand**, using guidelines, references, and a conversational brief. It reduces the work of translating those inputs into an early editable 3D concept and keeps revisions tied to their context and feedback.

The current experience is single-user on one local machine. Team review is represented through stored version-specific comments and sample reviewer identities; actual multi-user collaboration is future work.

## 2. Inputs and outputs

Inputs include brand/design/product guidelines in text-based PDF, DOCX, Markdown or text; logos, references and moodboards in PNG, JPEG or WebP; and chat messages describing product type, functions, target users, constraints, deadline and optional effort/budget notes. Typography and palette are captured in the interpreted brand context. The intake schema currently requires three palette colors; this is a working interpretation, not proof that the source specified exactly three colors.

Outputs are a declarative product plan, an editable `.blend`, an interactive GLB, front/three-quarter/detail renders, an object manifest, and version history. Redesigns also store approved field changes and a verification report.

Product categories are not allowlisted. The component builder uses boxes, cylinders, spheres, cones and tori, with stable IDs, dimensions, position, rotation, color, roughness, metallic and bevel. Local examples include chargers, speakers and a laptop. This does not imply arbitrary CAD capability or exact reconstruction of reference images.

## 3. Project setup and conversational intake

1. Create a named project with an optional brand name. Each project owns its conversation, sources, rules, plans, feedback and versions.
2. A new project has no preset palette, rules or product dimensions. Its context area invites source upload or a description in Chat. A legacy default Vela demo record may still exist locally.
3. Attachments remain queued until Send. Users can remove queued files or send files without text. Enter sends, Shift+Enter adds a newline, and IME composition does not submit.
4. Sending clears the composer immediately, uploads the queue, and requests AI understanding. A visible spinner describes the work. A sent-message placeholder bridges the wait for persisted chat state.
5. AI returns a natural reply and structured brand/product context, with source-attributed rules and qualified interpretations. Source documents are treated as data.
6. Brand and Product cards appear above a separate Chat panel. They show vibe, typography, palette, expandable rules, functions, audience, constraints and timing. Detailed style-interpretation chips are omitted from the current UI.
7. Changed context invalidates rule and build-plan approval. Stale responses are rejected using context revisions. Already saved messages/files remain available after AI errors, with a retry action.

Partial uploads are possible if a submission fails midway; file persistence is not an atomic transaction across the entire attachment batch. Unknown engineering requirements must not be presented as validated capabilities.

## 4. Initial concept generation

1. The designer presses **Review & approve rules**. The button indicates whether approval is needed or complete.
2. **Build concept** requests a component plan, validates it, approves the plan through the application flow, then starts Blender. There is no separate initial-plan approval dialog.
3. The canvas shows preparation immediately and rendering status while the scene job runs. Existing versions remain stored.
4. The backend prefers the local Blender GUI via MCP; otherwise it attempts background Blender. Only one scene job runs across projects at a time.
5. Blender builds the parts and a studio scene, adds logo/wordmark treatment where applicable, exports the preview and three renders, and writes a completion marker.
6. The new version becomes current after successful completion. Failures expose an error and do not create a successful version entry.

The plan schema and generated artifacts provide technical checks. Initial generation is not a comprehensive brand audit, physical-fit test, or engineering validation. The completion marker is not a guarantee of design quality.

## 5. Concept workspace and history

- White interface with a project sidebar, product canvas, design-direction cards and Chat.
- View controls for interactive 3D, perspective, front and detail; comparison against a source/other version; `.blend` download.
- No component-label strip below the canvas.
- A compact rebuild banner identifies the version and changed properties, including before/after color values.
- One concept-history stream. Expandable details include specification/context changes, rationale, source version, feedback decisions and approved edits where recorded. Raw project-update cards are not a separate visible history.
- Opening an earlier version changes the current selection; stored artifacts are retained. Older records may lack detailed snapshots.
- Each project has a delete control with confirmation. Current implementation is soft deletion: hidden from the project list, data retained. There is no restore-from-trash UI. Deletion is blocked during a scene job.

## 6. Team feedback and controlled redesign

### Current feedback surface

The designer sees comments for the selected version, with an optional reviewer name, role and small illustrated avatar. Local sample identities are fictional, not authenticated users. The visible UI has no hackathon banner, sample-loader button, reviewer identity selector, publication action, or extra comment composer. The local backend retains comment creation and sample-seeding endpoints. Sample comments in the development database are not shipped with the repository.

Personal revisions use Chat followed by rule review and another build. This path updates context and regenerates a concept; it does not promise preservation of every unchanged component. The feedback redesign path below is the restricted-edit workflow.

### Decisions and flow

1. Comments start pending. The designer selects **Approve** (stored as `accepted`) or **Remove** (stored as `removed`) for every comment.
2. Removed comments and decision history remain stored but are excluded from the redesign prompt.
3. **Redesign** requires approved brand rules, a component-based current version, no pending decisions, and at least one accepted comment.
4. The agent proposes edits using only accepted comments. Each change references accepted comment IDs; accepted feedback must be accounted for by changes or blockers.
5. A summary dialog presents before/after changes. Conflicts, unsupported requests and missing clarification block rebuilding.
6. **Rebuild** explicitly approves all displayed proposed changes. There is no separate “Approve proposal” step or per-change checkbox in the current UI.
7. The backend rejects stale/reused proposals and binds the approval to the source, source-file hash, feedback revision and project context.
8. Blender copies the source file, imports the copied scene and applies only the approved fields. The original scene file is retained.
9. Verification, a fresh manifest, GLB and three renders are produced. On success the new version becomes current and comparison uses its source. Failure leaves the source current and records an error.

### Allowed edits and verification boundary

Allowed properties are **color, roughness, metallic, dimensions_mm, position_mm, rotation_deg and bevel_mm** on existing components. Adding/removing parts, new logo placement, arbitrary code, lighting/camera changes and unsupported properties are not supported by this redesign path. Existing logo treatment may be preserved, but logo editing is not an allowlisted redesign operation.

Verification compares object membership, geometry hashes, transforms, primary material values, bevel and light energy against expected edits. It does not prove collision clearance, manufacturability, functional performance, exact brand fidelity, or preservation of every possible Blender data property.

## 7. Architecture and persistence

React/TypeScript handles the workspace; Three.js loads GLB previews. FastAPI validates requests and model output, stores state in SQLite, and starts scene jobs on a background thread. The configured OpenAI Responses API produces structured context, component plans and redesign proposals. Blender MCP invokes checked-in Python workers in the GUI; background Blender is the fallback.

`backend/main.py` owns project/intake/job orchestration; `backend/redesign.py` owns feedback approvals; `backend/mcp_bridge.py` owns MCP transport; `blender/product.py`, `scene.py` and `redesign.py` generate, render and verify scenes.

Project state is in `data/workspace.sqlite`, sources in `data/uploads/`, artifacts in `outputs/demo/<version>/`. Versions retain specifications and change evidence where available. Jobs are in-process, not a durable worker queue; automatic recovery after a server restart is not implemented. The header's Blender connection indicator checks socket reachability.

Credentials remain on the backend in environment variables or ignored `.env.local`. No credentials, local project database or generated artifacts belong in Git. There is no authentication or enforced designer/reviewer permission separation; this is a trusted local workspace.

## 8. Acceptance criteria and current status

| ID | Criterion | Status |
|---|---|---|
| PROJ-01 | Isolated projects with empty new-project context | Implemented; legacy demo retained |
| PROJ-02 | Delete a project with confirmation | Implemented as soft deletion |
| CHAT-01 | Queue attachments until Send and clear submitted text immediately | Implemented |
| CHAT-02 | Interpret sources and brief, show cards and useful waiting/error states | Implemented; requires AI access |
| GEN-01 | Approve rules, then build a generic component concept | Implemented |
| GEN-02 | Provide editable scene, GLB, manifest and three renders | Implemented; requires successful Blender job |
| HIST-01 | Compare/open versions and inspect detailed changes | Implemented; legacy detail coverage varies |
| REV-01 | Accept/remove version-specific comments | Implemented |
| REV-02 | Use accepted comments only and reject stale/conflicting proposals | Implemented |
| REV-03 | Apply changes only after explicit Rebuild approval | Implemented |
| REV-04 | Preserve source and verify allowed edits in a new version | Implemented within stated verification scope |
| TEAM-01 | Publish, invite reviewers, receive remote comments, enforce roles | Not implemented |

Repository checks are `npm run build` and backend unittest discovery (currently 31 tests). Tests do not substitute for a live Blender run or designer review.

## 9. Deferred capabilities

Authenticated teammate accounts, publication snapshots, invitations, public links, notifications, a real teammate comment composer, cross-project/team brand-alignment analysis, autonomous Designer/PM agents, deadline-risk or effort scoring, image-first preview generation, automatic cheaper-model routing, production CAD and engineering verification remain outside the current implementation.

The intended next collaboration layer can reuse version-specific feedback and designer approval. It must introduce real identity, access control and comment submission before being described as a working multi-user product.
