__author__ = 'roman'
from invoke import run
import os
from glob import glob


project = "rsna-pneumonia-detection-challenge"

kaggle_exe = "/home/roman/miniconda3/bin/kaggle"
cmd = "{} -v".format(kaggle_exe)
run(cmd)

kaggle_data_dir = os.path.expanduser("~/.kaggle/competitions")
project_data_dir = os.path.join(kaggle_data_dir, project)
if os.path.isdir(project_data_dir):
    print("skipping data download for {}".format(project))
else:
    cmd = "{} competitions download -c {}".format(kaggle_exe, project)
    result = run(cmd)
    assert result.ok, "got the data for project {}".format(project)

print("unzipping data files if any")
zipfiles = glob("{}/*.zip".format(project_data_dir))
if len(zipfiles):
    print("found {} zip archives".format(len(zipfiles)))
    outdir = project_data_dir
    for zipfile in zipfiles:
        fname = os.path.basename(zipfile)
        parts = fname.split(".")
        if len(parts) == 2:
            # it's a directory filedir.zip
            outdir = os.path.join(project_data_dir, parts[0])
            if os.path.isdir(outdir):
                continue
        elif len(parts) == 3:
            # it's a file fname.csv.zip
            unpacked = os.path.join(outdir, fname[:-4])
            if os.path.isfile(unpacked):
                continue
        else:
            raise Exception("can't deal with archives having more than 2 dots in its name")
        print("unpacking {}".format(zipfile))
        print("unzip dir {}/".format(outdir))
        result = run("unzip {} -d {}".format(zipfile, outdir))
        print("Done")