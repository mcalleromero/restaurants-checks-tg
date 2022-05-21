from bs4 import BeautifulSoup
import mechanize


class FormScraper:
    def __init__(self):
        self.br = mechanize.Browser()
        self.br.set_handle_robots(False)
        self.br.addheaders = [
            (
                "User-agent",
                "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1",
            )
        ]
        # TODO: URL must be passed as an env var as it may be changed
        self.url = "https://www.up-spain.com/cheque-gourmet/buscador-restaurantes/"

    def mechanize_test(self, restaurant, city="Madrid", cp=None):
        self.br.open(self.url)
        self.br.select_form(id="search-form")
        self.br.form["form[nombre]"] = restaurant
        self.br.form["form[provincia]"] = [city.upper()]
        if cp:
            self.br.form["form[cp]"] = cp
        self.restaurants_response = self.br.submit()
        return self._get_restaurants()

    def _get_restaurants(self):
        soup = BeautifulSoup(self.restaurants_response, "html.parser")

        restaurants = soup.find_all("div", {"class": "col-12 mb-4"})
        response = ""
        for restaurant in restaurants:
            name = restaurant.find("div", {"class": "text-gourmet-ticket"}).text.strip()
            calle = restaurant.find("div", {"class": "small"}).text.strip()
            telefono = restaurant.find("a")
            if telefono:
                telefono = telefono.text.strip()
            else:
                telefono = "NO TLF."

            response += f"{name}\n\t{calle}\n\t{telefono}\n\n"

        return response
