---
name: java-crud-stack-gen
description: "Generate complete Java CRUD stack (Entity + Mapper + DTO + VO + Converter + Service + Domain + Controller) from DDL or Entity, following Ruoyi + MyBatis-Plus conventions with Domain aggregation layer. Triggered when user wants full backend scaffold from database definition."
---

# Java CRUD Stack Generator

Generate complete Java backend CRUD stack from DDL or Entity class. Ruoyi + MyBatis-Plus style with Domain aggregation layer.

## Trigger

Invoke this skill when the user:
- Provides a DDL statement and asks to generate full backend / CRUD stack
- Provides an Entity class and asks for complete service layer
- Says "生成完整后端" / "生成 CRUD 全套" / "从 DDL 生成 Java 代码"

## Generated Files

**Total: 7 files**

| # | File | Path Pattern |
|---|------|-------------|
| 1 | Entity (PO) | `{module}/po/{Prefix}.java` |
| 2 | Mapper | `{module}/mapper/{Prefix}Mapper.java` |
| 3 | DTO | `{module}/dto/{Prefix}SaveDTO.java` |
| 4 | VO | `{module}/vo/{Prefix}VO.java` |
| 5 | Converter | `{module}/convert/{Prefix}Convert.java` |
| 6 | Service | `{module}/service/{Prefix}Service.java` |
| 7 | Domain | `{module}/service/domain/Sys{Prefix}Domain.java` |

**Controller** — generated but delegates to Domain:
| 8 | Controller | `{module}/controller/{Prefix}Controller.java` |

## Project Style Detection

### Detection Checklist

1. **Check existing Entity** — naming: `Se{Xxx}` or `{Xxx}Entity`?
2. **Check ID type** — `Long` (ASSIGN_ID) or `String` (ASSIGN_UUID)?
3. **Check Base class** — extends `BaseEntity` or standalone?
4. **Check Mapper** — extends `EasyBaseMapper` or `BaseMapper`?
5. **Check Controller** — extends `BaseController`?
6. **Check Service annotation** — `@Service("beanName")` or plain `@Service`?
7. **Check injection** — `@Resource` or `@RequiredArgsConstructor` + `final`?
8. **Check query wrapper** — `QueryWrapper` (string col names) or `LambdaQueryWrapper` (lambda)?
9. **Check Converter** — `@Mapper` factory or `componentModel = "spring"`?
10. **Check fixed conditions** — `hospitalId` / `tenantId` / `status` filter?
11. **Check common library package path** — used as `{commonPackage}` in common-module imports (`AjaxResult` / `TableDataInfo` / `BaseController` / `StatusEnum` / `Common`)

### If Project Cannot Be Detected

Use default Ruoyi style:
- Entity: `@TableName` + `Long` ID (`ASSIGN_ID`) + standalone (no base class)
- Mapper: extends `EasyBaseMapper<Entity>`
- Service: `@Service("beanName")` + extends `ServiceImpl<Mapper, Entity>`
- Controller: extends `BaseController`, `@Resource` injection
- Query: `QueryWrapper` with UPPER_SNAKE column names
- Converter: `@Mapper` factory style (Mappers.getMapper)
- Fixed: `Common.getHospitalId()` + `StatusEnum.IN_USE`

Always present detected style to user for confirmation.

## Two Input Modes

### Mode A: DDL provided

Parse DDL to extract columns, types, comments. Generate Entity draft → confirm → generate all.

### Mode B: Entity provided

Use Entity as-is. Generate DTO/VO/Converter/Service/Domain/Controller around it.

## File Generation Rules

### 1. Entity (PO)

**Path**: `{module}/po/{Prefix}.java`

