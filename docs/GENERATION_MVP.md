# Brand-aware generation workflow

See [PRD.md](PRD.md) for the complete implementation-aligned scope and [README](../README.md) for setup.

1. Create a project with empty brand/product context.
2. Queue guideline documents, logos or references and describe the product in Chat. Send uploads the files and starts interpretation.
3. Review Brand/Product cards. Context changes invalidate approvals.
4. Approve rules, then click Build concept. Planning and generation start directly; the canvas indicates preparation and rendering.
5. Review the GLB and three renders, compare versions, or download the `.blend`.
6. For personal revisions, update the direction in Chat and build again. This is regeneration, not a restricted component patch.
7. For existing feedback, approve/remove every comment, click Redesign, inspect the summary and click Rebuild. Only accepted comments enter planning; blockers prevent execution.
8. Rebuild applies approved allowlisted properties to a source copy and verifies the result before making it current.

The component builder supports boxes, cylinders, spheres, cones and tori across product categories. Restricted redesign supports color, roughness, metallic, dimensions, position, rotation and bevel. It does not add parts or change logos/cameras/lights. Initial outputs are visual concepts, not engineering validation.

Team comments currently come from local records or fixtures. The interface does not publish projects, authenticate teammates, or provide a second comment composer. The sidebar and sample reviewer profiles are fictional. Cross-team alignment remains deferred in [TEAM_ALIGNMENT_IDEA.md](TEAM_ALIGNMENT_IDEA.md).
