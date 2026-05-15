<template>
  <div class="app-layout">
    <header class="app-header">
      <div class="header-left">
        <span class="logo">🏛️</span>
        <h1 class="title">全国文保单位 POI 地图客户端</h1>
      </div>
      <div class="header-right">
        <el-button type="primary" size="small">登录</el-button>
        <el-button size="small">注册</el-button>
      </div>
    </header>

    <div class="app-body">
      <aside class="app-sidebar">
        <div class="sidebar-section">
          <h3>图例</h3>
          <div class="legend-item" v-for="item in legendItems" :key="item.label">
            <span class="legend-dot" :style="{ background: item.color }"></span>
            {{ item.label }}
          </div>
        </div>
      </aside>

      <main class="app-main">
        <div id="amap-container" ref="mapContainer"></div>
        <div v-if="mapLoading" class="map-overlay">
          <div class="overlay-box">
            <el-icon class="is-loading" :size="32"><Loading /></el-icon>
            <p style="margin-top:12px;color:#333;">正在加载高德地图...</p>
          </div>
        </div>
        <div v-if="mapError" class="map-overlay">
          <el-result icon="error" :title="mapError" sub-title="请确认高德地图 Key 有效且网络正常"></el-result>
        </div>
        <div v-if="loadingData" class="map-overlay" style="pointer-events:none;background:rgba(255,255,255,0.5);">
          <div class="overlay-box">
            <el-icon class="is-loading" :size="24"><Loading /></el-icon>
            <p style="margin-top:8px;color:#666;font-size:13px;">正在加载 POI 数据...</p>
          </div>
        </div>
        <div v-if="dataError" class="map-overlay">
          <el-result icon="error" title="数据加载失败" :sub-title="dataError"></el-result>
        </div>
        <div class="map-toolbar">
          <el-button circle @click="handleLocate" title="定位到当前位置">
            <el-icon><Aim /></el-icon>
          </el-button>
        </div>
        <div class="map-info">
          中心: {{ mapCenter.map(v => v.toFixed(4)).join(', ') }} | 缩放: {{ mapZoom }}
          <span v-if="loadingData"> | 正在加载数据...</span>
          <span v-else-if="displayedPoiCount"> | 已加载: {{ displayedPoiCount }} / {{ totalPoiCount }} 个文保单位</span>
          <span v-else> | 未加载到数据</span>
        </div>
      </main>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { Loading, Aim } from '@element-plus/icons-vue'
import { useAmap } from './composables/useAmap'
import apiClient from './api/index.js'

const mapCenter = ref([104.066, 35.576])
const mapZoom = ref(4)
const loadingData = ref(false)
const totalPoiCount = ref(0)
const displayedPoiCount = ref(0)
const dataError = ref('')

const legendItems = [
  { label: '古建筑', color: '#E74C3C' },
  { label: '古遗址', color: '#A0522D' },
  { label: '古墓葬', color: '#27AE60' },
  { label: '石窟寺及石刻', color: '#7F8C8D' },
  { label: '近现代建筑', color: '#2980B9' },
]

const mapContainer = ref(null)
const mapLoading = ref(true)
const mapError = ref('')
const { loadScript, initMap, renderPois, clearMarkers, destroyMap, getMap } = useAmap()

let mapInstance = null

onMounted(async () => {
  try {
    await loadScript()
    mapLoading.value = false

    mapInstance = initMap(mapContainer.value, {
      center: mapCenter.value,
      zoom: mapZoom.value
    })

    mapInstance.on('moveend', () => {
      const center = mapInstance.getCenter()
      mapCenter.value = [center.lng, center.lat]
      mapZoom.value = mapInstance.getZoom()
    })

    await loadAllPois()
  } catch (err) {
    mapLoading.value = false
    mapError.value = err.message || '地图加载失败'
  }
})

async function loadAllPois() {
  loadingData.value = true
  dataError.value = ''
  try {
    const res = await apiClient.get('/pois', { params: { page_size: 3000, page: 1 } })
    const data = res.data
    totalPoiCount.value = data.total
    displayedPoiCount.value = renderPois(data.items)
  } catch (err) {
    console.warn('POI数据加载失败:', err.message)
    dataError.value = '后端服务未启动，请先运行 python run.py'
  } finally {
    loadingData.value = false
  }
}

onUnmounted(() => {
  destroyMap()
})

function handleLocate() {
  const map = getMap()
  if (!map) return
  if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(
      (pos) => {
        const { longitude, latitude } = pos.coords
        map.setCenter([longitude, latitude])
        map.setZoom(13)
      },
      () => {
        console.warn('定位失败')
      }
    )
  }
}
</script>

<style scoped>
.app-layout {
  display: flex;
  flex-direction: column;
  height: 100vh;
}

.app-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 20px;
  height: 56px;
  background: #1a1a2e;
  color: #fff;
  flex-shrink: 0;
  z-index: 100;
}

.header-left {
  display: flex;
  align-items: center;
  gap: 10px;
}

.logo {
  font-size: 24px;
}

.title {
  font-size: 18px;
  font-weight: 600;
  letter-spacing: 1px;
}

.app-body {
  display: flex;
  flex: 1;
  overflow: hidden;
}

.app-sidebar {
  width: 125px;
  background: #f8f9fa;
  border-right: 1px solid #e8e8e8;
  overflow-y: auto;
  flex-shrink: 0;
}

.sidebar-section {
  padding: 14px;
  border-bottom: 1px solid #e8e8e8;
}

.sidebar-section h3 {
  font-size: 13px;
  font-weight: 600;
  color: #333;
  margin-bottom: 10px;
}

.legend-item {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 12px;
  color: #555;
  margin-bottom: 8px;
}

.legend-dot {
  width: 12px;
  height: 12px;
  border-radius: 50%;
  flex-shrink: 0;
  border: 2px solid #fff;
  box-shadow: 0 1px 3px rgba(0,0,0,0.3);
}

.app-main {
  flex: 1;
  position: relative;
  overflow: hidden;
}

#amap-container {
  width: 100%;
  height: 100%;
}

.map-overlay {
  position: absolute;
  inset: 0;
  z-index: 50;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(255,255,255,0.85);
}

.overlay-box {
  text-align: center;
}

.map-toolbar {
  position: absolute;
  top: 16px;
  right: 16px;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.map-toolbar .el-button {
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
}

.map-info {
  position: absolute;
  bottom: 8px;
  left: 8px;
  background: rgba(255, 255, 255, 0.9);
  padding: 4px 12px;
  border-radius: 4px;
  font-size: 12px;
  color: #666;
  box-shadow: 0 1px 4px rgba(0, 0, 0, 0.1);
}
</style>
