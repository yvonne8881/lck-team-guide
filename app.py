import os
import random
import psycopg2

from flask import Flask, abort, jsonify, render_template, request, url_for

def get_db_connection():
    database_url = os.getenv("DATABASE_URL") or os.getenv("DB_URL")

    if not database_url:
        raise RuntimeError("尚未設定 DATABASE_URL")

    return psycopg2.connect(
        database_url,
        sslmode="require",
        connect_timeout=10,
    )

from flask import Flask, abort, jsonify, render_template, request, url_for

app = Flask(__name__)


def roster(*names):
    """依選手名稱產生對應的 .webp 圖片檔名。"""
    return [
        {"name": name, "photo": f"{name.lower()}.webp"}
        for name in names
    ]


PLAYER_LANES = {
    "doran": "top", "kiin": "top", "zeus": "top", "siwoo": "top",
    "perfect": "top", "frog": "top", "kingen": "top", "clear": "top",
    "dudu": "top", "casting": "top",
    "oner": "jungle", "canyon": "jungle", "kanavi": "jungle",
    "lucid": "jungle", "cuzz": "jungle", "willer": "jungle",
    "sponge": "jungle", "raptor": "jungle", "pyosik": "jungle",
    "gideon": "jungle",
    "faker": "mid", "chovy": "mid", "zeka": "mid",
    "showmaker": "mid", "bdd": "mid", "ucal": "mid", "scout": "mid",
    "vicla": "mid", "clozer": "mid", "roamer": "mid",
    "peyz": "bot", "ruler": "bot", "gumayusi": "bot", "smash": "bot",
    "jiwoo": "bot", "aiming": "bot", "diable": "bot", "taeyoon": "bot",
    "deokdam": "bot", "teddy": "bot",
    "keria": "support", "duro": "support", "delight": "support",
    "career": "support", "effort": "support", "andil": "support",
    "lehends": "support", "kellin": "support", "life": "support",
    "namgung": "support",
}

LANE_FILES = {
    "top": "images/lane/top.jpg",
    "jungle": "images/lane/jug.jpeg",
    "mid": "images/lane/mid.jpg",
    "bot": "images/lane/bot.jpeg",
    "support": "images/lane/sup.jpg",
}

LANE_LABELS = {
    "top": "上路",
    "jungle": "打野",
    "mid": "中路",
    "bot": "下路",
    "support": "輔助",
}


