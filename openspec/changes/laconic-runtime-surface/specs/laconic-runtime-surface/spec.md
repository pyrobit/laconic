## ADDED Requirements

### Requirement: Laconic commands are the primary runtime interface
The runtime SHALL expose Laconic-named commands as the canonical command surface for activation, mode switching, and auxiliary skills. Canonical commands SHALL include `/laconic`, `/laconic terse`, `/laconic balanced`, `/laconic-commit`, `/laconic-review`, and `/laconic-compress`.

#### Scenario: Primary activation uses laconic naming
- **WHEN** a user enters `/laconic`
- **THEN** the runtime activates Laconic prose mode using the configured default Laconic mode

#### Scenario: Explicit Laconic mode selection
- **WHEN** a user enters `/laconic balanced`
- **THEN** the runtime activates Laconic prose mode in `balanced`
- **AND** subsequent runtime state reflects `balanced` as the active mode

#### Scenario: Auxiliary Laconic commands remain separate
- **WHEN** a user enters `/laconic-review`
- **THEN** the runtime activates the review-specific mode
- **AND** the base Laconic prose-mode reminder is not injected for that turn

### Requirement: Badge output uses Laconic labels
The statusline runtime SHALL render Laconic-branded badges for every canonical Laconic mode. Default prose mode SHALL render as `[LACONIC]`; non-default modes SHALL render as `[LACONIC:<MODE>]` using uppercase canonical mode names.

#### Scenario: Default badge label
- **WHEN** the active runtime mode is the default Laconic prose mode
- **THEN** the statusline shows `[LACONIC]`

#### Scenario: Non-default prose mode badge label
- **WHEN** the active runtime mode is `balanced`
- **THEN** the statusline shows `[LACONIC:BALANCED]`

#### Scenario: Auxiliary mode badge label
- **WHEN** the active runtime mode is `commit`
- **THEN** the statusline shows `[LACONIC:COMMIT]`

### Requirement: Runtime-visible prose modes match the Laconic skill
The runtime SHALL use the same primary prose-mode vocabulary exposed by the Laconic skill. User-facing prompts, help text, setup nudges, installer messages, and plugin metadata SHALL advertise `terse` and `balanced` as the primary Laconic prose modes and SHALL not present legacy Caveman-only levels as canonical options.

#### Scenario: Session-start guidance uses Laconic mode names
- **WHEN** the runtime emits SessionStart guidance for Laconic prose mode
- **THEN** the guidance references Laconic naming and Laconic mode names
- **AND** it does not instruct users to switch with Caveman-branded commands

#### Scenario: Command metadata advertises Laconic naming
- **WHEN** a user inspects built-in command metadata or default prompts
- **THEN** Laconic command names and Laconic mode names are shown as the primary interface

### Requirement: Runtime activation uses Laconic-only naming
The runtime SHALL expose Laconic-only command and activation terminology in its public behavior, documentation, and prompts.

#### Scenario: Primary slash command uses Laconic naming
- **WHEN** a user enters `/laconic`
- **THEN** the runtime activates the configured default Laconic prose mode

#### Scenario: Explicit terse mode uses Laconic naming
- **WHEN** a user enters `/laconic terse`
- **THEN** the runtime activates the `terse` Laconic mode
- **AND** the runtime stores and displays the canonical Laconic mode name

#### Scenario: Natural-language activation uses Laconic naming
- **WHEN** a user asks to "use laconic mode"
- **THEN** the runtime activates Laconic prose mode
- **AND** follow-up runtime reminders use Laconic naming
