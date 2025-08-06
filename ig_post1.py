import requests
import time
import json

class InstagramPoster:
    def __init__(self, access_token, instagram_account_id):
        self.access_token = access_token
        self.instagram_account_id = instagram_account_id
        self.base_url = "https://graph.facebook.com/v18.0"
    
    def create_media_container(self, image_url, caption="", is_video=False):
        """Create a media container for Instagram post"""
        url = f"{self.base_url}/{self.instagram_account_id}/media"
        
        if is_video:
            payload = {
                'media_type': 'VIDEO',
                'video_url': image_url,
                'caption': caption,
                'access_token': self.access_token
            }
        else:
            payload = {
                'image_url': image_url,
                'caption': caption,
                'access_token': self.access_token
            }
        
        response = requests.post(url, data=payload)
        
        if response.status_code == 200:
            result = response.json()
            return result.get('id')
        else:
            print(f"Error creating media container: {response.text}")
            return None
    
    def publish_media(self, creation_id):
        """Publish the media container to Instagram"""
        url = f"{self.base_url}/{self.instagram_account_id}/media_publish"
        
        payload = {
            'creation_id': creation_id,
            'access_token': self.access_token
        }
        
        response = requests.post(url, data=payload)
        
        if response.status_code == 200:
            result = response.json()
            print(f"Media published successfully! Media ID: {result.get('id')}")
            return result
        else:
            print(f"Error publishing media: {response.text}")
            return None
    
    def post_image(self, image_url, caption=""):
        """Complete workflow to post an image to Instagram"""
        print("Creating media container...")
        creation_id = self.create_media_container(image_url, caption)
        
        if creation_id:
            print(f"Media container created: {creation_id}")
            print("Waiting a moment before publishing...")
            time.sleep(2)  # Small delay to ensure container is ready
            
            print("Publishing media...")
            result = self.publish_media(creation_id)
            return result
        else:
            print("Failed to create media container")
            return None
    
    def post_video(self, video_url, caption=""):
        """Complete workflow to post a video to Instagram"""
        print("Creating video media container...")
        creation_id = self.create_media_container(video_url, caption, is_video=True)
        
        if creation_id:
            print(f"Video container created: {creation_id}")
            print("Waiting for video processing...")
            time.sleep(10)  # Videos need more time to process
            
            print("Publishing video...")
            result = self.publish_media(creation_id)
            return result
        else:
            print("Failed to create video container")
            return None
    
    def get_media_status(self, media_id):
        """Check the status of a media container"""
        url = f"{self.base_url}/{media_id}"
        
        params = {
            'fields': 'status_code',
            'access_token': self.access_token
        }
        
        response = requests.get(url, params=params)
        
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error checking status: {response.text}")
            return None

# Example usage
if __name__ == "__main__":
    # You need to get these from Facebook Developer Console
    ACCESS_TOKEN = "your_instagram_access_token_here"
    INSTAGRAM_ACCOUNT_ID = "your_instagram_business_account_id_here"
    
    ig_poster = InstagramPoster(ACCESS_TOKEN, INSTAGRAM_ACCOUNT_ID)
    
    # Post image (image must be publicly accessible URL)
    image_url = "https://example.com/your-image.jpg"
    caption = "Posted from Python! 🐍 #python #automation"
    
    # ig_poster.post_image(image_url, caption)
    
    # Post video (uncomment to use)
    # video_url = "https://example.com/your-video.mp4"
    # ig_poster.post_video(video_url, "Amazing video posted via Python!")

# Helper function to upload local file to a hosting service first
def upload_to_imgur(image_path, client_id):
    """Example function to upload image to Imgur and get public URL"""
    import base64
    
    url = "https://api.imgur.com/3/upload"
    
    with open(image_path, 'rb') as image_file:
        image_data = base64.b64encode(image_file.read()).decode()
    
    headers = {
        'Authorization': f'Client-ID {client_id}'
    }
    
    payload = {
        'image': image_data,
        'type': 'base64'
    }
    
    response = requests.post(url, headers=headers, data=payload)
    
    if response.status_code == 200:
        result = response.json()
        return result['data']['link']
    else:
        print(f"Error uploading to Imgur: {response.text}")
        return None
