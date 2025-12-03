import requests

CAFE_API_URL = "https://cafenomad.tw/api/v1.2/cafes"

class DataManager:

    def __init__(self):
        self.cafes_list = []

    def get_info(self, target_city):
        # 在開始篩選前清空實例變數
        self.cafes_list = []
        response = requests.get(url=CAFE_API_URL)
        response.raise_for_status()
        data = response.json()

        for city_name in data:
            if city_name.get("city") == target_city:
                fields = ["name", "address", "wifi", "url", "open_time"]
                cafe_info = {}

                # 從當前咖啡館字典中取出需要的資訊
                for field in fields:
                    # 如果欄位不存在則返回 None
                    cafe_info[field] = city_name.get(field)
                self.cafes_list.append(cafe_info)

        return self.cafes_list

