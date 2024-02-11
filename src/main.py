import time

import spotipy
import spotipy.util as util
from pycaw.pycaw import AudioUtilities

from config import (SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET,
                    SPOTIFY_REDIRECT_URI, scope, username)


def set_app_mute_state(app_name: str, mute: bool) -> None:
    """Mutes or unmutes specific application"""
    try:
        sessions = AudioUtilities.GetAllSessions()
        for session in sessions:
            if session.Process and session.Process.name() == app_name:
                volume = session.SimpleAudioVolume
                volume.SetMute(int(mute), None)
    except Exception as e:
        print(f"Error {'muting' if mute else 'unmuting'} {app_name}: {e}")


def main():
    token = util.prompt_for_user_token(username, scope, SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET, SPOTIFY_REDIRECT_URI)
    spotify = spotipy.Spotify(auth=token)

    while True:
        music = spotify.currently_playing()

        if music and music['currently_playing_type'] == 'ad':
            set_app_mute_state('Spotify.exe', True)
        else:
            set_app_mute_state('Spotify.exe', False)

        time.sleep(3) # Increase the delay if the program eliminates


if __name__ == '__main__':
    main()
