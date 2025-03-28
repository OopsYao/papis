import os
import string
from typing import Optional, List, FrozenSet, Dict, Any, Iterator

import click

import papis.config
import papis.importer
import papis.filetype
import papis.document
import papis.format
import papis.logging

logger = papis.logging.get_logger(__name__)

# NOTE: see the BibLaTeX docs for an up to date list of types and keys:
#   https://ctan.org/pkg/biblatex?lang=en

#: A set of known BibLaTeX types (as described in Section 2.1 of the
#: `manual <https://ctan.org/pkg/biblatex?lang=en>`__). These types can be
#: extended with :ref:`config-settings-extra-bibtex-types`.
bibtex_types: FrozenSet[str] = frozenset([
    # regular types (Section 2.1.1)
    "article",
    "book", "mvbook", "inbook", "bookinbook", "suppbook", "booklet",
    "collection", "mvcollection", "incollection", "suppcollection",
    "dataset",
    "manual",
    "misc",
    "online",
    "patent",
    "periodical", "suppperiodical",
    "proceedings", "mvproceedings", "inproceedings",
    "reference", "mvreference", "inreference",
    "report",
    # "set",
    "software",
    "thesis",
    "unpublished",
    # "xdata",
    # "custom[a-f]",
    # non-standard types (Section 2.1.3)
    "artwork",
    "audio",
    "bibnote",
    "commentary",
    "image",
    "jurisdiction",
    "legislation",
    "legal",
    "letter",
    "movie",
    "music",
    "performance",
    "review",
    "standard",
    "video",
    # type aliases (Section 2.1.2)
    "conference", "electronic", "mastersthesis", "phdthesis", "techreport", "www",
]) | frozenset(papis.config.getlist("extra-bibtex-types"))

# NOTE: Zotero translator fields are defined in
#   https://github.com/zotero/zotero-schema
# and were extracted with
#   curl -s https://raw.githubusercontent.com/zotero/zotero-schema/master/schema.json | jq ' .itemTypes[].itemType'  # noqa: E501

#: A mapping of arbitrary types to BibLaTeX types in :data:`bibtex_types`. This
#: mapping can be used when translating from other software, e.g. Zotero has
#: custom fields in its `schema <https://github.com/zotero/zotero-schema>`__.
bibtex_type_converter: Dict[str, str] = {
    # Zotero
    "annotation": "misc",
    "attachment": "misc",
    "audioRecording": "audio",
    "bill": "legislation",
    "blogPost": "online",
    "bookSection": "inbook",
    "case": "jurisdiction",
    "computerProgram": "software",
    "conferencePaper": "inproceedings",
    "dictionaryEntry": "misc",
    "document": "article",
    "email": "online",
    "encyclopediaArticle": "article",
    "film": "video",
    "forumPost": "online",
    "hearing": "jurisdiction",
    "instantMessage": "online",
    "interview": "article",
    "journalArticle": "article",
    "magazineArticle": "article",
    "manuscript": "unpublished",
    "map": "misc",
    "newspaperArticle": "article",
    "note": "misc",
    "podcast": "audio",
    "preprint": "unpublished",
    "presentation": "misc",
    "radioBroadcast": "audio",
    "statute": "jurisdiction",
    "tvBroadcast": "video",
    "videoRecording": "video",
    "webpage": "online",
    # Others
    "journal": "article",
    "monograph": "book",
}

