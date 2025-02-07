#!/usr/bin/env python3

# Turn hideous XML into less-hideous line-by-line XML fragments
# https://wiki.openstreetmap.org/wiki/OSM_XML
# Typical invocation:
# pv ../planet-latest.osm.bz2 | bzcat | ../disassemble-osm.py | split -C1000M -d -a 4 --additional-suffix='.xml' --filter='gzip > $FILE.gz' - osm-planet-


import sys
from lxml import etree


def main(instream, outstream):
    try:
        # Use iterparse with clear_tags for memory efficiency
        context = etree.iterparse(instream, events=['start', 'end'], remove_blank_text=True, remove_comments=True)
        action, root = next(context)  # get root element
        record_nesting_level = 0
        
        # Track progress
        processed_count = 0
        
        for event, elem in context:
            if event == 'start':
                record_nesting_level += 1
            elif event == 'end':
                record_nesting_level -= 1
                if record_nesting_level != 0:
                    continue

                try:
                    xml = etree.tostring(elem).strip()
                    assert b'\n' not in xml
                    outstream.write(xml)
                    outstream.write(b'\n')
                    
                    processed_count += 1
                    if processed_count % 10000 == 0:
                        print(f"Processed {processed_count} elements", file=sys.stderr)
                        
                finally:
                    # Always clean up the element
                    elem.clear()
                    while elem.getprevious() is not None:
                        del elem.getparent()[0]
        
        # Clean up the root element at the end
        root.clear()

    except etree.XMLSyntaxError as e:
        print(f"Invalid XML input at element {processed_count}: {e}", file=sys.stderr)
        sys.exit(1)
    except etree.XMLError as e:
        print(f"XML processing error at element {processed_count}: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred at element {processed_count}: {e}", file=sys.stderr)
        sys.exit(1)


main(sys.stdin.buffer, sys.stdout.buffer)
