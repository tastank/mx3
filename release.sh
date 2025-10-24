#!/bin/sh
set -e

ASSETTO_CARS_DIR='/b/Program Files/SteamLibrary/steamapps/common/assettocorsa/content/cars/'

STARTING_BRANCH=$(git branch --show-current)
BASE_BRANCH='master'
BRANCHES=('master' 'k8')

for BRANCH in ${BRANCHES[@]}; do
    git checkout "$BRANCH"
    git rebase "$BASE_BRANCH"
    TARGET_NAME=$(cat name.txt)
    TARGET_DIR="$ASSETTO_CARS_DIR$TARGET_NAME"
    if [ -d "$TARGET_DIR" ]; then
        echo "Removing existing target: $TARGET_DIR"
        rm -r "$TARGET_DIR"
    fi
    mkdir "$TARGET_DIR"
    # from https://www.reddit.com/r/zsh/comments/145kapy/clean_way_to_copy_excluding_certain_filesfolders/jnmnum5/
    tar --exclude-vcs --exclude-from="exclude-from-release.txt" -cf - . | tar -xf - -C "$TARGET_DIR"
done
git checkout "$STARTING_BRANCH"
