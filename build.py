#!/usr/bin/env python3
"""
Static Site Generator for Personal Academic Website

This script builds a static website from Markdown content and HTML templates.
It processes blog posts, generates the homepage, and copies static assets.

Usage: python build.py

Requirements:
- Python 3.8+
- python-markdown library
"""

import os
import shutil
import re
from datetime import datetime
from pathlib import Path
import markdown
import yaml

class SiteBuilder:
    def __init__(self):
        self.content_dir = Path("content")
        self.templates_dir = Path("templates")
        self.output_dir = Path("public")
        self.blog_posts = []
        
        # Site configuration - modify these values as needed
        self.config = {
            'name': 'Dr. Alex Smith',
            'bio': '''<p>I am a researcher in computer science with a focus on machine learning and artificial intelligence. 
                     My work spans theoretical foundations and practical applications of AI systems.</p>
                     <p>I am currently a postdoctoral researcher at Example University, where I work on developing 
                     more interpretable and robust machine learning models.</p>''',
            'research_description': '''I research the intersection of machine learning theory and practice, 
                                    with particular interest in explainable AI and robustness of neural networks.''',
            'blog_description': '''I write about machine learning research, academic life, and thoughts on the future of AI.''',
            'publications': [
                {
                    'title': 'Understanding Deep Learning Through Information Theory',
                    'year': 2023,
                    'authors': 'Alex Smith, Jane Doe, John Wilson',
                    'venue': 'International Conference on Machine Learning (ICML)',
                    'pdf_url': 'assets/papers/smith2023understanding.pdf',
                    'arxiv_url': 'https://arxiv.org/abs/2301.12345'
                },
                {
                    'title': 'Robust Neural Networks: A Survey',
                    'year': 2022,
                    'authors': 'Alex Smith, Sarah Johnson',
                    'venue': 'Journal of Machine Learning Research',
                    'pdf_url': 'assets/papers/smith2022robust.pdf'
                }
            ]
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
        
        with open(template_path, 'r', encoding='utf-8') as f:
            return f.read()
    
    def parse_blog_post(self, file_path):
        """Parse a Markdown blog post file and extract metadata"""
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Extract YAML frontmatter if present
        frontmatter = {}
        if content.startswith('---'):
            try:
                parts = content.split('---', 2)
                if len(parts) < 3:
                    raise ValueError("Invalid frontmatter format: missing closing ---")
                _, fm, content = parts
                frontmatter = yaml.safe_load(fm.strip())
                if frontmatter is None:
                    frontmatter = {}
            except yaml.YAMLError as e:
                raise ValueError(f"Invalid YAML in frontmatter: {e}")
            except Exception as e:
                raise ValueError(f"Could not parse frontmatter: {e}")
        
        # Extract date and slug from filename
        filename = file_path.stem
        date_match = re.match(r'^(\d{4}-\d{2}-\d{2})-(.+)$', filename)
        if not date_match:
            raise ValueError(f"Invalid filename format: {filename}. Expected: YYYY-MM-DD-title")
        
        date_str, slug = date_match.groups()
        try:
            date = datetime.strptime(date_str, '%Y-%m-%d')
        except ValueError as e:
            raise ValueError(f"Invalid date format in filename {filename}: {e}")
        
        # Get title from frontmatter or generate from slug
        title = frontmatter.get('title', slug.replace('-', ' ').title())
        
        return {
            'title': title,
            'date': date,
            'date_str': date.strftime('%B %d, %Y'),
            'slug': slug,
            'content': content.strip(),
            'frontmatter': frontmatter
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
                md = markdown.Markdown(extensions=['codehilite', 'tables', 'fenced_code'])
                post_html = md.convert(post['content'])
                
                # Load and fill post template
                post_template = self.load_template('post')
                base_template = self.load_template('base')
                
                # Fill post template
                post_content = post_template.replace('{{ title }}', post['title'])
                post_content = post_content.replace('{{ date }}', post['date_str'])
                post_content = post_content.replace('{{ content }}', post_html)
                post_content = post_content.replace('{{ site_name }}', self.config['name'])
                post_content = post_content.replace('{{ current_year }}', str(datetime.now().year))
                
                # Fill base template
                final_html = base_template.replace('{{ title }}', f"{post['title']} - {self.config['name']}")
                final_html = final_html.replace('{{ description }}', f"Blog post: {post['title']}")
                final_html = final_html.replace('{{ content }}', post_content)
                
                # Write output file
                output_file = blog_output_dir / f"{post['slug']}.html"
                with open(output_file, 'w', encoding='utf-8') as f:
                    f.write(final_html)
                
                print(f"✓ Processed blog post: {post['title']}")
                
            except Exception as e:
                print(f"✗ Error processing {md_file}: {e}")
        
        # Sort posts by date (newest first)
        self.blog_posts.sort(key=lambda x: x['date'], reverse=True)
        print(f"✓ Processed {len(self.blog_posts)} blog posts")
    
    def generate_publications_html(self):
        """Generate HTML for the publications section"""
        html = ""
        for pub in self.config['publications']:
            html += '<div class="publication">\n'
            html += f'  <div class="publication-title">{pub["title"]}</div>\n'
            html += f'  <div>{pub["authors"]} ({pub["year"]})</div>\n'
            html += f'  <div class="publication-venue">{pub["venue"]}</div>\n'
            
            # Add links
            links = []
            if 'pdf_url' in pub:
                links.append(f'<a href="{pub["pdf_url"]}">PDF</a>')
            if 'arxiv_url' in pub:
                links.append(f'<a href="{pub["arxiv_url"]}">arXiv</a>')
            
            if links:
                html += f'  <div>{" | ".join(links)}</div>\n'
            
            html += '</div>\n'
        
        return html
    
    def generate_recent_posts_html(self):
        """Generate HTML for recent blog posts"""
        html = ""
        recent_posts = self.blog_posts[:5]  # Show 5 most recent posts
        
        for post in recent_posts:
            html += '<div class="blog-post-item">\n'
            html += f'  <div><a href="blog/{post["slug"]}.html">{post["title"]}</a></div>\n'
            html += f'  <div class="blog-post-date">{post["date_str"]}</div>\n'
            html += '</div>\n'
        
        return html
    
    def generate_homepage(self):
        """Generate the homepage HTML"""
        # Load templates
        homepage_template = self.load_template('homepage')
        base_template = self.load_template('base')
        
        # Fill homepage template with content
        homepage_content = homepage_template.replace('{{ name }}', self.config['name'])
        homepage_content = homepage_content.replace('{{ bio }}', self.config['bio'])
        homepage_content = homepage_content.replace('{{ research_description }}', self.config['research_description'])
        homepage_content = homepage_content.replace('{{ blog_description }}', self.config['blog_description'])
        homepage_content = homepage_content.replace('{{ publications }}', self.generate_publications_html())
        homepage_content = homepage_content.replace('{{ recent_posts }}', self.generate_recent_posts_html())
        homepage_content = homepage_content.replace('{{ current_year }}', str(datetime.now().year))
        
        # Fill base template
        final_html = base_template.replace('{{ title }}', self.config['name'])
        final_html = final_html.replace('{{ description }}', f"Personal website of {self.config['name']}")
        final_html = final_html.replace('{{ content }}', homepage_content)
        
        # Write homepage
        with open(self.output_dir / "index.html", 'w', encoding='utf-8') as f:
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
        print(f"🌐 Open {self.output_dir.absolute()}/index.html in your browser to view the site")

def main():
    """Main entry point"""
    try:
        builder = SiteBuilder()
        builder.build()
    except Exception as e:
        print(f"❌ Build failed: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())