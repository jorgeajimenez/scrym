# Gemini CLI: Rules of Engagement

## 🛠 Operation Mode: Systematic & Issue-Driven
1. **GitHub Issues First:** NO WORK (implementation, refactoring, or bug fixing) shall be performed without a corresponding GitHub Issue.
2. **Atomic Commits:** Each issue should ideally map to a specific task or feature.
3. **Resource Isolation:** The `resources/nfl/` directory is for **read-only reference**. No code shall be copied directly; logic must be re-implemented to comply with hackathon "New Work" rules.
4. **Mockups:** Visual and UX validation should be placed in the `mockups/` directory as pure JS/HTML/CSS for rapid iteration before full-stack implementation.
5. **Validation:** Every implementation step must be followed by verification (tests/build checks).
6. **No Python Execution:** The agent MUST NEVER execute Python scripts (training, inference, verification, etc.) directly. All script execution is the sole responsibility of the user. The agent shall only provide the necessary commands.

## 🚀 Hackathon Mandates
- **Track:** Statement One - The Playbook (Computational Sports).
- **Primary Deliverable:** 4th Down Bot Demo.
- **Deadline:** Saturday, Jan 31, 2026, 5:00 PM.
- **Compliance:** New Work Only, Open Source.

## 🤖 Interaction Protocol

- **Plan before Acting:** Always propose a plan and obtain approval.

- **Explicit Approval Required:** NEVER start building or working on an issue without a direct "Go ahead" or confirmation from the user for that specific task.

- **Progress Tracking:** Update `PROGRESS.md` immediately upon the completion of any issue or significant milestone.

- **Explain Critical Commands:** Especially those modifying the system or filesystem.

- **Conciseness:** Keep text output minimal and professional.
