import re
from flask import Flask, request, jsonify,send_from_directory
from environs import Env
from werkzeug.exceptions import NotFound,Conflict,UnsupportedMediaType
import os
from app.kenzie.image import verifica_se_existe,verifica_tipo,verifica_repetido,upload_file,get_all_files,get_specif_dir,download_file
env=Env()
env.read_env()
app = Flask(__name__)
maxSize=env("MAX_CONTENT_LENGTH")
app.config['MAX_CONTENT_LENGTH'] = int(maxSize)

@app.post("/upload")
def upload():
    
    try:
        primeiro_arquivo=request.files
        verifica_se_existe(request.files)
        verifica_tipo(primeiro_arquivo)
        verifica_repetido(primeiro_arquivo)
        extensao=primeiro_arquivo["file"].filename.rsplit('.', 1)[1].lower()
        upload_file(primeiro_arquivo,extensao)
        return jsonify({"message":"Updlaod realizado com sucesso"}),201
    except NotFound:
       return jsonify({"message":"Arquivo inexistente"}),400
    except UnsupportedMediaType:
        return jsonify({"message":"Tipo de Arquivo não suportado"}),415
    except Conflict:
        return jsonify({"message":"Arquivo ja existente"}),409
    
@app.get("/files")
def get_files ():
   result=get_all_files()      
   return jsonify(result)

@app.get("/files/<extension>")
def specif_Route(extension):
   try:
       result=get_specif_dir(extension)
       print(result)
       return jsonify(result)
   except NotFound:
       return jsonify({"message":"Tipo invalido"}),404
@app.get("/download/<name>")
def download(name):
  if("."in name):
    extensao=name.rsplit('.', 1)[1].lower()
  else:
      return jsonify({"message":"Arquivo invalido"}),404
  try:
     return download_file(name,extensao)
  except NotFound:
      return jsonify({"message":"Arquivo invalido"}),404
            
@app.get("/download-zip/query_params")
def download_zip():
    file=request.args.get("file_extension")
    compression_ratio=request.args.get("compression_ratio")
    os.system(f'zip -r zip/{file}.zip /home/daniel/Kenzie/Python/q3-sprint2-e6-banco-de-imagens-daniell18/imagens/Dir{file} -{compression_ratio}')
    name=f'{file}.zip'
    return download_file(name,file)



