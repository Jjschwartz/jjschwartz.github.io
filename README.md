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

- **Profile photo**: Place your image at `content/assets/images/profile.jpg`
- **Research papers**: Add PDFs to `content/assets/papers/`
- **Other images**: Add to `content/assets/images/`

## Local Development

### Serving the Site Locally

You can use Python's built-in server to preview your site:

```bash
# After building
cd public
python -m http.server 8000
```

Then visit `http://localhost:8000` in your browser.

### Development Workflow

1. Make changes to content or templates
2. Run `python build.py`
3. Refresh your browser to see changes

## Deployment

### GitHub Pages

This site is designed to work with GitHub Pages. You have two deployment options:

#### Option 1: GitHub Actions (Recommended)

Create `.github/workflows/build.yml`:

```yaml
name: Build and Deploy
on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  build-and-deploy:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
    
    - name: Setup Python
      uses: actions/setup-python@v2
      with:
        python-version: '3.9'
    
    - name: Install dependencies
      run: |
        pip install -r requirements.txt
    
    - name: Build site
      run: python build.py
    
    - name: Deploy to GitHub Pages
      uses: peaceiris/actions-gh-pages@v3
      if: github.ref == 'refs/heads/main'
      with:
        github_token: ${{ secrets.GITHUB_TOKEN }}
        publish_dir: ./public
```

#### Option 2: Manual Build and Deploy

```bash
# Build the site
python build.py

# Switch to gh-pages branch
git checkout gh-pages

# Copy built files
cp -r public/* .

# Commit and push
git add .
git commit -m "Update site"
git push origin gh-pages
```

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

## Performance

The generated site is optimized for performance:

- **Minimal CSS**: Only Pico.css loaded from CDN
- **No JavaScript**: Pure HTML/CSS for maximum speed
- **Optimized images**: Use appropriate formats and sizes
- **Clean HTML**: Semantic markup for better SEO

Target Lighthouse scores: 100/100 across all categories.

## Troubleshooting

### Common Issues

1. **Build fails with missing template**: Ensure all template files exist in `templates/`
2. **Blog posts not showing**: Check filename format: `YYYY-MM-DD-title.md`
3. **Images not loading**: Verify file paths in `content/assets/`
4. **Markdown not rendering**: Install required dependencies with `pip install -r requirements.txt`

### Getting Help

1. Check that your content follows the expected format
2. Verify all file paths are correct
3. Run `python build.py` and check for error messages
4. Ensure Python 3.8+ is installed

## License

This project is open source and available under the [MIT License](LICENSE).
