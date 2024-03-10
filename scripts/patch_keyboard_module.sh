#!/bin/bash
# The `keyboard` python module refuses to run without root access (as to
# support non-X systems). However, on most linux platforms, access to
# `/dev/input/whatever` can be gained with addition to the `input` group.
NOT_OKAY=
echo After adding yourself to the group, you should log out and back in again. This is required.
echo
echo Check permissions:
echo
for event in $(ls -dh /dev/input/event*); do
    event_group=$(stat -c %G ${event}) 
    if [ "${event_group}" == root ]; then
        echo FAILURE: ${event} REQUIRES ROOT ACCESS
        NOT_OKAY=0
    fi
    if groups ${USER} | grep -q ${event_group}; then
        echo OK: ${USER} is grouped with ${event}
    else
        echo NOT OK: ${USER} IS NOT GROUPED WITH ${event}
        NOT_OKAY=0
    fi
    if stat -c %a ${event} | grep -q .[6-7].; then
        echo OK: ${event_group} has r/w access on ${event}
    else
        echo NOT OK: ${event_group} DOES NOT HAVE R/W ACCESS ON ${event}
        NOT_OKAY=0
    fi
done

echo
echo Check venv:
if [ "$(/usr/bin/env python3 -c 'import sys; print(sys.prefix == sys.base_prefix)')" == False ]; then
    echo OK: In venv
else
    echo NOT OK: NOT IN VENV
    NOT_OKAY=0
fi

echo
echo Check module:
if [ "$(/usr/bin/env python3 -c 'import sys; print("keyboard" in sys.modules)')" == True ]; then
    echo OK: Keyboard module installed
else
    echo NOT OK: KEYBOARD MODULE NOT INSTALLED
    NOT_OKAY=0
fi

echo
if [ "${NOT_OKAY}" ]; then
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
FILE_PATH=$(/usr/bin/env python3 -c 'import keyboard; print(keyboard.__file__)' | xargs dirname)/_nixcommon.py

echo "${PATCH}"
if [ "$1" == -b ]; then
    patch --verbose -b "${FILE_PATH}" -i <( echo "${PATCH}" )
else
    patch --verbose "${FILE_PATH}" -i <( echo "${PATCH}" )
fi

echo
echo Done.