```java
package {basePackage}.{module}.po;

import com.baomidou.mybatisplus.annotation.*;
import {commonPackage}.datasource.enums.StatusEnum;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;
import lombok.extern.slf4j.Slf4j;

import java.io.Serializable;
import java.time.LocalDateTime;

/**
 * {tableComment}
 *
 * @author {author}
 */
@Slf4j
@Data
@TableName("{TABLE_NAME}")
@Builder
@AllArgsConstructor
@NoArgsConstructor
public class {Prefix} implements Serializable {

    private static final long serialVersionUID = 1L;

    @TableId(type = IdType.ASSIGN_ID)
    /** {pkComment} */
    private Long {pkName};

    // Business fields from DDL/Entity...

    /** 状态 */
    @TableField(fill = FieldFill.INSERT)
    private StatusEnum status;

    /** 创建人 */
    @TableField(fill = FieldFill.INSERT)
    private String createBy;

    /** 创建时间 */
    @TableField(fill = FieldFill.INSERT)
    private LocalDateTime createTime;

    /** 更新人 */
    @TableField(fill = FieldFill.INSERT_UPDATE)
    private String updateBy;

    /** 更新时间 */
    @TableField(fill = FieldFill.INSERT_UPDATE)
    private LocalDateTime updateTime;
}
```

### 2. Mapper

**Path**: `{module}/mapper/{Prefix}Mapper.java`

```java
package {basePackage}.{module}.mapper;

import {commonPackage}.datasource.config.mp.EasyBaseMapper;
import {basePackage}.{module}.po.{Prefix};
import {basePackage}.{module}.vo.{Prefix}VO;
import org.apache.ibatis.annotations.Param;

import java.util.List;

/**
 * {tableComment} Mapper
 *
 * @author {author}
 */
public interface {Prefix}Mapper extends EasyBaseMapper<{Prefix}> {

    /**
     * 查询 {prefix} 列表
     */
    List<{Prefix}VO> get{Prefix}List(@Param("{prefix}") {Prefix} {prefix},
                                      @Param("hospitalId") String hospitalId);
}
```

### 3. DTO

**Path**: `{module}/dto/{Prefix}SaveDTO.java`

```java
package {basePackage}.{module}.dto;

import lombok.Data;
import javax.validation.constraints.NotBlank;
import javax.validation.constraints.NotNull;
import java.io.Serializable;

/**
 * {tableComment} 前端数据传输对象
 *
 * @author {author}
 */
@Data
public class {Prefix}SaveDTO implements Serializable {
    private Long {pkName};
    @NotBlank(message = "{fieldName}不能为空")
    private String {fieldName};
    // Business fields with validation...
    private Integer showOrder;
    private Integer duration;
    private String useStatus;
    private Integer totalScoreRatio;
    // NO audit fields (createTime, updateTime, createBy, updateBy)
}
```

### 4. VO

**Path**: `{module}/vo/{Prefix}VO.java`

```java
package {basePackage}.{module}.vo;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

/**
 * {tableComment} 后端数据传输对象
 *
 * @author {author}
 */
@Data
@AllArgsConstructor
@NoArgsConstructor
@Builder
public class {Prefix}VO {
    private Long {pkName};
    private String {fieldName};
    // Business fields...
    // Display fields (code → name pairs)
    private String {field}Name;
    // Count/aggregate fields
    private Integer annexCount;
}
```

### 5. Converter

**Path**: `{module}/convert/{Prefix}Convert.java`

```java
package {basePackage}.{module}.convert;

import {basePackage}.{module}.dto.{Prefix}SaveDTO;
import {basePackage}.{module}.po.{Prefix};
import {basePackage}.{module}.vo.{Prefix}VO;
import org.mapstruct.Mapper;
import org.mapstruct.factory.Mappers;

import java.util.List;

/**
 * {tableComment} 映射转换类
 *
 * @author {author}
 */
@Mapper
public interface {Prefix}Convert {

    {Prefix}Convert INSTANCE = Mappers.getMapper({Prefix}Convert.class);

    /**
     * poList转voList
     */
    List<{Prefix}VO> poToVoList(List<{Prefix}> list);

    /**
     * dto转po
     */
    {Prefix} dtoToPo({Prefix}SaveDTO dto);

    /**
     * 批量dto转po
     */
    List<{Prefix}> dtoListToPoList(List<{Prefix}SaveDTO> dtoList);
}
```

