---
name: java-crud-stack-gen
description: "Generate complete Java CRUD stack (Entity + Mapper + DTO + QueryBO + VO + Converter + Service + Domain + Controller) from DDL or Entity, following Ruoyi + MyBatis-Plus conventions with Domain aggregation layer. Query methods unify the baseQueryMethod convention from ddl-to-service (QueryBO + LambdaQueryWrapper conditional chaining). Triggered when user wants full backend scaffold from database definition."
---

# Java CRUD Stack Generator

Generate complete Java backend CRUD stack from DDL or Entity class. Ruoyi + MyBatis-Plus style with Domain aggregation layer.

## Trigger

Invoke this skill when the user:
- Provides a DDL statement and asks to generate full backend / CRUD stack
- Provides an Entity class and asks for complete service layer
- Says "生成完整后端" / "生成 CRUD 全套" / "从 DDL 生成 Java 代码"

## Generated Files

**Total: 8 files**

| # | File | Path Pattern |
|---|------|-------------|
| 1 | Entity (PO) | `{module}/po/{Prefix}.java` |
| 2 | Mapper | `{module}/mapper/{Prefix}Mapper.java` |
| 3 | DTO | `{module}/dto/{Prefix}{DtoSuffix}.java`（`SaveDTO` 或 `DTO`，按项目习惯） |
| 4 | QueryBO | `{boPackage}/{Prefix}QueryBO.java` (默认 `{module}/bo/`，动态匹配) |
| 5 | VO | `{module}/vo/{Prefix}VO.java` |
| 6 | Converter | `{module}/convert/{Prefix}Convert.java` 或 `{module}/converter/{Prefix}Converter.java`（按 A/B 风格） |
| 7 | Service | `{module}/service/{Prefix}Service.java` |
| 8 | Domain | `{module}/service/domain/Sys{Prefix}Domain.java` |

**Controller** — generated but delegates to Domain:
| 9 | Controller | `{module}/controller/{Prefix}Controller.java` |

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
9. **Check Service interface** — 项目是否使用 `I{Prefix}Service` 接口 + `{Prefix}ServiceImpl` 实现类（若用，Service 按接口+实现生成）
10. **Check Converter** — `@Mapper` factory or `componentModel = "spring"`?
11. **Check fixed conditions** — `hospitalId` / `tenantId` / `status` filter?
12. **Check common library package path** — used as `{commonPackage}` in common-module imports (`AjaxResult` / `TableDataInfo` / `BaseController` / `StatusEnum` / `Common`)
13. **Check QueryBO package** — 现有 BO/QueryBO 所在包：`{basePackage}.{module}.bo`（`{module}/bo/`）还是 `domain.{module}.bo` / `pojo.bo` / `pojo.bo.{submodule}`？`{boPackage}` 跟随检测到的项目实际位置
14. **Check DTO naming** — 项目现有 DTO 命名是 `XxxSaveDTO` 还是 `XxxDTO`？`{DtoSuffix}` 跟随检测结果（默认 `SaveDTO`）
15. **Check author / date** — 项目 javadoc 使用的 `@author` 名字与 `@date` 日期格式（如 `yyyy-MM-dd`），`{author}` / `{date}` 跟随检测

### If Project Cannot Be Detected

Use default Ruoyi style:
- Entity: `@TableName` + `Long` ID (`ASSIGN_ID`) + standalone (no base class)
- Mapper: extends `EasyBaseMapper<Entity>`
- Service: `@Service("beanName")` + extends `ServiceImpl<Mapper, Entity>`
- Controller: extends `BaseController`, `@Resource` injection
- Query: `LambdaQueryWrapper` conditional chaining via `baseQueryMethod({Prefix}QueryBO)` (baseQueryMethod convention)
- QueryBO 包路径: `{boPackage}` = `{basePackage}.{module}.bo`（`{module}/bo/`）— 项目无法检测时的默认值；有检测依据时跟随项目实际位置
- Converter: `@Mapper` factory style (Mappers.getMapper)
- Fixed: optional comment templates (e.g. `Common.getHospitalId()` + `StatusEnum.IN_USE`), enabled only per user confirmation
- Javadoc: `@author {author}` + `@date {date}`（默认 `{author}=ruoyi`，`{date}` 格式 `yyyy-MM-dd`）