teams = [
    {
        "slug": "t1",
        "name": "T1",
        "logo": "t1.webp",
        "founded": "2013（LoL 分部；SK Telecom 電競隊母體成立於 2004）",
        "name_history": "SK Telecom T1 → T1（2019）",
        "intro": "英雄聯盟最具代表性的世界冠軍隊伍之一，以多次世界賽奪冠建立知名度。",
        "awards": [
            "世界賽冠軍：2013、2015、2016、2023、2024、2025",
            "MSI 冠軍：2016、2017",
        ],
        "players": roster("Doran", "Oner", "Faker", "Peyz", "Keria"),
    },
    {
        "slug": "gen-g",
        "name": "Gen.G",
        "logo": "geng.png",
        "founded": "2013（Samsung Galaxy LoL 隊伍沿革；Gen.G 品牌始於 2018）",
        "name_history": "Samsung Galaxy → KSV Esports → Gen.G（2018）",
        "intro": "近年 LCK 的長期強隊，曾連續奪下國內賽與 MSI 冠軍。",
        "awards": [
            "世界賽冠軍（隊伍沿革）：2014（Samsung White）、2017（Samsung Galaxy）",
            "LCK 冠軍：2022 夏、2023 春／夏、2024 春、2025、2026",
            "MSI 冠軍：2024、2025",
        ],
        "players": roster("Kiin", "Canyon", "Chovy", "Ruler", "Duro"),
    },
    {
        "slug": "hle",
        "name": "HLE",
        "logo": "hle.svg",
        "founded": "2018（成立 HLE 並承接 ROX Tigers）",
        "name_history": "ROX Tigers → Hanwha Life Esports（2018）",
        "intro": "近年成績大幅提升，從 LCK 冠軍隊伍進一步拿下國際賽冠軍。",
        "awards": [
            "LCK 夏季賽冠軍：2016（ROX Tigers）、2024",
            "LCK Cup 冠軍：2025",
            "First Stand 冠軍：2025",
            "MSI 冠軍：2026",
        ],
        "players": roster("Zeus", "Kanavi", "Zeka", "Gumayusi", "Delight"),
    },
    {
        "slug": "dplus-kia",
        "name": "Dplus KIA",
        "logo": "dplus_kia.webp",
        "founded": "2017",
        "name_history": "DAMWON Gaming → DWG KIA（2021）→ Dplus KIA（2023）",
        "intro": "從新興隊伍成長為世界冠軍，也曾在 LCK 建立連續奪冠的高峰。",
        "awards": [
            "世界賽冠軍：2020",
            "LCK 冠軍：2020 夏、2021 春／夏",
            "Esports World Cup 冠軍：2026",
        ],
        "players": roster("Siwoo", "Lucid", "ShowMaker", "Smash", "Career"),
    },
    {
        "slug": "kt",
        "name": "KT",
        "logo": "kt.webp",
        "founded": "2012（LoL 分部）",
        "name_history": "KT Rolster Arrows／Bullets → KT Rolster（2014 合併）",
        "intro": "歷史悠久的隊伍，曾奪下 LCK 冠軍，並在 2025 年打進世界賽決賽。",
        "awards": [
            "Champions 夏季賽冠軍：2014（KT Rolster Arrows）",
            "LCK 夏季賽冠軍：2018",
            "KeSPA Cup 冠軍：2017",
            "世界賽亞軍：2025",
        ],
        "players": roster("PerfecT", "Cuzz", "Bdd", "Jiwoo", "Effort"),
    },
    {
        "slug": "krx",
        "name": "KRX",
        "logo": "krx.png",
        "founded": "2012（隊伍沿革起點）",
        "name_history": (
            "Incredible Miracle → Longzhu Gaming → Kingzone DragonX "
            "→ DragonX／DRX → Kiwoom DRX（2026；代碼 KRX）"
        ),
        "intro": "隊史代表作是 2022 年世界賽冠軍；隊伍沿革中也曾多次奪下 LCK 冠軍。",
        "awards": [
            "LCK 冠軍：2017 夏、2018 春（前身隊伍）",
            "世界賽冠軍：2022（DRX）",
        ],
        "players": roster("Frog", "Willer", "Ucal", "Aiming", "Andil"),
    },
    {
        "slug": "ns",
        "name": "NS",
        "logo": "ns.webp",
        "founded": "2019（前身 Team Dynamics）",
        "name_history": "Team Dynamics → Nongshim RedForce（2020）",
        "intro": "重視選手培育的隊伍，隊史在次級聯賽累積多次冠軍。",
        "awards": [
            "Challengers Korea 冠軍：2019 夏",
            "LCK Challengers 冠軍：2020 夏",
            "LCK CL 冠軍：2023 夏",
        ],
        "players": roster("Kingen", "Sponge", "Scout", "Diable", "Lehends"),
    },
    {
        "slug": "bnk",
        "name": "BNK",
        "logo": "bnk.webp",
        "founded": "2018（SANDBOX Gaming 取得 Team BattleComics 的 LCK 席位）",
        "name_history": "SANDBOX Gaming → Liiv SANDBOX → FearX → BNK FEARX",
        "intro": "新興競爭者，已在跨賽區邀請賽奪冠，累積國際賽代表作。",
        "awards": [
            "League of Legends Asia Invitational 冠軍：2025",
            "LCK Cup 亞軍：2026",
        ],
        "players": roster("Clear", "Raptor", "VicLa", "Taeyoon", "Kellin"),
    },
    {
        "slug": "dns",
        "name": "DNS",
        "logo": "dns.webp",
        "founded": "2014（前身 Anarchy）",
        "name_history": (
            "Anarchy → Afreeca Freecs → Kwangdong Freecs "
            "→ DN Freecs → DN SOOPers"
        ),
        "intro": "有多年 LCK 隊史，沿革中的不同隊名時期曾在 KeSPA Cup 奪冠。",
        "awards": [
            "KeSPA Cup 冠軍：2019（Afreeca Freecs）、2026（DN SOOPers）",
        ],
        "players": roster("DuDu", "Pyosik", "Clozer", "deokdam", "Life"),
    },
    {
        "slug": "bro",
        "name": "BRO",
        "logo": "bro.png",
        "founded": "2018（以目前 LCK 隊伍沿革計）",
        "name_history": (
            "Kongdoo Monster → Brion Blade → hyFresh Blade → Fredit BRION "
            "→ BRION → OKSavingsBank BRION → Hanjin BRION"
        ),
        "intro": "曾被視為挑戰者隊伍，2024 年 KeSPA Cup 冠軍是隊伍的重要里程碑。",
        "awards": [
            "KeSPA Cup 冠軍：2024（OKSavingsBank BRION）",
        ],
        "players": roster("Casting", "GIDEON", "Roamer", "Teddy", "Namgung"),
    },
]


