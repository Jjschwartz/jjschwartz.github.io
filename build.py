#!/usr/bin/env python3
"""
This script builds a static website from Markdown content and HTML templates.
It processes blog posts, generates the homepage, and copies static assets.

Usage:
- uv run build.py

"""

from datetime import datetime
from html.parser import HTMLParser
from pathlib import Path
import re
import shutil
import traceback

import markdown
import yaml

from db import MY_NAME, PAPERS, PROJECTS


class TOCExtractor(HTMLParser):
    """Extract headings from HTML to generate table of contents"""

    def __init__(self):
        super().__init__()
        self.headings = []
        self.current_heading = None
        self.capture_text = False

    def handle_starttag(self, tag, attrs):
        if tag in ["h1", "h2", "h3", "h4", "h5", "h6"]:
            # Extract id from attributes if present
            heading_id = None
            for attr_name, attr_value in attrs:
                if attr_name == "id":
                    heading_id = attr_value
                    break

            self.current_heading = {
                "level": int(tag[1]),
                "tag": tag,
                "id": heading_id,
                "text": "",
            }
            self.capture_text = True

    def handle_endtag(self, tag):
        if tag in ["h1", "h2", "h3", "h4", "h5", "h6"] and self.current_heading:
            # Generate id if not present
            if not self.current_heading["id"]:
                self.current_heading["id"] = self.generate_id(
                    self.current_heading["text"]
                )

            self.headings.append(self.current_heading)
            self.current_heading = None
            self.capture_text = False

    def handle_data(self, data):
        if self.capture_text and self.current_heading:
            self.current_heading["text"] += data.strip()

    def generate_id(self, text):
        """Generate a URL-friendly id from heading text"""
        # Convert to lowercase, replace spaces with hyphens, remove special chars
        id_text = re.sub(r"[^a-zA-Z0-9\s-]", "", text.lower())
        id_text = re.sub(r"\s+", "-", id_text)
        return id_text.strip("-")


