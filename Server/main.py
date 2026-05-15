import math
from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from pymysql.cursors import DictCursor
from testdb import get_connection

app = FastAPI(title="全国文保单位 POI API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/v1/pois")
def list_pois(
    name: str = Query(None, description="POI名称模糊搜索"),
    province: str = Query(None, description="省份筛选"),
    category: str = Query(None, description="类别筛选"),
    batch: str = Query(None, description="批次筛选"),
    sw_lat: float = Query(None, description="矩形框西南纬度"),
    sw_lon: float = Query(None, description="矩形框西南经度"),
    ne_lat: float = Query(None, description="矩形框东北纬度"),
    ne_lon: float = Query(None, description="矩形框东北经度"),
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(100, ge=1, le=3000, description="每页数量"),
):
    conn = get_connection()
    cursor = conn.cursor()

    conditions = []
    params = []

    if name:
        conditions.append("name LIKE %s")
        params.append(f"%{name}%")
    if province:
        conditions.append("province LIKE %s")
        params.append(f"%{province}%")
    if category:
        conditions.append("category = %s")
        params.append(category)
    if batch:
        conditions.append("batch = %s")
        params.append(batch)

    if sw_lat is not None and sw_lon is not None and ne_lat is not None and ne_lon is not None:
        conditions.append(
            "longitude >= %s AND longitude <= %s AND latitude >= %s AND latitude <= %s"
        )
        params.extend([sw_lon, ne_lon, sw_lat, ne_lat])

    where = "WHERE " + " AND ".join(conditions) if conditions else ""

    cursor.execute(f"SELECT COUNT(*) AS cnt FROM pois {where}", params)
    total = cursor.fetchone()["cnt"]

    total_pages = math.ceil(total / page_size)
    offset = (page - 1) * page_size

    sql = f"""
        SELECT id, code, class_code, name, age, province, city, address,
               category, batch, remark, longitude, latitude, bd_longitude, bd_latitude
        FROM pois {where}
        ORDER BY id
        LIMIT %s OFFSET %s
    """
    cursor.execute(sql, params + [page_size, offset])
    rows = cursor.fetchall()

    items = []
    for r in rows:
        items.append({
            "id": r["id"],
            "code": r["code"],
            "class_code": r["class_code"],
            "name": r["name"],
            "age": r["age"],
            "province": r["province"],
            "city": r["city"],
            "address": r["address"],
            "category": r["category"],
            "batch": r["batch"],
            "remark": r["remark"],
            "longitude": r["longitude"],
            "latitude": r["latitude"],
            "bd_longitude": r["bd_longitude"],
            "bd_latitude": r["bd_latitude"],
        })

    cursor.close()
    conn.close()

    return {
        "code": 200,
        "message": "success",
        "data": {
            "total": total,
            "page": page,
            "page_size": page_size,
            "total_pages": total_pages,
            "items": items,
        },
    }


@app.get("/api/v1/stats/overview")
def stats_overview():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT
            COUNT(*) AS total,
            (SELECT COUNT(*) FROM pois WHERE category='古建筑') AS cnt_architecture,
            (SELECT COUNT(*) FROM pois WHERE category='古遗址') AS cnt_ruins,
            (SELECT COUNT(*) FROM pois WHERE category='古墓葬') AS cnt_tombs,
            (SELECT COUNT(*) FROM pois WHERE category='石窟寺及石刻') AS cnt_grottoes,
            (SELECT COUNT(*) FROM pois WHERE category='近现代重要史迹及代表性建筑') AS cnt_modern
        FROM pois
    """)
    row = cursor.fetchone()
    cursor.close()
    conn.close()
    return {"code": 200, "message": "success", "data": {
        "total": row["total"],
        "categories": {
            "古建筑": row["cnt_architecture"],
            "古遗址": row["cnt_ruins"],
            "古墓葬": row["cnt_tombs"],
            "石窟寺及石刻": row["cnt_grottoes"],
            "近现代": row["cnt_modern"],
        }
    }}


@app.get("/api/v1/health")
def health():
    return {"status": "ok"}
