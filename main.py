from uuid import uuid1
import requests
import json



def download_file(file_url: str) -> str:
    response = requests.get(file_url)


    path = f"images/{uuid1()}.webp"
    with open(path, "wb") as f:
        f.write(response.content)

    return path


def get_products(limit: int = 30) -> list:
    url = f"https://dummyjson.com/products?limit={limit}"
    response = requests.get(url)
    data = response.json()
    return data["products"]


def main() -> None:
    products = get_products(limit=30)

    if not products:
        print("Mahsulotlar olinmadi!")
        return

    result = []

    for product in products:
        image_url = product.get("thumbnail")
        if not image_url:
            print(f"Rasm yo'q: {product['title']}")
            continue

        image_path = download_file(image_url)

        item = {
            "id": product.get("id"),
            "title": product.get("title"),
            "description": product.get("description"),
            "category": product.get("category"),
            "price": product.get("price"),
            "path": image_path
        }

        result.append(item)

    if result:
        with open("products.json", "w", encoding="utf-8") as f:
            json.dump(result, f, indent=4, ensure_ascii=False)
        print(f"Tayyor ✅ {len(result)} ta mahsulot products.json ga yozildi")
        print("Rasmlar images/ papkaga saqlandi")
    else:
        print("Natija bo'sh, JSON faylga hech narsa yozilmadi.")


main()
