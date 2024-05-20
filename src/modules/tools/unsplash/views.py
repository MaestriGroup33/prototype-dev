from requests import get

from .models import Background
from .secrets import access_key


def buscar_imagem_aleatoria():
    url = "https://api.unsplash.com/photos/random"
    headers = {"Authorization": f"Client-ID {access_key}"}
    params = {"orientation": "landscape"}
    try:
        response = get(url, headers=headers, params=params)
        if response.status_code == 200:
            data = response.json()
            background = Background(
                id=data["id"],
                color=data["color"],
                description=data["description"]
                if data["description"]
                else "No description",
                url=data["urls"]["regular"],
                image=data["user"]["profile_image"]["large"],
                width=data["width"],
                height=data["height"],
            )
            background.save()  # Assuming there's a save method to store data in your database
            return background
        else:
            return f"Erro ao buscar imagem: {response.status_code}"
    except requests.RequestException as e:
        return f"Request falhou: {e}"
        # To use the function, simply call it and handle the returned result
        #


def buscar_imagem():
    url = "https://api.unsplash.com/photos/random"
    headers = {"Authorization": f"Client-ID {access_key}"}
    params = {"orientation": "landscape"}

    response = get(url, headers=headers, params=params)
    if response.status_code == 200:
        data = response.json()
        print(data)
