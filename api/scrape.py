import re

import httpx

from utils.utils import get_soup, get_status

digikey_url = "https://www.digikey.com/products/api/v3/mobile/filter-page/933"
pishop_url = "https://www.pishop.us/product-category/raspberry-pi/raspberry-pi-boards/current-pi-boards/"
chicagodist_url = "https://chicagodist.com/collections/raspberry-pi?_=pf&pf_pt_product_type=Raspberry%20Pi"


# digikey store
def digiPi():
    url = digikey_url
    querystring = dict(s="N4IgTCBcDaIE4EMDOAHARgUznAngAhQEsQBdAXyA")
    digiheaders = {
        "accept-language": "en-us",
        "referer": "https://www.digikey.com/en/products/result?s=N4IgTCBcDaIE4EMDOAHARgUznAngAhQEsQBdAXyA",
        "user-agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1",
        "x-currency": "USD",
    }
    response = httpx.get(url, headers=digiheaders, params=querystring)
    return response.json()


class RPIST:
    @staticmethod
    def digikey():
        apiResponse = digiPi()
        status = get_status("https://www.digikey.com/")
        base = apiResponse["data"]["products"]

        api = []
        for each in base:
            product_name = each["description"]
            product_id = each["id"]
            product_url = "https://www.digikey.com" + each["detailUrl"]
            product_price = each["unitPrice"]  # set to float
            product_isMarketplace = each["isMarketplace"]  # boolean

            if "RASPBERRY PI 4 MODEL B 2GB SDRAM" in product_name and product_price == "Active":
                product_price = "$45.00000"
            else:
                product_price = each["unitPrice"]

            if "RASPBERRY PI 4" in product_name:
                api.append(
                    {
                        "product_name": product_name,
                        "product_id": product_id,
                        "product_url": product_url,
                        "product_price": product_price[:-3],
                        "product_isMarketplace": product_isMarketplace,
                    }
                )

        data = {"status": status, "data": api}

        if status != 200:
            raise Exception("API response: {}".format(status))
        return data

    @staticmethod
    def pishop():
        URL = pishop_url
        status = get_status(URL)
        response = get_soup(URL)

        la_base = response.find("div", {"class": re.compile("products-list row")})
        la_module = la_base.find_all("div", {
            "class": re.compile("product-layout product-grid product-grid-4 col-lg-3 col-md-4 col-12")})

        get_urls = []
        for module in la_module:
            url = module.find("a", {"class": "product-item-photo"})["href"]
            if "raspberry-pi-4-model-b" in url:
                get_urls.append(url)

            get_product_data = []
            for each in get_urls:
                r = get_soup(each)
                #         # product_url = "https://www.pishop.us" + each
                product_name = r.find("h1", {"class": re.compile("productView-title")}).text
                product_name = product_name.replace("/", " - ")
                product_price = r.find("span", {"class": re.compile("price price--withoutTax")}).text
                #         # product_id = module.find("input", {"name": "product"})["value"]
                product_stock = r.find("input", {"id": "form-action-addToCart"})["value"]
                # turn product_stock into boolean
                if product_stock == 'Out of stock':
                    product_stock = False
                else:
                    product_stock = True
                #
                get_product_data.append(
                    {
                        "product_name": product_name,
                        "product_price": product_price,
                        "product_instock": product_stock,
                        "product_url": each,
                    }
                )

        data = {"status": status, "data": get_product_data}

        if status != 200:
            raise Exception("API response: {}".format(status))
        return data

    @staticmethod
    def chicagodist():
        URL = chicagodist_url
        status = get_status(URL)
        response = get_soup(URL)

        la_base = response.find("div", {"class": re.compile("twelve columns")})
        la_module = la_base.find_all("div", {
            "class": re.compile("product_container")})
        #
        # api = []
        # for module in la_module:
        #     product_url = 'https://chicagodist.com' + module.find("a")["href"]
        #     product_name = module.find("span").text
        #     product_price  = "$" + module.find("meta")["content"]
        #     product_instock= module.find("span", {"class": "price"}).text.strip()
        #     if product_instock == 'Sold Out':
        #         product_instock = False
        #     else:
        #         product_instock = True
        #
        #     if "Kits" not in product_name and "400" not in product_name and "Cable" not in product_name and "Pico" not in product_name:
        #         api.append(
        #             {
        #                 "product_name": product_name,
        #                 "product_price": product_price,
        #                 "product_instock": product_instock,
        #                 "product_url": product_url,
        #             }
        #         )
        #
        # data = {"status": status, "data": api}
        #
        # if status != 200:
        #     raise Exception("API response: {}".format(status))
        return la_module


if __name__ == '__main__':
    print(RPIST.chicagodist())
