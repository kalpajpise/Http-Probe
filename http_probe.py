import json
import time
import traceback
from subprocess import PIPE, Popen, TimeoutExpired

import ffmpeg
import vlc
from imutils.video import VideoStream
from pandas import read_excel

http_url = "http://10.10.11.52:5502"


def find_video_channel(channels):
    for index, channel in enumerate(channels):
        codec_type = str(channel.get("codec_type").lower())

        if codec_type == "video":
            return index
    return None


def probe_extract(file_name, cmd='ffprobe'):
    try:
        args = [cmd, '-show_format', '-fpsprobesize', '100', '-show_streams', '-of', 'json']
        args += [file_name]
        try:
            print("CMD ", args)
            p = Popen(args, stdout=PIPE, stderr=PIPE)
            out, err = p.communicate(timeout=15)
        except TimeoutExpired:
            print("Timout: %s", file_name)
            p.kill()
            outs, errs = p.communicate(timeout=15)

        print(out)

        if p.returncode != 0:
            raise Exception('ffprobe', out, err)
        return json.loads(out.decode('utf-8'))
    except Exception as e:
        raise Exception('ffprobe error %s', e)
    return {}


def probe_rtsp_info(row):
    try:
        print(".", end="")
        stream_url = str(row["Streams"]).strip()

        if stream_url is None or stream_url == "":
            raise Exception("RTSP URL EMPTY")

        # using ffmpeg probe
        # probe = ffmpeg.probe(stream_url)
        probe = probe_extract(stream_url)
        print("probe ", probe)
        channels = probe.get("streams", [])

        if not channels:
            raise Exception("Channel not found")

        # assume the RTSP stream has only single channel
        index = find_video_channel(channels)

        if not index is None:
            row["is_stream_running"] = "Yes"
            row["Codec Type"] = channels[index].get("codec_type")
            row["Codec"] = channels[index].get("codec_name")
            row["Codec Name"] = channels[index].get("codec_long_name")
            row["Width"] = channels[index].get("width")
            row["Height"] = channels[index].get("height")
            row["Frame rate"] = channels[index].get("r_frame_rate")
            row["Codec Type"] = channels[index].get("codec_type")
        else:
            row["is_stream_running"] = "No"
    except ffmpeg.Error as e:
        print("FFMPEG ERROR: ", e)
        row["is_stream_running"] = "No"
    except Exception as e:
        print("ERROR: ", e)
        row["is_stream_running"] = "No"

    return row


def vlc_method(row):
    try:
        print(".", end="")
        stream_url = str(row["Streams"]).strip()
        # stream_url = "rtsp://localhost:8554/mystream"
        # creating vlc media player object
        media_player = vlc.MediaPlayer()
        media = vlc.Media(stream_url)
        # start playing video
        media_player.set_media(media)
        media_player.play()
        time.sleep(10)
        print(media.get_stats())
        print("FPS ", media_player.get_media(), media_player.is_playing(), media_player.get_fps())
    except Exception as e:
        print("ERROR: ", e)


def cv_method(row):
    try:
        print(".", end="")
        stream_url = str(row["Streams"]).strip()
        # stream_url = "rtsp://localhost:8554/mystream"

        vs = VideoStream(http_url)
        print(vs.read())
        no_of_frames = 0
        while True:
            no_of_frames += 1
            et, frame = vs.read()

            if frame is None:
                continue
            else:
                print(len(frame))
    except Exception as e:
        print("ERROR: ", e)
        print(traceback.print_exc())


if __name__ == '__main__':
    # parser = argparse.ArgumentParser(description='Get RTSP Video information')
    # parser.add_argument('in_filename', help='Input filename')

    df = read_excel('http_url.xlsx')
    print(df.shape)
    # start the rtsp probe service
    df_output = df.apply(lambda row: cv_method(row), axis=1, result_type='expand')
    df_output.to_excel('http_url_output.xlsx', index=False)