#: A set of known BibLaTeX fields (as described in Section 2.2 of the
#: `manual <https://ctan.org/pkg/biblatex?lang=en>`__). These types can be
#: extended with :ref:`config-settings-extra-bibtex-keys`.
bibtex_keys: FrozenSet[str] = frozenset([
    # data fields (Section 2.2.2)
    "abstract", "addendum", "afterword", "annotation", "annotator", "author",
    "authortype", "bookauthor", "bookpagination", "booksubtitle", "booktitle",
    "booktitleaddon", "chapter", "commentator", "date", "doi", "edition",
    "editor", "editora", "editorb", "editorc", "editortype", "editoratype",
    "editorbtype", "editorctype", "eid", "entrysubtype", "eprint", "eprintclass",
    "eprinttype", "eventdate", "eventtitle", "eventtitleaddon", "file",
    "foreword", "holder", "howpublished", "indextitle", "institution",
    "introduction", "isan", "isbn", "ismn", "isrn", "issn", "issue",
    "issuesubtitle", "issuetitle", "issuetitleaddon", "iswc", "journalsubtitle",
    "journaltitle", "journaltitleaddon", "label", "language", "library",
    "location", "mainsubtitle", "maintitle", "maintitleaddon", "month",
    "nameaddon", "note", "number", "organization", "origdate", "origlanguage",
    "origlocation", "origpublisher", "origtitle", "pages", "pagetotal",
    "pagination", "part", "publisher", "pubstate", "reprinttitle",
    "series", "shortauthor", "shorteditor", "shorthand", "shorthandintro",
    "shortjournal", "shortseries", "shorttitle", "subtitle", "title",
    "titleaddon", "translator", "url", "urldate", "venue", "version",
    "volume", "volumes", "year",
    # special fields (Section 2.2.3)
    "crossref", "entryset", "execute", "gender", "langid", "langidopts",
    "ids", "indexsorttitle", "keywords", "options", "presort", "related",
    "relatedoptions", "relatedtype", "relatedstring", "sortkey", "sortname",
    "sortshorthand", "sorttitle", "sortyear", "xdata", "xref",
    # custom fields (Section 2.3.4)
    # name[a-c]
    # name[a-c]type
    # list[a-f]
    # user[a-f]
    # verb[a-c]
    # field aliases (Section 2.2.5)
    "address", "annote", "archiveprefix", "journal", "key", "pdf",
    "primaryclass", "school"
    # fields that we ignore
    # type,
]) | frozenset(papis.config.getlist("extra-bibtex-keys"))

# Zotero translator fields, see also
#   https://github.com/zotero/zotero-schema
#   https://github.com/papis/papis/pull/121

#: A mapping of arbitrary fields to BibLaTeX fields in :data:`bibtex_keys`. This
#: mapping can be used when translating from other software.
bibtex_key_converter: Dict[str, str] = {
    "abstractNote": "abstract",
    "university": "school",
    "conferenceName": "eventtitle",
    "place": "location",
    "publicationTitle": "journal",
    "proceedingsTitle": "booktitle"
}

#: A set of BibLaTeX fields to ignore when exporting from the Papis database.
#: These can be extended with :ref:`config-settings-bibtex-ignore-keys`.
bibtex_ignore_keys: FrozenSet[str] = (
    frozenset(papis.config.getlist("bibtex-ignore-keys"))
)


def exporter(documents: List[papis.document.Document]) -> str:
    return "\n\n".join(to_bibtex_multiple(documents))


class Importer(papis.importer.Importer):
    """Importer that parses BibTeX files."""

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(name="bibtex", **kwargs)

    @classmethod
    def match(cls, uri: str) -> Optional[papis.importer.Importer]:
        if (not os.path.exists(uri) or os.path.isdir(uri)
                or papis.filetype.get_document_extension(uri) == "pdf"):
            return None
        importer = Importer(uri=uri)
        importer.fetch()
        return importer if importer.ctx else None

    def fetch_data(self: papis.importer.Importer) -> Any:
        self.logger.info("Reading input file: '%s'.", self.uri)

        from papis.downloaders import download_document
        if (
                self.uri.startswith("http://")
                or self.uri.startswith("https://")):
            filename = download_document(self.uri, expected_document_extension="bib")
        else:
            filename = self.uri

        try:
            bib_data = bibtex_to_dict(filename) if filename is not None else []
        except Exception as exc:
            self.logger.error("Error reading BibTeX file: '%s'.",
                              self.uri, exc_info=exc)
            return

        if not bib_data:
            self.logger.warning("Empty or invalid BibTeX entry at '%s'.", self.uri)
            return

        if len(bib_data) > 1:
            self.logger.warning(
                "The BibTeX file contains %d entries. Picking the first one!",
                len(bib_data))

        self.ctx.data = bib_data[0]


