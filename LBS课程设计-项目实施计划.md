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
│      users       │         │         pois         │
├──────────────────┤         ├──────────────────────┤
│ PK  id           │◄────────│ FK  created_by       │
│     username     │         │ PK  id               │
│     email        │         │     code             │
│     password_hash│         │     class_code       │
│     role         │         │     name             │
│     apikey       │         │     age              │
│     is_active    │         │     province         │
│     created_at   │         │     city             │
│     updated_at   │         │     address          │
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
         │                   │      poi_media       │
         │                   ├──────────────────────┤
         │                   │ PK  id               │
         │                   │ FK  poi_id           │
         │                   │     media_type       │ (image/audio/video/website)
         │                   │     media_url        │
         │                   │     title            │
         │                   │     description      │
         │                   │     sort_order       │
         │                   └──────────────────────┘
         │
         │ 1 : N
         ▼
  ┌──────────────────────────┐
  │     api_usage_logs       │
  ├──────────────────────────┤
  │ PK  id                   │
  │ FK  user_id              │
  │     apikey               │
  │     endpoint             │
  │     method               │
  │     ip_address           │
  │     user_agent           │
  │     status_code          │
  │     response_time_ms     │
  │     created_at           │
  └──────────────────────────┘
```

---

## 六、设计模式选择与应用

### 6.1 服务端设计模式

| 设计模式 | 应用场景 | 项目中的具体体现 |
|----------|----------|-----------------|
| **分层架构 (Layered Architecture)** | 整体架构组织 | Router（路由层）→ Service（业务逻辑层）→ Repository（数据访问层）三层分离，各层之间通过接口通信，上层依赖下层，下层不感知上层 |
| **依赖注入 (Dependency Injection)** | 解耦组件依赖 | FastAPI `Depends()` 机制注入数据库会话 (`get_db`)、认证用户 (`get_current_user`)、服务实例，实现控制反转，便于单元测试时 Mock |
| **仓储模式 (Repository Pattern)** | 数据访问抽象 | `PoiRepository`、`UserRepository` 封装所有 SQL 操作，Service 层不直接编写 SQL。若未来需要切换为 PostgreSQL，仅需修改 Repository 层实现 |
| **DTO/Model 分离** | API 数据校验 | Pydantic `schemas`（`poi.py`, `user.py`）定义请求/响应数据模型，与数据库实体模型（SQLite 表结构）完全分离，防范 Mass Assignment 攻击 |
| **策略模式 (Strategy Pattern)** | 多种查询方式 | `SpatialQueryService` 根据请求参数动态选择查询策略：BBox 策略（矩形框选）→ SpatiaLite `ST_Within`；Radius 策略（中心半径）→ Haversine 公式；普通策略（属性筛选）→ SQL WHERE 组合 |
| **工厂模式 (Factory Pattern)** | 统一响应构建 | `utils/response.py` 提供工厂函数 `success_response(data)`、`error_response(code, message)`，确保所有接口返回格式严格一致 |
| **单例模式 (Singleton)** | 数据库连接管理 | SQLite 连接在应用启动时初始化，通过 FastAPI 的 lifespan 上下文管理，全局复用同一连接池 |
| **观察者模式 (Observer Pattern)** | API 使用日志 | 通过 FastAPI 中间件（Middleware）拦截所有 HTTP 请求，自动记录到 `api_usage_logs` 表，实现非侵入式的日志采集 |
| **代理模式 (Proxy Pattern)** | 访问控制 | `slowapi` 作为代理层控制 API 访问频率；JWT 认证中间件作为安全代理，拦截未授权请求 |
| **模板方法模式 (Template Method)** | 通用 CRUD 操作 | `BaseRepository` 定义通用 CRUD 方法骨架（`get_by_id`、`create`、`update`、`delete`），子类重写特定查询逻辑 |

### 6.2 客户端设计模式

| 设计模式 | 应用场景 | 项目中的具体体现 |
|----------|----------|-----------------|
| **组合模式 (Composite Pattern)** | UI 组件树 | Vue 组件嵌套：`AmapContainer` → `PoiMarker` → `PoiInfoWindow`，父组件管理子组件生命周期，Props 向下传递数据，Events 向上发送事件 |
| **状态管理模式** | 全局数据共享 | Pinia Store 管理三大核心状态：`auth`（用户认证状态）、`pois`（POI数据缓存）、`map`（地图交互状态），实现组件间数据同步 |
| **观察者模式 (Observer)** | 响应式数据绑定 | Vue 3 Composition API 的 `ref`/`reactive` + `watch`/`computed` 实现数据变化自动驱动 UI 更新 |
| **拦截器模式 (Interceptor)** | HTTP 请求/响应处理 | Axios Interceptors：请求拦截器自动附加 JWT Token 和 API Key；响应拦截器统一处理 401 跳转登录、429 限流提示 |
| **策略模式 (Strategy)** | 地图标记渲染 | 根据缩放级别选择：高缩放级别 → 单个 `PoiMarker` 渲染；低缩放级别 → `PoiCluster` 聚合显示（海量点聚合算法） |
| **单例模式 (Singleton)** | 高德地图实例 | 通过 `useAmap.js` composable 确保整个应用中只有一个 AMap 实例，避免重复加载 JS API 和内存泄漏 |
| **适配器模式 (Adapter)** | API 数据转换 | `api/pois.js` 中封装响应数据格式转换逻辑（将服务端 JSON 转换为前端组件所需的数据结构），隔离后端数据结构变化对前端的影响 |
| **路由守卫模式 (Guard)** | 页面访问控制 | Vue Router 的 `beforeEach` 导航守卫：检查 Token 有效性、角色权限（维护人员页面仅 role=maintainer 可访问） |

---

## 七、功能模块划分及模块间接口定义

### 7.1 服务端模块架构

```
┌──────────────────────────────────────────────────────────────────────────┐
│                         服务端模块架构                                     │
│                                                                          │
│  ┌─────────────────────────────────────────────────────────────────┐    │
│  │ 模块1: 认证模块 (Auth Module)                                     │    │
│  │ ┌───────────────┐ ┌───────────────┐ ┌───────────────────────┐   │    │
│  │ │ Router: auth.py│ │ Service:      │ │ Repository:           │   │    │
│  │ │ /register      │ │ auth_service  │ │ user_repository       │   │    │
│  │ │ /login         │ │ - register()  │ │ - create()            │   │    │
│  │ │ /apikey        │ │ - login()     │ │ - get_by_username()   │   │    │
│  │ │ /me            │ │ - gen_apikey()│ │ - get_by_email()      │   │    │
│  │ │ /profile       │ │ - verify_jwt()│ │ - update()            │   │    │
│  │ └───────────────┘ └───────────────┘ └───────────────────────┘   │    │
│  └─────────────────────────────────────────────────────────────────┘    │
│                                                                          │
│  ┌─────────────────────────────────────────────────────────────────┐    │
│  │ 模块2: POI 查询模块 (POI Query Module)                             │    │
│  │ ┌───────────────┐ ┌───────────────┐ ┌────────────────────────┐  │    │
│  │ │ Router: pois.py│ │ Service:      │ │ Repository:             │  │    │
│  │ │ GET /          │ │ poi_service   │ │ poi_repository          │  │    │
│  │ │ GET /{id}      │ │ - list()      │ │ - find_all()            │  │    │
│  │ │ GET /search    │ │ - get_detail()│ │ - find_by_id()          │  │    │
│  │ │ GET /nearby    │ │ - search()    │ │ - find_by_name()        │  │    │
│  │ │ GET /bbox      │ │               │ │ - find_nearby()         │  │    │
│  │ └───────────────┘ └───────────────┘ │ - find_by_bbox()        │  │    │
│  │                                      └────────────────────────┘  │    │
│  │  ┌──────────────────────────────────────────────────────────────┐ │    │
│  │  │ 子模块: 空间查询模块 (Spatial Module)                          │ │    │
│  │  │ ┌──────────────────────┐ ┌────────────────────────────────┐  │ │    │
│  │  │ │ Service:             │ │ Utils:                          │  │ │    │
│  │  │ │ spatial_service      │ │ spatial.py                      │  │ │    │
│  │  │ │ - query_nearby()     │ │ - haversine_distance()          │  │ │    │
│  │  │ │ - query_bbox()       │ │ - is_point_in_bbox()            │  │ │    │
│  │  │ │ - build_spatial_sql()│ │ - wgs84_to_bd09()               │  │ │    │
│  │  │ └──────────────────────┘ └────────────────────────────────┘  │ │    │
│  │  └──────────────────────────────────────────────────────────────┘ │    │
│  └─────────────────────────────────────────────────────────────────┘    │
│                                                                          │
│  ┌─────────────────────────────────────────────────────────────────┐    │
│  │ 模块3: POI 管理模块 (POI Management Module) [维护人员专用]         │    │
│  │ ┌───────────────┐ ┌───────────────┐ ┌────────────────────────┐  │    │
│  │ │ Router: pois.py│ │ Service:      │ │ Repository:             │  │    │
│  │ │ POST /         │ │ poi_service   │ │ poi_repository          │  │    │
│  │ │ PUT /{id}      │ │ - create()    │ │ - insert()              │  │    │
│  │ │ DELETE /{id}   │ │ - update()    │ │ - update_by_id()        │  │    │
│  │ └───────────────┘ │ - delete()    │ │ - delete_by_id()        │  │    │
│  │                    └───────────────┘ └────────────────────────┘  │    │
│  └─────────────────────────────────────────────────────────────────┘    │
│                                                                          │
│  ┌─────────────────────────────────────────────────────────────────┐    │
│  │ 模块4: 统计模块 (Statistics Module)                                │    │
│  │ ┌───────────────┐ ┌───────────────┐ ┌────────────────────────┐  │    │
│  │ │ Router:        │ │ Service:      │ │ Repository:             │  │    │
│  │ │ stats.py       │ │ stats_service │ │ poi_repository          │  │    │
│  │ │ /overview      │ │ - overview()  │ │ - count_by_province()   │  │    │
│  │ │ /by-province   │ │ - by_province│ │ - count_by_category()   │  │    │
│  │ │ /by-category   │ │ - by_category│ │ - count_by_batch()      │  │    │
│  │ │ /by-batch      │ │ - by_batch   │ │ - count_by_age()        │  │    │
│  │ │ /by-age        │ │ - by_age     │ └────────────────────────┘  │    │
│  │ └───────────────┘ └───────────────┘                              │    │
│  └─────────────────────────────────────────────────────────────────┘    │
│                                                                          │
│  ┌─────────────────────────────────────────────────────────────────┐    │
│  │ 模块5: 中间件模块 (Middleware Module)                               │    │
│  │ ┌────────────────┐ ┌──────────────────┐ ┌────────────────────┐  │    │
│  │ │ CORS 中间件     │ │ JWT 认证依赖      │ │ 限流中间件          │  │    │
│  │ │ 允许跨域来源     │ │ get_current_user │ │ slowapi Limiter    │  │    │
│  │ │ 允许方法/头      │ │ require_maintainer│ │ 100req/min(公众)   │  │    │
│  │ │ 凭据传递支持     │ │ require_apikey   │ │ 无限制(维护人员)    │  │    │
│  │ └────────────────┘ └──────────────────┘ └────────────────────┘  │    │
│  └─────────────────────────────────────────────────────────────────┘    │
└──────────────────────────────────────────────────────────────────────────┘
```

### 7.2 模块间接口定义

#### 7.2.1 Router → Service 接口（契约示例）

所有 Router 通过 FastAPI 的 `Depends()` 获取 Service 实例，Service 通过构造函数接收 Repository 实例（依赖注入）。

```text
PoiService 接口:
  - list_pois(filters, pagination, spatial=None) -> PaginatedResponse
    功能: POI 列表查询，支持组合筛选、分页、排序、空间过滤

  - get_poi_detail(poi_id) -> PoiDetailResponse
    功能: 获取 POI 详情，包含关联的所有媒体信息

  - create_poi(data, user_id) -> PoiResponse
    功能: 新增 POI，自动提取省份/城市信息

  - update_poi(poi_id, data) -> PoiResponse
    功能: 更新 POI，仅更新提供的字段（部分更新）

  - delete_poi(poi_id) -> None
    功能: 删除 POI，级联删除关联的媒体记录
