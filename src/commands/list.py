'''
  apkg
  ~~~~

  The Agda Package Manager.

'''

# ----------------------------------------------------------------------------

import click

from pony.orm import db_session, select

from ..service.database import db
from ..service.database import ( Library , LibraryVersion )
from natsort            import natsorted
from operator import attrgetter, itemgetter

import logging
import click_log as clog

# ----------------------------------------------------------------------------

# -- Logger def.
logger = logging.getLogger(__name__)
clog.basic_config(logger)

# -- Command def.
@click.group()
def list(): pass

@list.command()
@clog.simple_verbosity_option(logger)
@click.option('--short'
             , type=bool
             , is_flag=True 
             , help='Show name, version and description per package.')
@db_session
def list(short):
  """List of installed packages."""

  libraries = select(l for l in Library if l)[:]
  libraries = natsorted(libraries, key=attrgetter('name'))

  if len(libraries) == 0:
    logger.info("[!] No libraries available to list.")  
    logger.info("    Consider run the following command:")
    logger.info("      $ apkg init")
    return 

  orderFields = [  
                #, "library"
                #, "sha"
                  "description"
                # , "license"
                # , "include"
                # , "depend"
                # , "testedWith"
                , "keywords"
                # , "installed"
                # , "cached"
                # , "fromIndex"
                # , "fromUrl"
                # , "fromGit"
                , "origin"
                # , "default"
                ]

  i  = 0
  for library in libraries:
    v = library.getLatestVersion()    
    if v is not None:
      if not short:

        logger.info(v.library.name)
        logger.info("="*len(v.library.name))

        info = v.info

        for k in orderFields:
          val = info.get(k, None)
          if val is not None or val != "" or len(val) > 0:
            click.echo("{0}: {1}".format(k,val))

        vs = ','.join(str(ver) for ver in v.library.versions)
        if len(vs) > 0:
          print("Versions: ", vs)
      
      else:
        logger.info("{:<20.20} {:<7.7} {:.42}".format(v.library.name,v.name,v.description))

      i += 1
      if i < len(libraries):
        print()

  # logger.info(" "*30 + "--END--\n")

  # logger.info("[+] You may want to search by keywords over this list")
  # logger.info("    running the command:")
  # logger.info("      $ apkg search keyword\n")

  # logger.info("[+] To check information about a package.")
  # logger.info("    running the command:")
  # logger.info("      $ apkg info packageName")