def get_database_url():
    """支援 Render 環境變數 DATABASE_URL，也相容 DB_URL。"""
    return os.environ.get("DATABASE_URL") or os.environ.get("DB_URL")


def get_db_connection():
    database_url = get_database_url()
    if not database_url:
        raise RuntimeError("找不到 DATABASE_URL，請設定 PostgreSQL 連線網址。")
    return psycopg2.connect(database_url, connect_timeout=10)


def ensure_history_table(cursor):
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS draw_history (
            id BIGSERIAL PRIMARY KEY,
            user_name TEXT NOT NULL,
            player_name TEXT NOT NULL,
            team_name TEXT NOT NULL,
            position TEXT NOT NULL,
            drawn_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
        )
    """)


def ensure_players_table(cursor):
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS players (
            id BIGSERIAL PRIMARY KEY,
            team_slug TEXT NOT NULL,
            team_name TEXT NOT NULL,
            player_name TEXT NOT NULL,
            position TEXT NOT NULL,
            photo TEXT NOT NULL,
            search_vector TSVECTOR GENERATED ALWAYS AS (
                setweight(
                    to_tsvector(
                        'simple'::regconfig,
                        COALESCE(player_name, '')
                    ),
                    'A'
                )
                ||
                setweight(
                    to_tsvector(
                        'simple'::regconfig,
                        COALESCE(team_name, '')
                    ),
                    'B'
                )
                ||
                setweight(
                    to_tsvector(
                        'simple'::regconfig,
                        COALESCE(position, '')
                    ),
                    'C'
                )
            ) STORED,
            UNIQUE (team_slug, player_name)
        )
    """)
    cursor.execute("""
        CREATE INDEX IF NOT EXISTS players_search_vector_idx
        ON players USING GIN (search_vector)
    """)


def sync_players_to_database(cursor):
    """將 app.py 的名單同步進資料庫，重複執行會更新既有資料。"""
    for team in teams:
        for player in team["players"]:
            photo_name = player["photo"].rsplit(".", 1)[0].lower()
            position = PLAYER_LANES.get(photo_name)
            if not position:
                continue

            cursor.execute("""
                INSERT INTO players
                    (team_slug, team_name, player_name, position, photo)
                VALUES (%s, %s, %s, %s, %s)
                ON CONFLICT (team_slug, player_name)
                DO UPDATE SET
                    team_name = EXCLUDED.team_name,
                    position = EXCLUDED.position,
                    photo = EXCLUDED.photo
            """, (
                team["slug"],
                team["name"],
                player["name"],
                position,
                player["photo"],
            ))


