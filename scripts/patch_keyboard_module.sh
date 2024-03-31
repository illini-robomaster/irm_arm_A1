#!/bin/bash
# The `keyboard` python module refuses to run without root access (as to
# support non-X systems). However, on most linux platforms, access to
# `/dev/input/whatever` can be gained with addition to the `input` group.
__ScriptVersion="1.14.5.14"

function usage ()
{
    echo "Usage:   $0 [options] [--]

    Options:
    -h|help       Display this message
    -v|version    Display script version
    -b            Create backup
    -n            Ignore failed checks
    -e <PATH>     Source <PATH>"
}
while getopts ":hvne:b" opt
do
    case $opt in
        h|help) 
            usage;
            exit 0;;
        v|version)
            echo "$0 -- Version $__ScriptVersion";
            exit 0;;
        b)
            backup=-b;;
        n)
            no_fail=1;;
        e)
            venv=${OPTARG};;
        *)  echo -e "\n  Option does not exist : $OPTARG\n"
             usage;
             exit 1;;
    esac
done
shift $(($OPTIND-1))

python_exec="/usr/bin/env python3"

if [ "${venv}" ]; then
    echo Sourcing ${venv}
    source "${venv}"
    if [ $? -ne 0 -a ! "${no_fail}" ]; then
        echo Could not source ${venv}
        exit 1
    fi
fi

NOT_OKAY=
echo Check permissions:
if [ groups ${USER} | grep -q tty ]; then
    echo OK: ${USER} is in group tty for \`dumpkeys\`
else
    echo NOT OK: ${USER} IS NOT IN GROUP tty FOR \`dumpkeys\`
    NOT_OKAY=1
fi
for event in $(ls -dh /dev/input/event*); do
    event_group=$(stat -c %G ${event}) 
    if [ "${event_group}" == root ]; then
        echo FAILURE: ${event} REQUIRES ROOT ACCESS
        NOT_OKAY=1
    fi
    if groups ${USER} | grep -q ${event_group}; then
        echo OK: ${USER} is in group ${event_group} for ${event}
    else
        echo NOT OK: ${USER} IS NOT GROUPED WITH ${event}
        NOT_OKAY=1
    fi
    if stat -c %a ${event} | grep -q .[6-7].; then
        echo OK: ${event_group} has r/w access on ${event}
    else
        echo NOT OK: ${event_group} DOES NOT HAVE R/W ACCESS ON ${event}
        NOT_OKAY=1
    fi
done

echo
echo Check venv:
if $python_exec -c 'import sys; assert sys.prefix != sys.base_prefix' &> /dev/null; then
    echo OK: In venv
else
    echo NOT OK: NOT IN VENV
    NOT_OKAY=1
fi

echo
echo Check module:
if $python_exec -c 'import keyboard' &> /dev/null; then
    echo OK: Keyboard module installed
else
    echo NOT OK: KEYBOARD MODULE NOT INSTALLED
    NOT_OKAY=1
fi

echo
if [ "${NOT_OKAY}" -a ! "${no_fail}" ]; then
    echo Checks failed. I will not apply patches.
    exit 1
else
    echo Checks passed. I will apply patches.
fi

PATCH=$(cat << EOF
173,174c173
<     if os.geteuid() != 0:
<         raise ImportError('You must be root to use this library on linux.')
---
>     pass
EOF
)
FILE_PATH=$($python_exec -c 'import keyboard; print(keyboard.__file__)' | xargs dirname)/_nixcommon.py

echo "${PATCH}"
patch --verbose ${backup} "${FILE_PATH}" -i <( echo "${PATCH}" )
