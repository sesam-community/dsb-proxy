from requests import Session
from sesamutils import sesam_logger
from sesamutils.flask import serve
from flask import Flask, abort, Response


import time

app = Flask(__name__)
logger = sesam_logger("dsb-proxy", app=app)

now = time.time()
URL = f"https://innmelding.dsb.no/elvirksomhetsregisteret/virksomhetssok?0-1.0-searchForm=&antiCache={now}"


@app.route("/", methods=['GET'])
def process_request():

    logger.info(f"processing request for {URL}")

    session = Session()
    session.get(URL)

    resp = session.get(URL)

    try:
        resp.raise_for_status()
    except Exception as e:
        logger.error(f"Failed to get spreadsheet from host:\n{e}")
        abort(500, e)

    content_disposition = resp.headers.get("Content-Disposition")
    temp_resp = Response(resp.content, headers={"Content-Disposition": content_disposition})
    return temp_resp


if __name__ == "__main__":
    logger.info("Starting service...")
    serve(app)