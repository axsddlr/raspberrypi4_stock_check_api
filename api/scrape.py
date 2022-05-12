import re

import httpx
import ujson as json

from utils.utils import get_soup, get_status, headers

digikey_url = "https://www.digikey.com/products/api/v3/mobile/filter-page/933"
pishop_url = "https://www.pishop.us/product-category/raspberry-pi/raspberry-pi-boards/current-pi-boards/"
chicagodist_url = "https://chicagodist.com/collections/raspberry-pi?_=pf&pf_pt_product_type=Raspberry%20Pi"
sparkfun_url = "https://www.sparkfun.com/search/results_framework?term=Raspberry+Pi+4+Model+B"
okdo_url = "https://www.okdo.com/us/c/pi-shop/the-raspberry-pi/raspberry-pi4/"
vilros_url = "https://vilros.com/collections/raspberry-pi-4?refinementList%5Bnamed_tags.SUB_CAT%5D%5B0%5D=Boards"
adafruit_url = "https://www.adafruit.com/search?q=raspberry%20pi%204%20model%20b"


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


def vilrosPi():
    url = "https://nxer572r7u-dsn.algolia.net/1/indexes/*/queries"

    querystring = {
        "x-algolia-agent": "Algolia for JavaScript (3.35.1); Browser (lite); instantsearch.js (4.8.1); JS Helper ("
                           "3.2.2)",
        "x-algolia-application-id": "NXER572R7U", "x-algolia-api-key": "396a725556d12e53d9270e30bed2bbea"}

    payload = {"requests": [{"indexName": "shopify_vilros1products",
                             "params": "hitsPerPage=15&clickAnalytics=true&facetingAfterDistinct=true&query"
                                       "=&maxValuesPerFacet=10&highlightPreTag=%3Cspan%20class%3D%22ais-highlight%22"
                                       "%3E&highlightPostTag=%3C%2Fspan%3E&page=0&distinct=true&filters"
                                       "=collection_ids%3A%22126697209956%22&ruleContexts=%5B%22raspberry-pi-4%22%5D"
                                       "&facets=%5B%22named_tags.Kit%20Includes%22%2C%22options.color%22%2C%22options"
                                       ".size%22%2C%22named_tags.SUB_CAT%22%2C%22price_range%22%5D&tagFilters"
                                       "=&facetFilters=%5B%5B%22named_tags.SUB_CAT%3ABoards%22%5D%5D"},
                            {"indexName": "shopify_vilros1products",
                             "params": "hitsPerPage=1&clickAnalytics=false&facetingAfterDistinct=true&query"
                                       "=&maxValuesPerFacet=10&highlightPreTag=%3Cspan%20class%3D%22ais-highlight%22"
                                       "%3E&highlightPostTag=%3C%2Fspan%3E&page=0&distinct=true&filters"
                                       "=collection_ids%3A%22126697209956%22&ruleContexts=%5B%22raspberry-pi-4%22%5D"
                                       "&attributesToRetrieve=%5B%5D&attributesToHighlight=%5B%5D&attributesToSnippet"
                                       "=%5B%5D&tagFilters=&analytics=false&facets=named_tags.SUB_CAT"}]}

    headers = {
        'Accept-Language': "en-US,en;q=0.9",
        'Cache-Control': "no-cache",
        'Connection': "keep-alive",
        'Origin': "https://vilros.com",
        'Pragma': "no-cache",
        'Referer': "https://vilros.com/",
        'Sec-Fetch-Dest': "empty",
        'Sec-Fetch-Mode': "cors",
        'Sec-Fetch-Site': "cross-site",
        'User-Agent': "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Mobile Safari/537.36",
        'accept': "application/json",
        'content-type': "application/x-www-form-urlencoded",
        'sec-ch-ua': "^\^"
    }

    r = httpx.post(url, data=json.dumps(payload), headers=headers, params=querystring)
    return r.json()["results"][0]['hits']


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

        init_base = response.find("div", {"class": re.compile("products-list row")})
        modules = init_base.find_all("div", {
            "class": re.compile("product-layout product-grid product-grid-4 col-lg-3 col-md-4 col-12")})

        api = []
        for module in modules:
            product_url = module.find("a", {"class": "product-item-photo"})["href"]
            product_name = module.find("img")["title"]
            product_name = product_name.replace("/", " - ")
            product_id = module.find("div", {"class": "product-colors"})["data-product-id"]

            base_api = "https://www.pishop.us/remote/v1/product-attributes/"

            product_json_data = base_api + product_id
            response = httpx.get(product_json_data, headers=headers)
            apiResponse = response.json()

            product_stock = apiResponse["data"]["instock"]
            product_price = apiResponse["data"]["price"]["without_tax"]["formatted"]

            if "raspberry-pi-4-model-b" in product_url:
                api.append({
                    "product_name": product_name,
                    "product_price": product_price,
                    "product_instock": product_stock,
                    "product_url": product_url,
                })

        data = {"status": status, "data": api}

        if status != 200:
            raise Exception("API response: {}".format(status))
        return data

    @staticmethod
    def chicagodist():
        URL = chicagodist_url
        status = get_status(URL)
        response = get_soup(URL)

        init_base = response.find("div", {"class": re.compile("twelve columns")})
        modules = init_base.find_all("div", {
            "class": re.compile("three columns")})
        #
        api = []
        for module in modules:
            product_url = 'https://chicagodist.com' + module.find("a")["href"]
            product_name = module.find("span").text
            product_price = "$" + module.find("meta")["content"]
            product_instock = module.find("span", {"class": "price"}).text.strip()
            if product_instock == 'Sold Out':
                product_instock = False
            else:
                product_instock = True

            if "Raspberry Pi 4 Model B" in product_name and "Kit" not in product_name:
                api.append(
                    {
                        "product_name": product_name,
                        "product_price": product_price,
                        "product_instock": product_instock,
                        "product_url": product_url,
                    }
                )

        data = {"status": status, "data": api}

        if status != 200:
            raise Exception("API response: {}".format(status))
        return data

    # @staticmethod
    # def sparkfun():
    #     URL = sparkfun_url
    #     status = get_status(URL)
    #     response = get_soup(URL)
    #
    #     init_base = response.find("div", {"class": re.compile("col-md-10 col-sm-9 col-xs-12")})
    #     modules = init_base.find_all("div", {
    #         "class": re.compile("product-tile")})
    #
    #     get_urls = []
    #     for module in modules:
    #         url = module.find("a")["href"]
    #         # name = module.find("span").text
    #         get_urls.append(url)
    #
    #         get_product_data = []
    #         for each in get_urls:
    #             r = get_soup(each)
    #             product_url = each
    #             product_name = r.find("h1").text
    #             # product_name = product_name.replace("/", " - ")
    #             # product_price = r.find("span", {"class": re.compile("price price-sale calculated")}).text
    #             #         # product_id = module.find("input", {"name": "product"})["value"]
    #             # product_stock = r.find("input", {"id": "form-action-addToCart"})["value"]
    #             # turn product_stock into boolean
    #             # if product_stock == 'Out of stock':
    #             #     product_stock = False
    #             # else:
    #             #     product_stock = True
    #             #
    #             if "Raspberry Pi 4 Model B" in product_name:
    #                 get_product_data.append(
    #                     {
    #                         "product_name": product_name,
    #                         # "product_price": product_price,
    #                         # "product_instock": product_stock,
    #                         "product_url": product_url,
    #                     }
    #                 )
    #
    #     data = {"status": status, "data": get_product_data}
    #
    #     if status != 200:
    #         raise Exception("API response: {}".format(status))
    #     return data
    #

    @staticmethod
    def okdo():
        URL = okdo_url
        status = get_status(URL)
        response = get_soup(URL)

        init_base = response.find("div",
                                {"class": re.compile("c-product-listing--4x3-grid c-product-listing type-compact")})
        modules = init_base.find_all("a", {
            "class": re.compile("c-product-listing__item")})
        #
        api = []
        for module in modules:
            product_url = module["href"]
            product_name = module["data-name"]
            product_price = module.find("span", {"class": re.compile("woocommerce-Price-amount amount")}).text.strip()
            product_instock = module.find("span", {
                "class": re.compile("c-stock-level c-stock-level--small c-stock-level--low")}).text.strip()
            if product_instock == 'Out of stock':
                product_instock = False
            else:
                product_instock = True

            if "Raspberry Pi 4 Model B" in product_name and "Kit" not in product_name:
                api.append(
                    {
                        "product_name": product_name,
                        "product_price": product_price,
                        "product_instock": product_instock,
                        "product_url": product_url,
                    }
                )

        data = {"status": status, "data": api}

        if status != 200:
            raise Exception("API response: {}".format(status))
        return data

    @staticmethod
    def vilros():
        apiResponse = vilrosPi()
        status = get_status("https://vilros.com/")

        api = []
        for each in apiResponse:
            product_name = each["title"]
            product_id = each["id"]
            product_url = "https://vilros.com/products/" + each["handle"]
            product_price = "$" + str(each["price"])
            product_instock = each["inventory_available"]  # boolean

            # check if number after decimal is 0
            if product_price.split(".")[1] == "0":
                product_price = product_price.split(".")[0] + ".00"

            if "Raspberry Pi 4 Model B" in product_name:
                api.append(
                    {
                        "product_name": product_name,
                        "product_price": product_price,
                        "product_instock": product_instock,
                        "product_id": product_id,
                        "product_url": product_url,
                    }
                )

        data = {"status": status, "data": api}

        if status != 200:
            raise Exception("API response: {}".format(status))
        return data

    @staticmethod
    def adafruit():
        URL = adafruit_url
        status = get_status(URL)
        response = get_soup(URL)

        init_base = response.find(id="productListing")
        modules = init_base.find_all("div", {"class": re.compile("row product-listing")})

        api = []
        for module in modules:
            product_url = "https://www.adafruit.com" + module.find("a")["href"]
            product_name = module.find("h2").text.strip()
            product_price = module.find("div", {"class": re.compile("price")}).span.text.strip()
            product_instock = module.find("div", {"class": re.compile("stock")}).text.strip()
            product_instock = product_instock.replace("\n", " ")
            product_instock = product_instock.split("    ")[-1]
            if product_instock == 'Out of stock':
                product_instock = False
            else:
                product_instock = True

            if "Raspberry Pi 4 Model B" in product_name and "Kit" not in product_name and "with 1GB, 2GB, or 4GB RAM" not in product_name:
                api.append(
                    {
                        "product_name": product_name,
                        "product_price": product_price,
                        "product_instock": product_instock,
                        "product_url": product_url,
                    }
                )

        data = {"status": status, "data": api}

        if status != 200:
            raise Exception("API response: {}".format(status))
        return data


if __name__ == '__main__':
    print(RPIST.adafruit())
