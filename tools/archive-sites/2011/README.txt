QuinnDamerell.com historical-site recovery tools

Dependencies: Python 3.10+, beautifulsoup4, curl. Original website scripts are never executed. Install BeautifulSoup in a virtual environment or with pip install beautifulsoup4.

Keep mirror.py, retry.py, and publish.py together. Run from the repository root, or pass --repo-root explicitly. --output and --cache accept arbitrary directories. Recovery output resumes from manifest.json when the temporary cache is gone; publication works entirely from retained raw files and manifest.json.

Initial/resumed breadth-first recovery:
python mirror.py --repo-root PATH --output OUTPUT --cache CACHE --target 20110116181801 --home http://www.quinndamerell.com/index.php --workers 2

One bounded retry of unavailable resources (optional alternate timestamp):
python retry.py --repo-root PATH --output OUTPUT --cache CACHE --target 20110116181801 --alternate-timestamp 20110819004107 --workers 1

Continue discovery if a retry recovers pages or stylesheets:
python mirror.py --repo-root PATH --output OUTPUT --cache CACHE --target 20110116181801

Render the static archive from retained sources (no network):
python publish.py --repo-root PATH --output OUTPUT --cache CACHE --target 20110116181801

All commands also accept --fallback-archive PATH for an archive containing verified raw bytes and manifest.json (and optionally history/manifest.json). Target-date requests are attempted before fallback captures. The existing 2012 archive is the repository default fallback. Retrieval validates HTTP200, Memento capture dates and content kind, rejecting HTML homepages masquerading as image assets. A 24.9MB retrieval limit is recorded as a failed attempt if reached; no recovered file in this collection reached it.

The publisher removes original scripts, event handlers, embeds, active forms and tracking. One inspected DOM-only helper provides local photo accordions, galleries, video tabs and available image rollovers. Metadata distinguishes source hashes from served hashes and retains retrieval failures. Source-linked missing resources receive explicit local gap pages. No server features are emulated.

The crawler handles this site's historical markup and known PHP session parameter; it is not a general authenticated website copier. External links are preserved but not recursively mirrored. Historical Flash/Java players do not run. Query parameters other than PHPSESSID remain significant.
