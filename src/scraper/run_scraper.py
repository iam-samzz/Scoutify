from src.scraper.scraper import Scraper



#its basically a Worker Function / Background Worker Function.
# it waits for the background works to complete, because
''' 
when we call this func using multi threading, the endpoint must have 
        already retutn the status 'ok' , but this functions still runs in the background.
        
        
        MAIN idea is: The engine process thread keeps working because threads run independently of the function that created them.
        
        When you call thread.start(), you are handing that scraper function over to the operating system and the Python runtime 
        to execute on a separate lane. The moment that happens, the generate() 
        function and the background thread become completely detached.
'''

JOBS = {}

def scraper_worker_func(job_id: str, urls: list, addr_status: bool) -> None:

    print(addr_status , "-----------> this is address status",flush=True)
    try:
        
        print(f"job {job_id} is created.",flush=True)

        scraper = Scraper(urls,addr_status)

        # takes some time to process..
        result = scraper.scrape()

        JOBS[job_id] = {
            "status":"COMPLETED",
            "result":result}

    except Exception as e:

        JOBS[job_id] = {
            "status": "FAILED",
            "error": str(e)
        }