def save_draw(user_name, player):
    connection = get_db_connection()
    try:
        with connection:
            with connection.cursor() as cursor:
                ensure_history_table(cursor)
                cursor.execute("""
                    INSERT INTO draw_history
                        (user_name, player_name, team_name, position)
                    VALUES (%s, %s, %s, %s)
                    RETURNING id, drawn_at
                """, (
                    user_name,
                    player["name"],
                    player["team"],
                    player["position_label"],
                ))
                row = cursor.fetchone()
                return {"id": row[0], "drawn_at": row[1].isoformat()}
    finally:
        connection.close()


def get_draw_candidates():
    candidates = []
    for team in teams:
        for player in team["players"]:
            photo_name = player["photo"].rsplit(".", 1)[0].lower()
            position = PLAYER_LANES.get(photo_name)
            if not position:
                continue

            candidates.append({
                "name": player["name"],
                "team": team["name"],
                "team_slug": team["slug"],
                "position": position,
                "position_label": LANE_LABELS[position],
                "photo_url": url_for(
                    "static",
                    filename=(
                        "images/players/"
                        + team["slug"]
                        + "/"
                        + player["photo"]
                    ),
                ),
                "lane_url": url_for(
                    "static",
                    filename=LANE_FILES[position],
                ),
            })
    return candidates


@app.route("/", methods=["GET", "POST"])
def draw_page():
    draw_candidates = get_draw_candidates()
    player_name = request.form.get("player_name", "").strip()
    drawn_player = None
    error = None

    if request.method == "POST":
        if not player_name:
            error = "請輸入你的名字。"
        elif not draw_candidates:
            error = "目前沒有可抽卡的選手資料。"
        else:
            drawn_player = random.choice(draw_candidates)
            try:
                save_draw(player_name, drawn_player)
            except (psycopg2.Error, RuntimeError):
                app.logger.exception("儲存抽卡紀錄失敗")
                drawn_player = None
                error = "資料庫連線失敗，請檢查 DATABASE_URL 設定。"

    card_back_url = url_for(
        "static",
        filename="images/gacha/card-back.png",
    )
    return render_template(
        "draw.html",
        drawn_player=drawn_player,
        card_back_url=card_back_url,
        player_name=player_name,
        error=error,
    )


@app.route("/api/draw", methods=["POST"])
def api_draw():
    """API 1：抽選手，並將抽卡結果寫入 PostgreSQL。"""
    data = request.get_json(silent=True) or {}
    user_name = (data.get("name") or data.get("player_name") or "").strip()
    if not user_name:
        return jsonify({
            "error": "請提供姓名，例如：{\"name\": \"Yvonne\"}"
        }), 400

    candidates = get_draw_candidates()
    if not candidates:
        return jsonify({"error": "目前沒有可抽卡的選手資料。"}), 503

    player = random.choice(candidates)
    try:
        saved_record = save_draw(user_name, player)
    except (psycopg2.Error, RuntimeError):
        app.logger.exception("API 抽卡紀錄寫入資料庫失敗")
        return jsonify({"error": "資料庫連線失敗，請檢查 DATABASE_URL。"}), 503

    return jsonify({
        "message": "抽卡成功",
        "user_name": user_name,
        "player": player,
        "record": saved_record,
    }), 201


