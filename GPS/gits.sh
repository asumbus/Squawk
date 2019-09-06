#!/bin/bash

gitpython() {
    local cwd repo pipList found
    pipList=$(pip list)
    found=$(grep -o "GitPython" <<< "$pipList" | wc -l)
    repo="https://github.com/lbussy/GitPython.git"
    if [ "$found" -eq "0" ]; then
        echo -e "\nDownloading and installing GitPython for Python 2.7."
        cwd=$(pwd)
        git clone "$repo" "$HOME/git-python" &>/dev/null || die "$@"
        cd "$HOME/git-python" || die "$@"
        eval "python setup.py install" &>/dev/null || die "$@"
        cd "$cwd" || die "$@"
        rm -fr "$HOME/git-python"
        echo -e "\nGitPython for Python 2.7 install complete."
    else
        echo -e "\nGitPython for Python 2.7 already installed."
    fi
}

function die
{
    local message=$1
    [ -z "$message" ] && message="Died"
    echo "${BASH_SOURCE[1]}: line ${BASH_LINENO[0]}: ${FUNCNAME[1]}: $message." >&2
    exit 1
}

main() {
    gitpython "$@"
}

main "$?" && exit 0