from datetime import datetime
import xml.etree.ElementTree as ET

from django.contrib.syndication.views import Feed
from django.http import Http404
from django.utils import timezone

from main import models
from main.util import reading_time
from django.utils.feedgenerator import Rss201rev2Feed, Atom1Feed

class RSLRSSFeed(Rss201rev2Feed):
    def root_attributes(self):
        """
        Override the <rss> root attributes to include the RSL namespace.
        """
        attrs = super().root_attributes()
        attrs['xmlns:rsl'] = "https://rslstandard.org/rsl"
        return attrs
    
    def add_item_elements(self, handler, item):
        super().add_item_elements(handler, item)

        rsl_content = item.get("rsl_content")
        if rsl_content:
            # <rsl:content url="...">
            handler.startElement("rsl:content", {"url": rsl_content["url"]})

            # <rsl:license>
            handler.startElement("rsl:license", {})

            # <rsl:permits type="usage">train-ai</rsl:permits>
            permits = rsl_content.get("permits")
            if permits:
                handler.startElement("rsl:permits", {"type": permits["type"]})
                handler.characters(permits["value"])
                handler.endElement("rsl:permits")

            # <rsl:payment type="subscription">
            payment = rsl_content.get("payment")
            if payment:
                handler.startElement("rsl:payment", {"type": payment["type"]})
                
                # <rsl:custom>https://test.org/contact</rsl:custom>
                custom_url = payment.get("custom")
                if custom_url:
                    handler.startElement("rsl:custom", {})
                    handler.characters(custom_url)
                    handler.endElement("rsl:custom")
                
                # <rsl:standard>https://rslcollective.org/license</rsl:standard>
                standard_url = payment.get("standard")
                if standard_url:
                    handler.startElement("rsl:standard", {})
                    handler.characters(standard_url)
                    handler.endElement("rsl:standard")

                handler.endElement("rsl:payment")

            handler.endElement("rsl:license")
            handler.endElement("rsl:content")

class RSSBlogFeed(Feed):
    feed_type = RSLRSSFeed
    title = ""
    link = ""
    description = ""
    subdomain = ""

    def __call__(self, request, *args, **kwargs):
        if not hasattr(request, "subdomain"):
            raise Http404()
        user = models.User.objects.get(username=request.subdomain)
        self.user = user
        self.title = user.blog_title
        self.description = user.blog_byline_as_text
        self.subdomain = request.subdomain
        self.link = user.blog_url

        models.AnalyticPage.objects.create(user=user, path="rss")

        return super().__call__(request, *args, **kwargs)
    
    def items(self):
        return models.Post.objects.filter(
            owner__username=self.subdomain,
            published_at__isnull=False,
            published_at__lte=timezone.now().date(),
        ).order_by("-published_at")[:10]

    def item_title(self, item):
        return item.title

    def item_link(self, item):
        return item.get_proper_url()

    def item_description(self, item):
        html = item.body_as_html

        if not item.owner.reading_time_on:
            return html
        
        reading_time_text = f"<p style='font-style: italic; margin-top: 0.5em; margin-bottom: 1em;'>Estimated reading time: {reading_time(html)} min</p>"

        return reading_time_text + html

    def item_pubdate(self, item):
        # set time to 00:00 because we don't store time for published_at field
        return datetime.combine(item.published_at, datetime.min.time())
        
    def item_extra_kwargs(self, item):
        """
        Parse the user’s RSL XML and return dict for item_extra_elements.
        """
        user = self.user
        rsl_xml = user.reallysimplelicensing.license
        if rsl_xml and user.reallysimplelicensing.show_rss:
            rsl_content = parse_rsl_xml(rsl_xml, post_url=f'https:{item.get_proper_url()}')
            return {"rsl_content": rsl_content}
        return {}


class AtomBlogFeed(RSSBlogFeed):
    feed_type = Atom1Feed
    subtitle = RSSBlogFeed.description

    def __call__(self, request, *args, **kwargs):
        if not hasattr(request, "subdomain"):
            raise Http404()

        user = models.User.objects.get(username=request.subdomain)

        models.AnalyticPage.objects.create(user=user, path="atom")

        return super().__call__(request, *args, **kwargs)

# Helper to parse RSL XML

RSL_NS = {"rsl": "https://rslstandard.org/rsl"}

def parse_rsl_xml(rsl_xml, post_url=None):
    """
    Parse an RSL XML string and return a dict describing <content> license info.
    If post_url is provided, replace '/' URLs with it.
    """
    tree = ET.ElementTree(ET.fromstring(rsl_xml))
    root = tree.getroot()

    content_el = root.find("rsl:content", RSL_NS)
    if content_el is None:
        return None

    url = content_el.attrib.get("url", "")
    if post_url and url == "/":
        url = post_url

    license_el = content_el.find("rsl:license", RSL_NS)

    permits = None
    payment = None

    if license_el is not None:
        permits_el = license_el.find("rsl:permits", RSL_NS)
        if permits_el is not None:
            permits = {"type": permits_el.attrib.get("type"), "value": permits_el.text}

        payment_el = license_el.find("rsl:payment", RSL_NS)
        if payment_el is not None:
            payment = {"type": payment_el.attrib.get("type")}
            for tag in ["custom", "standard"]:
                child = payment_el.find(f"rsl:{tag}", RSL_NS)
                if child is not None:
                    payment[tag] = child.text

    return {"url": url, "permits": permits, "payment": payment}