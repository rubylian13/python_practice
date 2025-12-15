import requests


BREWERY_API_URL = "https://api.openbrewerydb.org/v1/breweries"

class DataManager:

    def __init__(self):
        pass

    def get_data(self):
        url = f"{BREWERY_API_URL}?per_page=9"
        response = requests.get(url=url)
        breweries = response.json() if response.status_code == 200 else []

        brewery_data = []
        for brewery in breweries:
            brewery_data.append({
                "name": brewery.get("name"),
                "country": brewery.get("country"),
                "city": brewery.get("city"),
                "brewery_type": brewery.get("brewery_type"),
                "website_url": brewery.get("website_url")
            })

        return brewery_data

    def search_breweries_by_value(self, field, query):
        # 前端欄位 → API 參數對照
        FIELD_MAP = {
            "name": "by_name",
            "brewery_type": "by_type",
            "country": "by_country",
            "city": "by_city"
        }

        # 根據選擇欄位轉成 API 參數
        api_field = FIELD_MAP.get(field, "by_name")  # 預設 by_name
        params = {api_field: query}

        response = requests.get(BREWERY_API_URL, params=params)
        breweries = response.json() if (response.status_code == 200 and isinstance(response.json(), list)) else []

        search_data = []
        for brewery in breweries:
            search_data.append({
                "name": brewery.get("name"),
                "country": brewery.get("country"),
                "city": brewery.get("city"),
                "brewery_type": brewery.get("brewery_type"),
                "website_url": brewery.get("website_url")
            })
        return search_data
