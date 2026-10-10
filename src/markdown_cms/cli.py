import argparse
import sys
import json
from .cms import MarkdownCMS
from .parser import FrontmatterParser


def main():
    parser = argparse.ArgumentParser(description="Markdown CMS API - Flat-file Markdown boshqaruvi")
    subparsers = parser.add_subparsers(dest="command", required=True)

    parse_p = subparsers.add_parser("parse", help="Alohida Markdown faylini tahlil qilish")
    parse_p.add_argument("file", help="Markdown fayli yo'li")

    list_p = subparsers.add_parser("list", help="Papkadagi postlar ro'yxati")
    list_p.add_argument("--dir", default="./content", help="Kontent papkasi")
    list_p.add_argument("--tag", help="Teg bo'yicha filter")
    list_p.add_argument("--drafts", action="store_true", help="Qoralamalarni ham ko'rsatish")

    args = parser.parse_args()

    if args.command == "parse":
        with open(args.file, "r", encoding="utf-8") as f:
            post = FrontmatterParser.parse(f.read())
        print(f"Title: {post.title} (Slug: {post.slug})")
        print(f"Date: {post.date} | Published: {post.published} | Reading Time: ~{post.reading_time_minutes} min")
        print(f"Tags: {', '.join(post.tags)}")
        print(f"Summary: {post.summary}")
    elif args.command == "list":
        cms = MarkdownCMS(args.dir)
        total = cms.reload()
        posts = cms.list_posts(tag=args.tag, include_drafts=args.drafts)
        print(f"Jami postlar: {len(posts)} ta (papka yuklandi: {total})")
        for p in posts:
            status = " [DRAFT]" if not p.published else ""
            print(f"• [{p.date}] {p.title}{status} -> /{p.slug} ({', '.join(p.tags)})")


if __name__ == "__main__":
    main()
