import os
import sys
from datetime import datetime, timezone, timedelta
from linebot.v3.messaging import Configuration, ApiClient, MessagingApi, PushMessageRequest, TextMessage

# Get environment variables from GitHub Secrets
CHANNEL_ACCESS_TOKEN = os.environ.get('CHANNEL_ACCESS_TOKEN')
USER_ID = os.environ.get('USER_ID')

def send_message():
    """ส่งข้อความเตือนชำระเงินผ่าน LINE"""
    try:
        if not CHANNEL_ACCESS_TOKEN:
            print("❗ ไม่พบ CHANNEL_ACCESS_TOKEN")
            return False
            
        if not USER_ID:
            print("❗ ไม่พบ USER_ID")
            return False
        
        print("🔄 กำลังส่งข้อความ...")
        
        configuration = Configuration(access_token=CHANNEL_ACCESS_TOKEN)
        
        with ApiClient(configuration) as api_client:
            line_bot_api = MessagingApi(api_client)
            
            # Bangkok timezone (UTC+7)
            bangkok_tz = timezone(timedelta(hours=7))
            current_time = datetime.now(bangkok_tz)
            current_hour = current_time.hour
            
            # สร้างข้อความตามเวลา
            if current_hour < 18:
                emoji = "☀️"
                greeting = "สวัสดีตอนบ่าย"
            else:
                emoji = "🌙"
                greeting = "สวัสดีตอนดึก"
            
            message_text = f"{emoji} {greeting}! อย่าลืมชำระเงิน 200 บาทนะครับ 💰\n\nเวลา: {current_time.strftime('%d/%m/%Y %H:%M')} 🕐"
            
            # ส่งข้อความ
            line_bot_api.push_message_with_http_info(
                PushMessageRequest(
                    to=USER_ID,
                    messages=[TextMessage(text=message_text)]
                )
            )
            
            print(f"✅ ส่งข้อความเตือนสำเร็จ!")
            print(f"📅 วันที่: {current_time.strftime('%d/%m/%Y %H:%M:%S')}")
            print(f"💬 ข้อความ: {message_text}")
            return True
            
    except Exception as e:
        print(f"❌ เกิดข้อผิดพลาด: {str(e)}")
        return False

if __name__ == "__main__":
    print("🚀 เริ่มการทำงานของ LINE Payment Reminder")
    success = send_message()
    
    if success:
        print("🎉 สำเร็จ! ปิดโปรแกรม")
    else:
        print("💥 ล้มเหลว! กรุณาตรวจสอบการตั้งค่า")
        sys.exit(1)
