.. _general-settings:

General settings
----------------

.. papis-config:: local-config-file

    Name AND relative path of the local configuration file that papis
    will additionally read if the file is present in the current
    directory or in the base directory of a given library.

    This is useful, for instance, if you have a library somewhere
    for which you want special configuration settings
    but do not want these settings to cluster in your configuration
    file. It is also useful if you're sharing a library with someone
    else and you want them to have the same settings in that library as
    you. Imagine you're sharing a library of datasheets with your friend
    Fulano. You have your library at

    ::

        ~/Documents/lib-with-fulano

    and you've set a local configuration file there

    ::

        ~/Documents/lib-with-fulano/.papis.config

    then whenever Fulano uses that library and the file is also present,
    his papis program will also read the configuration settings at
    the path above.

.. papis-config:: dir-umask

    This is the default ``umask`` that will be used to create the new
    documents' directories.

.. papis-config:: use-git

    Some commands will issue git commands if this option is set to ``True``.
    For example in ``mv`` or ``rename``.

.. papis-config:: user-agent

    User agent used by papis whenever it obtains information from external
    servers.

.. papis-config:: scripts-short-help-regex

    This is the format of the short help indicator in external papis
    commands.

.. papis-config:: info-name

    The default name of the information files.

.. papis-config:: doc-url-key-name

    Some documents might have, apart from an url, also a file url associated with them.
    The key name appearing in the information file is defined by
    this setting.

.. papis-config:: default-library

    The name of the library that is to be searched when ``papis``
    is run without library arguments.

.. papis-config:: format-doc-name

    This setting controls the name of the document in the papis format strings
    like in format strings such as ``match-format`` or ``header-format``.
    For instance, if you are managing videos, you might want to
    set this option to ``vid`` in order to set  the ``header-format`` to
    ``{vid[title]} - {vid[director]} - {vid[duration]}``.

.. papis-config:: match-format

    Default format that is used to match a document against in order to select
    it. For example if the ``match-format`` is equal to
    ``{doc[year]} {doc[author]}`` then the title of a document will not work
    to match a document, only the year and author.

.. papis-config:: header-format

    Default format that is used to show a document in order to select it.

.. papis-config:: header-format-file

    This option should have the path of a file with the ``header-format``
    template. Sometimes templates can get big so this is a way
    of not cluttering the config file with text.

    As an example you would set

    .. code:: ini

        [papers]

        header-format-file = ~/.papis/config/styles/header.txt

.. papis-config:: info-allow-unicode

    This flag is to be set if you want to allow unicode characters
    in your info file or not. If it is set to false then a representation
    for the unicode characters will be written in its place.
    Since we should be living in an unicode world, it is set to ``True``
    by default.

Tools options
-------------

.. papis-config:: opentool

    This is the general program that will be used to open documents.
    As for now papis is not intended to detect the type of document to be opened
    and decide upon how to open the document. You should set this
    to the right program for the tool. If you are on linux you might want
    to take a look at `ranger <https://ranger.github.io>`__ or let
    the default handle it in your system.
    For mac users you might set this to ``open``.

.. papis-config:: browser
    :default: $BROWSER

    Program to be used for opening websites, the default is the environment
    variable ``$BROWSER``.

.. papis-config:: picktool

    This is the program used whenever papis asks you to pick a document
    or options in general.

    Only option is:
        - papis

.. papis-config:: editor
    :default: $EDITOR

    Editor used to edit files in papis, e.g., for the ``papis edit``
    command. It defaults to the ``$EDITOR`` environment variable, if this is
    not set then it will default to the ``$VISUAL`` environment variable.
    Otherwise the default editor in your system will be used.

.. papis-config:: file-browser

    File browser to be used when opening a directory. It defaults to the
    default file browser in your system, however, you can set it to different
    file browsers such as ``dolphin``, ``thunar`` or ``ranger`` just to name a few.


.. _bibtex-options:

BibTeX options
--------------

.. papis-config:: bibtex-journal-key

  Journal publishers may request abbreviated journal titles. This
  option allows the user to set the key for the journal entry when using
  ``papis export --bibtex``.

  Set as ``full_journal_title`` or ``abbrev_journal_title`` for
  whichever style required. Default is ``journal``.