Always present detected style to user for confirmation.

## Two Input Modes

### Mode A: DDL provided

Parse DDL to extract columns, types, comments. Generate Entity draft → confirm → generate all.

### Mode B: Entity provided

Use Entity as-is. Generate DTO/QueryBO/VO/Converter/Service/Domain/Controller around it.

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
 * @date {date}
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

/**
 * {tableComment} Mapper
 *
 * @author {author}
 * @date {date}
 */
public interface {Prefix}Mapper extends EasyBaseMapper<{Prefix}> {
}
```

### 3. DTO

**Path**: `{module}/dto/{Prefix}{DtoSuffix}.java`

**DTO 命名（按项目习惯）**: `{DtoSuffix}` 为 `SaveDTO`（默认）或 `DTO`，与 mapstruct-converter-gen 的 DTO 命名约定一致。检测项目现有 DTO 命名（`XxxSaveDTO` / `XxxDTO`），跟随检测结果并向用户确认。

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
 * @date {date}
 */
@Data
public class {Prefix}{DtoSuffix} implements Serializable {
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

### 4. QueryBO

**Path**: `{boPackage}/{Prefix}QueryBO.java` — 默认 `{basePackage}.{module}.bo`（即 `{module}/bo/`），但**非固定**：需结合项目现有 BO 结构与查询场景动态匹配包路径，检测后向用户确认。

**查询对象统一遵循 ddl-to-service 的 `baseQueryMethod` 约定**（见 `ddl-to-service` 技能）：独立 QueryBO 承载查询条件，替代直接传 PO 查询。

**Rules:**
- **QueryBO 包路径动态匹配**（非强制，结合项目与问题）：默认 `{basePackage}.{module}.bo`（`{module}/bo/`）；先检查项目现有 BO/QueryBO 所在包（`domain.{module}.bo` / `pojo.bo` / `pojo.bo.{submodule}` 等），匹配已存在的位置，并将检测结果向用户确认后再生成
- Only include queryable fields — skip large text / blob columns
- Skip audit fields (`createTime`, `updateTime`, `createBy`, `updateBy`, `deleted`) unless user says otherwise; `{pkName}` IS included (business key for exact match)
- All fields are `String` type by default for varchar columns; numeric/date fields keep their types for range conditions
- Use `@Data` + `implements Serializable`
- Copy field comments from DDL / Entity

```java
package {boPackage};

import lombok.Data;

import java.io.Serializable;

/**
 * {tableComment}查询对象
 *
 * @author {author}
 * @date {date}
 */
@Data
public class {Prefix}QueryBO implements Serializable {

    private static final long serialVersionUID = 1L;

    /**
     * {columnComment}
     */
    private String {fieldName};

    // ... one field per queryable column
}
```

> 查询条件统一使用 `{Prefix}QueryBO`，不再生成独立的 SelectDTO。分页查询由 Controller 的 `startPage()`（MyBatis-Plus 分页拦截器）生效，`baseQueryMethod` 返回 `List<Entity>` 即可，无需单独的分页查询对象。

### 5. VO

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
 * @date {date}
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

### 6. Converter

**Path**: `{module}/convert/{Prefix}Convert.java`（Style A 工厂风格）或 `{module}/converter/{Prefix}Converter.java`（Style B Spring 风格）

**Converter 风格跟随检测到的项目 MapStruct 约定动态生成**（与 `mapstruct-converter-gen` 一致）：
- **Style A 工厂风格**：`@Mapper`（无 componentModel）+ `INSTANCE = Mappers.getMapper(...)` —— 默认
- **Style B Spring 风格**：`@Mapper(componentModel = "spring")`，无 INSTANCE，注入使用

#### Style A（工厂风格，默认）

```java
package {basePackage}.{module}.convert;

import {basePackage}.{module}.dto.{Prefix}{DtoSuffix};
import {basePackage}.{module}.po.{Prefix};
import {basePackage}.{module}.vo.{Prefix}VO;
import org.mapstruct.Mapper;
import org.mapstruct.factory.Mappers;

import java.util.List;

