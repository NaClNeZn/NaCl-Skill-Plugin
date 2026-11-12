# NaCl Skill Plugin

Personal skills plugin for NaCl's engineering workflows with Kimi Code.

## Features

### Native Skills

- **`ddl-to-service`**: Generate MyBatis-Plus Mapper / Service / ServiceImpl / Controller / QueryBO from DDL or a Java Bean (Domain/Entity class), with Ruoyi framework conventions. Queries use `baseQueryMethod` (QueryBO + LambdaQueryWrapper conditional chaining).
- **`mapstruct-converter-gen`**: Generate MapStruct Converter + DTO + VO from an Entity class. Supports both factory (`Mappers.getMapper`) and Spring DI (`componentModel`) styles.
- **`java-crud-stack-gen`**: Generate complete Java CRUD stack (Entity + Mapper + DTO + QueryBO + VO + Converter + Service + Domain + Controller) from DDL or Entity, with Ruoyi + MyBatis-Plus conventions, Domain aggregation layer, multi-tenant filtering, and logical delete support. Query paths use the `baseQueryMethod` convention from ddl-to-service (QueryBO + LambdaQueryWrapper conditional chaining).

### Bundled External Skills

Three curated skill collections are bundled directly — no external dependencies, version-managed by NaCl.

| Collection | Description | Skills |
|-----------|-------------|--------|
| **Superpowers** | Engineering workflow methodology (via [obra/superpowers](https://github.com/obra/superpowers)) | 14 skills: brainstorming, writing-plans, systematic-debugging, TDD, verification, parallel agents, code review, and more |
| **Agent Skills for Context Engineering** | Agent system design patterns (via [muratcankoylan/Agent-Skills-for-Context-Engineering](https://github.com/muratcankoylan/Agent-Skills-for-Context-Engineering)) | 17 skills: context fundamentals, degradation, compression, multi-agent patterns, memory, harness engineering, evaluation, and more |
| **SuperClaude Framework** | Pre-implementation checks and specialized workflows (via [SuperClaude-Org/SuperClaude_Framework](https://github.com/SuperClaude-Org/SuperClaude_Framework)) | 6 skills: confidence-check, brainstorm, deep-research, pm, token-efficiency, troubleshoot |

Bundle manifest: [`skills/external/manifest.json`](skills/external/manifest.json)

## Project Structure

```
nacl-skill/
├── .kimi-plugin/
│   └── plugin.json                  # Plugin manifest & skill registry
├── skills/
│   ├── using-naclskill/             # Session startup skill
│   ├── ddl-to-service/               # DDL → MyBatis-Plus service generator
│   ├── mapstruct-converter-gen/      # Entity → MapStruct Converter + DTO + VO
│   ├── java-crud-stack-gen/          # DDL/Entity → Java CRUD stack (8 files)
│   └── external/                     # Bundled third-party skills
│       ├── manifest.json             # External skills index & version info
│       ├── superpowers/              # 14 Superpowers skills
│       ├── agent-skills/             # 17 Context Engineering skills
│       └── superclaude/              # 6 SuperClaude skills
├── hooks/
│   └── hooks.json                    # Session hooks
├── scripts/
│   ├── update_external_skills.py     # Sync bundled skills from upstream repos
│   └── build_dsh_layout.py           # Flatten all skills to repo root for DSH
├── .nacl-dsh-skills.json             # Manifest of script-generated root skill dirs
├── {skill-name}/SKILL.md × 48        # Auto-generated flat layout for DSH (DeepSeek Harness)
├── package.json
├── AGENTS.md
└── README.md
```

## Integration Rules

1. **Process skills come first** — set approach, then implement
2. **confidence-check** (SuperClaude): Use BEFORE any implementation to verify >=90% readiness
3. **context-*** skills: Use when managing long context or multi-agent systems
4. **Superpowers skills**: Use for daily engineering workflow

## Installation

Copy this directory to your Kimi Code managed plugins folder, or reference it as a local plugin.

## Updating External Skills

1. Update manifest.json with new version info
2. Replace the relevant `SKILL.md` files in `skills/external/{collection}/`
3. Update `skillInstructions` in `plugin.json` if new skills are added
4. Run `python scripts/build_dsh_layout.py` to refresh the root-level flat layout

> Note: `python scripts/update_external_skills.py` runs the DSH layout rebuild
> automatically at the end of every sync (including the weekly CI workflow).

## DSH (DeepSeek Harness) Compatibility

DSH's skill discovery only scans **direct children** of a skill root
(`<root>/<id>/SKILL.md` or `<root>/<id>.md`). The Kimi Code layout
`skills/external/{collection}/{skill}/SKILL.md` is nested too deep, so
`scripts/build_dsh_layout.py` flattens every skill — native and external —
into `{skill-name}/SKILL.md` **at the repo root** (48 dirs), normalizing the
frontmatter to DSH rules (`name` = kebab-case dir name, description ≤500 chars
on one line). Generated dirs are tracked in `.nacl-dsh-skills.json`; re-runs
only touch script-created directories.

Point DSH's GitHub repo import at this repo and all 48 skills are discovered.
Kimi Code is unaffected: `plugin.json` still points at `./skills/`.

## License

MIT