.. papis-config:: extra-bibtex-keys
  :default: []

  When exporting documents in BibTeX format, you might want to add
  non-standard BibTeX keys such as ``doc_url`` or ``tags``. You can add
  these as a valid python list of strings, for instance:

  .. code:: ini

    [mylib]
    extra-bibtex-keys = ["tags", "doc_url"]

.. papis-config:: bibtex-ignore-keys
   :default: []

  When exporting a document to the BibTeX format, do not export the keys
  appearing in this list. This might be useful if you have some keys
  that have a lot of content, such as ``abstract``, or maybe you
  have used a valid BibTeX key for some other purposes, like the ``note``
  key.

.. papis-config:: extra-bibtex-types
  :default: []

  Allow non-standard BibTeX types to be recognized, e.g,

  .. code:: ini

    [mylib]
    extra-bibtex-types = ["wikipedia", "video", "song"]

  See the `BibTeX reference <https://mirror.easyname.at/ctan/biblio/bibtex/base/btxdoc.pdf>`__
  or the `BibLaTeX reference <https://ftp.snt.utwente.nl/pub/software/tex/macros/latex/contrib/biblatex/doc/biblatex.pdf>`__
  for supported types.

.. papis-config:: multiple-authors-format

    When retrieving automatic author information from services like
    `crossref.org <https://www.crossref.org>`__, papis usually builds the
    ``author`` field for the given document. The format how every single author
    name is built is given by this setting, for instance you could customize it
    by the following:

    ::

        multiple-authors-format = {au[surname]} -- {au[given_name]}

    which would given in the case of Albert Einstein the string
    ``Einstein -- Albert``.

.. papis-config:: multiple-authors-separator

    Similarly to ``multiple-authors-format``, this is the string that
    separates single authors in the ``author`` field. If it is set to
    `` and `` then you would have ``<author 1> and <author 2> and ....``
    in the ``author`` field.

.. papis-config:: bibtex-unicode

    Whether or not to allow direct unicode characters in the document
    fields to be exported into the BibTeX text.

.. papis-config:: bibtex-export-zotero-file

   A boolean value that can be used to add a ``"file"`` field to exported
   BibTeX entries. The files are added as a semicolon separated string.

.. _add-command-options:

``papis add`` options
---------------------

.. papis-config:: ref-format

    This flag is set to change the ``ref`` flag in the info.yaml file
    when a document is imported. For example: I prefer the format
    FirstAuthorYear e.g. Plews2019. This would be achieved by the
    following:

    ::

        ref-format = {doc[author_list][0][surname]}{doc[year]}

    In general however I recomment the default behaviour of just using the
    ``author`` key of the document, i.e.,
    ::

        ref-format = {doc[title]:.15} {doc[author]:.6} {doc[year]}

    The spaces in the value of the format will be important in order
    to capitalize the string, i.e., if you have a title like
    ``STUDIES ABOUT EARTH AND HIMMEL`` and and an author list like
    ``mesh-ki-ang-nuna`` then the built reference will be
    ``StudiesAboutEMeshKi``.

    .. note::
        Special characters will be replaced when generating the ``ref`` entry
        (e.g.  ``Ö → O``, ``.`` and other symbols will be striped from the
        string).

    If you want to add some punctuation, dots (``.``) and underscores (``_``)
    can be escaped by a backslash. For example,

    ::

        ref-format = {doc[author_list][0][surname]}\.{doc[year]}

    would result in 'Plews.2019'. To ensure correct capitalization you might
    consider inserting whitespaces after an escaped character.

.. papis-config:: add-confirm

    If set to ``True``, every time you run ``papis add``
    the flag ``--confirm`` will be added automatically. If is set to ``True``
    and you add it, i.e., you run ``papis add --confirm``, then it will
    have the contrary effect, i.e., it will not ask for confirmation.

.. papis-config:: add-folder-name
    :default: empty string

    Default name for the folder of newly added documents. For example, if you want
    the folder of your documents to be named after the format
    ``author-title`` then you should set it to
    the papis format: ``{doc[author]}-{doc[title]}``. You can create formatted
    subfolders by using path separators (i.e., ``/``) in this format string, e.g.,
    ``{doc[year]} / {doc[title]}``.
    Per default a hash followed by the author name is created.

