---
name: ddl-to-service
description: "Generate MyBatis-Plus Mapper/Service/ServiceImpl/Controller/QueryBO from DDL or a Java Bean (Domain/Entity class), following project-specific conventions. Triggered when user wants to scaffold service-layer code from database definitions or entity/domain objects."
---

# DDL to Service Generator

Generate complete MyBatis-Plus service layer code from DDL statements or Domain classes.

> **术语说明**: 本技能中的 "Domain class" 指 **Java Bean**（持久化实体 / POJO，即 Entity/DO/PO 类），不是业务聚合根。若用户提供的类位于 `domain.*` / `pojo.*` / `po.*` 等实体包，即视为 Java Bean。

## Trigger

Invoke this skill when the user:
- Provides a DDL statement and asks to generate service / mapper / controller
- Provides a Domain class and asks to generate the full service stack
- Mentions "生成service" / "从DDL生成" / "生成mapper" in the context of MyBatis-Plus

## Two Input Modes

### Mode A: DDL + Domain provided

User pastes both DDL and the Domain class. Use them as-is.

### Mode B: DDL only

User pastes only DDL. You MUST:
1. Parse the DDL to extract column names, types, and comments
2. Generate a Domain class draft
3. Present the Domain draft to the user for confirmation BEFORE proceeding
4. If user approves, continue to generate all files
5. If user requests changes, revise and re-present

## Project Style Detection

Before generating code, detect the project's conventions by examining existing files in the project. Look at a few ServiceImpl and Controller classes to determine:

### Detection Checklist

1. **BO 命名风格**: 查找已存在的 BO 类命名是 `XxxQueryBO` 还是 `XxxBaseQueryBO`，或是混合使用
2. **BO 包路径**: BO 放在 `domain.{module}.bo` 还是 `pojo.bo` 还是深层嵌套如 `pojo.bo.{submodule}`
3. **Service 接口**: 是否有独立的 `IXxxService` 接口，还是直接用 Service 类继承 `ServiceImpl`
4. **BaseController**: 完整包路径是什么
5. **固定查询条件**: baseQueryMethod 是否有固定的无参过滤条件（如 `Common.getHospitalId()`、状态过滤等）
6. **Controller 日志**: 是否使用 `@Slf4j` + `log.info()`
7. **RequestMapping 风格**: 驼峰 `/dimOrg` 还是 kebab-case `/res-info`，是否多层路径如 `/se/exam/plan/room`
8. **作者标签**: `@author` 用的是什么名字
9. **日期格式**: `@date` 用的日期格式
10. **Bean 命名**: 是否使用 `@Service("beanName")` 指定 bean 名称
11. **依赖注入方式**: `@Resource` 字段注入 还是 `@RequiredArgsConstructor` + `final` 构造器注入
12. **范围查询**: 是否使用 `.le()` / `.ge()` / `.between()` 进行范围条件
13. **排序**: 是否在 baseQueryMethod 中带 `.orderByAsc()` / `.orderByDesc()`
14. **字符串判空**: 是 `StrUtil.isNotBlank()` 还是 `StrUtil.isNotEmpty()` 还是 `StrUtil.isBlank()`

### If Project Cannot Be Detected

如果无法检测项目风格（空项目或新项目），使用**默认风格**：

- BO 命名: `XxxQueryBO`
- BO 包路径: `domain.{module}.bo`
- Service: 生成接口 `IXxxService` + 实现类
- BaseController: `com.ruoyi.common.core.controller.BaseController`
- 固定条件: 无
- Controller 日志: 无
- RequestMapping: 驼峰
- 作者: `ruoyi`
- 日期格式: `yyyy-MM-dd`

Always present detected style to user for confirmation: "检测到项目风格为: BO命名={xxx}, Service接口={有/无}, 固定条件={有/无}, 是否使用? 用户可覆盖。

## Auto-Detection Rules

### Package & Module Resolution

