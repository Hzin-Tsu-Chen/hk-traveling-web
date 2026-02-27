import os
import math
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import uvicorn

app = FastAPI()

# 設定靜態檔案服務
image_dir = "香港"
if os.path.exists(image_dir):
    app.mount("/images", StaticFiles(directory=image_dir), name="images")

# 設定模板目錄
templates = Jinja2Templates(directory="templates")

# 地點資料庫（含精確座標與類型標籤）
LOCATIONS = [
    {
        "id": 1,
        "image": "S__56188931_0.jpg",
        "name": "點心到 Dim Sum Here",
        "address": "佐敦廟街26-28號",
        "lat": 22.3049, "lng": 114.1694,
        "type": "food",
        "duration": 60,
        "desc": "地道佐敦點心名店，以港式點心聞名。",
    },
    {
        "id": 2,
        "image": "S__56188932_0.jpg",
        "name": "龍點心",
        "address": "尖沙咀海防道",
        "lat": 22.2988, "lng": 114.1720,
        "type": "food",
        "duration": 60,
        "desc": "尖沙咀人氣點心店。",
    },
    {
        "id": 3,
        "image": "S__56188933_0.jpg",
        "name": "蘭芳園 Lan Fong Yuen",
        "address": "中環結志街2號",
        "lat": 22.2814, "lng": 114.1545,
        "type": "food",
        "duration": 45,
        "desc": "發明絲襪奶茶的傳奇茶餐廳，中環必訪。",
    },
    {
        "id": 4,
        "image": "S__56188934_0.jpg",
        "name": "榕哥陳皮燒鵝",
        "address": "佐敦",
        "lat": 22.3062, "lng": 114.1710,
        "type": "food",
        "duration": 60,
        "desc": "以陳皮燒鵝聞名的佐敦特色食肆。",
    },
    {
        "id": 5,
        "image": "S__56188935_0.jpg",
        "name": "澳洲牛奶公司",
        "address": "佐敦白加士街47-49號",
        "lat": 22.3037, "lng": 114.1688,
        "type": "food",
        "duration": 45,
        "desc": "香港傳奇茶餐廳，炒蛋多士與燉蛋是招牌。",
    },
    {
        "id": 6,
        "image": "S__56188936_0.jpg",
        "name": "澳牛炒蛋",
        "address": "佐敦白加士街47-49號",
        "lat": 22.3037, "lng": 114.1688,
        "type": "food",
        "duration": 30,
        "desc": "澳洲牛奶公司招牌滑蛋套餐。",
    },
    {
        "id": 7,
        "image": "S__56188937_0.jpg",
        "name": "十三姨 Lady 13 Kitchen",
        "address": "佐敦白加士街120-122號",
        "lat": 22.3052, "lng": 114.1700,
        "type": "food",
        "duration": 60,
        "desc": "佐敦特色港式料理小館。",
    },
    {
        "id": 8,
        "image": "S__56188938_0.jpg",
        "name": "甘牌燒鵝 Kam's Roast Goose",
        "address": "灣仔軒尼詩道226號",
        "lat": 22.2777, "lng": 114.1733,
        "type": "food",
        "duration": 60,
        "desc": "米芝蓮推介燒鵝名店，皮脆肉嫩。",
    },
    {
        "id": 9,
        "image": "S__56188939_0.jpg",
        "name": "勝香園 Sing Heung Yuen",
        "address": "中環美輪街2號",
        "lat": 22.2835, "lng": 114.1554,
        "type": "food",
        "duration": 45,
        "desc": "中環隱世茶餐廳，番茄湯麵是傳奇。",
    },
    {
        "id": 10,
        "image": "S__56188940_0.jpg",
        "name": "勝香園番茄麵",
        "address": "中環美輪街2號",
        "lat": 22.2835, "lng": 114.1554,
        "type": "food",
        "duration": 30,
        "desc": "勝香園人氣招牌番茄湯底麵食。",
    },
    {
        "id": 11,
        "image": "S__56188942_0.jpg",
        "name": "德發牛丸粉麵",
        "address": "尖沙咀海防道390號",
        "lat": 22.3019, "lng": 114.1725,
        "type": "food",
        "duration": 45,
        "desc": "手打牛丸彈牙鮮美，尖沙咀平民美食。",
    },
    {
        "id": 12,
        "image": "S__56188943_0.jpg",
        "name": "瑞記咖啡 Shui Kee Coffee",
        "address": "上環皇后大道中2/F",
        "lat": 22.2862, "lng": 114.1515,
        "type": "food",
        "duration": 30,
        "desc": "上環百年老字號，西多士一絕。",
    },
    {
        "id": 13,
        "image": "S__56188944_0.jpg",
        "name": "蓮香樓 Lin Heung Lau",
        "address": "中環威靈頓街160號",
        "lat": 22.2830, "lng": 114.1531,
        "type": "food",
        "duration": 75,
        "desc": "百年老字號廣式茶樓，傳統推車點心。",
    },
    {
        "id": 14,
        "image": "S__56188948.jpg",
        "name": "Guilt Free Bakery",
        "address": "尖沙咀加拿分道49號",
        "lat": 22.2998, "lng": 114.1745,
        "type": "food",
        "duration": 30,
        "desc": "葡式蛋撻專門店，不甜不膩剛剛好。",
    },
    {
        "id": 15,
        "image": "S__56188953_0.jpg",
        "name": "嗇色園黃大仙祠",
        "address": "香港竹園竹園村二號",
        "lat": 22.3424, "lng": 114.1936,
        "type": "attraction",
        "duration": 90,
        "desc": "香港著名道觀，香火鼎盛，祈福求籤。",
    },
    {
        "id": 16,
        "image": "S__56188954_0.jpg",
        "name": "石板街 (砵典乍街)",
        "address": "中環砵典乍街",
        "lat": 22.2828, "lng": 114.1543,
        "type": "attraction",
        "duration": 45,
        "desc": "百年花崗岩石板路，中環歷史地標。",
    },
    {
        "id": 17,
        "image": "S__56188955_0.jpg",
        "name": "中環半山扶手電梯",
        "address": "中環樂成行",
        "lat": 22.2817, "lng": 114.1519,
        "type": "attraction",
        "duration": 30,
        "desc": "全球最長戶外扶手電梯，連接中環至半山。",
    },
    {
        "id": 18,
        "image": "S__56188956_0.jpg",
        "name": "置地廣場 LANDMARK",
        "address": "中環",
        "lat": 22.2808, "lng": 114.1580,
        "type": "shopping",
        "duration": 60,
        "desc": "中環頂級購物商場，品牌雲集。",
    },
    {
        "id": 19,
        "image": "S__56188958_0.jpg",
        "name": "杜莎夫人蠟像館",
        "address": "太平山頂凌霄閣",
        "lat": 22.2707, "lng": 114.1431,
        "type": "attraction",
        "duration": 120,
        "desc": "山頂凌霄閣內著名蠟像館，與明星同框。",
    },
    {
        "id": 20,
        "image": "S__56188959_0.jpg",
        "name": "太平山頂 Victoria Peak",
        "address": "香港山頂",
        "lat": 22.2715, "lng": 114.1453,
        "type": "attraction",
        "duration": 90,
        "desc": "俯瞰香港全景，最經典打卡地標。",
    },
    {
        "id": 21,
        "image": "S__56188960_0.jpg",
        "name": "山頂纜車 Peak Tram",
        "address": "中環花園道纜車總站",
        "lat": 22.2797, "lng": 114.1541,
        "type": "attraction",
        "duration": 30,
        "desc": "百年登山纜車，俯瞰香港島全貌。",
    },
    {
        "id": 22,
        "image": "S__56188961_0.jpg",
        "name": "維多利亞港夜景",
        "address": "尖沙咀海濱長廊",
        "lat": 22.2934, "lng": 114.1738,
        "type": "attraction",
        "duration": 60,
        "desc": "全球最美夜景之一，必看幻彩詠香江。",
    },
    {
        "id": 23,
        "image": "S__56188962_0.jpg",
        "name": "尖沙咀鐘樓",
        "address": "尖沙咀碼頭",
        "lat": 22.2937, "lng": 114.1717,
        "type": "attraction",
        "duration": 30,
        "desc": "殖民地時期歷史建築，維港地標。",
    },
    {
        "id": 24,
        "image": "S__56188966.jpg",
        "name": "星巴克 (雪廠街)",
        "address": "中環雪廠街22號",
        "lat": 22.2817, "lng": 114.1574,
        "type": "food",
        "duration": 30,
        "desc": "中環百年大樓內的特色星巴克門市。",
    },
]