.. papis-config:: add-file-name

    Same as ``add-folder-name``, but for files, not folders. If it is not set,
    the names of the files will be cleaned and taken ``as-is``.

.. papis-config:: add-interactive

    If set to ``True``, every time you run ``papis add``
    the flag ``--interactive`` will be added automatically. If is set to
    ``True`` and you add it, i.e., you run ``papis add --interactive``, then it
    will have the contrary effect, i.e., it will not run in interactive mode.

.. papis-config:: add-edit

    If set to ``True``, every time you run ``papis add``
    the flag ``--edit`` will be added automatically. If it is set to
    ``True`` and you add something, i.e., you run ``papis add --edit``, then it
    will have the contrary effect, i.e., it will not prompt to edit the info
    file.

.. papis-config:: add-open

    If set to ``True``, every time you run ``papis add``
    the flag ``--open`` will be added automatically. If it is set to
    ``True`` and you add something, i.e., you run ``papis add --open``, then it
    will have the contrary effect, i.e., it will not open the attached files
    before adding the document to the library.

.. papis-config:: add-subfolder
    :default: empty string

    Configure a default for the ``--subfolder`` command line option. Note that, this setting is not
    allowed to contain formatting options. However, one can also specify nested sub-folders.

.. papis-config:: add-download-files

    If set to *True* the ``--download-files`` flag will be added to every call
    of the ``papis add`` command (and ``--no-download-files`` if set to *False*).
    This flag is used to control downloading larger document files (e.g. PDFs)
    by the importers and downloaders that support it (metadata is always
    downloaded by ``papis add``).

``papis browse`` options
------------------------

.. papis-config:: browse-key

    This setting provides the key that is used to generate a URL for the
    ``papis browse`` command. In the simplest case, ``browse-key`` is just a
    key in the document (e.g. ``url``) that contains a URL to open. It also
    supports the following special values:

    * ``"doi"``: construct a URL from the DOI as ``https://dx.doi.org/<DOI>``.
    * ``"isbn"``: construct a URL from the ISBN as ``https://isbnsearch/isbn/<ISBN>``.
    * ``"ads"``: construct a URL for the Astrophysics Data System as
      ``https://ui.adsabs.harvard.edu/abs/<DOI>``.
    * ``"auto"``: automatically pick between ``url``, ``doi`` and ``isbn``
      (first existing key is chosen).
    * ``"search-engine"``: the :ref:`config-settings-search-engine` is used
      to search for the contents of :ref:`config-settings-browse-query-format`.

    If the required keys are not found in the document (e.g. the DOI or the
    ISBN), the key will fallback to the ``"search-engine"`` case.

.. papis-config:: browse-query-format

    The query string that is to be searched for in the ``papis browse`` command
    whenever a search engine is used (see :ref:`config-settings-browse-key`).

.. papis-config:: search-engine

    Search engine to be used by some commands like ``papis browse``. This should be
    a base URL that is then used to construct a search as ``<BASE>/?<PARAMS>``.

.. _edit-command-options:

``papis edit`` options
----------------------

.. papis-config:: notes-name

    In ``papis edit`` you can edit notes about the document. ``notes-name``
    is the default name of the notes file, which by default is supposed
    to be a TeX file. The ``notes-name`` is formated by the ``formater``, so
    that the filename of notes can be dynamically defined, e.g.:  ::

        notes-name = notes_{doc[title]:.15}.tex

.. papis-config:: notes-template

    When editing notes for the first time, a preliminary note will be generated
    based on a template. The path to this template is specified by
    ``notes-template``. The template will then be formated by ``formater``.
    This can be useful to enforce the same style in the notes for all documents.

    Default value is set to ``""``, which will return an empty notes file. If
    no file is found at the path to the template, then also an empty notes file
    will be generated.

.. _marks-options:

``papis doctor`` options
------------------------

.. papis-config:: doctor-default-checks

    A list of checks that are performed by default.

.. papis-config:: doctor-keys-exist-keys

    A list of keys used by the ``keys-exist`` check. The check will show an
    error if these keys are not present in a document.

.. papis-config:: doctor-duplicated-keys-keys

    A list of keys used by the ``duplicated-keys`` check. The check will show
    an error if the value of these keys is duplicated across multiple documents.

