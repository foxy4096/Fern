from markdown import Markdown
from markdown.postprocessors import Postprocessor
from markdown.extensions import Extension
import re
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe  # Ensure safe HTML output


class PollProcessor(Postprocessor):
    """
    Converts `[poll#id]` syntax in Markdown content to rendered poll elements.
    """

    POLL_PATTERN = r"\[poll#(\d+)\]"

    def run(self, text: str) -> str:
        """
        Processes Markdown text, replacing `[poll#id]` patterns with rendered polls.

        Args:
            text (str): The Markdown content to be processed.

        Returns:
            str: The modified Markdown content with embedded poll elements.
        """

        def replace_poll(match):
            poll_id = match.group(1)
            poll_html = render_to_string(
                "polls/islands/poll_block.html", {"poll_id": poll_id}
            )
            return mark_safe(poll_html)

        # Escape user-generated content within the poll template (polls/islands/poll_block.html)
        # ... (implement template escaping for title, description, options, etc.)

        return re.sub(self.POLL_PATTERN, replace_poll, text)


class PollExtension(Extension):
    def extendMarkdown(self, md: Markdown) -> None:
        return md.inlinePatterns.register(PollProcessor(md), "poll", 175)