/**
 * {tableComment} 映射转换类
 *
 * @author {author}
 * @date {date}
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
    {Prefix} dtoToPo({Prefix}{DtoSuffix} dto);

    /**
     * 批量dto转po
     */
    List<{Prefix}> dtoListToPoList(List<{Prefix}{DtoSuffix}> dtoList);
}
```

#### Style B（Spring componentModel 风格）

```java
package {basePackage}.{module}.converter;

import {basePackage}.{module}.dto.{Prefix}{DtoSuffix};
import {basePackage}.{module}.po.{Prefix};
import {basePackage}.{module}.vo.{Prefix}VO;
import org.mapstruct.Mapper;

import java.util.List;

/**
 * {tableComment} 映射转换类
 *
 * @author {author}
 * @date {date}
 */
@Mapper(componentModel = "spring")
public interface {Prefix}Converter {

    /**
     * poList转voList
     */
    List<{Prefix}VO> poToVoList(List<{Prefix}> list);

    /**
     * dto转po
     */
    {Prefix} dtoToPo({Prefix}{DtoSuffix} dto);

    /**
     * 批量dto转po
     */
    List<{Prefix}> dtoListToPoList(List<{Prefix}{DtoSuffix}> dtoList);
}
```

> Domain 中使用 `{Prefix}Convert.INSTANCE.xxx()` 的调用仅在 Style A 下有效；Style B 下应在 Domain 中 `@Resource` 注入 `{Prefix}Converter` 后调用实例方法（两者方法名一致）。

### 7. Service

**Path**: `{module}/service/{Prefix}Service.java`（若项目使用接口风格则为 `I{Prefix}Service` + `{Prefix}ServiceImpl`）

**查询方法统一遵循 ddl-to-service 的 `baseQueryMethod` 约定**: 使用独立 `QueryBO` 承载查询条件 + `LambdaQueryWrapper` 条件链（conditional chaining）。固定条件（如 `STATUS` / `HOSPITAL_ID`）遵循 baseQueryMethod 约定以**注释模板**形式给出，由用户按需启用，**不强制**。

**Service 接口风格（按项目习惯决定）**: 若检测到项目使用 `I{Prefix}Service` 接口 + `{Prefix}ServiceImpl` 实现类，则按接口风格生成；否则生成直接类 `{Prefix}Service`（继承 `ServiceImpl`）。方法集不变。

#### 直接类风格（默认，无接口）

```java
package {basePackage}.{module}.service;

import cn.hutool.core.collection.CollUtil;
import cn.hutool.core.util.StrUtil;
import com.baomidou.mybatisplus.core.conditions.query.LambdaQueryWrapper;
import com.baomidou.mybatisplus.core.conditions.update.UpdateWrapper;
import com.baomidou.mybatisplus.extension.service.impl.ServiceImpl;
import {commonPackage}.core.exception.ServiceException;
import {commonPackage}.datasource.enums.StatusEnum;
import {commonPackage}.satoken.common.Common;
import {boPackage}.{Prefix}QueryBO;
import {basePackage}.{module}.mapper.{Prefix}Mapper;
import {basePackage}.{module}.po.{Prefix};
import org.springframework.stereotype.Service;

import java.util.ArrayList;
import java.util.List;

/**
 * {tableComment} Service 层
 *
 * @author {author}
 * @date {date}
 */
@Service("{beanName}")
public class {Prefix}Service extends ServiceImpl<{Prefix}Mapper, {Prefix}> {

