import aiohttp
from sanic import Sanic
from sanic.response import json, text
from sanic_cors import CORS

app = Sanic(__name__)
CORS(app)


async def fetch(session, method, url, port, endpoint, request):

    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    print(method, url, endpoint)
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    if endpoint == "upload_csv":
        data = aiohttp.FormData()

        uploaded_file = request.files["file"][0]

        data.add_field(
            "file",
            uploaded_file.body,
            filename=uploaded_file.name,
            content_type=uploaded_file.type,
        )

        data.add_field("model", request.form["model"][0])
        data.add_field("user", request.form["user"][0])

        async with aiohttp.request(
            method, "http://" + url + ":" + port + "/" + endpoint, data=data
        ) as resp:
            try:
                data = await resp.json()
                data = json(data)
            except Exception:
                data = await resp.text()
                data = text(data)
            return data
    elif endpoint == "entity-file-log":
        data = aiohttp.FormData()

        uploaded_file = request.files["file"][0]

        data.add_field(
            "file",
            uploaded_file.body,
            filename=uploaded_file.name,
            content_type=uploaded_file.type,
        )

        data.add_field("senlevity", request.form["senlevity"][0])
        data.add_field("crf", request.form["crf"][0])
        data.add_field("regex", request.form["regex"][0])
        data.add_field("model", request.form["model"][0])
        data.add_field("u_id", request.form["u_id"][0])
        data.add_field("user", request.form["user"][0])

        async with aiohttp.request(
            method, "http://" + url + ":" + port + "/" + endpoint, data=data
        ) as resp:
            try:
                data = await resp.json()
                data = json(data)
            except Exception:
                data = await resp.text()
                data = text(data)
            return data
    else:
        async with aiohttp.request(
            method,
            "http://" + url + ":" + port + "/" + endpoint,
            headers={"content-type": request.get("content-type", "application/json")},
            json=request.json,
        ) as resp:
            try:
                data = await resp.json()
                data = json(data)
            except Exception:
                data = await resp.text()
                data = text(data)
            return data


@app.route("/<url>/<port>/<endpoint>", methods=["GET", "OPTIONS", "POST"])
async def api(request, url, port, endpoint):
    if request.method == "OPTIONS":
        return json({"OK": True})
    async with aiohttp.ClientSession() as session:
        data = await fetch(session, request.method, url, port, endpoint, request)
    return data


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
