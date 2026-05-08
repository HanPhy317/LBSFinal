# 全国文保单位 POI Web API 与地图客户端 —— 课程设计实施计划

> **课程**：《基于位置的服务》(LBS)  
> **选题**：专题 POI Web API 设计实现与地图客户端应用测试  
> **截止日期**：2026年5月30日 18:00  
> **代码仓库**：https://gitee.com/rsgis/lbs-252602.git  

---

## 目录

1. [需求理解与分析](#一需求理解与分析)
2. [技术选型方案](#二技术选型方案)
3. [项目架构设计](#三项目架构设计)
4. [API 接口设计](#四api-接口设计)
5. [数据模型设计](#五数据模型设计)
6. [设计模式选择与应用](#六设计模式选择与应用)
7. [功能模块划分及模块间接口定义](#七功能模块划分及模块间接口定义)
8. [开发阶段划分与里程碑设定](#八开发阶段划分与里程碑设定)
9. [质量保证与测试策略](#九质量保证与测试策略)
10. [多媒体数据整合方案](#十多媒数据整合方案)

---

## 一、需求理解与分析

### 1.1 课程核心要求

| 维度 | 要求 |
|------|------|
| **选题** | 专题 POI Web API 设计实现与地图客户端应用测试 |
| **数据** | 全国重点文物保护单位（含坐标、类别、批次、年代等12个字段） |
| **服务端** | REST风格 Web API，含用户认证、角色管理（维护人员/公众用户）、多条件查询、空间查询 |
| **客户端** | 将 API 与公众地图服务集成，以地图可视化形式查看 POI 信息 |
| **安全** | 用户认证授权、访问限速、HTTPS |
| **响应格式** | JSON，含HTTP状态码、业务错误码、数据实体 + 扩展信息（图片、官网链接） |
| **团队** | 不超过3人，使用码云（Gitee）管理代码 |
| **提交内容** | 代码（服务端+客户端两份独立项目）、课程设计报告、系统演示 |

### 1.2 架构关键约束

- **客户端与服务端必须分离**：作为两份独立的可运行项目文件提交
- **通过标准化 API 接口交互**：RESTful JSON API
- **职责边界清晰**：服务端负责数据处理、业务逻辑、资源管理；客户端负责UI展示和用户交互

### 1.3 数据呈现要求

- 充分利用课程提供的基础数据资源（全国文保单位 2356 条）
- 整合多媒体数据元素：高精度地图可视化、高质量图片、情境化音频或演示视频
- 遵循现代UI/UX设计原则：布局合理、色彩协调、交互流畅、响应迅速

### 1.4 数据资源分析

通过分析 `全国文保单位.xlsx`，获得以下关键信息：

| 指标 | 数值/内容 |
|------|-----------|
| **总记录数** | 2,356 条 |
| **字段数** | 12 个 |
| **类别分布** | 古建筑(1,094) > 古遗址(505) > 近现代重要史迹(381) > 古墓葬(204) > 石窟寺及石刻(164) > 其他(8) |
| **批次分布** | 第六批(1,080) > 第五批(526) > 第三批(258) > 第四批(250) > 第一批(180) > 第二批(61) > 第七批(1) |
| **坐标范围** | 经度: 75.52° ~ 134.28°E，纬度: 16.59° ~ 50.63°N（覆盖中国全境） |
| **扩展潜力** | 27条记录含备注信息，可转化为扩展多媒体数据切入点 |
| **配套格式** | 同时提供 SHP 格式（GIS软件）和 KMZ 格式（Google Earth） |

---

## 二、技术选型方案

### 2.1 技术栈总览

```
┌─────────────────────────────────────────────────────────────────────┐
│                         服务端 (Server)                              │
├────────────────┬───────────────────┬────────────────────────────────┤
│ Web 框架        │ FastAPI 0.111+     │ 自动OpenAPI文档、异步、类型校验  │
│ ASGI 服务器     │ Uvicorn 0.30+      │ 高性能异步服务器                 │
│ 数据库          │ SQLite + SpatiaLite│ 零配置、单文件、空间索引支持      │
│ 认证            │ python-jose (JWT)  │ 无状态认证，C/S友好             │
│ 限流            │ slowapi            │ IP/用户级别限流                 │
│ 空间计算        │ Shapely + GeoPy    │ 空间判断、距离计算、地理编码      │
│ CORS            │ FastAPI CORSMiddleware │ 跨域支持                  │
│ HTTPS           │ 自签名证书（开发）/ Let's Encrypt（部署）            │
├────────────────┼───────────────────┼────────────────────────────────┤
│                         客户端 (Client)                              │
├────────────────┬───────────────────┬────────────────────────────────┤
│ 核心框架        │ Vue 3 + Vite       │ Composition API、快速HMR      │
│ UI 组件库       │ Element Plus 2.8+  │ 企业级Vue3组件、中文友好         │
│ 地图服务        │ 高德地图 JS API 2.0 │ POI显示、聚合、空间搜索           │
│ 数据可视化      │ ECharts 5.5+       │ 统计图表、热力图、地理映射        │
│ HTTP 客户端     │ Axios 1.7+         │ 拦截器、请求/响应转换             │
│ 状态管理        │ Pinia 2.x          │ Vue 3 官方状态管理               │
│ 路由            │ Vue Router 4.x     │ SPA 路由管理                    │
│ CSS 方案        │ Tailwind CSS 3.4+  │ 原子化CSS、快速构建现代UI         │
└────────────────┴───────────────────┴────────────────────────────────┘
```

### 2.2 核心技术选型论证

#### 2.2.1 后端框架：FastAPI vs Flask vs Django

| 维度 | FastAPI | Flask | Django |
|------|---------|-------|--------|
| 异步支持 | ✅ 原生 async/await | ⚠️ 需扩展 | ⚠️ 3.1+ 支持 |
| API 文档自动生成 | ✅ Swagger/ReDoc | ❌ 需插件 | ⚠️ 需 DRF |
| 类型校验 | ✅ Pydantic 内置 | ❌ 手动实现 | ⚠️ Serializer |
| 性能 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ |
| 学习曲线 | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐ |
| 适合纯 API 项目 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ |

**结论**：FastAPI 的自动 OpenAPI 文档生成对课程答辩演示极为有利（可直接用 Swagger UI 展示所有 API），且 Pydantic 模型自动进行数据校验，大幅减少手工验证代码量。

#### 2.2.2 数据库：SQLite + SpatiaLite vs PostgreSQL + PostGIS

| 维度 | SQLite + SpatiaLite | PostgreSQL + PostGIS |
|------|---------------------|----------------------|
| 部署复杂度 | ✅ 零配置，单文件 | ⚠️ 需安装配置服务 |
| 提交便利性 | ✅ 文件直接包含 | ❌ 需导出/导入SQL |
| 空间能力 | ✅ R-Tree索引、ST_Distance | ✅ 完整PostGIS功能 |
| 并发性能 | ⚠️ 有限 | ✅ 优秀 |
| 2,356条数据规模 | ✅ 绰绰有余 | ✅ 过度设计 |

**结论**：SQLite + SpatiaLite 对课程项目规模完全足够，且无需安装配置数据库服务，提交时数据库文件可直接包含在项目中，老师或评审方克隆后即可运行。

#### 2.2.3 地图服务：高德地图 vs Leaflet (OSM) vs 百度地图 vs 腾讯地图

| 维度 | 高德地图 JS API 2.0 | Leaflet + OSM | 百度地图 | 腾讯地图 |
|------|---------------------|---------------|----------|----------|
| 中国数据精度 | ⭐⭐⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| POI 展示效果 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| 免费额度 | 30万次/日 | 无限 | 20万次/日 | 1万次/日 |
| 文档和示例 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ |
| 国内市场占有 | 第一 | N/A | 第二 | 第三 |

**结论**：高德地图在中国大陆数据精度最高，POI展示效果最好，且免费日调用量（30万次）对课程项目完全足够。

---

## 三、项目架构设计

### 3.1 系统架构图

```
┌────────────────────────────────────────────────────────────────────────────┐
│                    🖥️  客户端应用 (lbs-final-client)                         │
│                    Vue 3 + Vite + Element Plus + 高德地图                   │
│                                                                              │
│  ┌────────────────┐  ┌────────────────┐  ┌─────────────────────────────┐   │
│  │  🔐 认证模块     │  │  🗺️ 地图浏览模块  │  │  📊 数据概览模块              │   │
│  │  - 登录/注册     │  │  - 全图POI标记    │  │  - 省份分布图(ECharts)       │   │
│  │  - API Key管理  │  │  - 聚合显示       │  │  - 类别饼图(ECharts)         │   │
│  │  - 个人信息维护   │  │  - 位置定位       │  │  - 批次时间轴                 │   │
│  └────────────────┘  └────────────────┘  └─────────────────────────────┘   │
│                                                                              │
│  ┌────────────────┐  ┌────────────────┐  ┌─────────────────────────────┐   │
│  │  🔍 查询检索模块  │  │  📝 POI详情模块   │  │  ⚙️ 数据管理模块              │   │
│  │  - 关键词搜索    │  │  - 详细信息卡片   │  │  - POI新增/编辑/删除          │   │
│  │  - 省份筛选      │  │  - 图片轮播       │  │  - 扩展信息编辑              │   │
│  │  - 类别筛选      │  │  - 音频播放       │  │  - (仅维护人员可用)           │   │
│  │  - 空间框选      │  │  - 官网链接跳转   │  │                             │   │
│  │  - 半径搜索      │  │  - 街景/全景     │  │                             │   │
│  └────────────────┘  └────────────────┘  └─────────────────────────────┘   │
│                                                                              │
│                        Axios HTTP Client (拦截器/重试/认证)                  │
└───────────────────────────────┬──────────────────────────────────────────────┘
                                │  HTTPS / RESTful API (JSON)
                                │
┌───────────────────────────────┼──────────────────────────────────────────────┐
│                    🖥️  服务端应用 (lbs-final-server)                         │
│                    FastAPI + Uvicorn + SQLite/SpatiaLite                    │
│                                                                              │
│  ┌────────────────────────────────────────────────────────────────────────┐ │
│  │                          🔐 中间件层 (Middleware)                        │ │
│  │  ┌──────────────────┐ ┌──────────────────┐ ┌──────────────────────┐    │ │
│  │  │ CORS 跨域中间件    │ │ JWT 认证中间件     │ │ Rate Limit 限流中间件  │    │ │
│  │  └──────────────────┘ └──────────────────┘ └──────────────────────┘    │ │
│  └────────────────────────────────────────────────────────────────────────┘ │
│                                                                              │
│  ┌────────────────────────────────────────────────────────────────────────┐ │
│  │                          📡 API 路由层 (Routers)                        │ │
│  │  ┌───────────┐ ┌───────────┐ ┌───────────┐ ┌────────────────────┐     │ │
│  │  │ /auth     │ │ /pois     │ │ /users    │ │ /stats             │     │ │
│  │  │ 认证路由   │ │ POI路由   │ │ 用户路由   │ │ 统计路由            │     │ │
│  │  └───────────┘ └───────────┘ └───────────┘ └────────────────────┘     │ │
│  └────────────────────────────────────────────────────────────────────────┘ │
│                                                                              │
│  ┌────────────────────────────────────────────────────────────────────────┐ │
│  │                         🧠 业务逻辑层 (Services)                         │ │
│  │  ┌───────────────┐ ┌───────────────┐ ┌───────────────────────────┐     │ │
│  │  │ AuthService   │ │ PoiService    │ │ SpatialQueryService       │     │ │
│  │  │ - 密码哈希     │ │ - CRUD操作    │ │ - 矩形框选查询              │     │ │
│  │  │ - JWT签发     │ │ - 条件查询    │ │ - 中心半径查询              │     │ │
│  │  │ - API Key    │ │ - 批量操作    │ │ - 空间索引优化              │     │ │
│  │  └───────────────┘ └───────────────┘ └───────────────────────────┘     │ │
│  │  ┌───────────────┐ ┌───────────────┐                                   │ │
│  │  │ UserService   │ │ StatsService  │                                   │ │
│  │  │ - 注册/信息   │ │ - 聚合统计    │                                   │ │
│  │  └───────────────┘ └───────────────┘                                   │ │
│  └────────────────────────────────────────────────────────────────────────┘ │
│                                                                              │
│  ┌────────────────────────────────────────────────────────────────────────┐ │
│  │                       💾 数据访问层 (Repositories)                       │ │
│  │  ┌──────────────────────────┐ ┌───────────────────────────┐            │ │
│  │  │ PoiRepository            │ │ UserRepository            │            │ │
│  │  │ (SQL + Spatial 查询)     │ │ (SQL)                     │            │ │
│  │  └──────────────────────────┘ └───────────────────────────┘            │ │
│  └────────────────────────────────────────────────────────────────────────┘ │
│                                                                              │
│  ┌────────────────────────────────────────────────────────────────────────┐ │
│  │                       🗄️ SQLite + SpatiaLite                            │ │
│  │  ┌──────────┐ ┌──────────┐ ┌───────────┐ ┌──────────────────────┐     │ │
│  │  │ users    │ │ pois     │ │ poi_media │ │ api_usage_logs       │     │ │
│  │  └──────────┘ └──────────┘ └───────────┘ └──────────────────────┘     │ │
│  └────────────────────────────────────────────────────────────────────────┘ │
└──────────────────────────────────────────────────────────────────────────────┘
```

### 3.2 项目目录结构

```
lbs-final/                           # 项目根目录（Gitee仓库）
│
├── server/                          # 【服务端独立项目】
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py                  # FastAPI 应用入口
│   │   ├── config.py                # 配置管理
│   │   ├── database.py              # 数据库连接与初始化
│   │   │
│   │   ├── models/                  # Pydantic 数据模型 (DTO/Schema)
│   │   │   ├── __init__.py
│   │   │   ├── user.py              # 用户相关模型
│   │   │   ├── poi.py               # POI 请求/响应模型
│   │   │   └── common.py            # 通用响应模型
│   │   │
│   │   ├── routers/                 # API 路由（控制器层）
│   │   │   ├── __init__.py
│   │   │   ├── auth.py              # POST /auth/*
│   │   │   ├── pois.py              # GET/POST/PUT/DELETE /pois/*
│   │   │   ├── users.py             # GET/PUT /users/*
│   │   │   └── stats.py             # GET /stats/*
│   │   │
│   │   ├── services/                # 业务逻辑层
│   │   │   ├── __init__.py
│   │   │   ├── auth_service.py
│   │   │   ├── poi_service.py
│   │   │   ├── spatial_service.py
│   │   │   ├── user_service.py
│   │   │   └── stats_service.py
│   │   │
│   │   ├── repositories/            # 数据访问层
│   │   │   ├── __init__.py
│   │   │   ├── poi_repository.py
│   │   │   ├── user_repository.py
│   │   │   └── base.py
│   │   │
│   │   ├── middleware/              # 中间件
│   │   │   ├── __init__.py
│   │   │   ├── auth.py              # JWT 认证依赖
│   │   │   └── rate_limit.py        # 限流配置
│   │   │
│   │   └── utils/                   # 工具函数
│   │       ├── __init__.py
│   │       ├── security.py          # 密码哈希、JWT生成/验证
│   │       ├── spatial.py           # 空间计算工具
│   │       └── response.py          # 统一响应格式构建器
│   │
│   ├── data/                        # 数据文件
│   │   ├── import_data.py           # Excel→SQLite 数据导入脚本
│   │   └── 全国文保单位.xlsx
│   │
│   ├── tests/                       # 测试
│   │   ├── __init__.py
│   │   ├── conftest.py              # pytest fixtures
│   │   ├── test_auth.py
│   │   ├── test_pois.py
│   │   └── test_spatial.py
│   │
│   ├── cert/                        # SSL 证书（开发用）
│   │   ├── cert.pem
│   │   └── key.pem
│   │
│   ├── requirements.txt
│   ├── run.py                       # 启动脚本
│   └── README.md
│
├── client/                          # 【客户端独立项目】
│   ├── public/
│   │   └── favicon.ico
│   │
│   ├── src/
│   │   ├── main.js                  # Vue 应用入口
│   │   ├── App.vue                  # 根组件
│   │   │
│   │   ├── api/                     # API 调用层
│   │   │   ├── index.js             # Axios 实例配置（baseURL/拦截器）
│   │   │   ├── auth.js              # 认证相关 API
│   │   │   ├── pois.js              # POI 相关 API
│   │   │   ├── stats.js             # 统计相关 API
│   │   │   └── user.js              # 用户相关 API
│   │   │
│   │   ├── router/                  # Vue Router 路由
│   │   │   └── index.js
│   │   │
│   │   ├── stores/                  # Pinia 状态管理
│   │   │   ├── auth.js              # 认证状态
│   │   │   ├── pois.js              # POI 数据状态
│   │   │   └── map.js               # 地图交互状态
│   │   │
│   │   ├── views/                   # 页面视图
│   │   │   ├── HomeView.vue         # 首页（数据概览仪表盘）
│   │   │   ├── MapView.vue          # 地图浏览页（核心页面）
│   │   │   ├── LoginView.vue        # 登录页
│   │   │   ├── RegisterView.vue     # 注册页
│   │   │   ├── ProfileView.vue      # 个人中心
│   │   │   ├── PoiDetailView.vue    # POI 详情页
│   │   │   ├── PoiManageView.vue    # POI 管理页（维护人员）
│   │   │   └── AboutView.vue        # 关于页
│   │   │
│   │   ├── components/              # 公共组件
│   │   │   ├── layout/
│   │   │   │   ├── AppHeader.vue
│   │   │   │   ├── AppSidebar.vue
│   │   │   │   └── AppFooter.vue
│   │   │   ├── map/
│   │   │   │   ├── AmapContainer.vue       # 高德地图容器
│   │   │   │   ├── PoiMarker.vue           # POI 标记点
│   │   │   │   ├── PoiCluster.vue          # POI 聚合显示
│   │   │   │   ├── PoiInfoWindow.vue       # POI 信息窗
│   │   │   │   ├── SpatialSearchTool.vue   # 空间搜索工具条
│   │   │   │   └── LocationButton.vue      # 定位按钮
│   │   │   ├── poi/
│   │   │   │   ├── PoiCard.vue             # POI 卡片
│   │   │   │   ├── PoiFilter.vue           # 筛选面板
│   │   │   │   ├── PoiTable.vue            # POI 列表表格
│   │   │   │   └── PoiForm.vue             # POI 表单（新增/编辑）
│   │   │   ├── charts/
│   │   │   │   ├── ProvinceChart.vue       # 省份分布柱状图
│   │   │   │   ├── CategoryChart.vue        # 类别饼图
│   │   │   │   └── TimelineChart.vue       # 批次时间轴
│   │   │   └── common/
│   │   │       ├── MediaViewer.vue         # 多媒体查看器
│   │   │       ├── AudioPlayer.vue         # 音频播放器
│   │   │       └── LoadingSkeleton.vue     # 加载骨架屏
│   │   │
│   │   ├── composables/             # 组合式函数（Vue Hooks）
│   │   │   ├── useAmap.js           # 高德地图 Hook
│   │   │   ├── useGeolocation.js    # 浏览器定位 Hook
│   │   │   └── usePoiSearch.js      # POI 搜索 Hook
│   │   │
│   │   └── assets/                  # 静态资源
│   │       ├── styles/
│   │       │   ├── main.css
│   │       │   └── variables.css
│   │       └── images/
│   │
│   ├── index.html
│   ├── vite.config.js
│   ├── tailwind.config.js
│   ├── package.json
│   └── README.md
│
├── docs/                            # 文档
│   └── 项目实施计划.md
│
└── README.md                        # 项目说明、成员分工、运行指南
```

### 3.3 数据流架构

```
┌──────────┐    HTTP Request     ┌──────────────┐    SQL Query     ┌──────────┐
│  Client  │ ──────────────────> │   FastAPI    │ ──────────────> │  SQLite  │
│ (Vue 3)  │ <────────────────── │   Server     │ <────────────── │ +Spatia  │
│          │    JSON Response    │              │    Result Set    │  Lite    │
└──────────┘                     └──────────────┘                  └──────────┘
     │                                  │
     │  高德地图 JS API                  │  GeoPy (逆地理编码)
     │  (地图渲染/标记/交互)              │  Shapely (空间计算)
     │                                  │
     ▼                                  ▼
┌──────────┐                     ┌──────────────┐
│ 高德地图  │                     │  外部地理服务  │
│ 服务集群  │                     │ (可选增强)    │
└──────────┘                     └──────────────┘

数据流向详解:
1. 用户操作客户端 → 触发 API 调用
2. Axios 拦截器自动附加 JWT Token/API Key
3. FastAPI 认证中间件验证身份
4. 限流中间件检查访问频率
5. 路由层将请求分发到对应 Service
6. Service 调用 Repository 执行数据库操作
7. Repository 返回原始数据
8. Service 组装响应模型（含扩展媒体信息）
9. FastAPI 自动序列化为 JSON 返回
10. 客户端解析 JSON，更新 Pinia Store 和 UI
```

---

## 四、API 接口设计

### 4.1 接口总览

```
Base URL: https://localhost:8000/api/v1

┌────────┬──────────────────────────────┬──────────────┬──────────────────────────┐
│  方法   │           端点               │    角色       │          说明             │
├────────┼──────────────────────────────┼──────────────┼──────────────────────────┤
│  POST  │ /auth/register               │   公开        │ 用户注册                  │
│  POST  │ /auth/login                  │   公开        │ 用户登录，返回JWT Token    │
│  GET   │ /auth/apikey                 │   登录用户     │ 获取/刷新 API Key         │
│  GET   │ /auth/me                     │   登录用户     │ 获取当前用户信息           │
│  PUT   │ /auth/profile                │   登录用户     │ 更新个人信息              │
├────────┼──────────────────────────────┼──────────────┼──────────────────────────┤
│  GET   │ /pois                        │   公开(限速)  │ POI 列表查询（组合筛选）   │
│  GET   │ /pois/{id}                   │   公开(限速)  │ POI 详情                 │
│  POST  │ /pois                        │   维护人员     │ 新增 POI                 │
│  PUT   │ /pois/{id}                   │   维护人员     │ 更新 POI                 │
│  DELETE│ /pois/{id}                   │   维护人员     │ 删除 POI                 │
│  GET   │ /pois/search                 │   公开(限速)  │ 关键词/名称搜索           │
│  GET   │ /pois/nearby                 │   公开(限速)  │ 中心半径空间搜索          │
│  GET   │ /pois/bbox                   │   公开(限速)  │ 矩形框选空间搜索          │
├────────┼──────────────────────────────┼──────────────┼──────────────────────────┤
│  GET   │ /stats/overview              │   公开        │ 数据概览统计              │
│  GET   │ /stats/by-province           │   公开        │ 按省份统计                │
│  GET   │ /stats/by-category           │   公开        │ 按类别统计                │
│  GET   │ /stats/by-batch              │   公开        │ 按批次统计                │
│  GET   │ /stats/by-age                │   公开        │ 按年代统计                │
└────────┴──────────────────────────────┴──────────────┴──────────────────────────┘
```

### 4.2 核心接口详细设计

#### 4.2.1 POI 列表查询（组合筛选）

```http
GET /api/v1/pois?name=故宫&province=北京&category=古建筑&batch=第一批
      &has_media=true
      &sw_lat=39.4&sw_lon=115.4&ne_lat=41.0&ne_lon=117.5
      &center_lat=39.9&center_lon=116.4&radius=50000
      &page=1&page_size=20&sort_by=name&order=asc
```

**Query Parameters：**

| 参数 | 类型 | 必填 | 说明 |
|------|------|:---:|------|
| `name` | string | 否 | POI名称（模糊匹配，支持%通配） |
| `province` | string | 否 | 省份（模糊匹配） |
| `category` | string | 否 | 类别（精确匹配） |
| `batch` | string | 否 | 批次（精确匹配） |
| `age` | string | 否 | 年代（模糊匹配） |
| `has_media` | boolean | 否 | 是否有扩展多媒体信息 |
| `sw_lat` | float | 否 | 矩形框西南纬度（配合 sw_lon, ne_lat, ne_lon） |
| `sw_lon` | float | 否 | 矩形框西南经度 |
| `ne_lat` | float | 否 | 矩形框东北纬度 |
| `ne_lon` | float | 否 | 矩形框东北经度 |
| `center_lat` | float | 否 | 中心点纬度（配合 center_lon, radius） |
| `center_lon` | float | 否 | 中心点经度 |
| `radius` | float | 否 | 搜索半径（米） |
| `page` | int | 否 | 页码（默认 1） |
| `page_size` | int | 否 | 每页数量（默认 20，最大 100） |
| `sort_by` | string | 否 | 排序字段（name/age/batch/lat/lon） |
| `order` | string | 否 | 排序方向（asc/desc） |

**Response 200：**

```json
{
  "code": 200,
  "message": "success",
  "data": {
    "total": 2356,
    "page": 1,
    "page_size": 20,
    "total_pages": 118,
    "items": [
      {
        "id": 1,
        "code": 404,
        "class_code": "210",
        "name": "喜洲白族古建筑群",
        "age": "明、清",
        "province": "云南省",
        "city": "大理市",
        "address": "云南省大理市",
        "category": "古建筑",
        "batch": "第五批",
        "remark": null,
        "longitude": 100.126760,
        "latitude": 25.853924,
        "media": [
          {
            "id": 1,
            "media_type": "image",
            "media_url": "https://example.com/images/xizhou1.jpg",
            "title": "喜洲白族古建筑群全景",
            "description": "云南省大理市喜洲镇"
          }
        ],
        "created_at": "2026-05-01T10:00:00",
        "updated_at": "2026-05-01T10:00:00"
      }
    ]
  }
}
```

#### 4.2.2 POI 详情

```http
GET /api/v1/pois/1
```

**Response 200：**

```json
{
  "code": 200,
  "message": "success",
  "data": {
    "id": 1,
    "code": 404,
    "class_code": "210",
    "name": "喜洲白族古建筑群",
    "age": "明、清",
    "province": "云南省",
    "city": "大理市",
    "address": "云南省大理市",
    "category": "古建筑",
    "batch": "第五批",
    "remark": null,
    "longitude": 100.126760,
    "latitude": 25.853924,
    "bd_longitude": 100.134614,
    "bd_latitude": 25.856669,
    "media": [
      {
        "id": 1,
        "media_type": "image",
        "media_url": "https://example.com/images/xizhou1.jpg",
        "title": "喜洲白族古建筑群全景",
        "description": "全国重点文物保护单位"
      },
      {
        "id": 2,
        "media_type": "audio",
        "media_url": "https://example.com/audio/xizhou_intro.mp3",
        "title": "喜洲白族古建筑群语音导览",
        "description": "时长 3:20"
      },
      {
        "id": 3,
        "media_type": "video",
        "media_url": "https://example.com/video/xizhou_tour.mp4",
        "title": "喜洲古镇航拍",
        "description": "4K高清航拍视频"
      },
      {
        "id": 4,
        "media_type": "website",
        "media_url": "https://www.dali.gov.cn/cultural/xizhou",
        "title": "大理州文旅局 - 喜洲",
        "description": "官方介绍页面"
      }
    ],
    "created_at": "2026-05-01T10:00:00",
    "updated_at": "2026-05-01T10:00:00"
  }
}
```

#### 4.2.3 空间查询 - 中心半径搜索

```http
GET /api/v1/pois/nearby?lat=39.9042&lon=116.4074&radius=50000&category=古建筑&page=1&page_size=50
```

空间查询采用 Haversine 公式计算球面距离，利用 SpatiaLite R-Tree 空间索引加速查询。

#### 4.2.4 空间查询 - 矩形框选

```http
GET /api/v1/pois/bbox?sw_lat=39.8&sw_lon=116.1&ne_lat=40.1&ne_lon=116.6&batch=第一批
```

#### 4.2.5 新增 POI（维护人员）

```http
POST /api/v1/pois
Authorization: Bearer <jwt_token>

{
  "name": "测试文保单位",
  "age": "清",
  "address": "北京市东城区",
  "category": "古建筑",
  "batch": "第一批",
  "longitude": 116.4074,
  "latitude": 39.9042,
  "remark": "测试新增记录",
  "media": [
    {
      "media_type": "image",
      "media_url": "https://example.com/test.jpg",
      "title": "测试图片"
    }
  ]
}
```

### 4.3 错误响应格式

```json
{
  "code": 40401,
  "message": "未找到指定的 POI 记录",
  "detail": {
    "resource": "poi",
    "resource_id": 99999,
    "help_url": "https://api.example.com/docs/errors#40401"
  }
}
```

**错误码体系：**

| HTTP状态码 | 业务错误码范围 | 典型场景 |
|:----------:|:-------------:|----------|
| 400 | 40001 - 40099 | 请求参数缺失、格式错误、值超出范围 |
| 401 | 40101 - 40199 | Token 过期、无效、未提供 |
| 403 | 40301 - 40399 | 角色权限不足（公众用户尝试增删改） |
| 404 | 40401 - 40499 | POI 不存在、用户不存在、端点不存在 |
| 409 | 40901 - 40999 | 资源冲突（用户名已占用等） |
| 429 | 42901 - 42999 | API 调用频率超限 |
| 500 | 50001 - 50099 | 服务器内部错误、数据库异常 |

### 4.4 接口鉴权机制

```
┌──────────────────────────────────────────────────────────────────┐
│                        鉴权流程                                    │
│                                                                    │
│  公开接口（/stats/*, 部分 /pois/*）                                │
│    └── 无需认证，但有 Rate Limit（IP级别限流）                      │
│                                                                    │
│  登录用户接口（/auth/*, 部分 /pois GET）                           │
│    ├── Header: Authorization: Bearer <JWT Token>                  │
│    ├── JWT 载荷: { sub: user_id, role: "public", exp: ... }       │
│    └── 或使用 API Key: Header: X-API-Key: <apikey>               │
│                                                                    │
│  维护人员接口（POST/PUT/DELETE /pois/*）                           │
│    ├── 必须 JWT Token，且 role = "maintainer"                     │
│    └── 中间件验证 role 字段                                       │
│                                                                    │
│  CORS 配置：                                                       │
│    └── 仅允许 client 域名跨域访问                                  │
└──────────────────────────────────────────────────────────────────┘
```

---

## 五、数据模型设计

### 5.1 数据库表设计

```sql
-- ============================================================
-- 用户表
-- ============================================================
CREATE TABLE IF NOT EXISTS users (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    username        TEXT    NOT NULL UNIQUE,
    email           TEXT    NOT NULL UNIQUE,
    password_hash   TEXT    NOT NULL,
    role            TEXT    NOT NULL DEFAULT 'public'
                            CHECK (role IN ('public', 'maintainer')),
    apikey          TEXT    UNIQUE,
    apikey_created_at TEXT,
    is_active       INTEGER NOT NULL DEFAULT 1,
    created_at      TEXT    NOT NULL DEFAULT (datetime('now')),
    updated_at      TEXT    NOT NULL DEFAULT (datetime('now'))
);

-- ============================================================
-- POI 主表（含空间字段）
-- ============================================================
CREATE TABLE IF NOT EXISTS pois (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    code            INTEGER,
    class_code      TEXT,
    name            TEXT    NOT NULL,
    age             TEXT,
    province        TEXT,
    city            TEXT,
    address         TEXT,
    category        TEXT,
    batch           TEXT,
    remark          TEXT,
    longitude       REAL    NOT NULL,
    latitude        REAL    NOT NULL,
    bd_longitude    REAL,
    bd_latitude     REAL,
    created_by      INTEGER REFERENCES users(id) ON DELETE SET NULL,
    created_at      TEXT    NOT NULL DEFAULT (datetime('now')),
    updated_at      TEXT    NOT NULL DEFAULT (datetime('now'))
);

-- 创建空间索引
SELECT AddGeometryColumn('pois', 'geometry', 4326, 'POINT', 'XY');
SELECT CreateSpatialIndex('pois', 'geometry');

-- 创建普通索引
CREATE INDEX IF NOT EXISTS idx_pois_name      ON pois(name);
CREATE INDEX IF NOT EXISTS idx_pois_category  ON pois(category);
CREATE INDEX IF NOT EXISTS idx_pois_batch     ON pois(batch);
CREATE INDEX IF NOT EXISTS idx_pois_province  ON pois(province);

-- ============================================================
-- POI 多媒体扩展表
-- ============================================================
CREATE TABLE IF NOT EXISTS poi_media (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    poi_id          INTEGER NOT NULL REFERENCES pois(id) ON DELETE CASCADE,
    media_type      TEXT    NOT NULL
                            CHECK (media_type IN ('image', 'audio', 'video', 'website')),
    media_url       TEXT    NOT NULL,
    title           TEXT,
    description     TEXT,
    sort_order      INTEGER DEFAULT 0,
    created_at      TEXT    NOT NULL DEFAULT (datetime('now'))
);

CREATE INDEX IF NOT EXISTS idx_poi_media_poi_id ON poi_media(poi_id);

-- ============================================================
-- API 使用日志表
-- ============================================================
CREATE TABLE IF NOT EXISTS api_usage_logs (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id         INTEGER REFERENCES users(id) ON DELETE SET NULL,
    apikey          TEXT,
    endpoint        TEXT    NOT NULL,
    method          TEXT    NOT NULL,
    ip_address      TEXT,
    user_agent      TEXT,
    status_code     INTEGER,
    response_time_ms INTEGER,
    created_at      TEXT    NOT NULL DEFAULT (datetime('now'))
);

CREATE INDEX IF NOT EXISTS idx_logs_user_id   ON api_usage_logs(user_id);
CREATE INDEX IF NOT EXISTS idx_logs_endpoint  ON api_usage_logs(endpoint);
CREATE INDEX IF NOT EXISTS idx_logs_created   ON api_usage_logs(created_at);
```

### 5.2 实体关系图（ER图）

```
┌──────────────────┐         ┌──────────────────────┐
│      users        │         │         pois          │
├──────────────────┤         ├──────────────────────┤
│ PK  id           │◄────────│ FK  created_by       │
│     username      │         │ PK  id               │
│     email         │         │     code             │
│     password_hash │         │     class_code       │
│     role          │         │     name             │
│     apikey        │         │     age              │
│     is_active     │         │     province         │
│     created_at    │         │     city             │
│     updated_at    │         │     address          │
└────────┬─────────┘         │     category         │
         │                   │     batch            │
         │                   │     remark           │
         │                   │     longitude        │
         │                   │     latitude         │
         │                   │     bd_longitude     │
         │                   │     bd_latitude      │
         │                   │     geometry (空间)   │
         │                   │     created_at       │
         │                   │     updated_at       │
         │                   └──────────┬───────────┘
         │                              │ 1 : N
         │                   ┌──────────▼───────────┐
         │                   │      poi_media        │
         │                   ├────────────────────