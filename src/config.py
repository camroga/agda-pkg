'''
  apkg
  ~~~~

  The Agda Package Manager.

'''

# ----------------------------------------------------------------------------


import click
import git
import subprocess

from pathlib import Path

# -----------------------------------------------------------------------------

# -- AGDA DIRECTORIES:
AGDA_DIR_PATH = Path().home().joinpath(".agda")
AGDA_DEFAULTS_PATH = AGDA_DIR_PATH.joinpath("defaults")
AGDA_LIBRARIES_PATH = AGDA_DIR_PATH.joinpath("libraries")
AGDA_VERSION = ""

try:
  result = subprocess.run(["agda", "--version"], stdout=subprocess.PIPE)
  AGDA_VERSION = result.stdout.split()[2].decode()
  AGDA_LIBRARIES_PATH = AGDA_DIR_PATH.joinpath("libraries-"+AGDA_VERSION)
except Exception as e:
  print("[!] Agda may not be installed on this machine!")
  print("    Please consider to install Agda v2.5.4+")

AGDA_PKG_PATH = Path().home().joinpath('.apkg' + \
                ("@agda-" + AGDA_VERSION if len(AGDA_VERSION) > 0 else ""))
GITHUB_USER   = "apkgbot"
GITHUB_DOMAIN = "https://github.com/"

# The github repository index of all agda packages
INDEX_REPOSITORY_NAME = "package-index"
INDEX_REPOSITORY_URL = \
 GITHUB_DOMAIN + GITHUB_USER + "/" + INDEX_REPOSITORY_NAME + ".git"
INDEX_REPOSITORY_BRANCH = "master"
INDEX_REPOSITORY_PATH   = AGDA_PKG_PATH.joinpath(INDEX_REPOSITORY_NAME)

# this is folder where I keep all the source code for every library installed
PACKAGE_SOURCES_NAME = "package-sources"
PACKAGE_SOURCES_PATH = AGDA_PKG_PATH.joinpath(PACKAGE_SOURCES_NAME)

# We want to search fast queries using a database
DATABASE_FILE_NAME = INDEX_REPOSITORY_NAME + ".db"
DATABASE_FILE_PATH = AGDA_PKG_PATH.joinpath(DATABASE_FILE_NAME)
DATABASE_SEARCH_INDEXES_PATH = AGDA_PKG_PATH.joinpath("search-indexes")

REPO = None

PKG_SUFFIX = ".agda-pkg"
LIB_SUFFIX = ".agda-lib"

# -----------------------------------------------------------------------------

if not AGDA_PKG_PATH.exists():
  AGDA_PKG_PATH.mkdir()

if not INDEX_REPOSITORY_PATH.exists():
  INDEX_REPOSITORY_PATH.mkdir()

if not PACKAGE_SOURCES_PATH.exists():
  PACKAGE_SOURCES_PATH.mkdir()

try:
  REPO = git.Repo(INDEX_REPOSITORY_PATH, search_parent_directories=True)
except:
  try:
    REPO = git.Repo.clone_from(INDEX_REPOSITORY_URL, INDEX_REPOSITORY_PATH)
  except Exception as e:
    print(e)

if not DATABASE_FILE_PATH.exists():
  DATABASE_FILE_PATH.touch()

if not DATABASE_SEARCH_INDEXES_PATH.exists():
  DATABASE_SEARCH_INDEXES_PATH.mkdir()

if not AGDA_DIR_PATH.exists():
  AGDA_DIR_PATH.mkdir()
  AGDA_DEFAULTS_PATH.touch()
  AGDA_LIBRARIES_PATH.touch()
