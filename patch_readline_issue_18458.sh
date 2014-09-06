#!/bin/sh
#
# patch_readline_issue_18458.sh
# rev 0: 2013-10-22
#
# Disables the readline module of python.org pythons on OS X 10.9 Mavericks
# if they crash when used interactively.  Fixes for this problem should
# be available in the python.org 2.7.6, 3.3.3 and 3.4.0 releases.
#
# This patcher uses the "sudo" command to ensure the necessary privileges
# to rename and disable Python's readline.so.  On most systems, you will need
# to run this script from an administrator account.
#
# To use:
#   1. Download this file from the python.org tracker.
#   2. In a terminal session shell, run:
#        sh /path/to/patch_idle_issue_18458.sh
#      replacing "/path/to" with the folder where the file was downloaded,
#      for example, "sh ~/Downloads/patch_idle_issue_18458.sh"
#   3. If prompted for a password, enter your password.
#
# See http://bugs.python.org/issue18458 for more details and latest version.

set -e
FILENAME="readline.so"
FWROOT="/Library/Frameworks/Python.framework/Versions"
OSXVERSION="$(sw_vers -productVersion)"
echo " -- running on OS X ${OSXVERSION}"
if echo "${OSXVERSION}" | egrep -qvE '^10\.9'
then
    echo " -- This patcher is only needed on OS X 10.9.x"
    exit 1
fi
warn_needed="yes"

set -- 2.7 3.2 3.3 3.4
for pyver
do
    fwdynlib="${FWROOT}/${pyver}/lib/python${pyver}/lib-dynload"
    if [ ! -e "${fwdynlib}" ]
    then
        echo " -- ${pyver} not found - skipped"
        continue
    fi
    if [ ! -e "${fwdynlib}/${FILENAME}" ]
    then
        echo " -- ${pyver} has already been disabled - skipped"
        continue
    fi
    if script /dev/null "${FWROOT}/${pyver}/bin/python${pyver}" -E >/dev/null
    then
        echo " -- ${pyver} does not need to be patched - skipped"
        continue
    fi <<EOF
'-- line 1 - testing interactive input: if line 3 does not appear,'
'-- line 2 - this python crashed and will be patched'
'-- line 3 - OK!'
exit()
EOF
    echo " -- ${pyver} crashed"
    if [ -e "${fwdynlib}/${FILENAME}.disabled" ]
    then
        echo " -- ${pyver} moving existing backup to" \
             "${fwdynlib}/${FILENAME}.disabled.$$"
        [ "${warn_needed}" = "yes" ] && \
            warn_needed="no" && \
            echo " -- need to patch. Enter password if prompted"
        sudo mv -i "${fwdynlib}/${FILENAME}.disabled" \
                 "${fwdynlib}/${FILENAME}.disabled.$$"
    fi
    echo " -- ${pyver} moving readline extension to" \
             "${fwdynlib}/${FILENAME}.disabled"
    [ "${warn_needed}" = "yes" ] && \
        warn_needed="no" && \
        echo " -- need to patch. Enter password if prompted"
    sudo mv -i "${fwdynlib}/${FILENAME}" \
             "${fwdynlib}/${FILENAME}".disabled
    echo " -- ${pyver} is now patched"
done
echo " -- done"