
from flask import Flask, jsonify,send_from_directory
import os
from werkzeug.exceptions import NotFound,Conflict,UnsupportedMediaType
from environs import Env
env=Env()
env.read_env()
app = Flask(__name__)
maxSize=env("MAX_CONTENT_LENGTH")
app.config['MAX_CONTENT_LENGTH'] = int(maxSize)
diretorio_imagens=[]
diretorios=os.listdir("./imagens")
diretorios_raiz=env("FILES_DIRECTORY")
extensions=env("ALLOWED_EXTENSIONS")
list_extensions=[]

def converte_list (list,convertido):
    aux=""
    for i in list :
        if(i!=" " and i!="/"):
            aux+=i
        if(i==" " or i=="/"):
            convertido.append(aux)
            aux=""
converte_list(diretorios_raiz,diretorio_imagens)
converte_list(extensions,list_extensions)
diretorios_nao_existentes=list(set(diretorio_imagens) - set(diretorios))
if(len(diretorios_nao_existentes)>0):
    for i in diretorios_nao_existentes:
        os.mkdir(f'./imagens/{i}')
def verifica_se_existe(files):
    if not("file" in files):
        raise NotFound
def verifica_tipo(primeiro_arquivo):
    for dirpath,dirname,filename in os.walk("/home/daniel/Kenzie/Python/q3-sprint2-e6-banco-de-imagens-daniell18/imagens"):
        if not(primeiro_arquivo['file'].filename.rsplit('.', 1)[1].lower() in list_extensions):
            raise UnsupportedMediaType
def verifica_repetido(primeiro_arquivo):
    for dirpath,dirname,filename in os.walk("/home/daniel/Kenzie/Python/q3-sprint2-e6-banco-de-imagens-daniell18/imagens"):
        if primeiro_arquivo['file'].filename in filename:
           raise Conflict
def upload_file(file,extension):
    file['file'].save(os.path.join(f'/home/daniel/Kenzie/Python/q3-sprint2-e6-banco-de-imagens-daniell18/imagens/Dir{extension}', file['file'].filename))
def get_all_files():
        list_all_files=[]
        for dirpath,dirname,filename in os.walk("/home/daniel/Kenzie/Python/q3-sprint2-e6-banco-de-imagens-daniell18/imagens"):
            if len(filename)>0:
                list_all_files+=filename
        return list_all_files
def get_specif_dir(extension):
    if(extension in extensions):
        for dirpath,dirname,filename in os.walk(f'/home/daniel/Kenzie/Python/q3-sprint2-e6-banco-de-imagens-daniell18/imagens/Dir{extension.lower()}'):  
                return jsonify(filename)
    raise UnsupportedMediaType
def download_file(name,extension):
     diretorio_download=f'/home/daniel/Kenzie/Python/q3-sprint2-e6-banco-de-imagens-daniell18/imagens/Dir{extension}'
     return send_from_directory(
      directory=diretorio_download,
      path=name, 
      as_attachment=True
    )