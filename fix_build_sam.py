#!/usr/bin/env python3

import os
import os.path as osp
import glob


def fix_file(file_path, replacements):
	"""Apply multiple find-replace operations to a file"""
	if not osp.exists(file_path):
		print(f"❌ File not found: {file_path}")
		return False

	try:
		with open(file_path, 'r', encoding='utf-8') as f:
			content = f.read()

		original_content = content
		total_replacements = 0

		for find_text, replace_text in replacements:
			count = content.count(find_text)
			content = content.replace(find_text, replace_text)
			total_replacements += count
			if count > 0:
				print(f"   - Replaced {count} instances of '{find_text}' with '{replace_text}'")

		if content != original_content:
			with open(file_path, 'w', encoding='utf-8') as f:
				f.write(content)
			print(f"   ✅ Total replacements: {total_replacements}")
			return True
		else:
			print(f"   ℹ️  No changes needed")
			return False

	except Exception as e:
		print(f"   ❌ Error: {e}")
		return False


def main():
	repo_root = "/home/matthewvowels/GitHub/absolutely-not-samurai"  # Update this path
	sam2_dir = osp.join(repo_root, "sam2")

	print("🚀 Comprehensive fix for all absolutely-not-samurai references")
	print("=" * 70)

	fixed_files = 0

	# 1. Fix __init__.py - THE CRITICAL FIX
	print("1. Fixing __init__.py (CRITICAL)")
	init_file = osp.join(sam2_dir, "__init__.py")
	if fix_file(init_file, [
		('initialize_config_module("absolutely-not-samurai"', 'initialize_config_module("sam2"')
	]):
		fixed_files += 1

	# 2. Fix all YAML config files in configs/samurai/
	print("\n2. Fixing configs/samurai/ directory")
	samurai_configs = glob.glob(osp.join(sam2_dir, "configs", "samurai", "*.yaml"))
	for config_file in samurai_configs:
		print(f"   🔧 {osp.basename(config_file)}")
		if fix_file(config_file, [
			('_target_: absolutely-not-samurai.', '_target_: sam2.')
		]):
			fixed_files += 1

	# 3. Fix all YAML config files in configs/sam2.1/
	print("\n3. Fixing configs/sam2.1/ directory")
	sam21_configs = glob.glob(osp.join(sam2_dir, "configs", "sam2.1", "*.yaml"))
	for config_file in sam21_configs:
		print(f"   🔧 {osp.basename(config_file)}")
		if fix_file(config_file, [
			('_target_: absolutely-not-samurai.', '_target_: sam2.')
		]):
			fixed_files += 1

	# 4. Fix training config files
	print("\n4. Fixing configs/sam2.1_training/ directory")
	training_configs = glob.glob(osp.join(sam2_dir, "configs", "sam2.1_training", "*.yaml"))
	for config_file in training_configs:
		print(f"   🔧 {osp.basename(config_file)}")
		if fix_file(config_file, [
			('_target_: absolutely-not-samurai.', '_target_: sam2.'),
			('training.model.absolutely-not-samurai.', 'training.model.sam2.'),
			('checkpoint_path: ./checkpoints/absolutely-not-samurai.1', 'checkpoint_path: ./checkpoints/sam2.1')
		]):
			fixed_files += 1

	# 5. Fix build_sam.py comments (optional, but for cleanliness)
	print("\n5. Fixing build_sam.py comments (optional)")
	build_sam_file = osp.join(sam2_dir, "build_sam.py")
	# We'll only fix functional references, not comments
	print(f"   🔧 {osp.basename(build_sam_file)}")
	print(f"   ℹ️  Keeping comment references unchanged (they're just documentation)")

	print("=" * 70)
	print(f"✅ Fixed {fixed_files} files")
	print("\nNext steps:")
	print("1. Rebuild your package: python -m build")
	print("2. Reinstall: pip uninstall absolutely-not-samurai && pip install dist/absolutely_not_samurai-1.0-*.whl")
	print("3. Test again!")
	print("\nMost critical fix: __init__.py initialize_config_module() call")


if __name__ == "__main__":
	main()