### 6. Service

**Path**: `{module}/service/{Prefix}Service.java`

**Core query method pattern** (conditionally chained QueryWrapper):

```java
package {basePackage}.{module}.service;

import cn.hutool.core.collection.CollUtil;
import cn.hutool.core.util.StrUtil;
import com.baomidou.mybatisplus.core.conditions.query.QueryWrapper;
import com.baomidou.mybatisplus.core.conditions.update.UpdateWrapper;
import com.baomidou.mybatisplus.extension.service.impl.ServiceImpl;
import {commonPackage}.core.exception.ServiceException;
import {commonPackage}.datasource.enums.StatusEnum;
import {commonPackage}.satoken.common.Common;
import {basePackage}.{module}.mapper.{Prefix}Mapper;
import {basePackage}.{module}.po.{Prefix};
import org.springframework.stereotype.Service;

import java.util.ArrayList;
import java.util.List;

/**
 * {tableComment} Service 层
 *
 * @author {author}
 */
@Service("{beanName}")
public class {Prefix}Service extends ServiceImpl<{Prefix}Mapper, {Prefix}> {

    /**
     * 获取列表
     */
    public List<{Prefix}> get{Prefix}List({Prefix} {prefix}) {
        QueryWrapper<{Prefix}> queryWrapper = new QueryWrapper<>();
        queryWrapper.eq("STATUS", "0");
        queryWrapper.eq("HOSPITAL_ID", Common.getHospitalId());
        // Conditional query chain
        if ({prefix}.get{Field}() != null) {
            queryWrapper.eq("{FIELD_NAME}", {prefix}.get{Field}());
        }
        if (StrUtil.isNotEmpty({prefix}.get{FieldName}())) {
            queryWrapper.like("{FIELD_NAME}", {prefix}.get{FieldName}());
        }
        // ... other fields
        return this.baseMapper.selectList(queryWrapper);
    }

    /**
     * 新增
     */
    public int insert({Prefix} {prefix}) {
        {prefix}.setStatus(StatusEnum.IN_USE);
        return this.baseMapper.insert({prefix});
    }

    /**
     * 更新
     */
    public int update({Prefix} {prefix}) {
        if (this.getByCode({prefix}.get{pkName}()) == null) {
            throw new ServiceException("{prefix}不存在！");
        }
        UpdateWrapper<{Prefix}> updateWrapper = new UpdateWrapper<>();
        updateWrapper.eq("{PK_NAME}", {prefix}.get{pkName}());
        return this.baseMapper.update({prefix}, updateWrapper);
    }

    /**
     * 逻辑删除
     */
    public int updateToDelete(Long {pkName}) {
        if (this.getByCode({pkName}) == null) {
            throw new ServiceException("{prefix}不存在！");
        }
        UpdateWrapper<{Prefix}> updateWrapper = new UpdateWrapper<>();
        updateWrapper.eq("{PK_NAME}", {pkName});
        {Prefix} entity = new {Prefix}();
        entity.setStatus(StatusEnum.DELETED);
        return this.baseMapper.update(entity, updateWrapper);
    }

    /**
     * 按编码查询
     */
    public {Prefix} getByCode(Long {pkName}) {
        QueryWrapper<{Prefix}> queryWrapper = new QueryWrapper<>();
        queryWrapper.eq("{PK_NAME}", {pkName})
                   .eq("HOSPITAL_ID", Common.getHospitalId());
        return this.baseMapper.selectOne(queryWrapper);
    }

    /**
     * 批量查询
     */
    public List<{Prefix}> getListByCodes(List<Long> codes) {
        if (CollUtil.isNotEmpty(codes)) {
            QueryWrapper<{Prefix}> queryWrapper = new QueryWrapper<>();
            queryWrapper.in("{PK_NAME}", codes)
                       .eq("STATUS", "0")
                       .eq("HOSPITAL_ID", Common.getHospitalId())
                       .orderByAsc("SHOW_ORDER");
            return this.baseMapper.selectList(queryWrapper);
        }
        return new ArrayList<>();
    }
}
```

