Tools for converting between XML and JSON using the badgerfish convention.  Note that this code does *NOT* emit the active namespaces in each object in the JSON tree unlike the example given (example #9) in the www.sklar.com/badgerfish site.
This repo is a temporary workspace for code that will go into the OpenTreeOfLife project repositories. So, it has some NeXML specific features of use to that project.

Usage
=====
The executable xml2json-badgerfish.py takes two arguments: a code for the translation and the filepath to the input. Output is written to standard output.  The code is a letter for the input format and a letter for the output format:
    jn for JSON to NeXML
    jx for JSON to XML (generic, no NeXML element ordering)
    xj for XML to JSON
    nj for NeXML to JSON


Example numbers from http://www.sklar.com/badgerfish/
Requires xmllint and saxon-xslt

sortattr.xslt from http://stackoverflow.com/questions/1429991/using-xsl-to-sort-attributes other code by Mark Holder.


Release under BSD-license with NO WARRANTY
