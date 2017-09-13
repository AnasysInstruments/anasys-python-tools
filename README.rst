# anasys-python-tools
A suite of Python tools for use with Anasys Instruments products.
This repo is under development and nothing here should be considered "working."
Eventually this repo will move, probably right after alpha release. Probably soonish.

$project
========

$project will solve your problem of where to start with documentation,
by providing a basic explanation of how to do it easily.

Basic usage

    import anasyspythontools as anasys
    # Get your stuff done
    f = anasys.read("afmdata.axz")
    # Grab all the height map data from the file
    heightmaps = f.HeightMaps
    # Show off your beautiful images
    heightmaps['Height 1'].show()


Features
--------

- Be awesome
- Make things faster

Installation
------------

Install $project by running:

    install project

Contribute
----------

- Issue Tracker: github.com/$project/$project/issues
- Source Code: github.com/$project/$project

Support
-------

If you are having issues, please let us know.
We have a mailing list located at: project@google-groups.com

License
-------

The project is licensed under the BSD license.
