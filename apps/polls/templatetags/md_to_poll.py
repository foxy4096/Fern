import markdown
from markdown.inlinepatterns import Pattern
from django.utils.safestring import mark_safe


class PollExtension(markdown.Extension):
    def extendMarkdown(self, md):
        # Define a pattern for your poll syntax
        poll_pattern = r"\[poll#(\d+)\]"

        # Add the PollPattern to the Markdown instance
        md.inlinePatterns.register(
            PollPattern(poll_pattern, self.getConfigs()), "poll", 75
        )


class PollPattern(Pattern):
    def handleMatch(self, m):
        # Extract the poll ID from the match
        poll_id = m.group(1)

        # Render HTML for the poll
        poll_html = (
            f'<div class="poll" data-poll-id="{poll_id}">Your Poll Content Here</div>'
        )

        return mark_safe(poll_html)
