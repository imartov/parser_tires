import json
import requests


def get_data():
    result_list = []
    for i in range(1, 151):
        url = f"https://roscarservis.ru/catalog/legkovye/?form_id=catalog_filter_form&filter_mode=params&sort=asc&filter_type=tires&arCatalogFilter_458_1500340406=Y&set_filter=Y&arCatalogFilter_463=668736523&PAGEN_1={i}"
        headers = {
            "Accept": "*/*",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36",
            "X-Requested-With": "XMLHttpRequest",
        }

        r = requests.get(url=url, headers=headers)

        with open(f"data_pages/{i}_page.json", "w", encoding="utf-8") as file:
            json.dump(r.json(), file, indent=4, ensure_ascii=False)
            file.close()

        with open(f"data_pages/{i}_page.json", encoding="utf-8") as file:
            data_list = json.load(file)

        for data_item in data_list["items"]:
            title = data_item["name"]
            price = str(data_item["price"]) + " RUB"
            tire_url = "https://roscarservis.ru" + data_item["url"]
            picture_url = "https://roscarservis.ru" + data_item["imgSrc"]

            if "commonStores" in data_item:
                count = []
                sum_tires = 0
                for store in data_item["commonStores"]:
                    title_store = store["STORE_NAME"]
                    amount = store["AMOUNT"]

                    sum_tires += int(amount)

                    count.append(
                        {
                            "store": title_store,
                            "amount": amount
                        }
                    )
                result_list.append(
                    {
                        "name": title,
                        "price": price,
                        "url": tire_url,
                        "picture_url": picture_url,
                        "store": count,
                        "amount": sum_tires
                    }
                )
        print(f"completed {i}/150\n")

    with open("result_tires.json", "w", encoding="utf-8") as file:
        json.dump(result_list, file, indent=4, ensure_ascii=False)
        file.close()


def main():
    get_data()


if __name__ == "__main__":
    main()