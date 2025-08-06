import requests
import json

class FacebookPoster:
    def __init__(self, access_token, page_id):
        self.access_token = access_token
        self.page_id = page_id
        self.base_url = "https://graph.facebook.com/v18.0"
    
    def post_text(self, message):
        """Post text content to Facebook page"""
        url = f"{self.base_url}/{self.page_id}/feed"
        
        payload = {
            'message': message,
            'access_token': self.access_token
        }
        
        response = requests.post(url, data=payload)
        
        if response.status_code == 200:
            result = response.json()
            print(f"Post successful! Post ID: {result.get('id')}")
            return result
        else:
            print(f"Error posting: {response.text}")
            return None
    
    def post_photo(self, image_path, caption=""):
        """Post photo with caption to Facebook page"""
        url = f"{self.base_url}/{self.page_id}/photos"
        
        with open(image_path, 'rb') as image_file:
            files = {'source': image_file}
            data = {
                'message': caption,
                'access_token': self.access_token
            }
            
            response = requests.post(url, files=files, data=data)
        
        if response.status_code == 200:
            result = response.json()
            print(f"Photo posted successfully! Post ID: {result.get('id')}")
            return result
        else:
            print(f"Error posting photo: {response.text}")
            return None
    
    def post_link(self, link, message=""):
        """Post a link with optional message"""
        url = f"{self.base_url}/{self.page_id}/feed"
        
        payload = {
            'link': link,
            'message': message,
            'access_token': self.access_token
        }
        
        response = requests.post(url, data=payload)
        
        if response.status_code == 200:
            result = response.json()
            print(f"Link posted successfully! Post ID: {result.get('id')}")
            return result
        else:
            print(f"Error posting link: {response.text}")
            return None

# Example usage
if __name__ == "__main__":
    # You need to get these from Facebook Developer Console
    ACCESS_TOKEN = "your_page_access_token_here"
    PAGE_ID = "your_page_id_here"
    
    fb_poster = FacebookPoster(ACCESS_TOKEN, PAGE_ID)
    
    # Post text
    fb_poster.post_text("Hello from Python! 🐍")
    
    # Post photo (uncomment to use)
    # fb_poster.post_photo("path/to/your/image.jpg", "Check out this awesome photo!")
    
    # Post link (uncomment to use)
    # fb_poster.post_link("https://www.example.com", "Check out this interesting link!")