# --- 輔助函數：計算兩點間距離（公里）---
def _haversine(lat1, lng1, lat2, lng2):
    R = 6371
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lng2 - lng1)
    a = math.sin(dphi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2) ** 2
    return R * 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

# --- 貪婪 TSP：最近鄰居法排序行程 ---
def _nearest_neighbour(locs):
    if not locs:
        return []
    unvisited = locs[:]
    # 從最北邊（通常早上先去港島區）出發
    start = min(unvisited, key=lambda x: x["lat"])
    ordered = [start]
    unvisited.remove(start)
    while unvisited:
        last = ordered[-1]
        nearest = min(unvisited, key=lambda x: _haversine(last["lat"], last["lng"], x["lat"], x["lng"]))
        ordered.append(nearest)
        unvisited.remove(nearest)
    return ordered

# --- 推算交通方式 ---
def _transport(dist_km):
    if dist_km < 0.5:
        return "🚶 步行約 {}分鐘".format(int(dist_km * 1000 / 80))
    elif dist_km < 3:
        return "🚌 小巴/巴士約 {}分鐘".format(int(dist_km / 0.3))
    else:
        return "🚇 地鐵約 {}分鐘".format(int(dist_km / 0.8))


# ==================== 路由 ====================

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    import json
    locations_json = json.dumps(LOCATIONS)
    return templates.TemplateResponse(
        "index.html",
        {"request": request, "locations": LOCATIONS, "locations_json": locations_json}
    )