.. papis-config:: doctor-html-codes-keys

    A list of keys used by the ``html-codes`` check. The check will show an error
    if any of the keys contain unwanted HTML codes, e.g. ``&amp;``.

.. papis-config:: doctor-html-tags-keys

    A list of keys used by the ``html-tags`` check. The check will show an error
    if any of the keys contain unwanted HTML tags, e.g. ``<div>``.

.. papis-config:: doctor-key-type-check-keys

   A list of two tuples with ``(key, type)`` used by the ``key-type`` check. This
   check will show an error if the key does not have the corresponding type. The
   type should be a builtin Python type that can be used with ``eval``. For
   example, this can be ``[("year", "int"), ("tags", "list")]`` to check that the
   year is an integers and the tags are given as a list in a document.

.. papis-config:: doctor-key-type-check-separator

    A separator used by the ``key-type`` check fixer. When converting from
    :class:`str` to :class:`list`, it is used to split the string into a list,
    and when converting from :class:`list` to :class:`str`, it is used to join
    list items. The split will ignore additional whitespace around the separator
    (for instance, when set to ``,``, the string ``"extra,    whitespace"`` will
    be converted to the list ``["extra", "whitespace"]``). To preserve leading
    or trailing whitespace in the separator, make sure to quote it (for instance,
    ``", "``).

Citations options
-----------------

You can change the name of the citation files, however we discourage this.

.. papis-config:: citations-file-name

    The name of the file to store the citations of the documents.

.. papis-config:: cited-by-file-name

    The name of the file to store the citations to the document.


Marks
-----

.. papis-config:: open-mark

    If this option is set to ``True``, every time papis opens
    a document it will ask to open a mark first.
    If it is set to ``False``, then doing

    .. code::

        papis open --mark

    will avoid opening a mark.

.. papis-config:: mark-key-name

    This is the default key name for the marks in the info file. For
    example, if you set ``mark-key-name = bookmarks`` then you would have
    in your ``info.yaml`` file

    .. code::

        author: J. Krishnamurti
        bookmarks:
        - name: Chapter 1
          value: 120

.. papis-config:: mark-format-name

    This is the name of the mark to be passed to the options
    ``mark-header-format`` etc... E.g. if you set ``mark-format-name = m``
    then you could set ``mark-header-format = {m[value]} - {m[name]}``.

.. papis-config:: mark-header-format

    This is the format in which the mark will appear whenever the user
    has to pick one. You can change this in order to make ``marks`` work
    in the way you like. Per default it is assumed that every mark
    has a ``name`` and a ``value`` key.

.. papis-config:: mark-match-format

    Format in which the mark name has to match the user input.

.. papis-config:: mark-opener-format

    Due to the difficulty to generalize opening a general document
    at a given bookmark, the user should set this in whichever way
    it suits their needs. For example

    - If you are using the pdf viewer ``evince`` and you want to open a
      mark, you would use

        ::

            mark-opener-format = evince -p {mark[value]}

    - If you are using ``okular`` you would use

        ::

            mark-opener-format = okular -p {mark[value]}

    - If you are using ``zathura``, do

        ::

            mark-opener-format = zathura -P {mark[value]}

Downloaders
-----------

.. papis-config:: downloader-proxy

    There is the possibility of download papers using a proxy.
    To know more you can checkout this
    `link <https://docs.python-requests.org/en/latest/user/advanced/#proxies>`__.

.. papis-config:: isbn-service

    Sets the ISBN service used by the ISBN importer. Available plugins are
    documented
    `here <https://isbnlib.readthedocs.io/en/latest/devs.html#plugins>`__.

Databases
---------

.. papis-config:: default-query-string

    This is the default query that a command will take if no
    query string is typed in the command line. For example this is
    the query that is passed to the command ``open`` whenever no search
    string is typed:

    ::

        papis open

    Imagine you want to open all papers authored by ``John Smith`` whenever you do not
    specify an input query string, i.e., ``papis open``. Then setting

    ::

        default-query-string = author:"John Smith"

    would do the trick.
    Notice that the current example has been
    done assuming the ``database-backend = papis``.

.. papis-config:: database-backend

    The backend to use in the database. As for now papis supports
    the own database system ``papis`` and
    `whoosh <https://whoosh.readthedocs.io/en/latest/>`__.

