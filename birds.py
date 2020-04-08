from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route
import uvicorn
from fastai2.vision.all import (
    load_learner,
    PILImage,
)
import sys
from pathlib import Path
from io import BytesIO
import aiohttp
import asyncio
import validators
import json

app = Starlette()

# http get of image url
user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/601.3.9 (KHTML, like Gecko) Version/9.0.2 Safari/601.3.9'
headers = {'User-Agent': user_agent}


async def get_bytes(url):
    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.get(url) as response:
            print(response.headers)
            return await response.read()

# path to export model file export.pkl
path = Path('.')
# load model export.pkl
learner = load_learner(path/'export.pkl')

# route clasify-url param image url
@app.route("/classify-url", methods=["POST"])
async def classify_url(request):
    data = await request.json()
    valid = validators.url(data["url"])
    if (not valid):
        raise RuntimeError("Invalid URL")
    bytes = await get_bytes(data["url"])
    _, _, losses = learner.predict(bytes)
    return JSONResponse({
        "predictions": sorted(
            zip(learner.dls.vocab, map(float, losses)),
            key=lambda p: p[1],
            reverse=True
        )
    })


@app.route("/upload", methods=["POST"])
async def upload(request):
    data = await request.form()
    # print(data)
    bytes = await (data["image"].read())
    _, _, losses = learner.predict(bytes)
    # print(losses)
    return JSONResponse({
        "predictions": sorted(
            zip(learner.dls.vocab, map(float, losses)),
            key=lambda p: p[1],
            reverse=True
        )
    })


@app.route("/uploadb", methods=["POST"])
async def uploadb(request):
    bytes = await request.body()
    _, _, losses = learner.predict(bytes)
    return JSONResponse({
        "predictions": sorted(
            zip(learner.dls.vocab, map(float, losses)),
            key=lambda p: p[1],
            reverse=True
        )
    })


@app.route("/vocab", methods=["GET"])
async def vocab(request):
    return JSONResponse({
        "vocab": list(learner.dls.vocab)
    })

# call with python birds.py server
if __name__ == "__main__":
    if "serve" in sys.argv:
        uvicorn.run(app, host="0.0.0.0", port=8008)