### 7. Domain (聚合根)

**Path**: `{module}/service/domain/Sys{Prefix}Domain.java`

```java
package {basePackage}.{module}.service.domain;

import cn.hutool.core.collection.CollUtil;
import {basePackage}.{module}.convert.{Prefix}Convert;
import {basePackage}.{module}.dto.{Prefix}SaveDTO;
import {basePackage}.{module}.po.{Prefix};
import {basePackage}.{module}.service.{Prefix}Service;
import {basePackage}.{module}.vo.{Prefix}VO;
import org.springframework.stereotype.Component;
import org.springframework.transaction.annotation.Transactional;

import javax.annotation.Resource;
import java.util.HashMap;
import java.util.List;

/**
 * {tableComment} 聚合根 - 业务编排层
 *
 * @author {author}
 */
@Component
public class Sys{Prefix}Domain {

    @Resource
    private {Prefix}Service {prefix}Service;

    /**
     * 分页查询
     */
    public HashMap<String, Object> get{Prefix}List({Prefix} query) {
        List<{Prefix}> list = {prefix}Service.get{Prefix}List(query);
        List<{Prefix}VO> voList = {Prefix}Convert.INSTANCE.poToVoList(list);
        HashMap<String, Object> result = new HashMap<>();
        result.put("count", list.size());
        result.put("vos", voList);
        return result;
    }

    /**
     * 新增
     */
    @Transactional(rollbackFor = Exception.class)
    public int insert({Prefix}SaveDTO dto) {
        {Prefix} entity = {Prefix}Convert.INSTANCE.dtoToPo(dto);
        return {prefix}Service.insert(entity);
    }

    /**
     * 更新
     */
    @Transactional(rollbackFor = Exception.class)
    public int update({Prefix}SaveDTO dto) {
        {Prefix} entity = {Prefix}Convert.INSTANCE.dtoToPo(dto);
        return {prefix}Service.update(entity);
    }

    /**
     * 启用
     */
    @Transactional(rollbackFor = Exception.class)
    public int startByCode(Long code) {
        {Prefix} entity = {prefix}Service.getByCode(code);
        if (entity == null) return 0;
        entity.setStatus(StatusEnum.IN_USE);
        return {prefix}Service.update(entity);
    }

    /**
     * 停用
     */
    @Transactional(rollbackFor = Exception.class)
    public int stopByCode(Long code) {
        return {prefix}Service.updateToDelete(code);
    }

    /**
     * 删除
     */
    @Transactional(rollbackFor = Exception.class)
    public int deleteByCode(Long code) {
        return {prefix}Service.updateToDelete(code);
    }
}
```

### 8. Controller

**Path**: `{module}/controller/{Prefix}Controller.java`

