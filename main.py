from fastapi import FastAPI, UploadFile, File
from fastapi.responses import FileResponse
import uvicorn, os
from processing.audio_engine import process_audio

app = FastAPI()

@app.post("/process")
async def enhance_audio(file: UploadFile = File(...)):
    input_path = f"uploads/{file.filename}"
    output_path = f"processed/{file.filename}"
    os.makedirs("uploads", exist_ok=True)
    os.makedirs("processed", exist_ok=True)
    with open(input_path, "wb") as f:
        f.write(await file.read())
    process_audio(input_path, output_path)
    return FileResponse(output_path, filename=file.filename)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run(app, host="0.0.0.0", port=port)
