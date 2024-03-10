#!/bin/bash
# Create an executable zip for distribution.
script_name=$(basename "$0")
script_file=$(realpath "$0")
script_dir=$(realpath "${script_file}" | xargs dirname)
root_dir=${script_dir}/..

bash_exec=/bin/bash
python_exec="/usr/bin/env python3"

pythondir=${script_dir}/python
requirements=${root_dir}/requirements.txt
venv=venv

BUILDROOT=${root_dir}/build
BUILDDIR=${BUILDROOT}/scripts
OUTDIR=${root_dir}/dist
OUTNAME=pyscripts
OUTFILE=${OUTDIR}/${OUTNAME}

echo ::: Clean ${BUILDDIR}
rm -rf "${BUILDDIR}"
mkdir -p "${BUILDDIR}" "${OUTDIR}"
{
    echo ::: cd ${BUILDDIR}
    cd "${BUILDDIR}"
    # Copy files in.
    echo ::: Copy files
    cp -rvL "${pythondir}"/* .

    # Change to distribution mode
    sed -i 's/.*%DIST%//g' DISTINFO.py

    # Create the nessecary venv and install requirements.
    echo ::: Install requirements
    $python_exec -m venv "${venv}"
    source "${venv}"/bin/activate
    $python_exec -m pip install -vr "${requirements}" --target .
    deactivate

    # Apply patches.
    echo ::: Apply patches
    "${script_dir}"/patch_keyboard_module.sh -n -e venv/bin/activate
    # Delete patch backups
    find . -type f -not -path "./${venv}/*" -name "*.orig" -exec rm -rvf {} \;

    # Delete the venv.
    echo ::: Delete ${venv}
    rm -rf "${venv}"

    # Delete caches.
    echo ::: Delete __pycache__
    find . -type d -not -path "./${venv}/*" -name __pycache__ -exec rm -rf {} \;

    # Zip it.
    echo ::: Zip
    zip -r dist.zip .
    cat <( echo '#!/usr/bin/env python3' ) dist.zip > "${OUTNAME}"
    chmod +x "${OUTNAME}"
}

# Move to final destination.
rm -rvf "${OUTFILE}"
mv -v "${BUILDDIR}"/"${OUTNAME}" "${OUTFILE}"
