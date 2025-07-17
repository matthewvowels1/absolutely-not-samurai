#!/usr/bin/env python3

import sam2
import os
import os.path as osp

# Get the sam2 package directory
sam2_dir = osp.dirname(sam2.__file__)
configs_dir = osp.join(sam2_dir, "configs", "sam2")

print(f"Checking YAML files in: {configs_dir}")

# Check each YAML file for any references to module names
yaml_files = ["sam2_hiera_b+.yaml", "sam2_hiera_l.yaml", "sam2_hiera_s.yaml", "sam2_hiera_t.yaml"]

for yaml_file in yaml_files:
	yaml_path = osp.join(configs_dir, yaml_file)
	if osp.exists(yaml_path):
		print(f"\n{'=' * 50}")
		print(f"Contents of {yaml_file}:")
		print('=' * 50)

		with open(yaml_path, 'r') as f:
			content = f.read()
			print(content)

		# Check for any suspicious references
		if 'absolutely-not-samurai' in content:
			print("❌ Found 'absolutely-not-samurai' reference!")
		if 'samurai' in content.lower():
			print("⚠️  Found 'samurai' reference!")
		if '_target_' in content:
			print("ℹ️  Found _target_ (Hydra instantiation)")
	else:
		print(f"❌ {yaml_file} not found at {yaml_path}")

# Also check the root level YAML files
print(f"\n{'=' * 50}")
print("Checking root level YAML files:")
print('=' * 50)

for yaml_file in yaml_files:
	yaml_path = osp.join(sam2_dir, yaml_file)
	if osp.exists(yaml_path):
		print(f"\n--- {yaml_file} (root level) ---")
		with open(yaml_path, 'r') as f:
			content = f.read()
			print(content[:200] + "..." if len(content) > 200 else content)