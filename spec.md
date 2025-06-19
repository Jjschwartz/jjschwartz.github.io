# Personal Website Technical Specification

## Project Overview

A minimal static website for an academic/developer to share research papers and blog posts. The site should prioritize simplicity, fast load times, and ease of content creation.

## Core Requirements

### Technology Stack

- Static site generator using a custom Python build script
- Markdown files for blog post content
- Pico.css for styling (loaded from CDN)
- GitHub Pages for hosting
- No JavaScript required in the final output

### Design Principles

- Minimal external dependencies
- Fast build times (< 1 second)
- Clean, semantic HTML output
- Mobile-responsive design
- Perfect Lighthouse performance scores (target: 100/100)

## Site Structure

### Homepage (`index.html`)

The homepage should be a single-page layout with the following sections:

1. **Navigation Bar**
   - Fixed position with links to: About, Research, Blog
   - Clicking links should smooth-scroll to respective sections

2. **About Section**
   - Profile image (circular, centered)
   - Name as main heading
   - Bio paragraph(s) describing background and interests

3. **Research Section**
   - Brief description of research focus
   - List of key publications with:
     - Paper title (bold)
     - Year of publication
     - Co-authors
     - Conference/Journal name (italicized)
     - Links to PDF and/or arXiv

4. **Blog Section**
   - Brief description of blog topics
   - List of 5 most recent blog posts showing:
     - Post title (linked to full post)
     - Publication date
   - "View all posts" link at bottom

5. **Footer**
   - Copyright notice with current year

### Blog Posts

- Each post should be its own HTML page
- URL structure: `/blog/[post-slug].html`
- Post pages should include:
  - Navigation back to homepage
  - Post title
  - Publication date
  - Post content (converted from Markdown)
  - Footer with "Back to home" link

## Content Management

### Blog Post Creation

- Posts written in Markdown format
- Stored in `content/blog/` directory
- Filename convention: `YYYY-MM-DD-post-title.md`
- Date should be extracted from filename
- URL slug generated from title portion of filename

### Markdown Support

- Standard Markdown syntax
- Code blocks with syntax highlighting
- Tables
- YAML frontmatter for metadata (minimum: title)

### Asset Management

- Static assets stored in `content/assets/`
- Should include subdirectories for:
  - Images (including profile photo)
  - PDFs (research papers)
- Assets should be copied to output directory during build

## Build System Requirements

### Build Script (`build.py`)

The Python build script should:

1. Clean previous build output
2. Process all Markdown files in `content/blog/`
3. Convert Markdown to HTML
4. Apply HTML templates
5. Generate the homepage with dynamic blog listing
6. Copy static assets to output directory
7. Maintain proper directory structure in output

### Input Structure

```text
content/
  blog/
    YYYY-MM-DD-post-title.md
  assets/
    profile.jpg
    papers/
      paper1.pdf
```

### Output Structure

```text
public/
  index.html
  blog/
    post-title.html
  assets/
    profile.jpg
    papers/
      paper1.pdf
```

## Templates

### Required Templates

1. **Base template**: Common HTML structure with Pico.css
2. **Homepage template**: Layout for index.html
3. **Post template**: Layout for individual blog posts

### Template Features

- Placeholder variables for dynamic content
- Clean, semantic HTML5 markup
- Pico.css included via CDN
- Minimal custom CSS only where necessary

## Development Workflow

### Local Development

- Simple command to build: `python build.py`
- Clear console output showing build progress
- Local preview server command should be documented

### Adding Content

1. Create new Markdown file with proper naming convention
2. Run build script
3. Commit changes
4. Push to GitHub (triggers deployment)

## Deployment

### GitHub Pages Setup

- Site should be deployable to GitHub Pages
- Option 1: GitHub Actions workflow for automatic building
- Option 2: Build locally and push to `gh-pages` branch
- Clear documentation for both approaches

## Non-Functional Requirements

### Performance

- Total page weight < 100KB (excluding images)
- Build time < 1 second for 100 posts
- Zero JavaScript in production build

### Accessibility

- Semantic HTML structure
- Proper heading hierarchy
- Alt text for images
- Sufficient color contrast (handled by Pico.css)

### SEO

- Proper meta tags
- Clean URL structure
- Valid HTML markup

## Dependencies

### Python Requirements

- Python 3.8 or higher
- python-markdown library
- No other external dependencies

### Frontend Dependencies

- Pico.css (CDN-hosted, no local copy needed)
- No JavaScript libraries
- No build tools (webpack, etc.)

## Documentation Requirements

### README.md should include

- Project setup instructions
- How to add new blog posts
- How to update research section
- Build and deployment instructions
- Troubleshooting common issues

### Code Comments

- Build script should be well-commented
- Template files should include usage instructions

## Future Considerations (Out of Scope)

The following features are not required but the architecture should not prevent their future addition:

- RSS feed generation
- Blog post tags/categories
- Search functionality
- Comments system
- Analytics

## Acceptance Criteria

1. Homepage displays all sections with smooth navigation
2. Blog posts correctly convert from Markdown to HTML
3. All links function correctly
4. Site builds in under 1 second
5. Output passes HTML validation
6. Achieves 95+ Lighthouse scores
7. Responsive design works on mobile devices
8. GitHub Pages deployment functions correctly