1. Parse `package` declaration from the Domain class
2. Extract module name: the sub-package after `domain.` or `pojo.` (e.g., `domain.dimOrg` → module = `dimOrg`)
3. Extract class prefix: the Domain class simple name minus common suffixes (`Entity`, `DO`, `PO`)
   - If class is `CockpitDimOrg`, prefix = `CockpitDimOrg`
   - If class is `CockpitDimOrgEntity`, prefix = `CockpitDimOrg`

### User Override

Always auto-detect first, then ask: "检测到模块为 `{module}`，类前缀为 `{prefix}`，是否使用?" 用户可回复覆盖。

## Generated Files

根据检测到的项目风格，生成以下文件。如果项目没有 Service 接口，则跳过接口文件。

### 1. Mapper Interface

**Path**: `mapper/{module}/{Prefix}Mapper.java`

```java
package {basePackage}.mapper.{module};

import com.baomidou.mybatisplus.core.mapper.BaseMapper;
import {domainPackage}.{DomainClass};
import org.apache.ibatis.annotations.Mapper;

/**
 * {tableComment}Mapper接口
 *
 * @author {author}
 * @date {date}
 */
@Mapper
public interface {Prefix}Mapper extends BaseMapper<{DomainClass}> {
}
```

### 2. Mapper XML (only if user's project uses XML mappers)

**Path**: `mapper/{module}/{Prefix}Mapper.xml`

```xml
<?xml version="1.0" encoding="UTF-8" ?>
<!DOCTYPE mapper PUBLIC "-//mybatis.org//DTD Mapper 3.0//EN"
    "http://mybatis.org/dtd/mybatis-3-mapper.dtd">
<mapper namespace="{basePackage}.mapper.{module}.{Prefix}Mapper">

    <resultMap type="{domainPackage}.{DomainClass}" id="{Prefix}Result">
        <result property="dayId"    column="day_id"    />
        <!-- one result mapping per DDL column, snake_case → camelCase -->
    </resultMap>

</mapper>
```

### 3. QueryBO / BaseQueryBO

**Path**: `{boPackage}/{Prefix}{BoSuffix}.java`

**Rules**:
- BoSuffix: 根据项目风格是 `QueryBO` 或 `BaseQueryBO`
- BO 包路径: 根据项目风格是 `domain.{module}.bo` 或 `pojo.bo`
- Only include queryable fields (skip large text / blob columns)
- All fields are `String` type by default for varchar columns
- Use `@Builder`, `@Data`, `@AllArgsConstructor`, `@NoArgsConstructor`
- Copy field comments from DDL

```java
package {boPackage};

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.io.Serializable;

/**
 * {tableComment}查询对象
 *
 * @author {author}
 * @date {date}
 */
@Builder
@Data
@AllArgsConstructor
@NoArgsConstructor
public class {Prefix}{BoSuffix} implements Serializable {

    private static final long serialVersionUID = 1L;

    /**
     * {columnComment}
     */
    private String {fieldName};

    // ... one field per queryable column
}
```

### 4. Service Interface (only if project uses interfaces)

**Path**: `service/{module}/I{Prefix}Service.java`

```java
package {basePackage}.service.{module};

import com.baomidou.mybatisplus.extension.service.IService;
import {domainPackage}.{DomainClass};
import {boPackage}.{Prefix}{BoSuffix};

import java.util.List;

/**
 * {tableComment}Service接口
 *
 * @author {author}
 * @date {date}
 */
public interface I{Prefix}Service extends IService<{DomainClass}> {

    /**
     * 基础查询
     *
     * @param queryBO 查询条件
     * @return {tableComment}列表
     */
    List<{DomainClass}> baseQueryMethod({Prefix}{BoSuffix} queryBO);
}
```

### 5. ServiceImpl

**Path**: `service/{module}/impl/{Prefix}ServiceImpl.java`

