from superdesk.io.registry import (
    register_feeding_service,
    register_feeding_service_parser,
)
from superdesk.io.feeding_services import RSSFeedingService
from flask import current_app as app
from superdesk.io.iptc import subject_codes


class PARSSFeedingService(RSSFeedingService):
    """
    Parse the PA RSS feed, extract the subject, remove the source pre-amble from the content and remove the abstract
    if it only contains a full stop.
    """

    NAME = "PA_ATOM"
    label = "PA Atom"

    def _create_item(self, data, field_aliases=None, source="source"):
        item = super()._create_item(data, field_aliases, source)

        # The ATOM version of the PA feed seems to denote the topics with the code, we use that to map to Subjects
        if "tags" in data:
            subjects = []
            patopics = []
            pakeywords = []
            seen_codes = set()
            for tag in data.tags:
                term = tag.get("term")
                if term and isinstance(term, str) and term.startswith("medtop:"):
                    subject = app.mediatopics.get_subject_code(term)
                    if subject and subject not in seen_codes:
                        subjects.append(
                            {"qcode": subject, "name": subject_codes.get(subject, "")}
                        )
                        seen_codes.add(subject)
                if tag.get("scheme") == "urn:pa:subject:patopic":
                    patopics.append(tag.get("label") or tag.get("term"))
                if tag.get("scheme") == "urn:pa:subject:pakeyword":
                    pakeywords.append(tag.get("label") or tag.get("term"))
            if subjects:
                item["subject"] = subjects

            all_terms = patopics + pakeywords
            if all_terms:
                # Join everything with a single space
                item["slugline"] = " ".join(all_terms)

        # Remove the annoying . value they seem to send
        if item["abstract"] == ".":
            item.pop("abstract", None)

        # try extract the value again, as it has not been prefixed by the source
        item["body_html"] = (
            data.content[0].value
            if getattr(data, "content", None)
            else item.get("body_html")
        )

        return item


register_feeding_service(PARSSFeedingService)
register_feeding_service_parser(PARSSFeedingService.NAME, None)
