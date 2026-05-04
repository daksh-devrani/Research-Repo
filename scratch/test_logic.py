
# Minimal reproduction of the logic in signals.py to test normalization

PKG_TO_MODULE_MAP = {
    "pyyaml": "yaml",
    "pillow": "PIL",
    "pyjwt": "jwt",
}

def detect_package_usage_logic(package_input, file_imports, file_from_imports, file_aliases):
    # Strip version specifiers and lowercase for normalization
    package_name = package_input.split(">=")[0].split("==")[0].split("<=")[0].strip().lower()

    # Get the expected import module name(s)
    primary_module = PKG_TO_MODULE_MAP.get(package_name, package_name)

    # Generate variants (handling hyphens and underscores)
    search_roots = {
        package_name,
        package_name.replace("-", "_"),
        package_name.replace("_", "-"),
        primary_module.lower(),
        primary_module.lower().replace("-", "_"),
        primary_module.lower().replace("_", "-"),
    }

    # Check `import X` statements
    for imp in file_imports:
        root = imp.split(".")[0].lower()
        if root in search_roots:
            return True

    # Check `from X import Y` statements
    for module_name in file_from_imports:
        root = module_name.split(".")[0].lower()
        if root in search_roots:
            return True

    # Check if any alias maps back to the package
    for real_name in file_aliases.values():
        root = real_name.split(".")[0].lower()
        if root in search_roots:
            return True

    return False

def test_logic():
    file_imports = ["flask", "yaml", "PIL.Image"]
    file_from_imports = {"jwt": ["encode"]}
    file_aliases = {"np": "numpy"}

    test_cases = [
        ("Flask", True),        # Case mismatch
        ("PyYAML", True),       # Name mapping
        ("Pillow", True),       # Name mapping
        ("PyJWT", True),        # Name mapping
        ("requests", False),    # Not present
        ("numpy", True),        # Alias match
        ("ansible", False),     # Not present
    ]

    for pkg, expected in test_cases:
        used = detect_package_usage_logic(pkg, file_imports, file_from_imports, file_aliases)
        print(f"Package: {pkg:10} | Used: {used:5} | Expected: {expected:5} | {'PASS' if used == expected else 'FAIL'}")

if __name__ == "__main__":
    test_logic()
