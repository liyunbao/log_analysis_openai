import os

ALLOWED_EXTENSIONS = {'txt', 'log', 'csv'}
def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def getFileContent(dir):
    # read the content of the file under UPLOAD_FOLDER
    # delete UPLOAD_FOLDER after the reading is done
    import shutil
    from os import listdir
    from os.path import isfile, join
    onlyfiles = [f for f in listdir(dir) if isfile(join(dir, f))]
    log_file = None
    if len(onlyfiles) > 0:
        log_file = onlyfiles[0]

    content = None
    with open(os.path.join(dir, log_file), "r") as f:
        content = f.read()
    # delete upload folder
    shutil.rmtree(dir)

    # because GPT-4 has max token limitation(10,000)
    # so we need to limit the input size
    words = content.split(' ')
    result = ' '.join(words[:9000])
    return result


