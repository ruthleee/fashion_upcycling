from googleapiclient import discovery
def search_youtube(item_name, num_queries=10):
    api_key = "AIzaSyDChP61rSI95mLnjomoCBXKpnD-YrnZKO4"
    youtube = discovery.build('youtube', 'v3', developerKey=api_key)
    queries = [" DIY", "  Thrift Flip", " Upcycle Tutorial"]
    #num_results = 0 
    search_results = {}
    for query in queries: 
        search_by = item_name + query
        request = youtube.search().list(q=search_by, part='snippet', type='video', maxResults=num_queries, pageToken=None)
        result = request.execute() 
        #num_results += result['pageInfo.totalResults']
        items = result['items']
        for each_item in items: 
            search_results[each_item['snippet']['title']] = {"video_url": "https://www.youtube.com/watch?v=" + each_item['id']['videoId'], 
                                                            "description": each_item['snippet']['description'], 
                                                            "thumbnail_url": each_item['snippet']['thumbnails']['high']['url']}
        if len(search_results) > 0 and query == "  Thrift Flip": 
            break
        print(search_results)
    if len(search_results) == 0: 
        return "No upcycling tutorials were found for '" +  item-name + ".' Please try searching with a different item name."
    else: 
        return search_results