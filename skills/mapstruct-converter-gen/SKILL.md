---
name: mapstruct-converter-gen
description: "Generate MapStruct Converter interface + DTO + VO from an Entity class, following project conventions. Triggered when user wants to create object converters, DTO/VO mapping, or says '生成转换器' / 'Converter' / 'DTO转VO'."
---

# MapStruct Converter Generator

Generate MapStruct Converter interface with DTO → Entity → VO mapping methods from an Entity class.

## Trigger

Invoke this skill when the user:
- Provides an Entity class and asks to generate Converter / DTO / VO
- Says "生成转换器" / "生成 DTO" / "生成 VO" / "Converter"
- Mentions MapStruct in the context of object mapping

## Two Project Styles

This skill detects and supports two conventions used across NaCl's projects:

### Style A: Ruoyi + MapStruct factory

```java
// Package: {basePackage}.{module}.convert
@Mapper                          // no componentModel
public interface StationConvert {
    StationConvert INSTANCE = Mappers.getMapper(StationConvert.class);

    // PO → VO (batch)
    List<StationVO> poToVoList(List<SeStation> list);
    // DTO → PO
    SeStation dtoToPo(StationSaveDTO dto);
    // Single field → PO (for query by code)
    SeStation dtoToPo(Long stationCode);
}
```

### Style B: Spring componentModel

Used by: wlzyglg-business-backend, wlztgl-information-backend, xjfd-business-backend

```java
// Package: com.wenxuan.wl.{module}.converter
@Mapper(componentModel = "spring")   // Spring DI, no INSTANCE
public interface NoticeConverter {
    // PO → VO
    NoticeVO columnEntityToVO(Notice notice);
    // QO → PO (batch)
    List<Notice> columnListQoToEntity(List<NoticeQo> qoList);
    // DTO → PO (batch)
    List<Notice> listDtoToListEntity(List<NoticeDTO> dtoList);
    // DTO → PO (single)
    Notice dtoToEntity(NoticeDTO dto);
    // QO → PO (single)
    Notice columnQoToEntity(NoticeQo qo);
}
```

## Project Style Detection

Before generating, detect the project's MapStruct convention:

### Detection Checklist

1. **Check existing Converter files** — look for `*Convert.java` / `*Converter.java` in the project
2. **Check `@Mapper` annotation** — with or without `componentModel = "spring"`
3. **Check INSTANCE pattern** — `Mappers.getMapper()` present or absent
4. **Check package naming** — `converter` or `convert`
5. **Check DTO/VO/BO package** — `dto/`, `vo/`, `bo/` or `pojo/dto/`, `pojo/vo/`

### Detection Rules

| Condition | Style |
|-----------|-------|
| Has `INSTANCE = Mappers.getMapper()` | Style A (factory) |
| Has `componentModel = "spring"` | Style B (Spring DI) |
| No existing Converter | Default to Style A (factory) |

Always present detected style to user for confirmation.

## Input Modes

### Mode A: Entity + DTO + VO all provided

User pastes all three classes. Use them as-is.

### Mode B: Entity only

User pastes only Entity. You MUST:
1. Parse Entity fields and comments
2. Generate DTO draft (create/update fields with `@NotBlank`/`@NotNull` validation)
3. Generate VO draft (all fields + `@Builder` + `@AllArgsConstructor` + `@NoArgsConstructor`)
4. Present both drafts to user for confirmation BEFORE proceeding
5. If user approves, generate all files

### Mode C: Entity + target type

User provides Entity + specific target (e.g., "generate VO only"). Generate only requested files.

## Generated Files

### 1. Converter Interface

**Style A path**: `{module}/convert/{Prefix}Convert.java`
**Style B path**: `{module}/converter/{Prefix}Converter.java`

**Methods always generated:**
- `poToVoList(List<Entity>)` → `List<VO>` — batch PO→VO
- `dtoToPo(DTO)` → `Entity` — single DTO→PO
- `dtoListToPoList(List<DTO>)` → `List<Entity>` — batch DTO→PO (Style B only)

**Methods generated when Query Object exists:**
- `qoToEntity(QO)` → `Entity` — single QO→PO (Style B)
- `qoListToEntityList(List<QO>)` → `List<Entity>` — batch QO→PO (Style B)

**Methods generated when VO has extra fields not in Entity:**
- `entityToVo(Entity)` → `VO` — single PO→VO (for extra field manual mapping)

### 2. DTO Class

**Path**: `{module}/dto/{Prefix}SaveDTO.java` or `{module}/dto/{Prefix}DTO.java`

**Rules:**
- Use `@Data` + `implements Serializable`
- Include all Entity fields except audit (createTime, updateTime, createBy, updateBy, deleted)
- Add `@NotBlank` / `@NotNull` validation annotations based on nullable/required
- Copy field comments from Entity
- For Style B, also generate `{Prefix}Qo.java` (query object, all fields as String for flexible querying)

### 3. VO Class

**Path**: `{module}/vo/{Prefix}VO.java`

**Rules:**
- Use `@Data` + `@Builder` + `@AllArgsConstructor` + `@NoArgsConstructor`
- Include all Entity fields
- Add display-only / computed fields (e.g., `groupTypeName` when Entity has `groupTypeCode`)
- Add `List<{Prefix}BO>` for nested structures if Entity has one-to-many relations
- Copy field comments from Entity

### 4. Query Object (Style B only)

**Path**: `{module}/qo/{Prefix}Qo.java`

**Rules:**
- All fields as `String` type for flexible conditional querying
- Include business-meaningful fields only (skip id, audit fields)
- Use `@Data` + `implements Serializable`

## Field Mapping Rules