```java
package {basePackage}.{module}.controller;

import {commonPackage}.core.domain.AjaxResult;
import {commonPackage}.core.domain.TableDataInfo;
import {commonPackage}.datasource.base.BaseController;
import {basePackage}.{module}.dto.{Prefix}SaveDTO;
import {basePackage}.{module}.dto.{Prefix}SelectDTO;
import {basePackage}.{module}.po.{Prefix};
import {basePackage}.{module}.service.{Prefix}Service;
import {basePackage}.{module}.service.domain.Sys{Prefix}Domain;
import lombok.extern.slf4j.Slf4j;
import org.springframework.validation.annotation.Validated;
import org.springframework.web.bind.annotation.*;

import javax.annotation.Resource;
import java.util.HashMap;
import java.util.List;

/**
 * {tableComment} 管理
 *
 * @author {author}
 */
@Slf4j
@RestController
@RequestMapping("{mappingPath}")
public class {Prefix}Controller extends BaseController {

    @Resource
    private {Prefix}Service {prefix}Service;

    @Resource
    private Sys{Prefix}Domain sys{Prefix}Domain;

    /**
     * 分页查询
     */
    @GetMapping("/get{Prefix}PageList")
    public AjaxResult get{Prefix}PageList({Prefix}SelectDTO dto) {
        log.info("{module}/get{Prefix}PageList :: {}", dto);
        startPage();
        HashMap<String, Object> data = sys{Prefix}Domain.get{Prefix}List(dto);
        TableDataInfo dataTable = getDataTable((List<?>) data.get("count"));
        dataTable.setRows((List<?>) data.get("vos"));
        return AjaxResult.success(dataTable);
    }

    /**
     * 全量查询
     */
    @GetMapping("/get{Prefix}List")
    public AjaxResult get{Prefix}List({Prefix}SelectDTO dto) {
        log.info("{module}/get{Prefix}List :: {}", dto);
        HashMap<String, Object> data = sys{Prefix}Domain.get{Prefix}List(dto);
        return AjaxResult.success(data.get("vos"));
    }

    /**
     * 新增
     */
    @PostMapping("/add{Prefix}")
    public AjaxResult add{Prefix}(@RequestBody @Validated {Prefix}SaveDTO dto) {
        log.info("{module}/add{Prefix} :: {}", dto);
        int i = sys{Prefix}Domain.insert(dto);
        return i > 0 ? AjaxResult.success("添加成功") : AjaxResult.error("添加失败");
    }

    /**
     * 更新
     */
    @PutMapping("/{Prefix}Update")
    public AjaxResult {prefix}Update(@RequestBody {Prefix}SaveDTO dto) {
        log.info("{module}/{prefix}Update :: {}", dto);
        int i = sys{Prefix}Domain.update(dto);
        return i > 0 ? AjaxResult.success("更新成功") : AjaxResult.error("更新失败");
    }

    /**
     * 启用
     */
    @PutMapping("/startByCode")
    public AjaxResult startByCode(Long code) {
        log.info("{module}/startByCode :: {}", code);
        int i = sys{Prefix}Domain.startByCode(code);
        return i > 0 ? AjaxResult.success("启用成功") : AjaxResult.error("启用失败");
    }

    /**
     * 停用
     */
    @PutMapping("/stopByCode")
    public AjaxResult stopByCode(Long code) {
        log.info("{module}/stopByCode :: {}", code);
        int i = sys{Prefix}Domain.stopByCode(code);
        return i > 0 ? AjaxResult.success("停用成功") : AjaxResult.error("停用失败");
    }

    /**
     * 删除
     */
    @DeleteMapping("/deleteByCode")
    public AjaxResult deleteByCode(Long code) {
        log.info("{module}/deleteByCode :: {}", code);
        int i = sys{Prefix}Domain.deleteByCode(code);
        return i > 0 ? AjaxResult.success("删除成功") : AjaxResult.error("删除失败");
    }
}
```

## Query Select DTO (额外生成)

**Path**: `{module}/dto/{Prefix}SelectDTO.java`

**用于分页查询条件**，所有字段为查询用：

```java
package {basePackage}.{module}.dto;

import lombok.Data;
import java.io.Serializable;

/**
 * {tableComment} 查询条件
 */
@Data
public class {Prefix}SelectDTO implements Serializable {
    private Long {pkName};
    private String {fieldName};
    // 用于 like 查询的字段
    private String {searchField};
    // 用于精确匹配的字段
    private Long {exactField};
}
```

## Naming Conventions

