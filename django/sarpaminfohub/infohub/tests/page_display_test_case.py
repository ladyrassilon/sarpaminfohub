from sarpaminfohub.infohub.tests.sarpam_test_case import SarpamTestCase

class PageDisplayTestCase(SarpamTestCase):
    def check_search_field_visible_on_page(self, url):
        response = self.client.get(url)
        self.assertContains(response,
                            "<input type=\"text\" name=\"search\" id=\"id_search\" />")
        
    def check_search_results_link_visible_on_page(self, response):
        self.check_link_visible_on_page(response, href="/?search=amitrip",
                                        text="Search Results")

    def check_link_visible_on_page(self, response, href, text):
        self.assertContains(response, text)
        expected_link = "<a href=\"" + href + "\">" + text + "</a>"
        self.assertContains(response, expected_link)

    def check_tab_is_selected(self, response, text):
        self.assertContains(response, text)
        expected_li = "<li class=\"selected\">" + text + "</li>"
        self.assertContains(response, expected_li)
