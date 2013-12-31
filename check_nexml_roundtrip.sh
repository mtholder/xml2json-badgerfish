#!/bin/sh
inpnexml="${1}"
if ! test -f "${inpnexml}"
then
    echo "The first arg should be a nexml instance doc. ${inpnexml} does not exist"
    exit 1
fi
nexmlschemafp="${2}"
if ! test -f "${nexmlschemafp}"
then
    echo "Second arg should be the nexml schema. ${nexmlschemafp} does not exist"
    exit 1
fi
if test -f .1.xml
then
    echo "file .1.xml is in the way!"
    exit 1
fi
cat "${inpnexml}" | sed -e 's/<characters\(.*\) xml:base="[^"]*" */<characters\1 /' > .1.xml
if ! xmllint --schema "${nexmlschemafp}" .1.xml >/dev/null 2>&1
then
    echo "${inpnexml} is not a valid NeXML file"
    rm .1.xml
    exit 1
fi
rm .1.xml