@app.get("/location/{location_id}", response_class=HTMLResponse)
async def get_location(request: Request, location_id: int):
    """返回地點詳細資訊卡片（HTMX 局部更新用）"""
    loc = next((l for l in LOCATIONS if l["id"] == location_id), None)
    if not loc:
        return "<p>找不到地點</p>"
    type_map = {"food": ("🍜", "美食"), "attraction": ("🏛️", "景點"), "shopping": ("🛍️", "購物")}
    icon, type_label = type_map.get(loc["type"], ("📍", "地點"))
    return f"""
    <div class="p-5 animate-fade-in">
        <div class="flex items-start gap-4 mb-4">
            <img src="/images/{loc['image']}" class="w-24 h-24 object-cover rounded-2xl shadow-md flex-shrink-0">
            <div>
                <span class="inline-block text-xs font-semibold px-2 py-0.5 rounded-full bg-orange-100 text-orange-600 mb-1">{icon} {type_label}</span>
                <h3 class="text-xl font-bold text-stone-800">{loc['name']}</h3>
                <p class="text-sm text-stone-500 mt-1">📍 {loc['address']}</p>
                <p class="text-sm text-stone-500">⏱️ 建議停留 {loc['duration']} 分鐘</p>
            </div>
        </div>
        <p class="text-stone-600 text-sm mb-4">{loc['desc']}</p>
        <button
            onclick="addToItinerary({loc['id']}, '{loc['name'].replace("'", "\\'")}', {loc['duration']})"
            class="w-full py-2.5 px-4 bg-gradient-to-r from-orange-400 to-red-400 hover:from-orange-500 hover:to-red-500 text-white font-bold rounded-xl shadow-md transition-all active:scale-95">
            ＋ 加入今日行程
        </button>
    </div>
    """