.. papis-config:: use-cache

    Set to ``False`` if you do not want to use the ``cache``
    for the given library. This is only effective if you're using the
    ``papis`` database-backend.

.. papis-config:: cache-dir
  :default: $XDG_CACHE_HOME

.. papis-config:: whoosh-schema-fields

    Python list with the ``TEXT`` fields that should be included in the
    whoosh database schema. For instance, say that you want to be able
    to search for the ``doi`` and ``ref`` of the documents, then you could
    include

    ::

        whoosh-schema-fields = ['doi', 'ref']

.. papis-config:: whoosh-schema-prototype

    This is the model for the whoosh schema, check
    `the documentation <https://whoosh.readthedocs.io/en/latest/schema.html>`__
    for more information.

Terminal user interface (picker)
--------------------------------

These options are for the terminal user interface (tui).
They are defined in the section ``tui`` which means that you can set them
in your configuration file globally like

.. code:: ini

    [tui]
    status_line_format = "F1: Help"
    ...

or inside the library sections prepending a ``tui-``,

.. code:: ini

    [papers]
    tui-status_line_format = "Library papers**
    ...

.. papis-config:: status_line_format
    :section: tui

    This is the format of the string that appears at the bottom in the
    status line.  Right now there are only two variables defined:

    - ``selected_index``
    - ``number_of_documents``

    Which are self-explanatory.

.. papis-config:: status_line_style
    :section: tui

    The style the status line should have.
    Examples are ``fg:#ff00aa bg:black`` etc...
    More information can be found
    `here
    <https://python-prompt-toolkit.readthedocs.io/en/master/pages/advanced_topics/styling.html>`__
    .

.. papis-config:: message_toolbar_style
    :section: tui

    The style of the message toolbar, this toolbar is the one
    where messages of the ``echo`` command are rendered for instance.

.. papis-config:: options_list.selected_margin_style
    :section: tui

    Style of the margin of the selected document in the picker.

.. papis-config:: options_list.unselected_margin_style
    :section: tui

    Style of the margin of the unselected documents in the picker.
    If you don't want any coloring for them you can just set this setting
    to the empty string as such

    ::

        tui-options_list.unselected_margin_style =

.. papis-config:: error_toolbar_style
    :section: tui

    The style for the error messages.

.. papis-config:: editmode
    :section: tui

    Whenever the user is typing text, one can use either
    ``emacs`` like keybindings or ``vi``. If this does not tell you
    anything, you can just leave it as is.


.. papis-config:: move_down_key
    :section: tui

.. papis-config:: move_up_key
    :section: tui

.. papis-config:: move_down_while_info_window_active_key
    :section: tui

.. papis-config:: move_up_while_info_window_active_key
    :section: tui

.. papis-config:: focus_command_line_key
    :section: tui

.. papis-config:: edit_document_key
    :section: tui

.. papis-config:: open_document_key
    :section: tui

.. papis-config:: show_help_key
    :section: tui

.. papis-config:: show_info_key
    :section: tui

.. papis-config:: go_top_key
    :section: tui

.. papis-config:: go_bottom_key
    :section: tui

.. papis-config:: mark_key
    :section: tui

FZF integration
---------------

From version `0.12 <https://github.com/papis/papis/issues/334>`__
papis ships with an *out-of-the-box*
`fzf <https://github.com/junegunn/fzf>`__ integration for the picker.  A
minimal terminal user interface is provided and together with options
for its customization. You can set the picktool to ``fzf`` by setting

.. code:: ini

   picktool = fzf

in the configuration section of your library.

In comparison to the *built-in* papis tui the advantage of the fzf
picker is that it is much faster, however a disadvantage is that it is
restricted to one-line entries.
Also it is important to notice that ``fzf`` will **only**
match against what is shown on the terminal screen, as opposed to the papis
matcher, that can match against the **whole** title and **whole** author
text since this is controlled by the ``match-format`` setting.
However, for many uses it might not bother the user to have this limitation
of fzf.

.. papis-config:: fzf-binary

    Path to or name of the fzf binary.

.. papis-config:: fzf-extra-flags

    Extra flags to be passed to fzf every time it gets called.

.. papis-config:: fzf-extra-bindings

    Extra bindings to fzf as a python list.
    Refer to the fzf documentation for more details.

