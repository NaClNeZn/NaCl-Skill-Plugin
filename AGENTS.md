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
- QueryBO package: ddl-to-service 默认 `domain.{module}.bo`；java-crud-stack-gen 默认 `{basePackage}.{module}.bo`（`{module}/bo/`），但**非固定**——结合项目现有 BO 结构与查询场景动态匹配（`{boPackage}`），检测后向用户确认
- baseQueryMethod uses LambdaQueryWrapper with conditional chaining
- All query paths in generated code use the `baseQueryMethod` convention (ddl-to-service): standalone `{Prefix}QueryBO` + `LambdaQueryWrapper` conditional chaining; java-crud-stack-gen queries follow the same convention
- Fixed conditions (`hospitalId` / `STATUS`) are optional comment templates per baseQueryMethod convention — not mandatory
- Internal method calls in generated classes use `this.xxx()` style (no bare calls)
- "Domain" in ddl-to-service 指 **Java Bean**（持久化实体/POJO），不是聚合根
- DTO 命名 `{Prefix}{DtoSuffix}`：`SaveDTO` 或 `DTO`，按项目习惯
- Service 风格按项目习惯：直接类 `{Prefix}Service`，或 `I{Prefix}Service` 接口 + `{Prefix}ServiceImpl`
- Converter 按项目 MapStruct 约定生成 Style A（factory + INSTANCE）或 Style B（`componentModel = "spring"`）
- javadoc 统一 `@author {author}` + `@date {date}`
