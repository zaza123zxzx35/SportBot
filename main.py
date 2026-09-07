# ═══════════════════════════════════
# อัปเดตไฟล์ main.py (รองรับคลิปยาว)
# ═══════════════════════════════════
import os, requests
from datetime import datetime, timedelta, timezone

TOKEN = os.environ["TG_TOKEN"]
CHAT_ID = os.environ["TG_CHAT_ID"]
YT_KEY = os.environ["YT_KEY"]

CHANNELS = {
    "UC2n2v6oORuInJI-1IHnvhLQ": "Mr. Knockout",  # ONE Championship
    "UCG5qGWdu8nIRZqJ_GgDwQ-w": "Mr. Coach",     # Premier League
    "UCpcTrCXblq78GZrTUTLWeBw": "Mr. Coach",     # FIFA
    "UCvgfXK4nTYKudb0rFR6noLA": "Mr. Knockout",  # UFC
}

def get_youtube_clips():
    results = []
    # ย้อนหลัง 24 ชม.
    cutoff = (datetime.now(timezone.utc) - timedelta(hours=24)).isoformat().replace("+00:00", "Z")
    
    for cid, niche in CHANNELS.items():
        # videoDuration=long คือเน้นคลิปยาว (มากกว่า 20 นาที)
        url = f"https://www.googleapis.com/youtube/v3/search?key={YT_KEY}&channelId={cid}&part=snippet&order=date&type=video&videoDuration=long&publishedAfter={cutoff}"
        try:
            data = requests.get(url).json()
            for item in data.get("items", [])[:2]: # เอา 2 คลิปต่อช่อง
                results.append({
                    "title": item["snippet"]["title"],
                    "url": f"https://youtu.be/{item['id']['videoId']}",
                    "niche": niche,
                    "why": "คลิปยาวคุณภาพสูงจากช่องทางการ"
                })
        except: continue
    return results[:5]

clips = get_youtube_clips()
if not clips:
    msg = "🟡 วันนี้ยังไม่มีคลิปยาวใหม่ๆ จากช่องทางการในรอบ 24 ชม."
else:
    msg = f"🎬 LONG CLIP DIGEST — {datetime.now().strftime('%d/%m/%Y %H:%M')}\n\n"
    for c in clips:
        msg += f"📌 {c['title']}\n🔗 {c['url']}\n🎯 Niche: {c['niche']}\n💬 {c['why']}\n\n"

requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", json={"chat_id": CHAT_ID, "text": msg})