@click.command("bibtex")
@click.pass_context
@click.argument("bibfile", type=click.Path(exists=True))
@click.help_option("--help", "-h")
def explorer(ctx: click.core.Context, bibfile: str) -> None:
    """Import documents from a BibTeX file.

    This explorer be used as

    .. code:: sh

        papis explore bibtex 'lib.bib' pick
    """
    logger.info("Reading BibTeX file '%s'...", bibfile)

    docs = [
        papis.document.from_data(d)
        for d in bibtex_to_dict(bibfile)]
    ctx.obj["documents"] += docs

    logger.info("Found %d documents.", len(docs))


def bibtexparser_entry_to_papis(entry: Dict[str, Any]) -> Dict[str, Any]:
    """Convert the keys of a BibTeX entry parsed by :mod:`bibtexparser` to a
    papis-compatible format.

    :param entry: a dictionary with keys parsed by :mod:`bibtexparser`.
    :returns: a dictionary with keys converted to a papis-compatible format.
    """
    from bibtexparser.latexenc import latex_to_unicode

    _k = papis.document.KeyConversionPair
    key_conversion = [
        _k("ID", [{"key": "ref", "action": None}]),
        _k("ENTRYTYPE", [{"key": "type", "action": None}]),
        _k("link", [{"key": "url", "action": None}]),
        _k("title", [{
            "key": "title",
            "action": lambda x: latex_to_unicode(x.replace("\n", " "))
            }]),
        _k("author", [{
            "key": "author_list",
            "action": lambda author: papis.document.split_authors_name([
                latex_to_unicode(author)
                ], separator="and")
            }]),
    ]

    result = papis.document.keyconversion_to_data(
        key_conversion, entry, keep_unknown_keys=True)

    return result


def bibtex_to_dict(bibtex: str) -> List[Dict[str, str]]:
    """Convert a BibTeX file (or string) to a list of papis-compatible dictionaries.

    This will convert an entry like

    .. code:: tex

        @article{ref,
            author = { ... },
            title = { ... },
            ...,
        }

    to a dictionary such as

    .. code:: python

        { "type": "article", "author": "...", "title": "...", ...}

    :param bibtex: a path to a BibTeX file or a string containing BibTeX
        formatted data. If it is a file, its contents are passed to
        :class:`~bibtexparser.bparser.BibTexParser`.
    :returns: a list of entries from the BibTeX data in a compatible format.
    """
    from bibtexparser.bparser import BibTexParser
    parser = BibTexParser(
        common_strings=True,
        ignore_nonstandard_types=False,
        homogenize_fields=False,
        interpolate_strings=True)

    # bibtexparser has too many debug messages to be useful
    import logging
    logging.getLogger("bibtexparser.bparser").setLevel(logging.WARNING)

    if os.path.exists(bibtex):
        with open(bibtex) as fd:
            logger.debug("Reading in file: '%s'.", bibtex)
            text = fd.read()
    else:
        text = bibtex

    entries = parser.parse(text, partial=True).entries
    return [bibtexparser_entry_to_papis(entry) for entry in entries]


def ref_cleanup(ref: str) -> str:
    """Function to cleanup references to be acceptable for LaTeX.

    :returns: a slugified reference without any disallowed characters.
    """
    import slugify
    allowed_characters = r"([^a-zA-Z0-9._]+|(?<!\\)[._])"
    return string.capwords(str(slugify.slugify(
        ref,
        lowercase=False,
        word_boundary=False,
        separator=" ",
        regex_pattern=allowed_characters))).replace(" ", "")


