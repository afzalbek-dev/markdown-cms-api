import re
from dataclasses import dataclass, field
from typing import Dict, Any, List, Optional
import yaml


@dataclass
class ContentPost:
    slug: str
    title: str
    date: str
    tags: List[str]
    published: bool
    summary: str
    body_markdown: str
    reading_time_minutes: int
    raw_frontmatter: Dict[str, Any] = field(default_factory=dict)


class FrontmatterParser:
    """Markdown fayllaridagi YAML frontmatter qismini va asosiy matnni ajratish."""

    FRONTMATTER_REGEX = re.compile(r"^---\s*\n(.*?)\n---\s*\n(.*)$", re.DOTALL)

    @classmethod
    def parse(cls, content: str, default_slug: str = "post") -> ContentPost:
        match = cls.FRONTMATTER_REGEX.match(content.strip())
        if match:
            fm_text = match.group(1)
            body = match.group(2).strip()
            try:
                fm = yaml.safe_load(fm_text) or {}
            except Exception:
                fm = {}
        else:
            fm = {}
            body = content.strip()

        title = fm.get("title", default_slug.replace("-", " ").title())
        slug = fm.get("slug", default_slug)
        date_str = str(fm.get("date", "2026-01-01"))
        tags = fm.get("tags", [])
        if isinstance(tags, str):
            tags = [t.strip() for t in tags.split(",") if t.strip()]
        published = bool(fm.get("published", True))
        summary = fm.get("summary", body[:150] + "..." if len(body) > 150 else body)

        # O'qish vaqti: daqiqasiga ~200 ta so'z
        words = len(re.findall(r"\w+", body))
        reading_time = max(1, round(words / 200))

        return ContentPost(
            slug=slug,
            title=title,
            date=date_str,
            tags=tags,
            published=published,
            summary=summary,
            body_markdown=body,
            reading_time_minutes=reading_time,
            raw_frontmatter=fm,
        )
