=============
Release Guide
=============

This guide documents the `dask-image` release process.
It is based on the `napari` release guide created by Kira Evans.

This guide is primarily intended for core developers of `dask-image`.
They will need to have a [PyPI](https://pypi.org) account
with upload permissions to the `dask-image` package.

You will also need these additional release dependencies
to complete the release process:

..code-block:: bash

   pip install PyGithub>=1.44.1 twine>=3.1.1 tqdm



Set PyPI password as GitHub secret
----------------------------------

The `dask/dask-image` repository must have a PyPI API token as a GitHub secret.

This likely has been done already, but if it has not, follow
`this guide <https://pypi.org/help/#apitoken>`_ to gain a token and
`this other guide <https://help.github.com/en/actions/automating-your-workflow-with-github-actions/creating-and-using-encrypted-secrets>`_
to add it as a secret.


Generate the release notes
--------------------------

The release notes contain a list of merges, contributors, and reviewers.

1. Crate a GH_TOKEN environment variable on your computer.

    On Linux/Mac:

    .. code-block:: bash

       export GH_TOKEN=<your-gh-api-token>

    On Windows:

    .. code-block::

       set GH_TOKEN <your-gh-api-token>


    If you don't already have a
    `personal GitHub API token <https://github.blog/2013-05-16-personal-api-tokens/>`_,
    you can create one
    from the settings of your GitHub account:
    `<https://github.com/settings/tokens>`_


2. Run the python script to generate the release notes,
including all changes since the last tagged release.

    .. code-block:: bash

       python docs/release/generate_release_notes.py  <last-version-tag> master --version <new-version-number>

       # Example
       python docs/release/generate_release_notes.py  v0.14.0 master --version 0.15.0

    .. code-block:: bash

       python docs/release/generate_release_notes.py -h`` and following that file's usage.


3. Scan the PR titles for highlights, deprecations, API changes,
   and bugfixes, and mention these in the relevant sections of the notes.
   Try to present the information in an expressive way by mentioning
   the affected functions, elaborating on the changes and their
   consequences. If possible, organize semantically close PRs in groups.

4. Copy your edited release notes into the file `napari/HISTORY.rst`.

5. Make and merge a PR with the release notes before moving onto the next steps.


Tagging the new version
-----------------------

The version of `dask-image` is automatically determined by
`versioneer <https://github.com/warner/python-versioneer>'_
from the latest
`git tag <https://git-scm.com/book/en/v2/Git-Basics-Tagging>`_
beginning with `v`.

Thus, you'll need to tag the
`reference <https://git-scm.com/book/en/v2/Git-Internals-Git-References>`_
with the new version number. It is likely something like `X.Y.Z`.
First we will generate a release candidate, which will contain the letters `rc`.
Using release candidates allows us to test releases on PyPI
without using up the actual release number.
You can read more on tagging
`here <https://git-scm.com/book/en/v2/Git-Basics-Tagging>`_.

Tag the release candidate
^^^^^^^^^^^^^^^^^^^^^^^^^

You can tag the current master source code as a release candidate with:

.. code-block:: bash

    git tag vX.Y.Zrc1 master


If the tag is meant for a previous version of master,
simply reference the specific commit:

.. code-block:: bash

    git tag vX.Y.Zrc1 abcde42


Note here how we are using `rc` for release candidate to create a version
of our release we can test before making the real release.


Push the tag to GitHub
^^^^^^^^^^^^^^^^^^^^^^

Now we need to push the tag to GitHub.
Pushing the tag will automatically create a new release using GitHub actions,
and automatically uploads it to PyPI.

.. code-block:: bash

   git push upstream <tag_name>


Testing the release candidate
-----------------------------

The release candidate can then be tested with

.. code-block:: bash

   pip install --pre dask-image


It is recommended that the release candidate is tested in a virtual environment
in order to isolate dependencies.

If the release candidate is not what you want, make your changes and
repeat the process from the beginning but
incrementing the number after `rc` on tag (e.g. `vX.Y.Zrc2`).

Once you are satisfied with the release candidate it is time to generate
the actual release.

Generating the actual release
-----------------------------

To generate the actual release you will now repeat the processes above
but now dropping the `rc`.

For example:

.. code-block:: bash

   git tag vX.Y.Z master
   git push upstream --tags
