import json
import unittest
import requests
import time

URL = "https://regions-test.2gis.com/v1"

class TestToken(unittest.TestCase):

    def assertStatus(self, response, expected_code):
        """ Функция обработки сообщения об ошибке, приведение к читаемому формату вывода """
        self.assertEqual(
            response.status_code,
            expected_code,
            f"Ожидался статус {expected_code}, но получен {response.status_code}. "
            f"Ответ: {json.dumps(response.json(), ensure_ascii=False)}"
        )

    def getCode(self):
        response = requests.post(f"{URL}/auth/tokens")
        self.assertEqual(response.status_code, 200)
        cookie_header = response.headers.get("Set-Cookie")
        self.assertIsNotNone(cookie_header)
        token = cookie_header.split("token=")[1].split(";")[0]
        return token


    def test_case1(self):
        """ Успешное создание места """
        token = self.getCode()
        data = {
            "title": "Test Place",
            "lat": 55.028254,
            "lon": 82.918501,
            "color": "BLUE"
        }
        cookies = {"token": token}
        response = requests.post(f"{URL}/favorites", data=data, cookies=cookies)
        self.assertStatus(response, 200)
        json_data = response.json()
        self.assertEqual(json_data["title"], data["title"])
        self.assertEqual(json_data["lat"], data["lat"])
        self.assertEqual(json_data["lon"], data["lon"])
        self.assertEqual(json_data["color"], data["color"])

    def test_case2(self):
        """ Создание места без токена """
        data = {
            "title": "Test Place",
            "lat": 55.028254,
            "lon": 82.918501,
            "color": "BLUE"
        }
        response = requests.post(f"{URL}/favorites", data=data)
        self.assertStatus(response, 401)

    def test_case3(self):
        """ Создание места с просроченным токеном """
        token = self.getCode()
        data = {
            "title": "Test Place",
            "lat": 55.028254,
            "lon": 82.918501,
            "color": "BLUE"
        }
        cookies = {"token": token}
        time.sleep(3)
        response = requests.post(f"{URL}/favorites", data=data, cookies=cookies)
        self.assertStatus(response, 401)

    def test_case4(self):
        """ Создание места без параметра title"""
        token = self.getCode()
        data = {
            "lat": 55.028254,
            "lon": 82.918501,
            "color": "BLUE"
        }
        cookies = {"token": token}
        response = requests.post(f"{URL}/favorites", data=data, cookies=cookies)
        self.assertStatus(response, 400)

    def test_case5(self):
        """ Создание места без параметра lat"""
        token = self.getCode()
        data = {
            "title": "Test Place",
            "lon": 82.918501,
            "color": "BLUE"
        }
        cookies = {"token": token}
        response = requests.post(f"{URL}/favorites", data=data, cookies=cookies)
        self.assertStatus(response, 400)

    def test_case6(self):
        """ Создание места без параметра lon"""
        token = self.getCode()
        data = {
            "title": "Test Place",
            "lat": 55.028254,
            "color": "BLUE"
        }
        cookies = {"token": token}
        response = requests.post(f"{URL}/favorites", data=data, cookies=cookies)
        self.assertStatus(response, 400)

    def test_case7(self):
        """ Создание места с некорректным цветом """
        token = self.getCode()
        data = {
            "title": "Test Place",
            "lat": 55.028254,
            "lon": 82.918501,
            "color": "PURPLE"
        }
        cookies = {"token": token}
        response = requests.post(f"{URL}/favorites", data=data, cookies=cookies)
        self.assertStatus(response, 400)

    def test_case8(self):
        """ Передача строки вместо координат lat """
        token = self.getCode()
        data = {
            "title": "Test Place",
            "lat": "xyz",
            "lon": 82.918501,
            "color": "BLUE"
        }
        cookies = {"token": token}
        response = requests.post(f"{URL}/favorites", data=data, cookies=cookies)
        self.assertStatus(response, 400)

    def test_case9(self):
        """ Передача строки вместо координат lon """
        token = self.getCode()
        data = {
            "title": "Test Place",
            "lat": 55.028254,
            "lon": "xyz",
            "color": "BLUE"
        }
        cookies = {"token": token}
        response = requests.post(f"{URL}/favorites", data=data, cookies=cookies)
        self.assertStatus(response, 400)

    def test_case10(self):
        """ Передача title, в котором > 1000 символов """
        token = self.getCode()
        bigTitle = "A" * 1001
        data = {
            "title": bigTitle,
            "lat": 55.028254,
            "lon": 82.918501,
            "color": "BLUE"
        }
        cookies = {"token": token}
        response = requests.post(f"{URL}/favorites", data=data, cookies=cookies)
        self.assertStatus(response, 400)

    def test_case11(self):
        """ Передача title, в котором > 1000 символов """
        token = self.getCode()
        data = {
            "title": "",
            "lat": 55.028254,
            "lon": 82.918501,
            "color": "BLUE"
        }
        cookies = {"token": token}
        response = requests.post(f"{URL}/favorites", data=data, cookies=cookies)
        self.assertStatus(response, 400)

    def test_case12(self):
        """ Успешное создание 2 мест при помощи 1 токена """
        token = self.getCode()
        data = {
            "title": "Place",
            "lat": 55.028254,
            "lon": 82.918501,
            "color": "BLUE"
        }
        cookies = {"token": token}
        response = requests.post(f"{URL}/favorites", data=data, cookies=cookies)
        self.assertStatus(response, 200)
        response1 = requests.post(f"{URL}/favorites", data=data, cookies=cookies)
        self.assertStatus(response1, 200)

    def test_case13(self):
        """ Отправка запроса с параметром Title = None """
        token = self.getCode()
        data = {
            "title": None,
            "lat": 55.028254,
            "lon": 82.918501,
            "color": "BLUE"
        }
        cookies = {"token": token}
        response = requests.post(f"{URL}/favorites", data=data, cookies=cookies)
        self.assertStatus(response, 400)

    def test_case14(self):
        """ Отправка запроса с параметром Lat = None """
        token = self.getCode()
        data = {
            "title": "Place",
            "lat": None,
            "lon": 82.918501,
            "color": "BLUE"
        }
        cookies = {"token": token}
        response = requests.post(f"{URL}/favorites", data=data, cookies=cookies)
        self.assertStatus(response, 400)

    def test_case15(self):
        """ Отправка запроса с параметром Lon = None """
        token = self.getCode()
        data = {
            "title": "Place",
            "lat": 55.028254,
            "lon": None,
            "color": "BLUE"
        }
        cookies = {"token": token}
        response = requests.post(f"{URL}/favorites", data=data, cookies=cookies)
        self.assertStatus(response, 400)

    def test_case16(self):
        """ Отправка запроса с параметром Color = None """
        token = self.getCode()
        data = {
            "title": "Place",
            "lat": 55.028254,
            "lon": 82.918501,
            "color": None
        }
        cookies = {"token": token}
        response = requests.post(f"{URL}/favorites", data=data, cookies=cookies)
        self.assertStatus(response, 200)

    def test_case17(self):
        """ Отправка запроса с параметром Token = None """
        token = None
        data = {
            "title": "Place",
            "lat": 55.028254,
            "lon": 82.918501,
            "color": "BLUE"
        }
        cookies = {"token": token}
        response = requests.post(f"{URL}/favorites", data=data, cookies=cookies)
        self.assertStatus(response, 401)


if __name__ == "__main__":
    unittest.main()