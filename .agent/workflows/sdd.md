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
   - Run verification scripts.
   - If verification fails, **FIX** the code and re-run immediately. Do not stop to ask the user unless blocked.
   - Proceed to the next step only after verification passes.

6. **Documentation** (CRITICAL):
   - **Immediately** after verification, update `README.md`.
   - Add new tools to the "Available Tools" table (Name, Description, Arguments).
   - Update the "Features" section if applicable.

7. **Completion**:
   - Only call `notify_user` to finish the milestone **AFTER** `README.md` is updated.
