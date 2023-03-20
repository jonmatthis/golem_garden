import time
from datetime import datetime


def get_gmt_offset_string():
    # from - https://stackoverflow.com/a/53860920/14662833
    gmt_offset_int = int(time.localtime().tm_gmtoff / 60 / 60)
    return f"{gmt_offset_int:+}"


def get_iso6201_time_string(timespec: str = "milliseconds", make_filename_friendly: bool = True):
    iso6201_timestamp = datetime.now().isoformat(timespec=timespec)
    gmt_offset_string = f"_gmt{get_gmt_offset_string()}"
    iso6201_timestamp_w_gmt = iso6201_timestamp + gmt_offset_string
    if make_filename_friendly:
        iso6201_timestamp_w_gmt = iso6201_timestamp_w_gmt.replace(":", "_")
        iso6201_timestamp_w_gmt = iso6201_timestamp_w_gmt.replace(".", "ms")
    return iso6201_timestamp_w_gmt


def get_formatted_timestamp():
    return time.strftime(get_iso6201_time_string(timespec="seconds"))
