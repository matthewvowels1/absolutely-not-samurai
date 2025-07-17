#!/usr/bin/env python3

import os
import os.path as osp

# Define the paths to fix
repo_root = "/home/matthewvowels/GitHub/absolutely-not-samurai"  # Update this to your actual path

# Config files to fix
config_paths = [
	osp.join(repo_root, "sam2", "configs", "sam2", "sam2_hiera_b+.yaml"),
	osp.join(repo_root, "sam2", "configs", "sam2", "sam2_hiera_l.yaml"),
	osp.join(repo_root, "sam2", "configs", "sam2", "sam2_hiera_s.yaml"),
	osp.join(repo_root, "sam2", "configs", "sam2", "sam2_hiera_t.yaml"),
	osp.join(repo_root, "sam2", "sam2_hiera_b+.yaml"),
	osp.join(repo_root, "sam2", "sam2_hiera_l.yaml"),
	osp.join(repo_root, "sam2", "sam2_hiera_s.yaml"),
	osp.join(repo_root, "sam2", "sam2_hiera_t.yaml"),
]


def fix_yaml_file(file_path):
	"""Replace absolutely-not-samurai with sam2 in a YAML file"""
	if not osp.exists(file_path):
		print(f"❌ File not found: {file_path}")
		return False

	print(f"🔧 Fixing {file_path}")

	# Read the file
	with open(file_path, 'r') as f:
		content = f.read()

	# Count replacements
	original_count = content.count('absolutely-not-samurai')

	# Replace all instances
	fixed_content = content.replace('absolutely-not-samurai', 'sam2')

	# Write back
	with open(file_path, 'w') as f:
		f.write(fixed_content)

	new_count = fixed_content.count('absolutely-not-samurai')
	replaced_count = original_count - new_count

	print(f"   ✅ Replaced {replaced_count} instances")
	return True


def main():
	print("🚀 Fixing YAML config files...")
	print("=" * 50)

	total_fixed = 0
	for config_path in config_paths:
		if fix_yaml_file(config_path):
			total_fixed += 1

	print("=" * 50)
	print(f"✅ Fixed {total_fixed} files")
	print("\nNext steps:")
	print("1. Rebuild your package: python -m build")
	print("2. Reinstall: pip uninstall absolutely-not-samurai && pip install dist/absolutely_not_samurai-1.0-*.whl")
	print("3. Test again!")


if __name__ == "__main__":
	main()