from fastapi import FastAPI, UploadFile, File
import zstandard as zstd
import os

app = FastAPI()

@app.post("/compress/")
async def compress_file(file: UploadFile = File(...)):
    input_file_path = file.filename
    compressed_file_path = f"{file.filename}.zst"

    with open(input_file_path, "wb") as f:
        f.write(await file.read())

    # Compress the file using Zstandard
    cctx = zstd.ZstdCompressor()
    with open(input_file_path, "rb") as f_in, open(compressed_file_path, "wb") as f_out:
        f_out.write(cctx.compress(f_in.read()))

    os.remove(input_file_path)  # Clean up original file (optional)

    return {"compressed_file": compressed_file_path}

@app.post("/decompress/")
async def decompress_file(file: UploadFile = File(...)):
    input_file_path = file.filename
    decompressed_file_path = f"{file.filename}.decompressed"

    with open(input_file_path, "wb") as f:
        f.write(await file.read())

    dctx = zstd.ZstdDecompressor()
    with open(input_file_path, "rb") as f_in, open(decompressed_file_path, "wb") as f_out:
        f_out.write(dctx.decompress(f_in.read()))

    os.remove(input_file_path)  # Clean up compressed file (optional)

    return {"decompressed_file": decompressed_file_path}