    /**
     * 基础查询（baseQueryMethod 约定，源自 ddl-to-service）
     */
    public List<{Prefix}> baseQueryMethod({Prefix}QueryBO queryBO) {
        LambdaQueryWrapper<{Prefix}> queryWrapper = new LambdaQueryWrapper<{Prefix}>()
                // 固定条件（遵循 baseQueryMethod 约定，按需启用）
                // .eq({Prefix}::getStatus, StatusEnum.IN_USE)
                // .eq({Prefix}::getHospitalId, Common.getHospitalId())
                // --- 查询条件（conditional chaining）---
                .eq(StrUtil.isNotBlank(queryBO.get{FieldName}()), {Prefix}::get{FieldName}, queryBO.get{FieldName}())
                // ... one condition per queryable field
                // String 模糊查询: .like(StrUtil.isNotBlank(queryBO.get{Field}()), {Prefix}::get{Field}, queryBO.get{Field}())
                // 非 String 字段: .eq(queryBO.get{Field}() != null, {Prefix}::get{Field}, queryBO.get{Field}())
                // 集合字段: .in(CollUtil.isNotEmpty(queryBO.get{Field}()), {Prefix}::get{Field}, queryBO.get{Field}())
                // 范围: .le/.ge/.between(queryBO.get{Field}() != null, {Prefix}::get{Field}, ...)
                // 排序: .orderByAsc({Prefix}::getShowOrder)
                ;
        return this.list(queryWrapper);
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
        LambdaQueryWrapper<{Prefix}> queryWrapper = new LambdaQueryWrapper<{Prefix}>()
                .eq({Prefix}::get{pkName}, {pkName});
                // 固定条件（按需启用）
                // .eq({Prefix}::getHospitalId, Common.getHospitalId())
        return this.baseMapper.selectOne(queryWrapper);
    }

    /**
     * 批量查询
     */
    public List<{Prefix}> getListByCodes(List<Long> codes) {
        if (CollUtil.isNotEmpty(codes)) {
            LambdaQueryWrapper<{Prefix}> queryWrapper = new LambdaQueryWrapper<>();
            queryWrapper.in({Prefix}::get{pkName}, codes)
                    // 固定条件（按需启用）
                    // .eq({Prefix}::getStatus, StatusEnum.IN_USE)
                    // .eq({Prefix}::getHospitalId, Common.getHospitalId())
                    .orderByAsc({Prefix}::getShowOrder);
            return this.baseMapper.selectList(queryWrapper);
        }
        return new ArrayList<>();
    }
}
```

#### 接口风格（项目使用 `I{Prefix}Service` 接口时）

**接口 Path**: `{module}/service/I{Prefix}Service.java`

```java
package {basePackage}.{module}.service;

import com.baomidou.mybatisplus.extension.service.IService;
import {boPackage}.{Prefix}QueryBO;
import {basePackage}.{module}.po.{Prefix};

import java.util.List;

/**
 * {tableComment} Service 接口
 *
 * @author {author}
 * @date {date}
 */
public interface I{Prefix}Service extends IService<{Prefix}> {

    /**
     * 基础查询
     */
    List<{Prefix}> baseQueryMethod({Prefix}QueryBO queryBO);

    int insert({Prefix} {prefix});

    int update({Prefix} {prefix});

    int updateToDelete(Long {pkName});

    {Prefix} getByCode(Long {pkName});

    List<{Prefix}> getListByCodes(List<Long> codes);
}
```

**实现类 Path**: `{module}/service/impl/{Prefix}ServiceImpl.java` — 与直接类风格方法体一致，类声明改为：

```java
@Service("{beanName}")
public class {Prefix}ServiceImpl extends ServiceImpl<{Prefix}Mapper, {Prefix}> implements I{Prefix}Service {
    // 方法体与直接类风格一致，并加 @Override
}
```

### 8. Domain (聚合根)

**Path**: `{module}/service/domain/Sys{Prefix}Domain.java`

注入的 Service 类型跟随检测到的 Service 风格：直接类为 `{Prefix}Service`，接口风格为 `I{Prefix}Service`。

```java
package {basePackage}.{module}.service.domain;

import cn.hutool.core.collection.CollUtil;
import {boPackage}.{Prefix}QueryBO;
import {basePackage}.{module}.convert.{Prefix}Convert;
import {basePackage}.{module}.dto.{Prefix}{DtoSuffix};
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
 * @date {date}
 */
@Component
public class Sys{Prefix}Domain {

    @Resource
    private {Prefix}Service {prefix}Service;

    // Style B 时改为 @Resource 注入 Converter，并去掉 INSTANCE：
    // @Resource
    // private {Prefix}Converter {prefix}Converter;

