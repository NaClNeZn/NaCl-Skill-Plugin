---
name: using-naclskill
description: Use when starting any conversation - establishes NaCl skill framework and requires skill invocation before any response
---

<SUBAGENT-STOP>
If you were dispatched as a subagent to execute a specific task, ignore this skill.
</SUBAGENT-STOP>

<EXTREMELY-IMPORTANT>
If you think there is even a 1% chance a skill might apply to what you are doing, you MUST invoke the skill.

IF A SKILL APPLIES TO YOUR TASK, YOU DO NOT HAVE A CHOICE. YOU MUST USE IT.

This is not negotiable. You cannot rationalize your way out of this.
</EXTREMELY-IMPORTANT>

## The Rule

**Invoke relevant or requested skills BEFORE any response or action** — including clarifying questions, exploring the codebase, or checking files.

## Available Skills

### Native Skills (nacl-skill)
- **ddl-to-service**: Generate MyBatis-Plus Mapper/Service/ServiceImpl/Controller/QueryBO from DDL or a Java Bean (Domain/Entity class), with Ruoyi conventions. Queries use `baseQueryMethod` (QueryBO + LambdaQueryWrapper conditional chaining).
- **mapstruct-converter-gen**: Generate MapStruct Converter + DTO + VO from an Entity class. Supports both factory (Mappers.getMapper) and Spring DI (componentModel) styles.
- **java-crud-stack-gen**: Generate complete Java CRUD stack (Entity+Mapper+DTO+QueryBO+VO+Converter+Service+Domain+Controller) from DDL or Entity, with Domain aggregation layer and BaseController. Queries use the baseQueryMethod convention from ddl-to-service (QueryBO + LambdaQueryWrapper conditional chaining).

### Superpowers (skills/external/superpowers/)
- **using-superpowers**: Master skill routing to all other superpowers skills
- **brainstorming**: Structured brainstorming before any implementation
- **writing-plans**: Write implementation plans before coding
- **systematic-debugging**: Step-by-step debugging methodology
- **test-driven-development**: TDD workflow
- **verification-before-completion**: Verify work before declaring done
- **dispatching-parallel-agents**: Parallel agent orchestration
- **executing-plans**: Execute pre-written plans safely
- **subagent-driven-development**: Delegate to subagents effectively
- **finishing-a-development-branch**: Complete feature branches
- **receiving-code-review / requesting-code-review**: Code review workflows
- **using-git-worktrees**: Git worktree parallel development
- **writing-skills**: How to write new skills

### Context Engineering (skills/external/agent-skills/)
- **context-fundamentals**: Context mechanics in LLM agents
- **context-degradation**: Detect and prevent context degradation
- **context-compression**: Compression for long sessions
- **context-optimization**: Signal-to-noise maximization
- **multi-agent-patterns**: Supervisor, swarm, hierarchical architectures
- **memory-systems**: Memory design patterns
- **tool-design**: Design robust agent tools
- **filesystem-context**: Filesystem as external context
- **hosted-agents**: Remote sandbox infrastructure
- **long-horizon-prompting**: Launch prompt design
- **latent-briefing**: KV memory sharing
- **evaluation / advanced-evaluation**: Evaluation frameworks
- **harness-engineering**: Operating loop reliability
- **self-improvement-loops**: Meta-improvement patterns
- **project-development**: LLM-assisted development
- **bdi-mental-states**: BDI agent modeling

### SuperClaude Framework (skills/external/superclaude/)
- **confidence-check**: Pre-implementation confidence >=90%
- **brainstorm**: Brainstorming methodology
- **deep-research**: Research workflows
- **pm**: Project management
- **token-efficiency**: Token optimization
- **troubleshoot**: Systematic troubleshooting

## Skill Priority

Process skills come first — they set the approach, then implementation skills carry it out.

- "Generate service from DDL" → nacl-skill:ddl-to-service
- "Generate converter/DTO/VO from Entity" → nacl-skill:mapstruct-converter-gen
- "Generate full CRUD stack" → nacl-skill:java-crud-stack-gen
- "Let's build X" → superpowers:brainstorming → superpowers:writing-plans → [implementation skill]
- "Fix this bug" → superpowers:systematic-debugging → [domain skill]
- "Starting implementation" → superclaude:confidence-check → [implementation]
- "Multi-agent design" → agent-skills:multi-agent-patterns
- "Context optimization" → agent-skills:context-fundamentals / context-optimization

## Red Flags

| Thought | Reality |
|---------|---------|
| "This is just a simple question" | Questions are tasks. Check for skills. |
| "Let me explore the codebase first" | Skills tell you HOW to explore. Check first. |
| "I'll just do this one thing first" | Check BEFORE doing anything. |
