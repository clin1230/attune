# Brand-aware 3D generation MVP

The current product focus is a separate workspace per project: brand sources and product brief → documented brand understanding → reviewed design decisions → editable 3D concept. Designer/PM agents and deadline-risk scoring are deferred.

Inputs include brand/design/product guideline documents (PDF, DOCX, Markdown, text), logo and reference images (PNG/JPEG/WebP), three palette colors, typography notes, functional requirements, target user, design constraints, deadline, and an optional effort/budget note. Conversation updates append or replace an explicitly selected guideline with version history. These updates invalidate earlier approvals.

Brand extraction and design planning use the configured OpenAI Responses API. Without API configuration the interface clearly disables automated interpretation; users can supply rules and parameters manually. Uploaded text is source material, not executable instructions. Model-generated decisions must cite sources or identify inferences.

The Blender generator accepts product categories through a validated declarative component plan. Named boxes, cylinders, spheres, cones and tori have dimensions, positions, rotations, colors, finishes and bevels. This supports editable visual concepts such as portable chargers, furniture, lights and speakers without a category allowlist. Complex organic shapes, exact image reconstruction, functional internals and production CAD are not guaranteed. The original speaker worker remains for seeded legacy demos. Typography notes and references inform AI planning but do not automatically install fonts or reconstruct reference geometry. Functional requirements, deadlines and budgets are context, not engineering guarantees or estimates.

Outputs are an editable Blender scene, interactive GLB, three rendered views, stable object IDs and version history. Each project has separate documents, messages, inputs and versions. Blender jobs serialize across projects because they share one local Blender process. This local workspace is not a multi-user authentication system.

## Conversation workspace

Brand and product cards stay above the conversation with style, vibe, typography direction, palette, requirements, target user and constraints. Files are queued locally in the composer, with removal available. Nothing is uploaded or sent to AI until Send (or Enter) is pressed. A file-only submission is allowed. Sending uploads the queue then runs understanding once with the message and saved sources. The cards remain drafts until reviewed. Two primary actions open rule approval and concept planning. No model generation starts on a chat message alone. Input errors preserve messages/uploads and expose a retry. Context revisions reject stale model responses. Product-only conversation changes preserve brand approval when the brand context and rules are unchanged, but invalidate the build plan.

New concept versions record their specification, rule version, source version, parameter changes and rationale. Earlier versions without snapshots are explicitly marked as lacking detailed change records. Brand/brief updates retain before-and-after context. The shared-team alignment idea is saved in TEAM_ALIGNMENT_IDEA.md and remains deferred.

## Evaluate feedback and redesign

Each comment belongs to a source concept and starts as Needs decision. Accepted comments enter planning; Removed comments remain saved with decision history but are excluded from the model prompt. All comments must be evaluated before requesting a proposal. Redesign is available for concepts with component specifications; legacy concepts without a specification require a new build.

The proposal includes only allowlisted component properties: color, roughness, metallic, dimensions, bevel, position and rotation. Conflicts, unsupported requests and unresolved clarifications block execution until feedback is resolved and a fresh proposal is generated. Each proposed change cites accepted comment IDs. Every accepted comment must be accounted for. Requests requiring coupled edits are flagged for clarification because selective approval must remain independent.

Nothing executes until the designer checks changes and presses Approve changes & redesign. The backend validates selections and binds approval to the source file hash, selected version, feedback decisions, current brand rules and project context. Submitted proposals cannot be reused. Source scenes are appended as copies; only approved properties change. Fresh manifests, GLBs and three renders are produced. Object membership, geometry hashes, transforms, primary material values, bevel and light energy are compared with the expected changes. These checks do not constitute engineering or subjective brand validation. Failed jobs keep the source current and expose the failure on the proposal.

Successful redesign versions retain source version, accepted feedback, all feedback decisions, selected changes, timestamps and a verification report. Compare uses that source version. Removed feedback is auditable from the source's feedback panel and the resulting version's details.
