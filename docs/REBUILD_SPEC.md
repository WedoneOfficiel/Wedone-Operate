# Wedone Operate — Phoenix rebuild specification

> Working branch: `phoenix-rebuild`
> Baseline: `c4c4dc746c4590aa604d971551f218027a6a9c05`
> This is a greenfield product/UI redesign. The legacy application remains available as a reference and data source; it is not the design constraint.

## Product promise

A polished, reliable, local-first mental-maths practice application for:
- one person practising independently;
- a teacher running a classroom with separate student and teacher entry points;
- school levels from CP through lycée, with exercises grounded in the French curriculum and configurable by skill rather than arbitrary number ranges.

No cloud account, no mandatory network connection, no admin account, and no forced import of legacy data.

## First launch and navigation

The first launch asks one question: **Individual use** or **Classroom use**.

### Individual use
- Opens directly into practice. No "guest account", no login tab, no profile selection.
- Saves personal preferences and optional personal history locally.
- The user can switch to classroom mode in Settings without deleting data.

### Classroom use
- Home screen presents two separate destinations: **Student area** and **Teacher area**.
- Student area: choose class → optional group → student profile. A quick "Practise without a profile" action is secondary, not a third tab.
- Teacher area: teacher profile selection / creation and authentication where configured.
- Teacher profile editing is available in the teacher's own space.
- Groups remain optional.
- No administrator role in the product model.

The selected usage mode is persisted and can be changed later. Changing mode must never silently delete or overwrite data.

## Interface and technology

- Replace the legacy Qt Widgets screens rather than styling them indefinitely.
- Prototype **PySide6 + Qt Quick/QML** for the new UI; keep Python for domain logic, exercise generation, persistence, and services.
- Use reusable QML components and a small, explicit design system: typography, spacing, surfaces, buttons, fields, dialogs, navigation, feedback, charts, and empty states.
- Responsive layout and keyboard-first operation are requirements, not polish tasks.
- Default UI scale should be comfortably larger than the legacy interface.
- Accessibility settings: interface scale, text scale, contrast, reduced motion, and keyboard focus visibility.
- Remove explanatory marketing copy from operational screens. Each screen should prioritise the action the user came to perform.
- Do not claim native blur or platform integration unless implemented and verified.

## Domain and persistence

- Separate domain services from presentation. UI code must not contain business rules or SQL.
- Replace scattered JSON files with a transactional SQLite database, with schema versioning and tested migrations.
- Keep local-first storage under the platform's standard per-user application-data directory.
- Provide an in-app data centre: create backup, restore backup, export, import, and reset.
- Reset must require explicit confirmation and explain exactly what will be removed.
- Keep a safety backup before destructive operations and migrations.
- Legacy JSON import is optional and explicit. Never silently import files from the current working directory or Downloads.
- The new release may break compatibility with old app versions, but must not silently destroy old data. Preserve the old data directory and offer an optional import path.
- Include a clear first-run state, so a clean installation is reproducibly testable.

## Functional scope

### Practice
- Configurable question count, skills, difficulty, optional timer, feedback, and session goals.
- Deterministic, testable exercise generators with seeded test cases.
- Avoid repeated questions within a session where practical.
- Separate "practice" from "assessment" semantics.
- Support partial results if a session is intentionally ended, with clear status.

### Teacher/classroom
- Teacher profiles, classes, optional groups, students, and reusable exercise plans.
- CRUD operations must be consistently available from the relevant user's own space.
- Search, filters, multi-selection, bulk assignment, duplication, archive/restore, and safe deletion.
- Class-level plans with group-specific overrides.
- Student identity and privacy choices must be explicit.

### Progress and statistics
- Define one consistent statistical model. Distinguish question-weighted accuracy from the average of session percentages.
- Student progress by skill, operation, and time period.
- Teacher dashboard with actionable information, not decorative counters.
- Explain sample size and distinguish "no data" from poor performance.
- Export useful student/class reports.

## Curriculum model

Do not encode school level as a single fixed difficulty range. Represent:
- school year / pathway;
- mathematical skill or learning objective;
- number domains and operation families;
- expected strategies / complexity;
- configurable practice difficulty.

Curriculum content must be researched against the official French programmes and their staggered implementation dates. Initial sources:
- Cycle 2 mathematics programme (BO 31 October 2024; in force since 2025): https://www.education.gouv.fr/bo/2024/Hebdo41/MENE2415135A
- Cycle 3 mathematics programme (BO 17 April 2025; phased implementation 2025–2026): https://www.education.gouv.fr/bo/2025/Hebdo16/MENE2504620A
- Cycle 4 mathematics programme (BO 5 March 2026; 5e from 2026, 4e from 2027, 3e from 2028): https://www.education.gouv.fr/bo/2026/Hebdo10/MENE2602912A
- Official Eduscol mental-calculation guidance for CP–CM2: https://eduscol.education.gouv.fr/sites/default/files/document/calcul-mentalv2pdf-111834.pdf
- General/technological lycée mathematics resources and programme rollout: https://eduscol.education.gouv.fr/5817/programmes-et-ressources-en-mathematiques-voie-gt

The lycée model must distinguish general/technological pathways and relevant options/specialities rather than treating "Lycée" as one homogeneous level. Only implement exercise types that the product can assess reliably.

## Quality gates

- Unit tests for every exercise generator and scoring rule.
- Integration tests for first launch, mode switching, student/teacher access, CRUD, and session lifecycle.
- Persistence tests for migrations, backup/restore, corruption recovery, and interrupted writes.
- UI tests for keyboard navigation, focus, scaling, dark/light themes, and window resizing.
- Build and smoke-test on macOS, Windows, and Linux.
- No release from this branch without explicit approval. `main` remains untouched.
- Do not remove or overwrite legacy data during development.

## Delivery sequence

1. Architecture and domain model.
2. New persistence layer and safe backup/import.
3. New first-launch and mode-selection flow.
4. New design system and application shell.
5. Practice engine integration and full session lifecycle.
6. Teacher/student classroom workflows.
7. Statistics and exports.
8. Accessibility, curriculum validation, automated tests, and packaging.

## Acceptance principle

A feature is not complete merely because it compiles. It must be usable through the intended workflow, visually consistent, keyboard-accessible where relevant, recoverable after errors, and covered by tests.
