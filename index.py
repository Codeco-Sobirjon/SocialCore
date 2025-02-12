import requests

url = "http://localhost:8000/auth/vk/"
data = {
    "access_token": "vk1.a 7bsvtKxBgo-5U0WtJliziHGy25bcv3W47I7oyJjZQsQ0cLV-cbWceyFc8kSCArDSiiJ0ipnlfO52SI90TM2rILwU20jE7e5kIcesRBohDI63mmT1bshagoifZbKHjjrIsa3NrYLvATF0H0U9IjQxRHpBkNBgW5J4MCf6jJBqKQF_kBoD_dniq4uk3jJRlhRKW-lXkLfVWMjgiuz84ZRmiw"}
headers = {"Content-Type": "application/json"}

response = requests.post(url, json=data, headers=headers)
print(response)