def create_reference(doc: Dict[str, Any], force: bool = False) -> str:
    """Try to create a reference for the document *doc*.

    If the document *doc* does not have a ``"ref"`` key, this function attempts
    to create one, otherwise the existing key is returned. When creating a new
    reference:

    * the :ref:`config-settings-ref-format` key is used, if available,
    * the document DOI is used, if available,
    * a string is constructed from the document data (author, title, etc.).

    :param force: if *True*, the reference is re-created even if the document
        already has a ``"ref"`` key.
    :returns: a clean reference for the document.
    """
    # Check first if the paper has a reference
    ref = str(doc.get("ref", ""))
    if not force and ref:
        return ref

    # Otherwise, try to generate one somehow
    ref_format = papis.config.get("ref-format")
    if ref_format is not None:
        ref = papis.format.format(str(ref_format), doc, default="")

    if not ref:
        ref = str(doc.get("doi", ""))

    if not ref:
        ref = str(doc.get("isbn", ""))

    if not ref:
        # Just try to get something out of the data
        ref = "{:.30}".format(
              " ".join(string.capwords(str(d)) for d in doc.values()))

    logger.debug("Generated ref '%s'.", ref)
    return ref_cleanup(ref)


def to_bibtex_multiple(documents: List[papis.document.Document]) -> Iterator[str]:
    for doc in documents:
        bib = to_bibtex(doc)
        if not bib:
            logger.warning("Skipping document export: '%s'.",
                           doc.get_info_file())
            continue

        yield bib


def to_bibtex(document: papis.document.Document, *, indent: int = 2) -> str:
    """Convert a document to a BibTeX containing only valid metadata.

    To convert a document, it must have a valid BibTeX type
    (see :data:`bibtex_types`) and a valid reference under the ``"ref"`` key
    (see :func:`create_reference`). Valid BibTeX keys (see :data:`bibtex_keys`)
    are exported, while other keys are ignored (see :data:`bibtex_ignore_keys`)
    with the following rules:

    * :ref:`config-settings-bibtex-unicode` is used to control whether the
      field values can contain unicode characters.
    * :ref:`config-settings-bibtex-journal-key` is used to define the field
      name for the journal.
    * :ref:`config-settings-bibtex-export-zotero-file` is used to also add a
      ``"file"`` field to the BibTeX entry, which can be used by e.g. Zotero to
      import documents.

    :param document: a papis document.
    :param indent: set indentation for the BibTeX fields.
    :returns: a string containing the document metadata in a BibTeX format.
    """
    bibtex_type = ""

    # determine bibtex type
    if "type" in document:
        if document["type"] in bibtex_types:
            bibtex_type = document["type"]
        elif document["type"] in bibtex_type_converter:
            bibtex_type = bibtex_type_converter[document["type"]]
        else:
            logger.error("BibTeX type '%s' not valid in document: '%s'.",
                         document["type"],
                         document.get_info_file())
            return ""

    if not bibtex_type:
        bibtex_type = "article"

    # determine ref value
    ref = create_reference(document)
    if not ref:
        logger.error("No valid ref found for document: '%s'.",
                     document.get_info_file())

        return ""

    logger.debug("Using ref '%s'.", ref)

    from bibtexparser.latexenc import string_to_latex

    # process keys
    supports_unicode = papis.config.getboolean("bibtex-unicode")
    journal_key = papis.config.getstring("bibtex-journal-key")
    lines = [f"{ref}"]

    for key in sorted(document):
        bib_key = bibtex_key_converter.get(key, key)
        if bib_key not in bibtex_keys:
            continue

        if bib_key in bibtex_ignore_keys:
            continue

        bib_value = str(document[key])
        logger.debug("Processing BibTeX entry: '%s: %s'.", bib_key, bib_value)

        if bib_key == "journal":
            if journal_key in document:
                bib_value = str(document[journal_key])
            else:
                logger.warning(
                    "'journal-key' key '%s' is not present for ref '%s'.",
                    journal_key, document["ref"])

        override_key = f"{bib_key}_latex"
        if override_key in document:
            bib_value = str(document[override_key])

        if not supports_unicode:
            bib_value = string_to_latex(bib_value)

        lines.append(f"{bib_key} = {{{bib_value}}}")

    # Handle file for zotero exporting
    if (papis.config.getboolean("bibtex-export-zotero-file")
            and document.get_files()):
        lines.append("{} = {{{}}}".format("file",
                                          ";".join(document.get_files())))

    separator = ",\n" + " " * indent
    return "@{type}{{{keys},\n}}".format(type=bibtex_type,
                                         keys=separator.join(lines))
