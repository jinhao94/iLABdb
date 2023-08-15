#!/bin/bash
csvtk join -t -T -H -f"1" $1 /ddn/script/script_sup/module.description.all | perl -lane 'BEGIN{print "Module\tCoverage\tDescription\tCategory"}; print $_' > $2