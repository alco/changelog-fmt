Changelog formatter
===================

Organizes your Changelog file by ordering changes by category.

Requires Python 2.7.

## Sample usage ##

    # Save modified changelog in result. All sections preceding the
    # first release line will be sorted.
    ./organize_changelog.py Changelog -o result

    # Sort only the first section with changes
    ./organize_changelog.py Changelog -n 1 -o result

    # Sort all sections modifying the file in-place
    ./organize_changelog.py Changelog -n -1

Type

    ./organize_changelog.py -h

to see detailed description of supported options.
