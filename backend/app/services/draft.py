async def analyze_file(file: UploadFile = File(...)):

    logger.info(f"Analyzing file: {file.filename}")
    # Enregistrement temporaire du fichier
    temp_path = f"/tmp/{file.filename}"
    with open(temp_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Détection du type MIME
    mime_type, _ = mimetypes.guess_type(temp_path)
    if mime_type is None:
        os.remove(temp_path)
        raise HTTPException(status_code=400, detail="Type de fichier non reconnu")

    result = {"filename": file.filename, "type": mime_type, "actions": []}

    # Analyse conditionnelle selon type MIME
    if mime_type.startswith("video"):
        result["actions"].append("video detected")
        # handle_video(temp_path)  # À implémenter si besoin

    if mime_type.startswith("audio"):
        result["actions"].append("audio analysis")
        analyze_audio(temp_path)
        
    if mime_type.startswith("text") or mime_type in ["application/pdf"]:
        analyze_text(temp_path)
        result["actions"].append("text analysis")

    # Nettoyage
    os.remove(temp_path)

    return JSONResponse(content=result)

def analyze_video(temp_path):
    logger.info(f"Video detected: {temp_path}")
    pass

def analyze_audio(temp_path):
    logger.info(f"Audio detected: {temp_path}")
    pass

def analyze_text(temp_path):
    logger.info(f"Text detected: {temp_path}")
    pass