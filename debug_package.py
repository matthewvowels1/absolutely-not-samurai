#!/usr/bin/env python3

import sam2
import os
import os.path as osp
import re


def scan_file_for_references(file_path, search_term):
	"""Scan a file for references to a search term and return line numbers and content"""
	if not osp.exists(file_path):
		return []

	try:
		with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
			lines = f.readlines()

		matches = []
		for i, line in enumerate(lines):
			if search_term in line:
				matches.append((i + 1, line.strip()))
		return matches
	except:
		return []


def scan_directory_recursively(directory, search_term, extensions=None):
	"""Recursively scan a directory for files containing the search term"""
	if extensions is None:
		extensions = ['.py', '.yaml', '.yml', '.cfg', '.conf']

	all_matches = {}

	for root, dirs, files in os.walk(directory):
		for file in files:
			if any(file.endswith(ext) for ext in extensions):
				file_path = osp.join(root, file)
				matches = scan_file_for_references(file_path, search_term)
				if matches:
					rel_path = osp.relpath(file_path, directory)
					all_matches[rel_path] = matches

	return all_matches


def main():
	# Get the installed sam2 directory
	sam2_dir = osp.dirname(sam2.__file__)
	print(f"Scanning installed SAM2 package: {sam2_dir}")
	print("=" * 70)

	# Search for any remaining references to 'absolutely-not-samurai'
	matches = scan_directory_recursively(sam2_dir, 'absolutely-not-samurai')

	if matches:
		print("❌ Found remaining 'absolutely-not-samurai' references:")
		print("=" * 70)

		for file_path, file_matches in matches.items():
			print(f"\n📁 {file_path}:")
			for line_num, line_content in file_matches:
				print(f"   {line_num:3d}: {line_content}")
	else:
		print("✅ No 'absolutely-not-samurai' references found in installed package!")

	print("\n" + "=" * 70)
	print("Now let's check for Hydra configuration issues...")
	print("=" * 70)

	# Let's also check if there are any .hydra or config cache files
	hydra_paths = []
	for root, dirs, files in os.walk(sam2_dir):
		for file in files:
			if 'hydra' in file.lower() or file.endswith('.cache'):
				hydra_paths.append(osp.join(root, file))

	if hydra_paths:
		print("Found potential Hydra cache/config files:")
		for path in hydra_paths:
			print(f"  📄 {path}")

	# Check the specific build_sam.py compose calls
	build_sam_path = osp.join(sam2_dir, 'build_sam.py')
	if osp.exists(build_sam_path):
		print(f"\n📄 Examining build_sam.py compose calls:")
		with open(build_sam_path, 'r') as f:
			lines = f.readlines()

		for i, line in enumerate(lines):
			if 'compose(' in line:
				print(f"   Line {i + 1}: {line.strip()}")
				# Show context around compose calls
				start = max(0, i - 3)
				end = min(len(lines), i + 4)
				for j in range(start, end):
					if j != i:
						print(f"        {j + 1}: {lines[j].rstrip()}")
				print()

	# Let's try to manually load the config to see what Hydra is doing
	print("\n" + "=" * 70)
	print("Testing manual config loading...")
	print("=" * 70)

	try:
		from hydra import compose, initialize_config_dir
		from hydra.core.global_hydra import GlobalHydra

		# Clear any existing Hydra instance
		GlobalHydra.instance().clear()

		# Try to initialize with the config directory
		config_dir = osp.join(sam2_dir, "configs", "sam2")
		print(f"Trying to initialize Hydra with config_dir: {config_dir}")

		with initialize_config_dir(config_dir=config_dir, version_base=None):
			cfg = compose(config_name="sam2_hiera_b+.yaml")
			print("✅ Manual config loading succeeded!")
			print(f"Config model target: {cfg.model._target_}")

	except Exception as e:
		print(f"❌ Manual config loading failed: {e}")
		print(f"Error type: {type(e).__name__}")

		# Try to get more details about the error
		import traceback
		print("\nFull traceback:")
		traceback.print_exc()


if __name__ == "__main__":
	main()