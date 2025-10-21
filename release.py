import os
import shutil

RELEASE_DIR = "release"
ROOT_MOD_NAME = "mazda_mx3"
VARIANTS = ["", "_v6"]

RELEASE_PATH = os.path.join(".", RELEASE_DIR)
ROOT_MOD_PATH = os.path.join(RELEASE_PATH, ROOT_MOD_NAME)

# TODO if RELEASE_PATH exists, nuke it before doing this.
if (os.path.exists(RELEASE_PATH)):
    shutil.rmtree(RELEASE_PATH)
os.makedirs(RELEASE_PATH)

#shutil.copytree(src=".", dst=ROOT_MOD_PATH, ignore=shutil.ignore_patterns(".git*", "release*", "_*"))
ignoredirs = []

for variant in VARIANTS:
    variant_path = ROOT_MOD_PATH + variant
    print(f"variant_path: {variant_path}")
    shutil.copytree(src=".", dst=variant_path, ignore=shutil.ignore_patterns(".git*", "release*", "_*"))
    # special case "" is the base mod and will not work if handled the same way as the other variants
    if variant:
        for root, subdirs, files in os.walk(variant_path):
            for file in files:
                base, extension = os.path.splitext(file)
                if base.endswith(variant) and root not in ignoredirs:
                    base_file = os.path.join(root, base[:-len(variant)] + extension)
                    if os.path.exists(base_file):
                        os.remove(base_file)
                    print("Rename {} to {}".format(os.path.join(root, file), base_file))
                    os.rename(os.path.join(root, file), base_file)
            for subdir in subdirs:
                if subdir.endswith(variant):
                    base_dir = os.path.join(root, subdir[:-len(variant)])
                    shutil.rmtree(base_dir)
                    print("Rename {} to {}".format(os.path.join(root, subdir), base_dir))
                    os.rename(os.path.join(root, subdir), base_dir)
                    ignoredirs.append(base_dir)