```

#### 7.2.2 Service → Repository 接口（契约示例）

```text
PoiRepository 接口:
  - find_all(filters, spatial_filter, pagination, sort) -> (list, int)
    返回: (POI列表, 总记录数) 元组

  - find_by_id(poi_id) -> Optional[dict]
    返回: POI 字典或 None

  - find_media_by_poi_id(poi_id) -> list[dict]
    返回: 该 POI 的媒体列表

  - insert(data) -> int
    返回: 新插入的 POI ID

  - update_by_id(poi_id, data) -> bool
    返回: 是否成功更新

  - delete_by_id(poi_id) -> bool
    返回: 是否成功删除
```

### 7.3 客户端 API 调用 ↔ 服务端端点映射

| 客户端 API 函数 | HTTP 方法 | 服务端端点 | 说明 |
|----------------|:---------:|-----------|------|
| `authApi.login(credentials)` | POST | `/auth/login` | 登录获取 Token |
| `authApi.register(data)` | POST | `/auth/register` | 用户注册 |
| `authApi.getApiKey()` | GET | `/auth/apikey` | 获取 API Key |
| `poiApi.getList(params)` | GET | `/pois` | POI 列表（筛选+分页） |
| `poiApi.getDetail(id)` | GET | `/pois/{id}` | POI 详情 |
| `poiApi.searchNearby(params)` | GET | `/pois/nearby` | 中心半径搜索 |
| `poiApi.searchBbox(params)` | GET | `/pois/bbox` | 矩形框选搜索 |
| `poiApi.create(data)` | POST | `/pois` | 新增 POI |
| `poiApi.update(id, data)` | PUT | `/pois/{id}` | 更新 POI |
| `poiApi.delete(id)` | DELETE | `/pois/{id}` | 删除 POI |
| `statsApi.getOverview()` | GET | `/stats/overview` | 数据概览 |
| `statsApi.getByProvince()` | GET | `/stats/by-province` | 省份统计 |
| `statsApi.getByCategory()` | GET | `/stats/by-category` | 类别统计 |

### 7.4 前端页面路由与权限表

| 路由路径 | 页面组件 | 权限要求 | 说明 |
|----------|----------|:--------:|------|
| `/` | `HomeView` | 公开 | 首页：数据概览仪表盘 |
| `/map` | `MapView` | 公开 | 地图浏览（核心页面） |
| `/map/:id` | `PoiDetailView` | 公开 | POI 详情弹窗/侧边栏 |
| `/login` | `LoginView` | 未登录 | 登录页 |
| `/register` | `RegisterView` | 未登录 | 注册页 |
| `/profile` | `ProfileView` | 登录用户 | 个人中心 |
| `/manage` | `PoiManageView` | 维护人员 | POI 数据管理 |
| `/about` | `AboutView` | 公开 | 关于页面 |

---

## 八、开发阶段划分与里程碑设定

### 8.1 五个开发阶段

```
总工期: 约 3 周 (2026年5月8日 -> 2026年5月29日)
截止提交: 2026年5月30日 18:00
```

#### 第一阶段：环境搭建与数据准备（2天，5月8日 - 5月9日）

**目标**：项目骨架搭建完毕，数据成功导入数据库，前后端可独立运行

| 任务 | 负责人 | 产出 | 验证标准 |
|------|:------:|------|----------|
| Gitee 仓库克隆、创建开发分支 | 全组 | 分支创建 | 各成员可正常 push/pull |
| 服务端项目初始化（FastAPI + 目录结构） | 后端 | `server/` 骨架 | `python run.py` 启动成功 |
| 客户端项目初始化（Vue3 + Vite + Element Plus） | 前端 | `client/` 骨架 | `npm run dev` 启动成功 |
| Excel 转 SQLite 数据导入 + SpatiaLite 初始化 | 后端 | `data/lbs.db` | 2356条数据正确导入、空间索引创建成功 |
| 安装依赖包并锁定版本 | 全组 | `requirements.txt`、`package.json` | 其他成员可复现环境 |

#### 第二阶段：核心 API 实现（5天，5月10日 - 5月14日）

**目标**：所有 API 端点实现完毕，可通过 Swagger UI 测试

| 任务 | 说明 | 验证标准 |
|------|------|----------|
| 认证模块（注册、登录、JWT签发验证） | `/auth/*` 全部端点 | 登录获取 Token，Token 可正常解析 |
| POI 查询模块（列表、详情、搜索） | `/pois` GET 系列 | 支持全部筛选参数组合 |
| POI 空间查询模块（nearby、bbox） | 空间搜索端点 | 框选/半径返回正确范围内的 POI |
| POI 管理模块（增删改） | 维护人员 CRUD | 增删改操作正确，权限控制生效 |
| 统计模块 | `/stats/*` 全部端点 | 统计数据与实际数据一致 |
| 中间件（CORS、JWT认证、限流） | 全局中间件 | 未认证请求被拒绝，超限请求返回429 |
| 统一错误响应格式 | 全部端点 | 所有错误返回标准 JSON 格式 |

#### 第三阶段：客户端核心页面开发（5天，5月15日 - 5月19日）

**目标**：客户端全部页面完成，与 API 联调通过

| 任务 | 说明 | 验证标准 |
|------|------|----------|
| 布局框架（Header、Sidebar、Footer） | 全局布局 | 页面导航流畅 |
| 登录/注册页面 | 认证流程 | 登录后正确存储 Token |
| 首页仪表盘（统计图表） | ECharts 图表展示 | 数据与服务端统计 API 一致 |
| **地图浏览页面（核心）** | 高德地图集成、POI标记、聚合 | POI 点正确显示在地图上 |
| **空间搜索交互（框选、半径搜索）** | 地图交互式选择 | 绘制矩形/圆形后正确搜索 |
| POI 信息窗与详情页 | 点击标记弹出信息 | 信息完整显示（含扩展媒体） |
| POI 列表与筛选面板 | 侧边栏列表+筛选 | 筛选后列表和地图同步更新 |
| **设备位置定位** | 浏览器 Geolocation API | 获得授权后显示蓝色定位点 |
| POI 管理页面 | 维护人员增删改操作 | CRUD 操作后数据实时更新 |
| 个人中心页面 | 个人信息、API Key 管理 | 信息修改生效 |
| Axios 拦截器（Token、错误处理） | HTTP 层 | 401 自动跳转登录页 |

#### 第四阶段：多媒体整合与 UI/UX 优化（4天，5月20日 - 5月23日）

**目标**：多媒体数据到位，UI 视觉效果达到高分标准

| 任务 | 说明 | 验证标准 |
|------|------|----------|
| 文保单位图片资源收集 | 为重点文保单位收集/抓取图片 | 至少覆盖 100+ 重点文保单位 |
| 语音导览音频制作 | 录制或 TTS 合成文保单位介绍音频 | 至少覆盖 30+ 重点文保单位 |
| 官网/百科链接收集 | 为文保单位添加官网或百科链接 | 至少覆盖 200+ 文保单位 |
| 多媒体数据导入数据库 | 通过 `poi_media` 表管理 | 多媒体数据可通过 API 查询 |
| 图片轮播组件 | 详情页图片查看 | 多图时支持轮播/缩略图 |
| 音频播放器组件 | 详情页音频播放 | 播放/暂停/进度条正常 |
| 视频播放支持 | 嵌入视频链接 | 视频可正常播放 |
| 全局色彩主题定制 | 古风/国风配色方案 | 与"文保单位"主题协调 |
| 响应式布局适配 | 不同屏幕尺寸 | 桌面端和移动端均正常显示 |
| 加载骨架屏 | 数据加载时显示 | 骨架屏与内容布局一致 |
| 过渡动画 | 页面切换、组件展示 | 动画流畅自然 |

#### 第五阶段：测试、文档与提交（4天，5月24日 - 5月29日）

**目标**：全部测试通过，文档完备，代码提交至 Gitee

| 任务 | 说明 | 验证标准 |
|------|------|----------|
| 服务端单元测试 | `pytest` 覆盖核心 API | 覆盖率 >= 80% |
| API 集成测试 | 完整请求-响应流程测试 | 核心场景测试通过 |
| 客户端功能测试 | 手动功能遍历 | 无阻断性 Bug |
| 跨域联调测试 | 前后端分离部署联调 | 所有功能正常 |
| 课程设计报告撰写 | 按栏目格式要求填写 | 内容完整、格式规范 |
| README 撰写（含成员分工） | 运行指南、分工说明 | 他人可依 README 运行项目 |
| API 文档检查 | Swagger UI 文档完整性 | 所有端点描述清晰 |
| 代码最终 Review 与合并 | 分支合并至 master | 代码无冲突 |
| 成果演示准备 | 演示流程排练 | 演示流畅、时间可控 |

### 8.2 里程碑（Milestones）

```
M0 --- 5月9日  |  [OK] 环境搭建完成
               |  - 前后端项目可独立运行
               |  - 数据导入数据库成功
               |
M1 --- 5月14日 |  [OK] 全部 API 实现完毕
               |  - Swagger UI 可测试所有端点
               |  - 认证 + 权限 + 限流全部生效
               |
M2 --- 5月19日 |  [OK] 客户端所有页面完成
               |  - 地图浏览 + 空间搜索 + CRUD 联调通过
               |  - 前后端完整功能链路打通
               |
M3 --- 5月23日 |  [OK] 多媒体 + UI 优化完成
               |  - 图片/音频/视频整合到位
               |  - 视觉效果达到演示标准
               |
M4 --- 5月29日 |  [OK] 测试 + 文档 + 提交完成
               |  - 测试全部通过
               |  - 报告 + README 撰写完毕
               |  - 代码 Push 至 Gitee master
               |
TGT -- 5月30日 |  [TGT] 18:00 截止提交 + 现场演示
```

### 8.3 团队分工建议（3人）

| 角色 | 主要职责 | 任务量占比 |
|:----:|----------|:----------:|
| **组长（全栈协调）** | 服务端架构设计、认证模块、中间件、数据库设计、代码 Review、Gitee 管理、课程报告整合 | 35% |
| **后端开发** | POI CRUD API、空间查询模块、统计模块、数据导入脚本、单元测试、API 文档 | 35% |
| **前端开发** | Vue 项目架构、地图集成、所有页面开发、多媒体整合、UI/UX 优化、客户端测试 | 30% |

---

## 九、质量保证与测试策略

### 9.1 测试金字塔

```
         /\
        /  \          E2E 测试（手动 + 可选的自动化）
       /    \         - 完整用户流程
      /------\        - 现场演示场景覆盖
     /        \
    / 集成测试  \      集成测试（pytest + TestClient）
   /------------\     - API 端点完整请求-响应
  /              \    - 认证流程 + CRUD 流程
 /   单元测试      \   - 空间查询正确性
/------------------\ 单元测试（pytest）
                      - Service 层业务逻辑
                      - Utility 函数
                      - 空间计算函数
```

### 9.2 服务端测试覆盖范围

| 测试对象 | 测试内容 | 目标覆盖率 |
|----------|----------|:----------:|
| `utils/security.py` | 密码哈希/验证、JWT 生成/解析 | 100% |
| `utils/spatial.py` | Haversine 距离计算、坐标转换、框选判断 | 100% |
| `utils/response.py` | 统一响应格式（成功/错误） | 100% |
| `services/auth_service.py` | 注册、登录、Token验证、API Key生成 | >= 90% |
| `services/poi_service.py` | 列表查询、详情、CRUD 逻辑 | >= 90% |
| `services/spatial_service.py` | 中心半径查询、矩形框选查询 | >= 90% |
| `services/stats_service.py` | 各统计查询方法 | >= 85% |
| `repositories/poi_repository.py` | SQL 查询正确性 | >= 80% |

### 9.3 集成测试核心场景

```text
核心集成测试场景:
  1. 用户注册 -> 登录 -> 获取 Token -> 访问受保护端点
  2. 无 Token 访问受保护端点 -> 返回 401
  3. 公众用户调用 POST /pois -> 返回 403
  4. 维护人员新增 POI -> 查询确认存在 -> 更新 -> 删除 -> 确认删除
  5. 按名称搜索 -> 验证返回结果包含关键字的 POI
  6. 按省份筛选 -> 验证所有结果的 province 字段匹配
  7. 中心半径搜索 -> 验证所有结果在指定半径内（Haversine复算）
  8. 矩形框选搜索 -> 验证所有结果的坐标在矩形内
  9. 分页查询 -> 验证 page_size 和 total 字段正确
  10. API 限流 -> 连续发送超过限制的请求 -> 返回 429
  11. 统计接口 -> 验证统计数据与 POI 总数一致
```

### 9.4 客户端测试策略

| 测试类型 | 方法 | 覆盖内容 |
|----------|------|----------|
| **组件渲染测试** | 手动 | 关键组件是否正确渲染 |
| **功能测试** | 手动遍历测试清单 | 所有页面功能、表单提交、地图交互 |
| **API 联调测试** | 手动 + 浏览器 DevTools | 所有 API 调用请求和响应正确 |
| **地图交互测试** | 手动 | 标记显示、聚合、信息窗、空间搜索工具 |
| **边界测试** | 手动 | 无网络、API 报错、空数据等场景 |
| **响应式测试** | 手动（浏览器缩放/F12设备模拟） | 桌面端、平板、手机三种视图 |
| **浏览器兼容性** | 手动 | Chrome 最新版（主要目标） |

### 9.5 测试工具汇总

| 工具 | 用途 |
|------|------|
| **pytest + pytest-cov** | Python 单元测试 + 覆盖率报告 |
| **FastAPI TestClient** | API 集成测试（无需启动服务器） |
| **httpx** | 异步 HTTP 客户端（测试用） |
| **pytest-asyncio** | 异步测试支持 |
| **Swagger UI (/docs)** | 手动 API 调试和演示 |
| **Chrome DevTools** | 网络请求检查、性能分析 |
| **Postman / Insomnia** | API 手动测试（可选） |

### 9.6 代码质量保障

| 措施 | 工具/方法 |
|------|----------|
| **代码风格检查** | Python: `ruff` (lint + format)；JavaScript: ESLint + Prettier |
| **类型校验** | Python: Pydantic 运行时校验 |
| **Git 提交规范** | Conventional Commits 格式：`feat:`、`fix:`、`docs:`、`test:` |
| **代码审查** | 合并至 master 前至少一人 Review |
| **分支策略** | 每人在自己的分支开发，功能完成后 PR 合并 |

---

## 十、多媒体数据整合方案

### 10.1 多媒体类型规划

| 媒体类型 | 数据来源 | 覆盖目标 | 展示方式 |
|----------|----------|:--------:|----------|
| **图片** | 百度百科/维基百科/文旅部官网的公开图片 | >= 100 个文保单位 | 详情页轮播、地图信息窗缩略图 |
| **音频** | 使用百度/讯飞 TTS 语音合成技术生成介绍音频 | >= 30 个文保单位 | 详情页音频播放器、背景语音导览 |
| **视频** | B站/YouTube 的公开纪录片/航拍视频（嵌入） | >= 10 个文保单位 | 详情页视频播放器 |
| **官网链接** | 各文保单位官方/权威介绍页面 | >= 200 个文保单位 | 详情页外链按钮、信息窗内链接 |
| **全景/街景** | 百度街景 / 高德全景链接（如有） | >= 50 个文保单位 | 详情页全景查看按钮 |
| **3D 模型** | Sketchfab 嵌入（如故宫、长城等） | >= 5 个标志性文保单位 | 详情页 3D 展示区域（可选加分项） |

### 10.2 多媒体数据管理流程

```
数据采集              存储/托管            数据库记录          客户端展示
-----------          -----------          -----------         -----------
- 爬取/下载     --->  - static/media/  --> poi_media 表   --> - 图片轮播
- TTS 合成            - 图床/CDN          记录 meta           - 音频播放器
- 链接收集            - 外部嵌入          (type,url,          - 视频嵌入
                                          title,desc)        - 链接跳转
```

### 10.3 UI/UX 设计原则

1. **色彩方案**：采用"古风国韵"配色——主色调选择**中国传统色谱**：
   - 朱砂红 `#C3272B`（文保单位标记色）
   - 琉璃黄 `#E8B74B`（高亮/强调色）
   - 青花蓝 `#2E4E8C`（主文字/标题色）
   - 辅以中性灰色调（背景/边框），营造"文物保护"的庄重感和历史厚重感

2. **地图视觉**：POI 标记按类别使用不同图标和颜色：
   - 古建筑=红色，古遗址=棕色，石刻=灰色，古墓葬=深绿，近现代=蓝色
   - 标记点为自定义 SVG 图标，区分度高

3. **信息层级**：首页仪表盘 → 地图总览 → 点击详情，信息由浅入深，符合用户认知流程

4. **交互反馈**：所有可点击元素均有视觉反馈（hover 状态、active 状态、过渡动画），加载状态有骨架屏占位

5. **响应式设计**：
   - 桌面端：左右分栏布局（地图 + 侧边栏）
   - 移动端：上下分栏布局（地图 + 底部面板）

6. **空状态处理**：搜索无结果、网络错误、数据为空等场景有友好的提示和引导

---

## 附录：技术依赖清单

### A. Python 依赖 (requirements.txt)

```
fastapi==0.111.*
uvicorn[standard]==0.30.*
pydantic==2.7.*
python-jose[cryptography]==3.3.*
passlib[bcrypt]==1.7.*
slowapi==0.1.*
shapely==2.0.*
geopy==2.4.*
pandas==2.2.*
openpyxl==3.1.*
pytest==8.2.*
pytest-cov==5.0.*
pytest-asyncio==0.23.*
httpx==0.27.*
ruff==0.4.*
```

### B. Node.js 依赖 (package.json)

```json
{
  "dependencies": {
    "vue": "^3.5",
    "vue-router": "^4.4",
    "pinia": "^2.2",
    "axios": "^1.7",
    "element-plus": "^2.8",
    "@element-plus/icons-vue": "^2.3",
    "echarts": "^5.5",
    "vue-echarts": "^7.0"
  },
  "devDependencies": {
    "@vitejs/plugin-vue": "^5.1",
    "vite": "^5.4",
    "tailwindcss": "^3.4",
    "autoprefixer": "^10.4",
    "postcss": "^8.4",
    "eslint": "^9.5",
    "prettier": "^3.3"
  }
}
```

---

> **文档版本**：v1.0
> **制定日期**：2026年5月8日
> **下次评审**：每个里程碑节点
> **Gitee 仓库**：https://gitee.com/rsgis/lbs-252602.git
        