import pytest
from markdown_cms.parser import FrontmatterParser
from markdown_cms.cms import MarkdownCMS


def test_frontmatter_parser():
    md = """---
title: "FastAPI bilan REST API yaratish"
slug: "fastapi-rest-api"
date: "2026-05-10"
tags: [python, fastapi, backend]
published: true
summary: "Ushbu maqolada FastAPI asoslari o'rganiladi."
---

# FastAPI ga Kirish

FastAPI - bu Python uchun zamonaviy, tezkor (yuqori unumdor) veb freymvork.
U OpenAPI va JSON Schema standartlariga asoslangan.
"""
    post = FrontmatterParser.parse(md)
    assert post.title == "FastAPI bilan REST API yaratish"
    assert post.slug == "fastapi-rest-api"
    assert post.tags == ["python", "fastapi", "backend"]
    assert post.published is True
    assert "FastAPI ga Kirish" in post.body_markdown
    assert post.reading_time_minutes >= 1


def test_markdown_cms_directory_index(tmp_path):
    p1 = tmp_path / "post1.md"
    p1.write_text("""---
title: "Post 1"
date: "2026-01-01"
published: true
tags: [news]
---
Birinchi yangilik
""")

    p2 = tmp_path / "draft.md"
    p2.write_text("""---
title: "Qoralama Post"
date: "2026-02-01"
published: false
tags: [dev]
---
Bu qoralama matn
""")

    cms = MarkdownCMS(str(tmp_path))
    cms.reload()

    # Drafts ko'rinmasligi kerak
    public_posts = cms.list_posts(include_drafts=False)
    assert len(public_posts) == 1
    assert public_posts[0].title == "Post 1"

    # Drafts bilan
    all_posts = cms.list_posts(include_drafts=True)
    assert len(all_posts) == 2

    # Slug orqali olish
    post = cms.get_post("post1")
    assert post is not None
    assert post.title == "Post 1"
