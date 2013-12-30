#!/usr/bin/env python
import xml.dom.minidom
import json
import codecs

def _gen_bf_el(x):
    '''
    Builds a dictionary from the ElementTree element x
    The function
    Uses as hacky splitting of attribute or tag names using {}
        to remove namespaces.
    returns a pair of: the tag of `x` and the badgerfish
        representation of the subelements of x
    '''
    obj = {}
    # grab the tag of x
    t = x.nodeName
    # add the attributes to the dictionary
    att_container = x.attributes
    for i in xrange(att_container.length):
        attr = att_container.item(i)
        obj['@' + attr.name] = attr.value

    tl = []
    ntl = []
    x.normalize()
    # store the text content of the element under the key '$'
    for c in x.childNodes:
        if c.nodeType == xml.dom.minidom.Node.TEXT_NODE:
            tl.append(c)
        else:
            ntl.append(c)
    try:
        tl = [i.data for i in tl]
        text_content = ''.join(tl)
    except:
        text_content = ''
    if text_content:
        obj['$'] = text_content
    # accumulate a list of the children names in ko, and 
    #   the a dictionary of tag to xml elements.
    # repetition of a tag means that it will map to a list of
    #   xml elements
    cd = {}
    ko = []
    ks = set()
    for child in ntl:
        k = child.nodeName
        if k not in ks:
            ko.append(k)
            ks.add(k)
        p = cd.get(k)
        if p is None:
            cd[k] = child
        elif isinstance(p, list):
            p.append(child)
        else:
            cd[k] = [p, child]
    # Converts the child XML elements to dicts by recursion and
    #   adds these to the dict.
    for k in ko:
        v = cd[k]
        if isinstance(v, list):
            dcl = []
            ct = None
            for xc in v:
                ct, dc = _gen_bf_el(xc)
                dcl.append(dc)
        else:
            ct, dcl = _gen_bf_el(v)
        # this assertion will trip is the hacky stripping of namespaces
        #   results in a name clash among the tags of the children
        assert ct not in obj
        obj[ct] = dcl
    return t, obj

def to_badgerfish_dict(filepath=None, file_object=None, encoding=u'utf8'):
    '''Takes either:
            (1) a file_object, or
            (2) (if file_object is None) a filepath and encoding
    Returns a dictionary with the keys/values encoded according to the badgerfish convention
    See http://badgerfish.ning.com/

    Caveats/bugs:
        
    '''
    if file_object is None:
        file_object = codecs.open(filepath, 'rU', encoding=encoding)
    doc = xml.dom.minidom.parse(file_object)
    root = doc.documentElement
    key, val = _gen_bf_el(root)
    return {key: val}

def get_ot_study_info_from_nexml(filepath=None, file_object=None, encoding=u'utf8'):
    '''Converts an XML doc to JSON using the badgerfish convention (see to_badgerfish_dict)
    and then prunes elements not used by open tree of life study curartion.

    Currently:
        removes nexml/characters @TODO: should replace it with a URI for 
            where the removed character data can be found.
    '''
    o = to_badgerfish_dict(fn)
    try:
        del o['nexml']['characters']
    except:
        pass
    return o

def get_ot_study_info_from_treebase_nexml(filepath=None, file_object=None, encoding=u'utf8'):
    '''Just a stub at this point. Intended to normalize treebase-specific metadata 
    into the locations where open tree of life software that expects it. 
    @TODO: need to investigate which metadata should move or be copied
    '''
    o = get_ot_study_info_from_nexml(filepath=filepath, file_object=file_object, encoding=encoding)
    return o

if __name__ == '__main__':
    import sys
    fn = sys.argv[1]
    o = get_ot_study_info_from_nexml(filepath=fn)
    outf = sys.stdout
    json.dump(o, outf, indent=0, sort_keys=True)
    outf.write('\n')
