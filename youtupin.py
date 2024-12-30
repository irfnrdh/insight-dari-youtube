import csv
import pandas as pd
from googleapiclient.discovery import build

# Ganti dengan API Key Anda
api_key = 'YOUR_API_KEY'
channel_id = ''  # Channel ID 

# Membuat koneksi ke YouTube API
youtube = build('youtube', 'v3', developerKey=api_key)

# Fungsi untuk mendapatkan daftar video dari channel
def get_video_data(channel_id):
    video_data = []
    
    # Mendapatkan daftar video dari channel
    request = youtube.search().list(
        part='snippet',
        channelId=channel_id,
        maxResults=50  # Maksimal 50 video per request
    )
    response = request.execute()

    for item in response['items']:
        video_id = item['id']['videoId']
        title = item['snippet']['title']
        description = item['snippet']['description']
        published_at = item['snippet']['publishedAt']
        tags = item['snippet'].get('tags', [])
        
        # Mendapatkan data statistik video
        stats_request = youtube.videos().list(
            part='statistics,snippet',
            id=video_id
        )
        stats_response = stats_request.execute()
        
        for video in stats_response['items']:
            views = video['statistics'].get('viewCount', 0)
            likes = video['statistics'].get('likeCount', 0)
            comments = video['statistics'].get('commentCount', 0)
            category_id = video['snippet']['categoryId']
            
            # Mendapatkan kategori berdasarkan categoryId
            categories_request = youtube.videoCategories().list(
                part='snippet',
                id=category_id
            )
            categories_response = categories_request.execute()
            category_name = categories_response['items'][0]['snippet']['title']
            
            # Menyimpan data video ke dalam list
            video_data.append({
                'Title': title,
                'Description': description,
                'Link': f'https://www.youtube.com/watch?v={video_id}',
                'Views': views,
                'Likes': likes,
                'Comments': comments,
                'Category': category_name,
                'Tags': ', '.join(tags)  # Menggabungkan tags menjadi satu string
            })
    
    return video_data

# Menyimpan data video ke dalam file CSV
def save_to_csv(video_data, filename='youtube_video_data.csv'):
    df = pd.DataFrame(video_data)
    df.to_csv(filename, index=False)
    print(f"Data berhasil disimpan ke {filename}")

# Menjalankan fungsi
video_data = get_video_data(channel_id)
save_to_csv(video_data)
