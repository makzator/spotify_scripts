from playwright.sync_api import sync_playwright, Playwright, Response

def scrape_response(response: Response):
    if ("products" in response.request.url):
        response_json = response.json()
        date_artists = []
        for ind, i in enumerate(response_json):
            headliners = i["headliners"]
            event_date = i["eventDate"][:-9]
            date_artists.append(event_date + ' ' + headliners + '\n')

        with open('lincoln_hall_artists.txt', 'w') as f:
            f.writelines(date_artists)

def run(playwright: Playwright):
    chromium = playwright.chromium # or "firefox" or "webkit".
    browser = chromium.launch() #headless=False

    page = browser.new_page()

    page.on("response", lambda response: scrape_response(response))
    # page.on("request", lambda request: print("Response: " + request.request.url))
    page.goto("https://lh-st.com/")
    page.pause()
    # other actions...
    browser.close()

with sync_playwright() as playwright:
    run(playwright)