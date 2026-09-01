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

## License

MIT
