import sys
import pandas as pd
import pymysql
from testdb import get_connection, DB_CONFIG

EXCEL_PATH = r"D:/pythoncode/LBSFinal/全国文保单位/全国文保单位.xlsx"


def import_pois():
    print("正在读取 Excel 文件...")
    df = pd.read_excel(EXCEL_PATH)
    total = len(df)
    print(f"共读取 {total} 条记录")

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) AS cnt FROM pois")
    existing = cursor.fetchone()["cnt"]
    if existing > 0:
        cursor.execute("DELETE FROM poi_media")
        cursor.execute("DELETE FROM pois")
        conn.commit()
        print(f"已清空旧数据 ({existing} 条)")

    inserted = 0
    batch_size = 500
    batch = []

    for _, row in df.iterrows():
        address = str(row.get("add", "")).strip() if pd.notna(row.get("add")) else ""
        province, city = _extract_province_city(address)

        record = (
            int(row["code"]) if pd.notna(row.get("code")) else None,
            str(row.get("classCode", "")).strip() if pd.notna(row.get("classCode")) else None,
            str(row["name"]).strip(),
            str(row.get("age", "")).strip() if pd.notna(row.get("age")) else None,
            province,
            city,
            address,
            str(row.get("type", "")).strip() if pd.notna(row.get("type")) else None,
            str(row.get("batch", "")).strip() if pd.notna(row.get("batch")) else None,
            str(row.get("remark", "")).strip() if pd.notna(row.get("remark")) else None,
            float(row["lon"]),
            float(row["lat"]),
            float(row["bd_lon"]) if pd.notna(row.get("bd_lon")) else None,
            float(row["bd_lat"]) if pd.notna(row.get("bd_lat")) else None,
        )
        batch.append(record)

        if len(batch) >= batch_size:
            _flush_batch(cursor, batch)
            inserted += len(batch)
            print(f"\r导入进度: {inserted}/{total} ({inserted * 100 // total}%)", end="")
            batch.clear()

    if batch:
        _flush_batch(cursor, batch)
        inserted += len(batch)
        print(f"\r导入进度: {inserted}/{total} (100%)")

    conn.commit()
    cursor.close()
    conn.close()
    print(f"\n导入完成! 共写入 {inserted} 条 POI 记录")


def _flush_batch(cursor, batch):
    sql = """
        INSERT INTO pois
            (code, class_code, name, age, province, city, address,
             category, batch, remark, longitude, latitude, bd_longitude, bd_latitude, geom)
        VALUES
            (%s, %s, %s, %s, %s, %s, %s,
             %s, %s, %s, %s, %s, %s, %s,
             ST_GeomFromText(%s, 4326))
    """
    values = []
    for r in batch:
        lon, lat = r[10], r[11]
        wkt = f"POINT({lat} {lon})"
        values.append(r[:14] + (wkt,))
    cursor.executemany(sql, values)


def _extract_province_city(address):
    province = ""
    city = ""
    rest = address
    if not address:
        return province, city

    provinces = [
        "北京市", "天津市", "上海市", "重庆市",
        "河北省", "山西省", "辽宁省", "吉林省", "黑龙江省",
        "江苏省", "浙江省", "安徽省", "福建省", "江西省", "山东省",
        "河南省", "湖北省", "湖南省", "广东省", "广西壮族自治区",
        "海南省", "四川省", "贵州省", "云南省", "西藏自治区",
        "陕西省", "甘肃省", "青海省", "宁夏回族自治区", "新疆维吾尔自治区",
        "内蒙古自治区", "香港特别行政区", "澳门特别行政区", "台湾省",
    ]
    for p in provinces:
        if p in address:
            province = p
            rest = address.replace(p, "").strip()
            break

    if not province:
        short = ["北京", "天津", "上海", "重庆", "河北", "山西", "辽宁", "吉林", "黑龙江",
                 "江苏", "浙江", "安徽", "福建", "江西", "山东", "河南", "湖北", "湖南",
                 "广东", "广西", "海南", "四川", "贵州", "云南", "西藏", "陕西", "甘肃",
                 "青海", "宁夏", "新疆", "内蒙古", "香港", "澳门", "台湾"]
        long_map = dict(zip(short, provinces))
        for s in short:
            if s in address:
                province = long_map[s]
                rest = address.replace(s, "").strip()
                break

    if province and "省" not in province and "自治区" not in province and "特别行政区" not in province and "市" not in province:
        province += "省"

    if "市" in rest:
        idx = rest.index("市")
        if idx < 6:
            city = rest[:idx + 1]

    return province, city


if __name__ == "__main__":
    print("=" * 50)
    print("全国文保单位数据导入")
    print(f"数据库: {DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['database']}")
    print("=" * 50)
    import_pois()
