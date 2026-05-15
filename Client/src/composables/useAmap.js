import { ref } from 'vue'

const isReady = ref(false)

function waitForAMap() {
  return new Promise((resolve, reject) => {
    if (window.AMap) { isReady.value = true; resolve(window.AMap); return }
    const maxWait = 15000; const start = Date.now()
    const timer = setInterval(() => {
      if (window.AMap) { clearInterval(timer); isReady.value = true; resolve(window.AMap) }
      else if (Date.now() - start > maxWait) { clearInterval(timer); reject(new Error('高德地图加载超时')) }
    }, 200)
  })
}

function makeInfoContent(poi) {
  let h = `<div style="padding:4px;max-width:260px;"><b style="font-size:15px;">${poi.name}</b>`
  if (poi.age) h += `<br><span style="color:#888">年代：</span>${poi.age}`
  if (poi.category) h += `<br><span style="color:#888">类别：</span>${poi.category}`
  if (poi.batch) h += `<br><span style="color:#888">批次：</span>${poi.batch}`
  if (poi.address) h += `<br><span style="color:#888;font-size:12px;">${poi.address}</span>`
  h += '</div>'; return h
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
    infoWindow = new window.AMap.InfoWindow({ offset: new window.AMap.Pixel(0, -30) })
    return mapInstance
  }

  function renderPois(pois) {
    clearMarkers()
    if (!pois || pois.length === 0) return 0

    allMarkers = []
    for (let i = 0; i < pois.length; i++) {
      const poi = pois[i]
      const m = new window.AMap.Marker({ position: [poi.longitude, poi.latitude], title: poi.name })
      m.on('click', () => {
        infoWindow.setContent(makeInfoContent(poi))
        infoWindow.open(mapInstance, m.getPosition())
      })
      allMarkers.push(m)
    }

    mapInstance.add(allMarkers)
    mapInstance.setFitView(null, false, [60, 60, 60, 60])
    return allMarkers.length
  }

  function clearMarkers() {
    if (mapInstance) mapInstance.clearMap()
    if (infoWindow) infoWindow.close()
    allMarkers = []
  }

  function destroyMap() {
    clearMarkers()
    if (mapInstance) { mapInstance.destroy(); mapInstance = null }
  }

  function getMap() { return mapInstance }

  return { isReady, loadScript: waitForAMap, initMap, renderPois, clearMarkers, destroyMap, getMap }
}
