# Markdown CMS API

Git repozitoriysiga asoslangan flat-file fayllardan ishlovchi, YAML frontmatter tahlil qiluvchi, teglash va o'qish vaqtini hisoblovchi yengil headless Markdown CMS dvigateli.

## Xususiyatlari
- **0 Baza (Flat-file)**: Hech qanday murakkab SQL/NoSQL bazalarsiz to'g'ridan-to'g'ri `.md` fayllardan o'qiydi.
- **YAML Frontmatter**: Sarlavha, sana, teglar, slug, qoralama (draft/published) holatlarini tahlil qilish.
- **Tezkor Kesh**: Xotirada keshlab, millisoniyalarda REST/GraphQL darajasida javob qaytarish.
- **Avtomatlashtirilgan Metrikalar**: So'zlar soni asosida o'qish davomiyligini (reading time) hisoblash.

## Foydalanish (Python)
```python
from markdown_cms import MarkdownCMS

cms = MarkdownCMS("./content")
cms.reload()

# E'lon qilingan maqolalar
posts = cms.list_posts(tag="python")
for p in posts:
    print(p.title, p.slug, p.reading_time_minutes)

# Slug bo'yicha maqolani olish
post = cms.get_post("fastapi-guide")
print(post.body_markdown)
```

## CLI
```bash
markdown-cms list --dir ./content --tag python
markdown-cms parse article.md
```

## Testlar
```bash
pytest tests/ -v
```

## Litsenziya
MIT
