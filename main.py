# ═══════════════════════════════════
# main.py สำหรับ GitHub Actions
# ═══════════════════════════════════
import os, requests
from datetime import datetime, timedelta, timezone

# ตั้งค่าผ่าน Secrets
TOKEN = os.environ["TG_TOKEN"]
CHAT_ID = os.environ["TG_CHAT_ID"]
YT_KEY = os.environ["YT_KEY"]

# ช่อง YouTube ที่ต้องการสแกน
CHANNELS = {
    "UC2n2v6oORuInJI-1IHnvhLQ": "Mr. Knockout",  # ONE Championship
    "UCG5qGWdu8nIRZqJ_GgDwQ-w": "Mr. Coach",     # Premier League
    "UCpcTrCXblq78GZrTUTLWeBw": "Mr. Coach",     # FIFA
    "UCvgfXK4nTYKudb0rFR6noLA": "Mr. Knockout",  # UFC
}

def get_youtube_clips():
    results = []
    cutoff = (datetime.now(timezone.utc) - timedelta(hours=24)).isoformat().replace("+00:00", "Z")
    
    for cid, niche in CHANNELS.items():
        url = f"https://www.googleapis.com/youtube/v3/search?key={YT_KEY}&channelId={cid}&part=snippet&order=date&type=video&publishedAfter={cutoff}"
        data = requests.get(url).json()
        
        for item in data.get("items", [])[:3]: # เอา 3 คลิปแรกต่อช่อง
            title = item["snippet"]["title"]
            # กรองคีย์เวิร์ดที่เน้นคลิป
            if any(k in title.lower() for k in ["highlight", "ko", "knockout", "goal", "skill"]):
                results.append({
                    "title": title,
                    "url": f"https://youtu.be/{item['id']['videoId']}",
                    "niche": niche,
                    "why": "คลิปไฮไลต์จากช่องทางการล่าสุด"
                })
    return results[:5] # รวมแล้วไม่เกิน 5 คลิป

# สร้างข้อความ
clips = get_youtube_clips()
if not clips:
    msg = "🟡 วันนี้ยังไม่มีคลิปไฮไลต์ใหม่จากแหล่งทางการ"
else:
    msg = f"🎬 CLIP DIGEST — {datetime.now().strftime('%d/%m/%Y')}\n\n"
    for c in clips:
        msg += f"📌 {c['title']}\n🔗 {c['url']}\n🎯 Niche: {c['niche']}\n💬 Why it's clip-worthy: {c['why']}\n\n"

# ส่ง Telegram
requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", json={"chat_id": CHAT_ID, "text": msg})