.. papis-config:: fzf-header-format

    Format for the entries for fzf.
    Notice that if you want colors you should have in ``fzf-extra-flags``
    the ``--ansi`` flag and include the colors in the header-format
    as ``ansi`` escape sequences.

    The papis format string is given the additional variable
    ``c`` which contains the package ``colorama`` in it.
    Refer to the ``colorama`` documentation to see which colors
    are available
    `here <https://github.com/tartley/colorama/blob/master/colorama/ansi.py#L49>`__.
    For instance, if you want the title in red you would put in your
    ``fzf-header-format``

    .. code:: python

        "{c.Fore.RED}{doc[title]}{c.Style.RESET_ALL}"

``fzf`` with a preview window
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

``fzf`` has the disadvantage that it does not support
multiline output and it matches only against what it shows
on the screen.

You can go around this issue by composing an ``fzf`` customization.
The following configuration

.. code:: ini

    fzf-extra-flags = ["--ansi", "--multi", "-i",
                       "--preview", "echo {} | sed -r 's/~~/\\n/g; /^ *$/d' ",
                       "--preview-window", "bottom:wrap:20%%",
                       "--color", "preview-fg:#F6E6E4,preview-bg:#5B6D5B"]

    fzf-extra-bindings = ["ctrl-s:jump",
                          "ctrl-t:toggle-preview"]

    fzf-header-format = {c.Fore.MAGENTA}{doc[title]}{c.Style.RESET_ALL}~~ {c.Fore.CYAN}{doc[author]}{c.Style.RESET_ALL}~~ {c.Fore.YELLOW}«{doc[year]}»{c.Style.RESET_ALL}~~ {c.Fore.YELLOW}{doc[journal]}{c.Style.RESET_ALL}~~ :{doc[tags]}

will have unrestricted titles, author, journal etc fields against which the query will match and it will show
in the ``fzf`` preview window a tidy description of the currently selected field by replacing the token ``~~``
by a newline. You can try this out and play with ``fzf`` customizations.
Please note that ``bottom:wrap:20%%`` has two ``%`` since the config file
interpolator uses ``%`` as a reserved symbol, so it must be escaped
by writing two of them.

Other
-----

.. papis-config:: unique-document-keys

    Whenever you add a new document, papis tries to figure out if
    you have already added this document before. This is partially done
    checking for some special keys, and checking if they match.
    Which keys are checked against is decided by this option, which
    should be formatted as a python list, just as in the default value.

    For instance, if you add a paper with a given ``doi``, and then you
    add another document with the same ``doi``, then papis will notify
    you that there is already another document with this ``doi`` because
    the ``doi`` key is part of the ``unique-document-keys`` option.

.. papis-config:: document-description-format

    ``papis`` sometimes will have to tell you which document it is processing
    through text, for instance, imagine you are updating a document

    .. code:: yaml

        author: Albert Einstein
        title: General Relativity

    and papis is doing something with it. Then if your
    ``document-description-format`` is set to
    ``{doc[title]} - {doc[author]}``, you will see that papis tells you

    ::

        .....
        Updating 'General Relativity - Albert Einstein'
        ...

    so you will know exactly what is going on.

.. papis-config:: sort-field

  As of version ``0.10``, some command line commands have the ``--sort`` option
  to sort the documents according to a given field. If you set
  ``sort-field`` in your configuration file, this will sort by default
  the documents according to this sort field. For instance,
  if you want your documents by default to be sorted by ``year``, you
  would set ``sort-field = year``.

.. papis-config:: sort-reverse

    Augments ``sort-field`` by allowing the documents to be sorted in
    reverse order. For example, when sorting by year, this allows sorting
    ascendingly or descendingly. This is a boolean option that can be set to
    ``True`` or ``False``.

.. papis-config:: time-stamp

  Whether or not to add a timestamp to a document when is being added to
  papis. If documents have a timestamp, then they will be sortable
  using ``--sort time-added`` option.

.. papis-config:: formater

    Picks the formater for templated strings in the configuration file and
    in various strings presented to the user. Supported formaters are

    * ``"python"``: based on :class:`papis.format.PythonFormater`.
    * ``"jinja2"``: based on :class:`papis.format.Jinja2Formater`.

    Note that the default values of many of the papis configuration settings are
    based on the Python formatter. These will need to all be specified explicitly
    if another formater is chosen.
