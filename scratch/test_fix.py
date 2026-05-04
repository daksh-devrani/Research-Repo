
import sys
from pathlib import Path

# Add the project root to sys.path
sys.path.append(str(Path.cwd()))

from research.models import Vulnerability
from research.static_analysis.parser import FileAST
from research.static_analysis.signals import detect_package_usage

def test_detect_package_usage():
    # Mock FileASTs
    file_asts = [
        FileAST(
            path="app.py",
            imports=["flask", "yaml", "PIL.Image"],
            from_imports={"jwt": ["encode"]},
            aliases={"np": "numpy"}
        )
    ]

    test_cases = [
        ("Flask", True),        # Case mismatch
        ("PyYAML", True),       # Name mapping
        ("Pillow", True),       # Name mapping
        ("PyJWT", True),        # Name mapping
        ("requests", False),    # Not present
        ("numpy", True),        # Alias (though aliases are resolved in parser, let's check signals)
        ("ansible", False),     # Not present
    ]

    for pkg, expected in test_cases:
        vuln = Vulnerability(
            id="CVE-TEST",
            package=pkg,
            version="1.0",
            severity="HIGH",
            description="test"
        )
        used, locations = detect_package_usage(vuln, file_asts)
        print(f"Package: {pkg:10} | Used: {used:5} | Expected: {expected:5} | {'PASS' if used == expected else 'FAIL'}")

if __name__ == "__main__":
    test_detect_package_usage()
