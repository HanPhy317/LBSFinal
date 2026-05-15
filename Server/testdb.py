import pymysql
from pymysql.cursors import DictCursor

DB_CONFIG = {
    "host": "localhost",
    "port": 3306,
    "user": "root",
    "password": "root",
    "database": "lbsdb",
    "charset": "utf8mb4",
    "cursorclass": DictCursor,
}

BASE_TABLES_SQL = """
CREATE TABLE IF NOT EXISTS users (
    id           INT AUTO_INCREMENT PRIMARY KEY,
    username     VARCHAR(50)  NOT NULL UNIQUE,
    email        VARCHAR(120) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    role         VARCHAR(20)  NOT NULL DEFAULT 'public',
    apikey       VARCHAR(64)  UNIQUE,
    is_active    TINYINT(1)   NOT NULL DEFAULT 1,
    created_at   DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at   DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS pois (
    id           INT AUTO_INCREMENT PRIMARY KEY,
    code         INT,
    class_code   VARCHAR(20),
    name         VARCHAR(200) NOT NULL,
    age          VARCHAR(100),
    province     VARCHAR(50),
    city         VARCHAR(50),
    address      VARCHAR(500),
    category     VARCHAR(50),
    batch        VARCHAR(50),
    remark       TEXT,
    longitude    DOUBLE NOT NULL,
    latitude     DOUBLE NOT NULL,
    bd_longitude DOUBLE,
    bd_latitude  DOUBLE,
    geom         GEOMETRY NOT NULL SRID 4326,
    created_at   DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at   DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    SPATIAL INDEX(geom),
    INDEX idx_name(name),
    INDEX idx_category(category),
    INDEX idx_province(province),
    INDEX idx_lng_lat(longitude, latitude)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS poi_media (
    id           INT AUTO_INCREMENT PRIMARY KEY,
    poi_id       INT          NOT NULL,
    media_type   VARCHAR(20)  NOT NULL,
    media_url    VARCHAR(500) NOT NULL,
    title        VARCHAR(200),
    description  TEXT,
    sort_order   INT DEFAULT 0,
    created_at   DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (poi_id) REFERENCES pois(id) ON DELETE CASCADE,
    INDEX idx_poi_id(poi_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
"""


def get_connection():
    """获取数据库连接"""
    return pymysql.connect(**DB_CONFIG)


def get_cursor(conn=None):
    """获取游标，不传 conn 则自动创建并返回 (conn, cursor)"""
    if conn is None:
        conn = get_connection()
        return conn, conn.cursor()
    return conn.cursor()


def init_database():
    """初始化数据库：创建基础表"""
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            for stmt in BASE_TABLES_SQL.split(";"):
                stmt = stmt.strip()
                if stmt:
                    cursor.execute(stmt + ";")
        conn.commit()
        print("数据库表初始化成功")
        return True
    except Exception as e:
        conn.rollback()
        print(f"数据库初始化失败: {e}")
        return False
    finally:
        conn.close()


def test_connection():
    """测试数据库连接是否正常"""
    try:
        conn = get_connection()
        with conn.cursor() as cursor:
            cursor.execute("SELECT VERSION() AS version, DATABASE() AS db, NOW() AS time")
            result = cursor.fetchone()
        conn.close()
        print(f"MySQL 连接成功")
        print(f"  版本: {result['version']}")
        print(f"  数据库: {result['db']}")
        print(f"  服务器时间: {result['time']}")
        return True
    except pymysql.err.OperationalError as e:
        error_code = e.args[0] if e.args else ""
        if error_code == 2003:
            print(f"连接失败: 无法连接到 MySQL 服务器 ({DB_CONFIG['host']}:{DB_CONFIG['port']})")
            print("请检查 MySQL 服务是否已启动")
        elif error_code == 1045:
            print("连接失败: 用户名或密码错误")
        elif error_code == 1049:
            print(f"连接失败: 数据库 '{DB_CONFIG['database']}' 不存在，将尝试创建")
            return _create_database()
        else:
            print(f"连接失败 [{error_code}]: {e}")
        return False
    except Exception as e:
        print(f"连接失败: {e}")
        return False


def _create_database():
    """数据库不存在时，先创建数据库再重试"""
    config = DB_CONFIG.copy()
    db_name = config.pop("database")
    try:
        conn = pymysql.connect(**config)
        with conn.cursor() as cursor:
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS `{db_name}` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
        conn.close()
        print(f"数据库 '{db_name}' 创建成功，重新测试连接...")
        return test_connection()
    except Exception as e:
        print(f"创建数据库失败: {e}")
        return False


if __name__ == "__main__":
    print("=" * 50)
    print("MySQL 数据库连接测试")
    print(f"  主机: {DB_CONFIG['host']}:{DB_CONFIG['port']}")
    print(f"  用户: {DB_CONFIG['user']}")
    print(f"  数据库: {DB_CONFIG['database']}")
    print("=" * 50)

    if test_connection():
        init_database()
