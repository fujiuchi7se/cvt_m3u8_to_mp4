from flask import Flask, render_template, request, send_file
import ffmpeg
import os

app = Flask(__name__)

def cvt_m3u8_to_mp4(input_m3u8: str, output_mp4: str):
    try:
        ffmpeg.input(input_m3u8).output(output_mp4, vcodec="copy", **{"bsf:a": "aac_adtstoasc"}).run(overwrite_output=True)
    except ffmpeg.Error as e:
        print(f"Error: {e.stderr.decode()}")

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        url = request.form.get("url")
        output_file_name = request.form.get("output_file_name") + ".mp4"
        output_path = os.path.join("output", output_file_name)

        try:
            cvt_m3u8_to_mp4(url, output_path)
            return send_file(output_path, as_attachment=True)
        except Exception as e:
            return f"Error: {e}"
    
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)