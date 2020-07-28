from googleapiclient import discovery


def youtube_search(): 
    api_key = "AIzaSyDChP61rSI95mLnjomoCBXKpnD-YrnZKO4"
    #savitha's first api_key = "AIzaSyCSsfexfhI7I3r-MXUuSmD3_0oVRNLjs1s"
    # ruth's api_key = "AIzaSyC6rqXcj4ZRxEBW_t-mPzr_3G4ei25HtO8"
    youtube = discovery.build('youtube', 'v3', developerKey=api_key)
    search_by = 'DIY crop hoodie'
    search_keyword = youtube.search().list(q=search_by, part='snippet', type='video', maxResults=10, pageToken=None)
    print(search_keyword)
    response = search_keyword.execute() 
    results = response['items']
    # results = search_keyword.get("items", []) 
    for each_item in results: 
        print(each_item['id']['videoId'])
        print(each_item['snippet']['title'])
        print(each_item['snippet']['description'])
        print(each_item['snippet']['thumbnails']['high']['url'])
    return "search complete"

