import requests
from config import Config

def find_id():
    headers = {"Authorization": f"Bearer {Config.Printify_API_KEY}"}
    res = requests.get(f"{Config.Printify_API_URL}/shops.json", headers=headers)
    
    if res.status_code == 200:
        shops = res.json()
        print("\n📡 找到以下店铺资产:")
        for shop in shops:
            print(f"✅ 店铺名称: {shop['title']} | 真实 ID: {shop['id']}")
    else:
        print(f"❌ 无法获取店铺信息: {res.text}")

if __name__ == "__main__":
    find_id()