If project uses Service interface:
```java
package {basePackage}.service.{module}.impl;

import cn.hutool.core.collection.CollUtil;
import cn.hutool.core.util.StrUtil;
import com.baomidou.mybatisplus.core.conditions.query.LambdaQueryWrapper;
import com.baomidou.mybatisplus.extension.service.impl.ServiceImpl;
import {domainPackage}.{DomainClass};
import {boPackage}.{Prefix}{BoSuffix};
import {basePackage}.mapper.{module}.{Prefix}Mapper;
import {basePackage}.service.{module}.I{Prefix}Service;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;

import java.util.List;

/**
 * {tableComment}Service业务层处理
 *
 * @author {author}
 * @date {date}
 */
@Service
@Slf4j
public class {Prefix}ServiceImpl extends ServiceImpl<{Prefix}Mapper, {DomainClass}> implements I{Prefix}Service {

    /**
     * 基础查询
     *
     * @param queryBO 查询条件
     * @return {tableComment}列表
     */
    @Override
    public List<{DomainClass}> baseQueryMethod({Prefix}{BoSuffix} queryBO) {
        LambdaQueryWrapper<{DomainClass}> queryWrapper = new LambdaQueryWrapper<{DomainClass}>()
                // 固定条件 (如果项目有)
                // .eq({DomainClass}::getStatus, StatusEnum.IN_USE)
                // .eq({DomainClass}::getHospitalId, Common.getHospitalId())
                // --- 查询条件 ---
                .eq(StrUtil.isNotBlank(queryBO.get{FieldName}()), {DomainClass}::get{FieldName}, queryBO.get{FieldName}())
                // ... one condition per field
                ;
        return this.list(queryWrapper);
    }
}
```

If project does NOT use Service interface (direct class):
```java
package {basePackage}.service.{module};

import cn.hutool.core.collection.CollUtil;
import cn.hutool.core.util.StrUtil;
import com.baomidou.mybatisplus.core.conditions.query.LambdaQueryWrapper;
import com.baomidou.mybatisplus.extension.service.impl.ServiceImpl;
import {domainPackage}.{DomainClass};
import {boPackage}.{Prefix}{BoSuffix};
import {basePackage}.mapper.{module}.{Prefix}Mapper;
import org.springframework.stereotype.Service;

import java.util.List;

/**
 * {tableComment}Service业务层处理
 *
 * @author {author}
 * @date {date}
 */
@Service("{beanName}")  // 有些项目需要指定 bean 名称
public class {Prefix}ServiceImpl extends ServiceImpl<{Prefix}Mapper, {DomainClass}> {

    /**
     * 基础查询
     *
     * @param queryBO 查询条件
     * @return {tableComment}列表
     */
    public List<{DomainClass}> baseQueryMethod({Prefix}{BoSuffix} queryBO) {
        LambdaQueryWrapper<{DomainClass}> queryWrapper = new LambdaQueryWrapper<{DomainClass}>()
                // 固定条件 (如果项目有)
                // .eq({DomainClass}::getStatus, StatusEnum.IN_USE)
                // .eq({DomainClass}::getHospitalId, Common.getHospitalId())
                // --- 查询条件 ---
                .eq(StrUtil.isNotBlank(queryBO.get{FieldName}()), {DomainClass}::get{FieldName}, queryBO.get{FieldName}())
                // ... one condition per field
                // 排序 (如果项目需要)
                // .orderByAsc({DomainClass}::getShowOrder)
                ;
        return this.list(queryWrapper);
    }
}
```

### ServiceImpl Annotations & Injection Detection

Detect from existing project code and apply:

- **Bean naming**: If project uses `@Service("beanName")`, generate with bean name. Otherwise use plain `@Service`.
- **Import style**: If project uses `@RequiredArgsConstructor` + `final` fields, add that. Otherwise use `@Resource` field injection.
- **Slf4j**: If project Services use `@Slf4j`, add it. Otherwise skip.
- **Fixed conditions**: Always include as commented template, ask user to confirm/enable.

### 6. Controller

**Path**: `controller/{module}/{Prefix}Controller.java`

**Rules**:
- 根据项目风格决定是否继承 BaseController
- 只暴露一个查询接口
- 根据项目风格决定是否加 `@Slf4j` + `log.info()`
- 根据项目风格决定 RequestMapping 命名风格（驼峰 / kebab-case / 多级路径）
- 根据项目风格选择注入方式（`@Resource` / `@RequiredArgsConstructor`）
- 使用项目的 AjaxResult 路径（如 `com.ruoyi.common.core.domain.AjaxResult`）

