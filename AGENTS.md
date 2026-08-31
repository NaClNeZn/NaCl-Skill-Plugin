# NaCl Skill Plugin

Personal skills plugin for NaCl's engineering workflows.

## Plugin Structure

- `.kimi-plugin/plugin.json` — Plugin manifest & skill registry
- `skills/using-naclskill/` — Session startup skill (always invoked first)
- `skills/ddl-to-service/` — DDL → MyBatis-Plus service generator
- `skills/external/` — Bundled third-party skills (Superpowers, Context Engineering, SuperClaude)
- `hooks/hooks.json` — Session hooks

## Bundled Skills

Three external skill collections are bundled in `skills/external/`:

| Collection | Source | Skill Count |
|-----------|--------|-------------|
| Superpowers | github.com/obra/superpowers | 14 |
| Context Engineering | github.com/muratcankoylan/Agent-Skills-for-Context-Engineering | 17 |
| SuperClaude | github.com/SuperClaude-Org/SuperClaude_Framework | 6 |

See `skills/external/manifest.json` for the full index with descriptions.

## Adding New External Skills

1. Clone the source repo
2. Copy `SKILL.md` files to `skills/external/{collection}/{skill-name}/`
3. Update `skills/external/manifest.json` with the new entry
4. Update `skillInstructions` in `.kimi-plugin/plugin.json`

## Conventions

- Generated code follows Ruoyi + MyBatis-Plus conventions
- ServiceImpl extends `ServiceImpl<Mapper, Entity>`
- Controller extends `BaseController`
- QueryBO lives in `domain.{module}.bo`
- baseQueryMethod uses LambdaQueryWrapper with conditional chaining
