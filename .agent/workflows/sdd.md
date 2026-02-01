---
description: How to follow the Software Design Document (SDD) workflow
---

# SDD Workflow

Before implementing any complex feature (Milestone B, C, D, F), follow this process:

1. **Create Design Doc**:
   - Copy `docs/design/TEMPLATE.md` to `docs/design/milestone_X_feature_name.md`.
   - Fill out the sections. Focus on API signatures and Risk sections.

2. **Review**:
   - Ask the user to review the design doc.
   - Refine based on feedback.

3. **Implementation Plan**:
   - Create/Update `implementation_plan.md` referencing the agreed design.
   - Break down into small tasks.

4. **Code**:
   - Implement following the design.
   - If you need to deviate significantly, update the design doc first.

5. **Verify**:
   - Ensure implementation matches the behaviors defined in the design.
