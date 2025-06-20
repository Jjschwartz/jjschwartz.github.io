# My Website

A minimal static website. Includes a simple markdown to html generator.

## Quick Start

1. **Build the site**:

   ```bash
   uv run build.py
   ```

2. **View the site**:

  ```bash
  open `public/index.html`
  # or open in your browser
  ```

## Project Structure

```text
├── build.py              # Static site generator script
├── pyproject.toml        # Python dependencies
├── uv.lock               # Python dependencies
├── content/              # Content source files
│   ├── blog/             # Blog posts (Markdown)
│   └── assets/           # Static assets
│       ├── images/       # Images (including profile photo)
│       └── papers/       # Research papers (PDFs)
├── templates/            # HTML templates
│   ├── base.html         # Base template with common HTML structure
│   ├── homepage.html     # Homepage layout
│   └── post.html         # Blog post layout
└── public/               # Generated website (output)
    ├── index.html        # Homepage
    ├── blog/             # Individual blog post pages
    └── assets/           # Copied static assets
```

## Adding Content

### Adding a New Blog Post

1. Create a new Markdown file in `content/blog/` with the naming convention:

   ```text
   YYYY-MM-DD-post-title.md
   ```

2. Add YAML frontmatter at the top:

   ```markdown
   ---
   title: Your Post Title
   ---
   
   Your content here...
   ```

3. Run the build script:

   ```bash
   python build.py
   ```

### Customize the site

Edit the configuration in `build.py` to customize:

- Your name and bio
- Research description
- Publications list
- Blog description

Example configuration:

```python
self.config = {
    'name': 'Your Name',
    'bio': '<p>Your bio here...</p>',
    'research_description': 'Description of your research...',
    'blog_description': 'What you blog about...',
    'publications': [
        {
            'title': 'Paper Title',
            'year': 2024,
            'authors': 'Author List',
            'venue': 'Conference/Journal Name',
            'pdf_url': 'assets/papers/paper.pdf',
            'arxiv_url': 'https://arxiv.org/abs/...'
        }
    ]
}
```

### Adding Assets

- **Profile photo**: Place profile image at `content/assets/images/profile.jpg`
- **Research papers**: Add PDFs to `content/assets/papers/`
- **Other images**: Add to `content/assets/images/`

## Local Development

### Serving the Site Locally

You can use Python's built-in server to preview your site:

```bash
# After building
cd public
uv run python -m http.server 8000
```

Then visit `http://[::]:8000` in your browser.

## Customization

### Styling

The site uses [Pico.css](https://picocss.com/) for styling. You can:

1. **Customize colors**: Pico.css supports CSS custom properties
2. **Add custom CSS**: Edit the `<style>` section in `templates/base.html`
3. **Override Pico defaults**: Add your own CSS rules

### Templates

The site uses three templates:

- `base.html`: Common HTML structure, includes Pico.css
- `homepage.html`: Layout for the main page
- `post.html`: Layout for individual blog posts

Templates use simple `{{ variable }}` syntax for content replacement.