```java
package {basePackage}.controller.{module};

import {boPackage}.{Prefix}{BoSuffix};
import {servicePackage}.{Prefix}ServiceImpl;
import {baseControllerPath};
import {ajaxResultPath};
import lombok.extern.slf4j.Slf4j;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import javax.annotation.Resource;

/**
 * {tableComment}Controller
 *
 * @author {author}
 * @date {date}
 */
@Slf4j  // 如果项目Controller使用日志
@RestController
@RequestMapping("/{mappingPath}")
public class {Prefix}Controller extends BaseController {

    @Resource
    private {Prefix}ServiceImpl {module}Service;

    /**
     * 查询{tableComment}列表
     */
    @GetMapping("/list")
    public AjaxResult list({Prefix}{BoSuffix} queryBO) {
        log.info("查询{tableComment}列表: {}", queryBO);
        return AjaxResult.success({module}Service.baseQueryMethod(queryBO));
    }
}
```

## Conditional Chaining Rules for baseQueryMethod

The `baseQueryMethod` MUST use `LambdaQueryWrapper` with conditional chaining. Follow these rules:

### String fields — exact match

```java
.eq(StrUtil.isNotBlank(queryBO.get{Field}()), {Entity}::get{Field}, queryBO.get{Field}())
```

### String fields — exact match (isNotEmpty variant)

```java
.eq(StrUtil.isNotEmpty(queryBO.get{Field}()), {Entity}::get{Field}, queryBO.get{Field}())
```

### String fields — fuzzy match (like)

```java
.like(StrUtil.isNotBlank(queryBO.get{Field}()), {Entity}::get{Field}, queryBO.get{Field}())
```

### Non-String / typed fields (Long, Integer, BigDecimal, etc.)

```java
.eq(queryBO.get{Field}() != null, {Entity}::get{Field}, queryBO.get{Field}())
```

### Collection fields (List, Set)

```java
.in(CollUtil.isNotEmpty(queryBO.get{Field}()), {Entity}::get{Field}, queryBO.get{Field}())
```

Requires import: `cn.hutool.core.collection.CollUtil`

### Range conditions (date/number ranges)

```java
// Less than or equal
.le(queryBO.getStartTime() != null, {Entity}::getStartTime, queryBO.getEndTime())
// Greater than or equal
.ge(queryBO.getStartTime() != null, {Entity}::getEndTime, queryBO.getStartTime())
// Between
.between(queryBO.getStartDate() != null, {Entity}::getDate, queryBO.getStartDate(), queryBO.getEndDate())
```

### Fixed conditions (always applied, no conditional)

```java
.eq({Entity}::getHospitalId, Common.getHospitalId())
.eq({Entity}::getStatus, StatusEnum.IN_USE)
.eq({Entity}::getStatus, StatusEnum.IN_USE.getCode())
```

NOTE: Some projects use the enum directly (`StatusEnum.IN_USE`), others use `.getCode()`. Detect from existing code.

### Ordering (append at the end)

```java
.orderByAsc({Entity}::getShowOrder)
.orderByDesc({Entity}::getStartTime)
```

### Default Generation Strategy

When auto-generating without user guidance:

1. All `varchar` / `String` columns → `.eq(StrUtil.isNotBlank(...), ...)`
2. All numeric columns (Long, Integer) → `.eq(... != null, ...)`
3. No `.like()` conditions by default
4. No fixed conditions by default — user can request them
5. No range conditions by default
6. No ordering by default

Always ask after generation: "是否需要调整字段的查询方式（精确/模糊/范围）、添加固定条件或排序?"

## Fixed Conditions Template

If the project has common fixed query conditions, include them as a template comment in the generated ServiceImpl:

```java
// 固定条件（根据项目情况添加）
// .eq(Entity::getStatus, StatusEnum.IN_USE)
// .eq(Entity::getHospitalId, Common.getHospitalId())
// .eq(Entity::getDelStatus, DelStatusEnum.NORMAL.getCode())
```

## Field Name Mapping

### DDL → Java field naming

