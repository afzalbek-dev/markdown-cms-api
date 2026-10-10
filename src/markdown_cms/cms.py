import os
from typing import List, Dict, Any, Optional
from .parser import FrontmatterParser, ContentPost


class MarkdownCMS:
    """Flat-file papkadagi barcha Markdown postlarni indekslash va API taqdim etish."""

    def __init__(self, content_dir: str):
        self.content_dir = content_dir
        self.posts: Dict[str, ContentPost] = {}

    def reload(self) -> int:
        self.posts.clear()
        if not os.path.exists(self.content_dir):
            return 0

        for root, _, files in os.walk(self.content_dir):
            for file in files:
                if file.endswith((".md", ".markdown")):
                    full_path = os.path.join(root, file)
                    slug = os.path.splitext(file)[0]
                    try:
                        with open(full_path, "r", encoding="utf-8") as f:
                            post = FrontmatterParser.parse(f.read(), default_slug=slug)
                        self.posts[post.slug] = post
                    except Exception:
                        continue

        return len(self.posts)

    def get_post(self, slug: str) -> Optional[ContentPost]:
        return self.posts.get(slug)

    def list_posts(self, tag: Optional[str] = None, include_drafts: bool = False) -> List[ContentPost]:
        results = []
        for post in self.posts.values():
            if not include_drafts and not post.published:
                continue
            if tag and tag not in post.tags:
                continue
            results.append(post)

        results.sort(key=lambda p: p.date, reverse=True)
        return results