class SiteBuilder:
    def __init__(self):
        self.content_dir = Path("content")
        self.templates_dir = Path("templates")
        self.output_dir = Path("public")
        self.blog_posts = []

        # Site configuration - modify these values as needed
        self.config = {
            "title": "Jonathon Schwartz",
            "email": "jonathon.schwartz12@gmail.com",
            "github": "https://github.com/Jjschwartz",
            "scholar": "https://scholar.google.com.au/citations?user=cxKsPAYAAAAJ&hl",
            "name": "Jonathon Schwartz",
            "bio": (
                '<p>Hello! I am a researcher at <a href="https://imbue.com/">Imbue</a> '
                "where I work on building machine learning agents and software that "
                "help humans code.</p> "
                "<p>Previously, I completed my PhD at the Australian National "
                "University, advised by "
                '<a href="https://comp.anu.edu.au/people/hanna-kurniawati/">'
                "Hanna Kurniawati</a>. "
                "My thesis focused on building practical agents for partially "
                "observable, multi-agent environments by leveraging the combination "
                "of planning and reinforcement learning.</p>"
                "<p>When I'm not writing code or running experiments, I spend my time "
                "rock climbing and being outside in nature.</p>"
            ),
            "updated_at": datetime.now().strftime("%Y-%m-%d"),
        }

    def clean_output_dir(self):
        """Remove and recreate the output directory"""
        if self.output_dir.exists():
            shutil.rmtree(self.output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        print(f"✓ Cleaned output directory: {self.output_dir}")

    def load_template(self, template_name):
        """Load an HTML template from the templates directory"""
        template_path = self.templates_dir / f"{template_name}.html"
        if not template_path.exists():
            raise FileNotFoundError(f"Template not found: {template_path}")

        with open(template_path, "r", encoding="utf-8") as f:
            return f.read()

    def generate_toc_html(self, headings):
        """Generate HTML for table of contents"""
        if not headings:
            return ""

        # Filter headings to only include levels 1, 2, and 3 (h1, h2, h3)
        filtered_headings = [h for h in headings if h["level"] <= 3]

        if not filtered_headings:
            return ""

        html = '<nav class="toc">\n<ul class="toc-list">\n'

        for heading in filtered_headings:
            indent_class = f"toc-level-{heading['level']}"
            html += f'<li class="{indent_class}">'
            html += f'<a href="#{heading["id"]}" class="toc-link" data-target="{heading["id"]}">'
            html += f"{heading['text']}</a></li>\n"

        html += "</ul>\n</nav>"
        return html

    def add_heading_ids(self, html_content, headings):
        """Add id attributes to headings in HTML content"""
        for heading in headings:
            if heading["id"]:
                # Find the heading and add id attribute
                pattern = f"<{heading['tag']}>"
                replacement = f'<{heading["tag"]} id="{heading["id"]}">'
                html_content = html_content.replace(pattern, replacement, 1)

        return html_content

    def wrap_tables_in_containers(self, html_content):
        """Wrap tables in scrollable containers for horizontal scrolling"""
        import re

        # Pattern to match table tags
        table_pattern = r"(<table[^>]*>.*?</table>)"

        def wrap_table(match):
            table_html = match.group(1)
            return f'<div class="table-container">{table_html}</div>'

        # Replace all tables with wrapped versions
        html_content = re.sub(table_pattern, wrap_table, html_content, flags=re.DOTALL)

        return html_content

    def parse_blog_post(self, file_path):
        """Parse a Markdown blog post file and extract metadata"""
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        # Extract YAML frontmatter if present
        frontmatter = {}
        if content.startswith("---"):
            try:
                parts = content.split("---", 2)
                if len(parts) < 3:
                    raise ValueError("Invalid frontmatter format: missing closing ---")
                _, fm, content = parts
                frontmatter = yaml.safe_load(fm.strip())
                if frontmatter is None:
                    frontmatter = {}
            except yaml.YAMLError as e:
                raise ValueError(f"Invalid YAML in frontmatter: {e}") from e
            except Exception as e:
                raise ValueError(f"Could not parse frontmatter: {e}") from e

        # Extract date and slug from filename
        filename = file_path.stem
        date_match = re.match(r"^(\d{4}-\d{2}-\d{2})-(.+)$", filename)
        if not date_match:
            raise ValueError(
                f"Invalid filename format: {filename}. Expected: YYYY-MM-DD-title"
            )

        date_str, slug = date_match.groups()
        try:
            date = datetime.strptime(date_str, "%Y-%m-%d")
        except ValueError as e:
            raise ValueError(f"Invalid date format in filename {filename}: {e}") from e

        # Get title from frontmatter or generate from slug
        title = frontmatter.get("title", slug.replace("-", " ").title())

        return {
            "title": title,
            "date": date,
            "date_str": date.strftime("%B %d, %Y"),
            "slug": slug,
            "content": content.strip(),
            "frontmatter": frontmatter,
        }

    def process_blog_posts(self):
        """Process all blog posts and convert them to HTML"""
        blog_dir = self.content_dir / "blog"
        if not blog_dir.exists():
            print(f"Warning: Blog directory not found: {blog_dir}")
            return

        # Create blog output directory
        blog_output_dir = self.output_dir / "blog"
        blog_output_dir.mkdir(exist_ok=True)

        # Process each markdown file
        for md_file in blog_dir.glob("*.md"):
            try:
                post = self.parse_blog_post(md_file)
                self.blog_posts.append(post)

                # Convert markdown to HTML
                md = markdown.Markdown(
                    extensions=["tables", "fenced_code", "footnotes"]
                )
                post_html = md.convert(post["content"])

                # Wrap tables in scrollable containers
                post_html = self.wrap_tables_in_containers(post_html)

                # Extract headings for TOC
                toc_extractor = TOCExtractor()
                toc_extractor.feed(post_html)
                headings = toc_extractor.headings

                # Add id attributes to headings
                post_html = self.add_heading_ids(post_html, headings)

                # Generate TOC HTML
                toc_html = self.generate_toc_html(headings)

                # Load and fill post template
                post_template = self.load_template("post")
                base_template = self.load_template("base")

                # Fill post template
                post_content = post_template.replace("{{ title }}", post["title"])
                post_content = post_content.replace("{{ date }}", post["date_str"])
                post_content = post_content.replace("{{ content }}", post_html)
                post_content = post_content.replace("{{ toc }}", toc_html)
                post_content = post_content.replace(
                    "{{ site_name }}", self.config["name"]
                )
                post_content = post_content.replace(
                    "{{ current_year }}", str(datetime.now().year)
                )

                # Fill base template
                final_html = base_template.replace(
                    "{{ title }}", f"{post['title']} - {self.config['name']}"
                )
                final_html = final_html.replace(
                    "{{ description }}", f"Blog post: {post['title']}"
                )
                final_html = final_html.replace("{{ content }}", post_content)

                # Write output file
                output_file = blog_output_dir / f"{post['slug']}.html"
                with open(output_file, "w", encoding="utf-8") as f:
                    f.write(final_html)

                print(f"✓ Processed blog post: {post['title']}")

            except Exception as e:
                print(f"✗ Error processing {md_file}: {e}")

        # Sort posts by date (newest first)
        self.blog_posts.sort(key=lambda x: x["date"], reverse=True)
        print(f"✓ Processed {len(self.blog_posts)} blog posts")

    def generate_publications_html(self):
        """Generate HTML for the publications section"""
        html = ""
        for paper in PAPERS:
            html += '<div class="publication">\n'
            html += f'  <div class="publication-title">{paper.title}</div>\n'

            # Bold my name in the author list
            authors_text = paper.authors.replace(MY_NAME, f"<strong>{MY_NAME}</strong>")
            html += f"  <div>{authors_text}</div>\n"
            venue_year_block = '  <div class="publication-venue">'
            if paper.venue:
                venue_year_block += f"{paper.venue}"
            venue_year_block += f" ({paper.year})</div>\n"
            html += venue_year_block

            # Add links from urls dictionary
            if paper.urls:
                links = []
                for name, url in paper.urls.items():
                    links.append(f'<a href="{url}">{name}</a>')

                if links:
                    html += f"  <div>{' | '.join(links)}</div>\n"

            html += "</div>\n"

        return html

    def generate_projects_html(self):
        """Generate HTML for the projects section"""
        html = ""
        for project in PROJECTS:
            html += '<div class="project">\n'
            html += (
                f'  <a href="{project.url}" target="_blank" class="project-link">'
                f"{project.title}</a> {project.description}\n"
            )
            html += "</div>\n"

        return html

    def generate_recent_posts_html(self):
        """Generate HTML for recent blog posts"""
        html = ""
        recent_posts = self.blog_posts[:5]  # Show 5 most recent posts

        for post in recent_posts:
            html += '<div class="blog-post-item">\n'
            html += (
                f'  <div><a href="blog/{post["slug"]}.html">{post["title"]}</a></div>\n'
            )
            html += f'  <div class="blog-post-date">{post["date_str"]}</div>\n'
            html += "</div>\n"

        return html

    def generate_homepage(self):
        """Generate the homepage HTML"""
        # Load templates
        homepage_template = self.load_template("homepage")
        base_template = self.load_template("base")

        # Fill homepage template with content
        homepage_content = homepage_template.replace("{{ name }}", self.config["name"])
        homepage_content = homepage_content.replace("{{ bio }}", self.config["bio"])
        homepage_content = homepage_content.replace(
            "{{ publications }}", self.generate_publications_html()
        )
        homepage_content = homepage_content.replace(
            "{{ projects }}", self.generate_projects_html()
        )
        homepage_content = homepage_content.replace(
            "{{ recent_posts }}", self.generate_recent_posts_html()
        )
        homepage_content = homepage_content.replace(
            "{{ current_year }}", str(datetime.now().year)
        )
        homepage_content = homepage_content.replace(
            "{{ updated_at }}", self.config["updated_at"]
        )
        homepage_content = homepage_content.replace("{{ email }}", self.config["email"])
        homepage_content = homepage_content.replace(
            "{{ github }}", self.config["github"]
        )
        homepage_content = homepage_content.replace(
            "{{ scholar_url }}", self.config["scholar"]
        )

        # Fill base template
        final_html = base_template.replace("{{ title }}", self.config["title"])
        final_html = final_html.replace(
            "{{ description }}", f"Personal website of {self.config['name']}"
        )
        final_html = final_html.replace("{{ content }}", homepage_content)

        # Write homepage
        with open(self.output_dir / "index.html", "w", encoding="utf-8") as f:
            f.write(final_html)

        print("✓ Generated homepage")

    def copy_assets(self):
        """Copy static assets to the output directory"""
        assets_dir = self.content_dir / "assets"
        if not assets_dir.exists():
            print(f"Warning: Assets directory not found: {assets_dir}")
            return

        output_assets_dir = self.output_dir / "assets"
        if output_assets_dir.exists():
            shutil.rmtree(output_assets_dir)

        shutil.copytree(assets_dir, output_assets_dir)
        print(f"✓ Copied assets from {assets_dir} to {output_assets_dir}")

    def build(self):
        """Build the entire website"""
        print("Building website...")
        start_time = datetime.now()

        # Build steps
        self.clean_output_dir()
        self.process_blog_posts()
        self.generate_homepage()
        self.copy_assets()

        # Calculate build time
        build_time = (datetime.now() - start_time).total_seconds()

        print(f"\n✅ Website built successfully in {build_time:.3f} seconds")
        print(f"📁 Output directory: {self.output_dir.absolute()}")
        print(
            f"🌐 Open {self.output_dir.absolute()}/index.html "
            "in your browser to view the site"
        )


def main():
    """Main entry point"""
    try:
        builder = SiteBuilder()
        builder.build()
    except Exception as e:
        print(f"❌ Build failed: {e}")

        traceback.print_exc()
        return 1

    return 0


if __name__ == "__main__":
    exit(main())
