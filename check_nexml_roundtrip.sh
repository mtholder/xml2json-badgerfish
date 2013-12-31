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
if test -f .1.xml -o -f .1.json -o -f .2.xml
then
    echo "file .#.* is in the way!"
    exit 1
fi

# 1. Verify that the input is valid NeXML

# an apparent bug in xmllint
#   see http://sourceforge.net/mailarchive/message.php?msg_id=31798087
# necessitates some hacky expunging of attributes from a characters block...
cat "${inpnexml}" | sed -e 's/<characters\(.*\) xml:base="[^"]*" */<characters\1 /' > .1.xml

if ! xmllint --schema "${nexmlschemafp}" .1.xml >/dev/null 2>&1
then
    echo "${inpnexml} is not a valid NeXML file"
    rm .1.xml
    exit 1
fi

# 2. Convert to JSON
if ! ./xml2json-badgerfish.py nj .1.xml > .1.json
then
    echo "Conversion of .1.xml to JSON failed"
    rm .1.json
    exit 1
fi

# 3. Convert back to NeXML
if ! ./xml2json-badgerfish.py jn .1.json > .2.xml
then
    echo "Conversion of .1.json to JSON failed"
    rm .1.xml
    rm -f .2.xml
    exit 1
fi

if ! diff .1.xml .2.xml 
then
    echo "Did not roundtrip"
    rm .1.json
    exit 1
fi
rm .1.json
rm .1.xml
rm .2.xml