### Entity → DTO mapping

| Entity Field | DTO Field | Notes |
|-------------|-----------|-------|
| `id` / `{prefix}Id` | `{prefix}Code` or removed | DTO may use business code instead of PK |
| `createTime`, `updateTime` | **SKIP** | Audit fields not in DTO |
| `createBy`, `updateBy` | **SKIP** | Audit fields |
| `deleted` / `isDeleted` | **SKIP** | Logical delete flag |
| `tenantId` | **SKIP** | Multi-tenant, auto-filled |
| All other fields | Same name + type | Copy with comments |

### Entity → VO mapping

All Entity fields included. Add display fields:
- `xxxCode` → add `xxxName` for display
- Status fields → add `statusDesc` / `useStatusDesc`
- Count/aggregate fields → add computed count fields

### DTO → Entity mapping

Direct field name matching. Fields present in DTO but not Entity → skip (DTO-only fields like `formIds` list).

## Generation Workflow

1. **Parse Entity** — extract fields, types, comments
2. **Detect Project Style** — check existing Converters
3. **Auto-Detect** — package, module, prefix
4. **Present Plan** — show:
   - Detected style (A/B)
   - Package path
   - List of files to generate
   - Field mapping table
5. **Get Confirmation** — user approves or adjusts
6. **Generate All Files** — write every file
7. **Ask for Adjustments** — "是否需要调整字段映射、添加额外方法?"

## Example

### Input Entity

```java
// SeStation.java
@TableName("SE_STATION")
@Data @Builder @AllArgsConstructor @NoArgsConstructor
public class SeStation implements Serializable {
    @TableId(type = IdType.ASSIGN_ID)
    private Long stationCode;        // 考站编码
    private String stationName;      // 考站名称
    private Long groupTypeCode;      // 分组类型
    private Long groupCode;          // 专业类型
    private Integer showOrder;       // 显示顺序
    private Integer duration;        // 时长
    private String useStatus;        // 启用状态;1:启用、0:禁用
    private Integer totalScoreRatio; // 总分占比
    private Integer annexCount;      // 附件数量
    @TableField(fill = FieldFill.INSERT)
    private String createBy;
    @TableField(fill = FieldFill.INSERT_UPDATE)
    private String updateBy;
    @TableField(fill = FieldFill.INSERT)
    private LocalDateTime createTime;
    @TableField(fill = FieldFill.INSERT_UPDATE)
    private LocalDateTime updateTime;
}
```

### Generated Converter (Style A)

```java
package com.example.osce.se.station.convert;

import com.example.osce.se.station.dto.StationSaveDTO;
import com.example.osce.se.station.po.SeStation;
import com.example.osce.se.station.vo.StationVO;
import org.mapstruct.Mapper;
import org.mapstruct.factory.Mappers;

import java.util.List;

/**
 * 考站映射转换类
 *
 * @author NaCl
 * @since 2023/4/16
 */
@Mapper
public interface StationConvert {

    StationConvert INSTANCE = Mappers.getMapper(StationConvert.class);

    /**
     * poList转voList
     */
    List<StationVO> poToVoList(List<SeStation> seStations);

    /**
     * dto转po
     */
    SeStation dtoToPo(StationSaveDTO dto);

    /**
     * 把stationCode封装成po
     */
    SeStation dtoToPo(Long stationCode);
}
```

### Generated DTO

```java
package com.example.osce.se.station.dto;

import lombok.Data;
import javax.validation.constraints.NotBlank;
import javax.validation.constraints.NotNull;
import java.io.Serializable;

/**
 * 考站前端数据传输对象
 */
@Data
public class StationSaveDTO implements Serializable {
    private Long stationCode;              // 考站编码
    @NotBlank(message = "考站名称不能为空")
    private String stationName;            // 考站名称
    @NotNull(message = "分组类型不能为空")
    private Long groupTypeCode;            // 分组类型
    @NotNull(message = "专业类型不能为空")
    private Long groupCode;                // 专业类型
    private Integer showOrder;             // 显示顺序
    private Integer duration;              // 时长
    private String useStatus;              // 启用状态
    @NotNull(message = "总分占比不能为空")
    private Integer totalScoreRatio;       // 总分占比
    private Integer annexCount;            // 附件数量
}
```

### Generated VO

```java
package com.example.osce.se.station.vo;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

/**
 * 考站后端数据传输对象
 */
@Data
@AllArgsConstructor
@NoArgsConstructor
@Builder
public class StationVO {
    private Long stationCode;              // 考站编码
    private String stationName;            // 考站名称
    private Long groupTypeCode;            // 分组类型
    private String groupTypeName;          // 分组类型名称（显示用）
    private Long groupCode;                // 专业类型
    private String groupName;              // 专业名称（显示用）
    private Integer showOrder;             // 显示顺序
    private Integer duration;              // 时长
    private String useStatus;              // 启用状态
    private Integer totalScoreRatio;       // 总分占比
    private Integer annexCount;            // 附件数量
}
```

## Important Constraints

1. **NEVER skip the Converter** — it MUST be generated in the detected package
2. **NEVER skip the INSTANCE field** (Style A) or `componentModel` (Style B)
3. **ALWAYS include batch methods** — `poToVoList` / `dtoListToPoList` are mandatory
4. **ALWAYS detect project style first** — never assume conventions
5. **Audit fields are NEVER in DTO** — createTime/updateTime/createBy/updateBy always excluded
6. **VO includes display fields** — code → name pairs for enum/dropdown fields
7. **Ask user to confirm before generating** — never auto-generate blindly
8. **When Entity-only mode, show drafts first** — get user approval on DTO/VO before proceeding