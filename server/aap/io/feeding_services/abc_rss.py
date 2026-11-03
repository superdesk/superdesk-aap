from superdesk.io.registry import (
    register_feeding_service,
    register_feeding_service_parser,
)
from superdesk.io.feeding_services import RSSFeedingService
import html


class ABCRSSFeedingService(RSSFeedingService):
    """
    Parse the ABC RSS feed
    """

    NAME = "ABC_RSS"
    label = "ABC RSS"

    def _create_item(self, data, field_aliases=None, source="source"):
        item = super()._create_item(data, field_aliases, source)
        item["ingest_id"] = item.get("guid")
        item.setdefault("keywords", ["marketplace"])

        thumbnails = getattr(data, "media_thumbnail", [])
        if thumbnails:
            thumb = thumbnails[0]
            url = thumb.get("url", "")

            if url:
                safe_url = html.escape(url)
                width = thumb.get("width")
                height = thumb.get("height")

                caption_text = thumb.get("description", thumb.get("title", ""))
                if caption_text:
                    alt_text = ""
                else:
                    alt_text = html.escape(data.get("title", "Article thumbnail"))

                img_attrs = (
                    f"src='{safe_url}' alt='{alt_text}' "
                    "style='max-width: 100%; height: auto; object-fit: cover;'"
                )

                if width:
                    img_attrs += f" width='{width}'"
                if height:
                    img_attrs += f" height='{height}'"

                img_tag = f"<img {img_attrs}>"

                if caption_text:
                    safe_caption = html.escape(caption_text)
                    figure_block = (
                        f"<figure style='margin: 0 0 1rem 0;'>\n"
                        f"  {img_tag}\n"
                        f"  <figcaption>{safe_caption}</figcaption>\n"
                        f"</figure>\n"
                    )
                else:
                    figure_block = f"<figure style='margin: 0 0 1rem 0;'>\n  {img_tag}\n</figure>\n"

                item["body_html"] = figure_block + item.get("body_html", "")

        return item


register_feeding_service(ABCRSSFeedingService)
register_feeding_service_parser(ABCRSSFeedingService.NAME, None)