| Element | Rule | Example |
|---------|------|---------|
| Entity class | `{Prefix}` | `SeStation` |
| Entity file | `{Prefix}.java` | `SeStation.java` |
| Mapper | `{Prefix}Mapper` | `StationMapper` |
| DTO | `{Prefix}SaveDTO` | `StationSaveDTO` |
| Select DTO | `{Prefix}SelectDTO` | `StationSelectDTO` |
| VO | `{Prefix}VO` | `StationVO` |
| Converter | `{Prefix}Convert` | `StationConvert` |
| Service | `{Prefix}Service` (bean: `{lowerPrefix}Service`) | `StationService` ("seStationService") |
| Domain | `Sys{Prefix}Domain` | `SysStationDomain` |
| Controller | `{Prefix}Controller` | `StationController` |
| Table | `UPPER_SNAKE_CASE` | `SE_STATION` |
| Column | `UPPER_SNAKE_CASE` | `STATION_CODE` |
| ID field | `Long {pkName}` | `Long stationCode` |

## Common Patterns Generated

### Fixed conditions (always included)
- `queryWrapper.eq("STATUS", "0")` — status filter
- `queryWrapper.eq("HOSPITAL_ID", Common.getHospitalId())` — multi-tenant
- `@TableField(fill = FieldFill.INSERT)` for `createBy`, `createTime`
- `@TableField(fill = FieldFill.INSERT_UPDATE)` for `updateBy`, `updateTime`
- `StatusEnum.IN_USE` / `StatusEnum.DELETED` for status transitions

### Query wrapper conditional chain
- `Long` / `Integer` fields → `.eq(field != null, "COL", field)`
- `String` fields → `.like(StrUtil.isNotEmpty(field), "COL", field)`
- `List` fields → `.in(CollUtil.isNotEmpty(list), "COL", list)`
- Always ends with `.orderByAsc("SHOW_ORDER")` if showOrder exists

### CRUD methods always generated
1. `getList({entity})` — conditional query with fixed filters
2. `insert({entity})` — set status + insert
3. `update({entity})` — check existence + update
4. `updateToDelete(id)` — logical delete (set DELETED status)
5. `getByCode(id)` — single by PK + tenant filter
6. `getListByCodes(List<Long>)` — batch query with order

### Controller endpoints always generated
1. `GET /get{Prefix}PageList` — paginated list (startPage + getDataTable)
2. `GET /get{Prefix}List` — full list
3. `POST /add{Prefix}` — create
4. `PUT /{Prefix}Update` — update
5. `PUT /startByCode` — enable
6. `PUT /stopByCode` — disable (logical delete)
7. `DELETE /deleteByCode` — remove

## Generation Workflow

1. **Parse Input** — extract DDL columns or parse Entity class
2. **Detect Project Style** — check existing codebase conventions
3. **Auto-Detect** — package, module, prefix, bean name
4. **Present Plan** — show:
   - Detected project style
   - Package structure
   - List of 8 files to generate
   - Field mapping (DDL column → Java field)
   - Query strategy per field
5. **Get Confirmation** — user approves or adjusts
6. **Generate All Files** — write every file
7. **Ask for Adjustments** — "是否需要调整查询条件、添加额外方法或修改字段映射?"

## Important Constraints

1. **NEVER skip the Domain layer** — it MUST be generated as aggregation root
2. **NEVER skip SelectDTO** — separate query DTO is required for list/search
3. **ALWAYS extend BaseController** — controller must extend detected base class
4. **ALWAYS include `hospitalId` filter** — multi-tenant is mandatory
5. **ALWAYS include `STATUS = 0` filter** — soft-delete filtering is mandatory
6. **NEVER skip `@Transactional`** — Domain write methods must have `rollbackFor = Exception.class`
7. **NEVER skip the Converter** — MapStruct is the standard mapping mechanism
8. **Service bean name must match** — `@Service("{beanName}")` with convention
9. **Ask user to confirm before generating** — never auto-generate blindly
10. **When DDL-only mode, show Entity draft first** — get user approval on Entity before proceeding