| DDL Column | Java Field |
|------------|------------|
| `day_id` | `dayId` |
| `city_id` | `cityId` |
| `level4_name` | `level4Name` |

Rules:
- Strip table prefix if present
- Convert snake_case to camelCase
- Keep column order from DDL in generated code

### Domain → QueryBO field mapping

Only include fields from Domain that are meaningful for querying. Skip:
- `id` / `createTime` / `updateTime` / `createBy` / `updateBy` / `remark` (unless user says otherwise)
- Large text / blob columns
- `dayId` IS included (it's a business key, not an audit field)

## Generation Workflow

1. **Parse Input** — Extract DDL columns or parse Domain class
2. **Detect Project Style** — Examine existing code to determine conventions
3. **Auto-Detect** — Package, module, class prefix
4. **Present Plan** — Show user:
   - Detected project style (BO naming, Service interface, fixed conditions, etc.)
   - Detected package, module, prefix
   - List of files to generate
   - Field mapping (DDL column → Java field)
   - Default query strategy per field
5. **Get Confirmation** — User approves or adjusts
6. **Generate All Files** — Write every file listed in "Generated Files" section
7. **Ask for Adjustments** — "是否需要调整查询方式、添加固定条件或补充其他方法?"

## Example

### Input (DDL)

```sql
create table ads_cockpit_dim_org (
    day_id      varchar(50)  null comment '账期',
    city_id     varchar(50)  null comment '地市id',
    city        varchar(100) null comment '地市',
    psncode     varchar(200) null comment '人员编码',
    psnname     varchar(200) null comment '人员姓名'
) comment '驾驶舱组织人员维度表';
```

### Input (Domain)

```java
package com.ruoyi.cockpit.domain.dimOrg;

@TableName("ads_cockpit_dim_org")
public class CockpitDimOrg implements Serializable {
    private String dayId;
    private String cityId;
    private String city;
    private String psncode;
    private String psnname;
}
```

### Detected Style (cockpit project)

- BO 命名: `QueryBO`
- BO 包路径: `domain.{module}.bo`
- Service 接口: 有
- 固定条件: 无

### Generated QueryBO fields

- `dayId` (账期)
- `cityId` (地市id)
- `city` (地市)
- `psncode` (人员编码)
- `psnname` (人员姓名)

### Generated baseQueryMethod

```java
@Override
public List<CockpitDimOrg> baseQueryMethod(CockpitDimOrgQueryBO queryBO) {
    LambdaQueryWrapper<CockpitDimOrg> queryWrapper = new LambdaQueryWrapper<CockpitDimOrg>()
            .eq(StrUtil.isNotBlank(queryBO.getDayId()), CockpitDimOrg::getDayId, queryBO.getDayId())
            .eq(StrUtil.isNotBlank(queryBO.getCityId()), CockpitDimOrg::getCityId, queryBO.getCityId())
            .eq(StrUtil.isNotBlank(queryBO.getCity()), CockpitDimOrg::getCity, queryBO.getCity())
            .eq(StrUtil.isNotBlank(queryBO.getPsncode()), CockpitDimOrg::getPsncode, queryBO.getPsncode())
            .eq(StrUtil.isNotBlank(queryBO.getPsnname()), CockpitDimOrg::getPsnname, queryBO.getPsnname());
    return this.list(queryWrapper);
}
```

## Important Constraints

1. **NEVER skip the QueryBO** — it MUST be generated in the detected BO package
2. **NEVER skip baseQueryMethod** — it MUST be in both interface and impl (or just impl if no interface)
3. **Controller ONLY has list endpoint** — no CRUD unless user explicitly asks
4. **ServiceImpl MUST extend ServiceImpl<Mapper, Entity>**
5. **Controller MUST extend the detected BaseController**
6. **String comparisons use StrUtil.isNotBlank** — not `!= null` or `.isEmpty()`
7. **Ask user to confirm before generating** — never auto-generate blindly
8. **When DDL-only mode, show the generated Domain first** — get user approval before proceeding
9. **Always detect project style first** — do NOT assume a project's conventions
10. **Follow existing project patterns exactly** — match BO naming, package paths, author tags, etc.
