#!/bin/sh

./organize_changelog.py -o test/temp test/1 
diff test/temp test/1.1
if [ "$?" != "0" ]; then
    echo 'Test 1 failed'
    exit 1
fi

./organize_changelog.py -o test/temp -n 1 test/1 
diff test/temp test/1.2
if [ "$?" != "0" ]; then
    echo 'Test 2 failed'
    exit 1
fi

./organize_changelog.py -o test/temp test/2
diff test/temp test/2.1
if [ "$?" != "0" ]; then
    echo 'Test 3 failed'
    exit 1
fi

./organize_changelog.py -o test/temp -n 1 test/2 
diff test/temp test/2.2
if [ "$?" != "0" ]; then
    echo 'Test 4 failed'
    exit 1
fi

./organize_changelog.py -o test/temp test/3
diff test/temp test/3.1
if [ "$?" != "0" ]; then
    echo 'Test 5 failed'
    exit 1
fi

./organize_changelog.py -o test/temp -n 2 test/3
diff test/temp test/3.2
if [ "$?" != "0" ]; then
    echo 'Test 6 failed'
    exit 1
fi

./organize_changelog.py -o test/temp -n -1 test/3
diff test/temp test/3.2
if [ "$?" != "0" ]; then
    echo 'Test 7 failed'
    exit 1
fi

./organize_changelog.py -o test/temp -n -1 test/1 
diff test/temp test/1.1
if [ "$?" != "0" ]; then
    echo 'Test 8 failed'
    exit 1
fi

echo 'ok'
rm test/temp