@app.post("/plan", response_class=HTMLResponse)
async def plan_itinerary(request: Request):
    """接收選定 ID，回傳優化行程 HTML"""
    from fastapi import Form
    body = await request.body()
    # 解析 HTMX 發送的 form data
    from urllib.parse import parse_qs
    data = parse_qs(body.decode())
    ids_raw = data.get("ids", [""])[0]
    if not ids_raw:
        return "<p class='text-stone-400 text-sm text-center py-8'>請先點擊地圖標記並加入地點</p>"
    
    try:
        ids = [int(i) for i in ids_raw.split(",") if i.strip()]
    except ValueError:
        return "<p class='text-red-400 text-sm'>資料格式錯誤</p>"
    
    selected = [l for l in LOCATIONS if l["id"] in ids]
    if not selected:
        return "<p class='text-stone-400 text-sm text-center py-8'>沒有找到符合的地點</p>"

    # 最近鄰居排序
    ordered = _nearest_neighbour(selected)
    
    total_duration = sum(l["duration"] for l in ordered)
    total_travel = 0
    
    html = '<div class="space-y-3">'
    current_time = 9 * 60  # 從早上 9:00 開始
    
    for i, loc in enumerate(ordered):
        hour = current_time // 60
        minute = current_time % 60
        time_str = f"{hour:02d}:{minute:02d}"
        type_colors = {"food": "bg-orange-50 border-orange-200", "attraction": "bg-purple-50 border-purple-200", "shopping": "bg-pink-50 border-pink-200"}
        card_style = type_colors.get(loc["type"], "bg-stone-50 border-stone-200")
        
        html += f"""
        <div class="border {card_style} rounded-xl p-3 flex items-start gap-3">
            <div class="text-center min-w-[44px]">
                <div class="text-xs font-bold text-orange-500">{time_str}</div>
                <div class="w-6 h-6 rounded-full bg-gradient-to-br from-orange-400 to-red-400 text-white text-xs flex items-center justify-center font-bold mx-auto mt-1">{i+1}</div>
            </div>
            <div class="flex-1 min-w-0">
                <p class="font-semibold text-stone-800 text-sm truncate">{loc['name']}</p>
                <p class="text-xs text-stone-500">⏱ {loc['duration']} 分鐘</p>
            </div>
        </div>"""
        
        current_time += loc["duration"]
        
        if i < len(ordered) - 1:
            dist = _haversine(loc["lat"], loc["lng"], ordered[i+1]["lat"], ordered[i+1]["lng"])
            transport = _transport(dist)
            travel_min = int(dist * 1000 / 80) if dist < 0.5 else (int(dist / 0.3) if dist < 3 else int(dist / 0.8))
            total_travel += travel_min
            current_time += travel_min
            html += f"""
            <div class="flex items-center gap-2 px-3">
                <div class="flex-1 border-t border-dashed border-stone-300"></div>
                <span class="text-xs text-stone-400 whitespace-nowrap">{transport}</span>
                <div class="flex-1 border-t border-dashed border-stone-300"></div>
            </div>"""
    
    html += "</div>"
    
    end_hour = current_time // 60
    end_min = current_time % 60
    html += f"""
    <div class="mt-4 p-3 bg-gradient-to-r from-orange-50 to-red-50 rounded-xl border border-orange-200">
        <div class="flex justify-between text-sm">
            <span class="text-stone-600">🕘 結束時間</span>
            <span class="font-bold text-orange-600">{end_hour:02d}:{end_min:02d}</span>
        </div>
        <div class="flex justify-between text-sm mt-1">
            <span class="text-stone-600">📍 共 {len(ordered)} 個景點</span>
            <span class="font-bold text-red-500">約 {(total_duration + total_travel) // 60}h {(total_duration + total_travel) % 60}m</span>
        </div>
    </div>"""
    
    return html


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
