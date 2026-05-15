import { ref } from 'vue'

const CATEGORY_COLORS = {
  '古建筑': '#E74C3C',
  '古遗址': '#A0522D',
  '古墓葬': '#27AE60',
  '石窟寺及石刻': '#7F8C8D',
  '近现代重要史迹及代表性建筑': '#2980B9',
}
const FALLBACK_COLOR = '#999999'

function dotHtml(color) {
  return `<div style="
    width:10px;height:10px;border-radius:50%;
    background:${color};border:2px solid #fff;
    box-shadow:0 1px 4px rgba(0,0,0,0.4);
  "></div>`
}

function waitForAMap() {
  return new Promise((resolve, reject) => {
    if (window.AMap) return resolve(window.AMap)
    const start = Date.now()
    const timer = setInterval(() => {
      if (window.AMap) { clearInterval(timer); resolve(window.AMap) }
      else if (Date.now() - start > 15000) { clearInterval(timer); reject(new Error('地图加载超时')) }
    }, 200)
  })
}

function proxyImageUrl(rawUrl) {
  return `http://localhost:8000/api/v1/proxy/image?url=${encodeURIComponent(rawUrl)}`
}

function infoHtml(poi) {
  const parts = []
  
  if (poi.media && poi.media.length > 0) {
    const img = poi.media.find(m => m.media_type === 'image')
    if (img) {
      parts.push(
        `<img src="${proxyImageUrl(img.media_url)}" style="width:100%;max-height:180px;object-fit:cover;border-radius:4px 4px 0 0;margin-bottom:8px;display:block;" alt="${poi.name}" onerror="this.style.display='none'"/>`
      )
    }
  }

  parts.push(`<div style="padding:6px 10px;max-width:280px;font-size:13px;">`)
  parts.push(`<b style="font-size:15px;color:#1a1a2e;">${poi.name}</b>`)
  if (poi.age) parts.push(`<br><span style="color:#999;">年代：</span>${poi.age}`)
  if (poi.category) parts.push(`<br><span style="color:#999;">类别：</span>${poi.category}`)
  if (poi.batch) parts.push(`<br><span style="color:#999;">批次：</span>${poi.batch}`)
  if (poi.address) parts.push(`<br><span style="color:#999;font-size:11px;">${poi.address}</span>`)
  parts.push(`</div>`)

  return parts.join('')
}

export function useAmap() {
  let mapInstance = null
  let infoWindow = null
  let allMarkers = []

  function initMap(container, options = {}) {
    if (!window.AMap) return null
    mapInstance = new window.AMap.Map(container, {
      center: [104.066, 35.576],
      zoom: 4,
      mapStyle: 'amap://styles/light',
      ...options,
    })
    mapInstance.addControl(new window.AMap.Scale())
    infoWindow = new window.AMap.InfoWindow({ offset: new window.AMap.Pixel(0, -20) })
    return mapInstance
  }

  function renderPois(pois) {
    clearMarkers()
    if (!pois || pois.length === 0) return 0

    allMarkers = pois.map((poi) => {
      const color = CATEGORY_COLORS[poi.category] || FALLBACK_COLOR
      const m = new window.AMap.Marker({
        position: [poi.longitude, poi.latitude],
        content: dotHtml(color),
        offset: new window.AMap.Pixel(-5, -5),
        zIndex: 100,
      })
      m.on('click', () => {
        infoWindow.setContent(infoHtml(poi))
        infoWindow.open(mapInstance, m.getPosition())
      })
      return m
    })

    mapInstance.add(allMarkers)
    mapInstance.setFitView(null, false, [60, 60, 60, 60])
    return allMarkers.length
  }

  function clearMarkers() {
    if (infoWindow) infoWindow.close()
    if (mapInstance) mapInstance.clearMap()
    allMarkers = []
  }

  function destroyMap() {
    clearMarkers()
    if (mapInstance) { mapInstance.destroy(); mapInstance = null }
  }

  function getMap() { return mapInstance }

  return { loadScript: waitForAMap, initMap, renderPois, clearMarkers, destroyMap, getMap }
}