@app.route("/api/history", methods=["GET"])
def api_history():
    """API 2：使用 SQL 查詢指定姓名的抽卡紀錄。"""
    user_name = (
        request.args.get("name") or request.args.get("user_name") or ""
    ).strip()
    if not user_name:
        return jsonify({
            "error": "請提供姓名，例如：/api/history?name=Yvonne"
        }), 400

    try:
        limit = int(request.args.get("limit", 20))
    except ValueError:
        return jsonify({"error": "limit 必須是數字。"}), 400
    limit = max(1, min(limit, 100))

    connection = None
    try:
        connection = get_db_connection()
        with connection:
            with connection.cursor() as cursor:
                ensure_history_table(cursor)
                cursor.execute("""
                    SELECT id, user_name, player_name, team_name, position, drawn_at
                    FROM draw_history
                    WHERE user_name = %s
                    ORDER BY drawn_at DESC
                    LIMIT %s
                """, (user_name, limit))
                rows = cursor.fetchall()
    except (psycopg2.Error, RuntimeError):
        app.logger.exception("查詢抽卡紀錄失敗")
        return jsonify({"error": "資料庫連線失敗，請檢查 DATABASE_URL。"}), 503
    finally:
        if connection is not None:
            connection.close()

    history = [
        {
            "id": row[0],
            "user_name": row[1],
            "player_name": row[2],
            "team_name": row[3],
            "position": row[4],
            "drawn_at": row[5].isoformat(),
        }
        for row in rows
    ]
    return jsonify({
        "user_name": user_name,
        "count": len(history),
        "history": history,
    })


@app.route("/api/players/search", methods=["GET"])
def api_player_search():
    """API 3：使用 PostgreSQL 全文搜尋選手、隊伍或位置。"""
    query = request.args.get("q", "").strip()
    if not query:
        return jsonify({
            "error": "請提供搜尋文字，例如：/api/players/search?q=faker"
        }), 400

    pattern = f"%{query}%"
    connection = None
    try:
        connection = get_db_connection()
        with connection:
            with connection.cursor() as cursor:
                ensure_players_table(cursor)
                sync_players_to_database(cursor)
                cursor.execute("""
                    SELECT
                        team_slug,
                        team_name,
                        player_name,
                        position,
                        photo,
                        ts_rank(
                            search_vector,
                            plainto_tsquery('simple', %s)
                        ) AS rank
                    FROM players
                    WHERE search_vector @@ plainto_tsquery('simple', %s)
                       OR player_name ILIKE %s
                       OR team_name ILIKE %s
                       OR position ILIKE %s
                    ORDER BY rank DESC, team_name, player_name
                    LIMIT 50
                """, (query, query, pattern, pattern, pattern))
                rows = cursor.fetchall()
    except (psycopg2.Error, RuntimeError):
        app.logger.exception("選手搜尋資料庫查詢失敗")
        return jsonify({"error": "資料庫連線失敗，請檢查 DATABASE_URL。"}), 503
    finally:
        if connection is not None:
            connection.close()

    results = []
    for row in rows:
        team_slug, team_name, player_name, position, photo, _rank = row
        results.append({
            "team": team_name,
            "team_slug": team_slug,
            "player": player_name,
            "position": position,
            "position_label": LANE_LABELS.get(position, position),
            "photo_url": url_for(
                "static",
                filename=f"images/players/{team_slug}/{photo}",
            ),
        })

    return jsonify({
        "query": query,
        "count": len(results),
        "results": results,
    })


@app.route("/teams")
def home():
    return render_template("index.html", teams=teams)


@app.route("/team/<slug>")
def team_detail(slug):
    original_team = next(
        (team for team in teams if team["slug"] == slug),
        None,
    )
    if original_team is None:
        abort(404)

    team = dict(original_team)
    team["players"] = []

    for player in original_team["players"]:
        player_copy = dict(player)
        photo_name = player_copy["photo"].rsplit(".", 1)[0].lower()
        position = PLAYER_LANES.get(photo_name)
        player_copy["position"] = position
        player_copy["position_label"] = LANE_LABELS.get(position, "")

        if position:
            player_copy["lane_url"] = url_for(
                "static",
                filename=LANE_FILES[position],
            )

        team["players"].append(player_copy)

    return render_template("team.html", team=team)


if __name__ == "__main__":
    app.run(debug=True, port=5001)
