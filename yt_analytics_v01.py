import googleapiclient.discovery
import pandas as pd
import datetime
import os

# API information
api_service_name = "youtube"
api_version = "v3"
# API key
DEVELOPER_KEY = 'key_goes_here'
# API client
print('initializing client')
youtube = googleapiclient.discovery.build(
    api_service_name, api_version, developerKey=DEVELOPER_KEY)

# Global variables:
print('hi_1a')
cwd = os.getcwd()
print(cwd)
now = datetime.datetime.now()
dtime_string = now.strftime("%Y-%m-%d---%H-%M-%S")
today_str = datetime.datetime.today().strftime('%Y-%m-%d')
today_dtime = datetime.datetime.today()
dir_to_send = cwd + str('\\_TO_SEND_\\') + dtime_string + str('\\')
print('hi_2x')
print(dir_to_send)
os.mkdir(dir_to_send)
print('hi_2y')

# Load email credentials from separate directory:
cred_dir = cwd + str('\\Credentials\\hotmail_credentials.csv')
csv_credentials = pd.read_csv(cred_dir, header=None)
hotmail_username = csv_credentials.iloc[0, 0]
hotmail_pw = csv_credentials.iloc[1, 0]

def video_details(video_id):

    list_videos_byid = youtube.videos().list(id=video_id,
                                             part="id, snippet, contentDetails, statistics").execute()
    results = list_videos_byid.get("items",[])
    videos = []
    for result in results:
        videos.append(result["snippet"]["title"])
        videos.append(result["statistics"])
    return videos, results

if __name__ == "__main__":
    video_ids = ["9X8XYp84iMs", "gkDiq4Ih0Tk"]
    df_export = pd.DataFrame(index=video_ids,columns=['Video ID', 'Views', 'Video Name'])
    for video_id_ii in video_ids:
        vids, res = video_details(video_id_ii)
        df_export.loc[video_id_ii, 'Video ID'] = video_id_ii
        df_export.loc[video_id_ii, 'Views'] = vids[1]['viewCount']
        df_export.loc[video_id_ii, 'Video Name'] = vids[0]

    # Put CSV of "df_export" in today's "TO_SEND" directory:
    csv_path = str(dir_to_send) + str("youtube_stats.csv")
    df_export.to_csv(csv_path)