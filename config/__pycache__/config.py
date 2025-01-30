# Spotify API configuration
SPOTIFY = {
    "client_id":  '829475f2db444c5cbd5c1026b0ee8ad2',
    "client_secret": '4db6ce0fb86244028d74a8b526d99f2f',
    "redirect_uri": "http://localhost:8080/oauth2callback",
}

# If you already have a token, you can add it here as well:
SPOTIFY_TOKEN = {
    'access_token': 'your_access_token',
    'refresh_token': 'your_refresh_token',
    'token_expiry': 'expiry_timestamp'  # Optional, if you want to store token expiry
}