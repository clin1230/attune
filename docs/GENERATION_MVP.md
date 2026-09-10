# Brand-aware 3D generation MVP

The current product focus is a separate workspace per project: brand sources and product brief → documented brand understanding → reviewed design decisions → editable 3D concept. Designer/PM agents and deadline-risk scoring are deferred.

Inputs include brand/design/product guideline documents (PDF, DOCX, Markdown, text), logo and reference images (PNG/JPEG/WebP), three palette colors, typography notes, functional requirements, target user, design constraints, deadline, and an optional effort/budget note. Conversation updates append or replace an explicitly selected guideline with version history. These updates invalidate earlier approvals.

Brand extraction and design planning use the configured OpenAI Responses API. Without API configuration the interface clearly disables automated interpretation; users can supply rules and parameters manually. Uploaded text is source material, not executable instructions. Model-generated decisions must cite sources or identify inferences.

The current Blender generator supports desktop speakers: width, height, depth, corner radius, shell/grille/accent colors, shell roughness and uploaded logo or brand wordmark. Other product categories are rejected until a corresponding builder is implemented. Typography notes and references inform AI planning but do not automatically install fonts or reconstruct reference geometry. Functional requirements, deadlines and budgets are context, not engineering guarantees or estimates.

Outputs are an editable Blender scene, interactive GLB, three rendered views, stable object IDs and version history. Each project has separate documents, messages, inputs and versions. Blender jobs serialize across projects because they share one local Blender process. This local workspace is not a multi-user authentication system.