    /**
     * 分页查询（委托给 baseQueryMethod）
     */
    public HashMap<String, Object> get{Prefix}List({Prefix}QueryBO queryBO) {
        List<{Prefix}> list = {prefix}Service.baseQueryMethod(queryBO);
        List<{Prefix}VO> voList = {Prefix}Convert.INSTANCE.poToVoList(list); // Style B: {prefix}Converter.poToVoList(list)
        HashMap<String, Object> result = new HashMap<>();
        result.put("count", list.size());
        result.put("vos", voList);
        return result;
    }

    /**
     * 新增
     */
    @Transactional(rollbackFor = Exception.class)
    public int insert({Prefix}{DtoSuffix} dto) {
        {Prefix} entity = {Prefix}Convert.INSTANCE.dtoToPo(dto); // Style B: {prefix}Converter.dtoToPo(dto)
        return {prefix}Service.insert(entity);
    }

    /**
     * 更新
     */
    @Transactional(rollbackFor = Exception.class)
    public int update({Prefix}{DtoSuffix} dto) {
        {Prefix} entity = {Prefix}Convert.INSTANCE.dtoToPo(dto); // Style B: {prefix}Converter.dtoToPo(dto)
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

### 9. Controller

**Path**: `{module}/controller/{Prefix}Controller.java`

注入的 Service 类型跟随检测到的 Service 风格（`{Prefix}Service` 或 `I{Prefix}Service`）。`@RequestMapping` 使用 `/` 前导斜杠。

```java
package {basePackage}.{module}.controller;

import {commonPackage}.core.domain.AjaxResult;
import {commonPackage}.core.domain.TableDataInfo;
import {commonPackage}.datasource.base.BaseController;
import {boPackage}.{Prefix}QueryBO;
import {basePackage}.{module}.dto.{Prefix}{DtoSuffix};
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
 * @date {date}
 */
@Slf4j
@RestController
@RequestMapping("/{mappingPath}")
public class {Prefix}Controller extends BaseController {

    @Resource
    private {Prefix}Service {prefix}Service;

    @Resource
    private Sys{Prefix}Domain sys{Prefix}Domain;

    /**
     * 分页查询（查询条件使用 QueryBO）
     */
    @GetMapping("/get{Prefix}PageList")
    public AjaxResult get{Prefix}PageList({Prefix}QueryBO queryBO) {
        log.info("{module}/get{Prefix}PageList :: {}", queryBO);
        this.startPage();
        HashMap<String, Object> data = sys{Prefix}Domain.get{Prefix}List(queryBO);
        TableDataInfo dataTable = this.getDataTable((List<?>) data.get("count"));
        dataTable.setRows((List<?>) data.get("vos"));
        return AjaxResult.success(dataTable);
    }

    /**
     * 全量查询（查询条件使用 QueryBO）
     */
    @GetMapping("/get{Prefix}List")
    public AjaxResult get{Prefix}List({Prefix}QueryBO queryBO) {
        log.info("{module}/get{Prefix}List :: {}", queryBO);
        HashMap<String, Object> data = sys{Prefix}Domain.get{Prefix}List(queryBO);
        return AjaxResult.success(data.get("vos"));
    }

    /**
     * 新增
     */
    @PostMapping("/add{Prefix}")
    public AjaxResult add{Prefix}(@RequestBody @Validated {Prefix}{DtoSuffix} dto) {
        log.info("{module}/add{Prefix} :: {}", dto);
        int i = sys{Prefix}Domain.insert(dto);
        return i > 0 ? AjaxResult.success("添加成功") : AjaxResult.error("添加失败");
    }

    /**
     * 更新
     */
    @PutMapping("/{Prefix}Update")
    public AjaxResult {prefix}Update(@RequestBody {Prefix}{DtoSuffix} dto) {
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

## Naming Conventions

| Element | Rule | Example |
|---------|------|---------|
| Entity class | `{Prefix}` | `SeStation` |
| Entity file | `{Prefix}.java` | `SeStation.java` |
| Mapper | `{Prefix}Mapper` | `StationMapper` |
| DTO | `{Prefix}{DtoSuffix}`（`SaveDTO` 或 `DTO`，按项目习惯） | `StationSaveDTO` |
| QueryBO | `{Prefix}QueryBO` | `StationQueryBO` |
| VO | `{Prefix}VO` | `StationVO` |
| Converter | `{Prefix}Convert`（Style A）或 `{Prefix}Converter`（Style B） | `StationConvert` / `StationConverter` |
| Service | `{Prefix}Service`（直接类）或 `I{Prefix}Service` + `{Prefix}ServiceImpl`（接口风格，按项目习惯） | `StationService` / `IStationService` |
| Domain | `Sys{Prefix}Domain` | `SysStationDomain` |
| Controller | `{Prefix}Controller` | `StationController` |
| Table | `UPPER_SNAKE_CASE` | `SE_STATION` |
| Column | `UPPER_SNAKE_CASE` | `STATION_CODE` |
| ID field | `Long {pkName}` | `Long stationCode` |

## Common Patterns Generated

### Fixed conditions (optional template, per baseQueryMethod convention)
- `.eq({Prefix}::getStatus, StatusEnum.IN_USE)` — status filter (logical delete)
- `.eq({Prefix}::getHospitalId, Common.getHospitalId())` — multi-tenant
- 按需启用：默认作为注释模板给出，用户确认后启用
- `@TableField(fill = FieldFill.INSERT)` for `createBy`, `createTime`
- `@TableField(fill = FieldFill.INSERT_UPDATE)` for `updateBy`, `updateTime`
- `StatusEnum.IN_USE` / `StatusEnum.DELETED` for status transitions

### LambdaQueryWrapper conditional chain (baseQueryMethod, from ddl-to-service)
- `Long` / `Integer` fields → `.eq(queryBO.get{Field}() != null, {Prefix}::get{Field}, queryBO.get{Field}())`
- `String` fields → `.eq(StrUtil.isNotBlank(queryBO.get{Field}()), {Prefix}::get{Field}, queryBO.get{Field}())` (exact) or `.like(...)` (fuzzy)
- `List` fields → `.in(CollUtil.isNotEmpty(queryBO.get{Field}()), {Prefix}::get{Field}, queryBO.get{Field}())`
- Range → `.le/.ge/.between(queryBO.get{Field}() != null, ...)`
- Always ends with `.orderByAsc({Prefix}::getShowOrder)` if showOrder exists

### CRUD methods always generated
1. `baseQueryMethod({QueryBO})` — conditional query (fixed conditions optional)
2. `insert({entity})` — set status + insert
3. `update({entity})` — check existence + update
4. `updateToDelete(id)` — logical delete (set DELETED status)
5. `getByCode(id)` — single by PK (fixed conditions optional)
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
   - List of 9 files to generate (8 + Controller)
   - Field mapping (DDL column → Java field)
   - Query strategy per field
5. **Get Confirmation** — user approves or adjusts
6. **Generate All Files** — write every file
7. **Ask for Adjustments** — "是否需要调整查询条件、添加额外方法或修改字段映射?"

## Important Constraints

1. **NEVER skip the Domain layer** — it MUST be generated as aggregation root
2. **NEVER skip QueryBO** — the `{Prefix}QueryBO` query object (per ddl-to-service `baseQueryMethod` convention) is required for all query paths
3. **ALWAYS use `baseQueryMethod` for queries** — list queries must go through `baseQueryMethod({Prefix}QueryBO)`, never direct PO or string-column QueryWrapper
4. **ALWAYS extend BaseController** — controller must extend detected base class
5. **固定条件遵循 baseQueryMethod 约定** — `hospitalId` / `STATUS` 等固定条件以注释模板给出，按需启用，不强制（检测到项目确有该约定时可默认启用并询问用户）
6. **NEVER skip `@Transactional`** — Domain write methods must have `rollbackFor = Exception.class`
7. **NEVER skip the Converter** — MapStruct is the standard mapping mechanism
8. **Service bean name must match** — `@Service("{beanName}")` with convention
9. **内部函数调用使用 `this.xxx()` 风格** — 调用当前类自身的方法（如 `this.getByCode()`、`this.list()`、`this.baseMapper.xxx()`）必须带 `this.` 前缀，不使用裸调用
10. **Ask user to confirm before generating** — never auto-generate blindly
11. **When DDL-only mode, show Entity draft first** — get user approval on Entity before proceeding