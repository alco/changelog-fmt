#!/bin/sh

function test_script() {
    test_name="$1"
    test_result="$2"
    shift 2

    ./organize_changelog.py -o test/temp "$@"
    diff test/temp "$test_result"
    if [ "$?" != "0" ]; then
        echo "$test_name failed"
        exit 1
    fi
}

test_script "Default test/1" test/1.1 test/1
test_script "One section test/1" test/1.2 -n 1 test/1
test_script "All sections test/1" test/1.1 -n -1 test/1
test_script "Default test/2" test/2.1 test/2
test_script "One section test/2" test/2.2 -n 1 test/2
test_script "Default test/3" test/3.1 test/3
test_script "Two sections test/3" test/3.2 -n 2 test/3
test_script "All sections test/3" test/3.2 -n -1 test/3

echo 'ok'
rm test/temp
