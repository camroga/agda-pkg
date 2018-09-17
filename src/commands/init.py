'''
  agda-pkg
  ~~~~~~~~~~~~~~~~~~~~~~~~~~
'''

# ----------------------------------------------------------------------------
import click
from pathlib import Path

from ..config import PACKAGE_SOURCES_PATH, INDEX_REPOSITORY_PATH, INDEX_REPOSITORY_URL

from ..service.readLibFile  import readLibFile
from ..service.database import db, pw
from ..service.database import ( Library
                               , LibraryVersion
                               , Keyword
                               , Dependency
                               )
from pony.orm import *

import logging
import click_log as clog
# ----------------------------------------------------------------------------

# -- Logger def.
logger = logging.getLogger(__name__)
clog.basic_config(logger)

# -- Command def.
@click.group()
def init():	pass

@init.command()
@clog.simple_verbosity_option(logger)
@click.option('--drop_tables', type=bool, default=True)
def init(drop_tables):

  if drop_tables:
    db.drop_all_tables(with_all_data=True)
    db.create_tables()

  f = INDEX_REPOSITORY_PATH
  src = f.joinpath("src")
  click.echo("Indexing libraries from " + INDEX_REPOSITORY_URL)

  with db_session:

    for lib in src.glob("*"):
      name = lib.name
      url  = Path(lib).joinpath("url").read_text()
      library = Library.get(name = name, url = url)
      if library is None:
        brary = Library(name = name, url = url)

      for version in lib.joinpath("versions").glob("*"):
        libVersion = LibraryVersion.get(library = library , name = version.name, fromIndex=True)
        if library is None:
          libVersion = LibraryVersion(library = library , name = version.name, fromIndex=True)
        
        if version.joinpath("sha1").exists():
          libVersion.sha = version.joinpath("sha1").read_text()
        else:
          logger.error(version.name + " no valid")
      commit()

    # With all libraries indexed, we proceed to create the dependencies
    # as objects for the index.
    for lib in src.glob("*"):
      library = Library.get(name = lib.name)

      for version in library.getSortedVersions():
        click.echo(version.freezeName)

        info = version.readInfoFromLibFile()

        for depend in info["depend"]:
          if type(depend) == list:
            logger.info("no supported yet but the format is X.X <= name <= Y.Y")
          else:
            dependency = Library.get(name = depend)
            if dependency is not None:
              version.depend.add(Dependency(library = dependency))
            else:
              logger.warning(depend + " is not in the index")


        info = version.readInfoFromLibFile()
        keywords = info.get("keywords", [])
        keywords += info.get("category", [])
        keywords = list(set(keywords))

        for word in keywords:
          keyword =  Keyword.get(word = word)
          if keyword is None:
            keyword = Keyword(word = word)
          keyword.libraries.add(library)
          keyword.libversions.add(version)