---
name: wget-crawler
description: "Smart site mirroring and bulk file downloading using wget. Use when user wants to crawl a website, mirror/clone a site locally, recursively download files of specific formats (PDFs, images, ZIPs, etc.), or archive sections of a site. Triggers on: crawl, mirror, clone site, download all files from, or wget. Does NOT trigger for: curl usage, reading one or few URLs, UI/UX debugging, scraping a single page, or browsing a site."
---

# wget-crawler

## Overview

Guide the user through a smart wget mirroring session: ask key decisions upfront, construct
the optimal wget command, and explain every flag used. Handles partial crawls, full clones,
format-filtered downloads, and rate-limited polite mirroring.

## Step 1 — Ask Decision Questions

Before building any command, ask the user these questions (group them, don't ask one at a time):

**Required decisions:**
1. **Scope** — Full site mirror, specific section/subdirectory, or specific file formats only?
2. **Depth** — Max recursion depth? (e.g. 2 = two levels below start URL; `inf` = unlimited)
3. **File formats** — Download everything, or specific extensions? (e.g. `pdf,zip,xlsx,mp4`)
4. **Output location** — Where to save locally? (default: current directory)

**Optional but important:**
5. **Stay on domain?** — Follow links only within the same domain/host? (almost always yes)
6. **Rate limiting** — Polite crawl (`--wait=1 --limit-rate=500k`) or fast as possible?
7. **Auth** — Does the site require login? (HTTP Basic, cookies, or form-based?)
8. **Resume support** — Continue interrupted download? (`-c` flag)

Skip questions that the user already answered in their request.

## Step 2 — Build the Command

Use the reference below to construct the command. Always show the full command with
explanation of each flag before running.

### Core Patterns

#### Full site mirror (offline browsing)
```bash
wget \
  --mirror \
  --convert-links \
  --adjust-extension \
  --page-requisites \
  --no-parent \
  --wait=1 \
  --limit-rate=500k \
  -P ./mirror-output \
  https://example.com/
```

#### Recursive download of specific file types
```bash
wget \
  --recursive \
  --no-clobber \
  --no-parent \
  --domains example.com \
  --accept pdf,xlsx,zip \
  --level=3 \
  -P ./downloads \
  https://example.com/resources/
```

#### Single-section archive (no external links)
```bash
wget \
  --recursive \
  --level=2 \
  --no-parent \
  --no-host-directories \
  --cut-dirs=2 \
  -P ./section-output \
  https://example.com/docs/
```

#### Resume interrupted download
```bash
wget -c --recursive --no-parent -P ./output https://example.com/
```

## Step 3 — Flag Reference

Use this to tune commands to user needs. Load only the relevant sections.

### Recursion & Scope
| Flag | Effect |
|------|--------|
| `--recursive` / `-r` | Enable recursive download |
| `--mirror` / `-m` | Shorthand for `-r -N -l inf --no-remove-listing` |
| `--level=N` / `-l N` | Max recursion depth (0 = infinite, default 5) |
| `--no-parent` / `-np` | Don't ascend to parent directories |
| `--domains=LIST` | Comma-separated list of accepted domains |
| `--exclude-domains=LIST` | Domains to never follow |
| `--span-hosts` / `-H` | Follow links to other hosts |
| `--include-directories=LIST` | Only recurse into these paths |
| `--exclude-directories=LIST` | Skip these paths |

### File Filtering
| Flag | Effect |
|------|--------|
| `--accept=LIST` / `-A LIST` | Accept only these extensions (e.g. `pdf,jpg,png`) |
| `--reject=LIST` / `-R LIST` | Reject these extensions |
| `--accept-regex=REGEX` | Accept URLs matching regex |
| `--reject-regex=REGEX` | Reject URLs matching regex |
| `--ignore-case` | Case-insensitive `-A`/`-R` matching |

### Output & File Handling
| Flag | Effect |
|------|--------|
| `-P DIR` / `--directory-prefix=DIR` | Save files under DIR |
| `--no-clobber` / `-nc` | Skip files that already exist |
| `-c` / `--continue` | Resume partially downloaded files |
| `--adjust-extension` | Add `.html` to HTML files missing extension |
| `--no-host-directories` | Don't create hostname directory |
| `--cut-dirs=N` | Strip N path components from saved path |
| `--restrict-file-names=unix` | Fix Windows-unsafe characters in filenames |

### Link & Page Handling
| Flag | Effect |
|------|--------|
| `--convert-links` / `-k` | Rewrite links for offline browsing |
| `--page-requisites` / `-p` | Download CSS, images needed to render page |
| `--html-extension` | Save HTML with `.html` extension |
| `--backup-converted` | Back up files before converting links |

### Rate & Politeness
| Flag | Effect |
|------|--------|
| `--wait=N` | Wait N seconds between requests |
| `--random-wait` | Randomize wait (0.5x–1.5x `--wait` value) |
| `--limit-rate=RATE` | Throttle download (e.g. `500k`, `2m`) |
| `--tries=N` / `-t N` | Retry failed downloads N times (0=infinite) |
| `--timeout=N` | Timeout per connection in seconds |

### Authentication
| Flag | Effect |
|------|--------|
| `--http-user=USER` | HTTP Basic auth username |
| `--http-password=PASS` | HTTP Basic auth password |
| `--load-cookies=FILE` | Use cookies from file (Netscape format) |
| `--save-cookies=FILE` | Save received cookies to file |
| `--keep-session-cookies` | Keep session (non-persistent) cookies |
| `--post-data=STRING` | Send POST data (for form-based login) |

### Logging & Debugging
| Flag | Effect |
|------|--------|
| `-q` / `--quiet` | Suppress output |
| `-nv` / `--no-verbose` | Minimal output |
| `-v` / `--verbose` | Full verbose output |
| `--progress=bar` | Show progress bar |
| `-o FILE` | Log to file |
| `-a FILE` | Append log to file |
| `--debug` | Print debugging info |
| `--spider` | Dry-run: check links without downloading |

### Timestamps & Caching
| Flag | Effect |
|------|--------|
| `-N` / `--timestamping` | Only download if remote file is newer |
| `--no-cache` | Disable server-side caching |
| `--no-if-modified-since` | Don't use conditional GET |

## Step 4 — Common Gotchas

- **`--mirror` already includes** `-r -N -l inf --no-remove-listing`. Don't double-specify.
- **`--convert-links` conflicts** with incremental updates — only use for one-shot offline archives.
- **`--page-requisites` ignores `--level`** — it always fetches inline assets regardless of depth.
- **Dynamic/JS-rendered sites** — wget only fetches static HTML. Use Playwright/Puppeteer for SPAs.
- **robots.txt** — wget respects it by default. Add `-e robots=off` to ignore (respect site ToS).
- **Large sites** — always add `--wait` and `--limit-rate` to avoid IP bans.
- **`--no-parent` is critical** for section downloads — omitting it causes wget to crawl the entire site.
- **Cookies for auth** — export from browser using a "Get cookies.txt" extension, then `--load-cookies=cookies.txt`.

## Step 5 — Present & Confirm

Show the final command with a brief explanation of each flag chosen. Ask for confirmation
before running, especially if the crawl could be large or the site requires auth.

After confirming, offer to:
- Run with `--spider` first (dry run, lists URLs without downloading)
- Estimate size with `--spider -nv 2>&1 | grep -i "saved"` pattern
- Run the actual download
