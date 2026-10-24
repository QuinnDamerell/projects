#!/usr/bin/env python3
"""Create and verify website.zip for a complete local website archive.

    python tools/package_site_archive.py docs/assets/media/<slug>

The existing ZIP is replaced only after its replacement passes byte-for-byte
verification and the 25 MB hosting limit. No archive source files are changed.
"""

import argparse
import hashlib
import json
from pathlib import Path
import tempfile
import zipfile


def package_archive(root: Path) -> dict:
    root = root.resolve(strict=True)
    for required in ('snapshot.html', 'manifest.json', 'archive-index.html'):
        if not (root / required).is_file():
            raise ValueError(f'Not a website archive: missing {required}')
    destination = root / 'website.zip'
    files = []
    for source in sorted(root.rglob('*')):
        if source.is_symlink():
            raise ValueError(f'Symlinks are not supported in an archive: {source}')
        if source.is_file() and source != destination:
            if source.stat().st_size > 25_000_000:
                raise ValueError(f'File exceeds the hosting limit: {source}')
            files.append(source)
    expected = {
        source.relative_to(root).as_posix(): hashlib.sha256(source.read_bytes()).digest()
        for source in files
    }
    with tempfile.NamedTemporaryFile(prefix='site-archive-', suffix='.zip', delete=False) as output:
        temporary = Path(output.name)
    try:
        with zipfile.ZipFile(temporary, 'w', zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
            for source in files:
                archive.write(source, source.relative_to(root).as_posix())
        if temporary.stat().st_size > 25_000_000:
            raise ValueError('ZIP exceeds the 25 MB hosting limit; host the package on R2.')
        with zipfile.ZipFile(temporary) as archive:
            if archive.testzip() is not None or set(archive.namelist()) != set(expected):
                raise ValueError('ZIP contents failed verification')
            for name, digest in expected.items():
                if hashlib.sha256(archive.read(name)).digest() != digest:
                    raise ValueError(f'ZIP content mismatch: {name}')
                if hashlib.sha256((root / name).read_bytes()).digest() != digest:
                    raise ValueError(f'Source changed during packaging: {name}; retry after recovery finishes')
        # Copy into the destination directory before replacing, including when
        # the system temporary directory and repository are on different drives.
        import shutil
        with tempfile.NamedTemporaryFile(prefix='.website-', suffix='.tmp', dir=root, delete=False) as output:
            replacement = Path(output.name)
        try:
            shutil.copyfile(temporary, replacement)
            replacement.replace(destination)
        finally:
            replacement.unlink(missing_ok=True)
        return {'archive': str(destination), 'files': len(files), 'bytes': destination.stat().st_size}
    finally:
        temporary.unlink(missing_ok=True)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('archive', type=Path)
    args = parser.parse_args()
    try:
        print(json.dumps(package_archive(args.archive), indent=2))
    except (OSError, ValueError, zipfile.BadZipFile) as error:
        parser.exit(1, f'{error}\n')


if __name__ == '__main__':
    main()
