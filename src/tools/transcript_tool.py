from urllib.parse import urlparse, parse_qs
from youtube_transcript_api import YouTubeTranscriptApi

def get_youtube_transcript(video_url: str) -> list[str]:
    """
    Fetches the transcript of a YouTube video given its URL.

    Args:
        video_url (str): The URL of the YouTube video.

    Returns:
        list[str]: A list of strings representing the transcript of the video.
    """
    try:
        parsed_url = urlparse(video_url)
        print(f"Parsed URL: {parsed_url}")
        video_id = parse_qs(parsed_url.query).get("v", [None])[0]
        
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        
        transcript_text = []
        
        for entry in transcript:
            transcript_text.append(entry['text'])
            
        return transcript_text
    except Exception as e:
        print(f"Error fetching transcript: {e}")
        return []
    

# For testing purposes, you can run this script directly
# and it will fetch the transcript for a sample YouTube video.
if __name__ == "__main__":
    video_url = "https://www.youtube.com/watch?v=7onC2-SoHbc"
    transcript = get_youtube_transcript(video_url)
    print("\n".join(transcript))