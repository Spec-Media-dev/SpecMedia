import subprocess, time, json, urllib.request, asyncio
import websockets

async def run():
    chrome_path = r'C:\Program Files\Google\Chrome\Application\chrome.exe'
    proc = subprocess.Popen([
        chrome_path,
        '--headless=new',
        '--remote-debugging-port=9222',
        '--no-first-run',
        '--no-default-browser-check',
        '--user-data-dir=C:/Users/acer/Desktop/specmedia/.chrome_debug_temp'
    ])
    
    time.sleep(2)
    try:
        # Create new target
        with urllib.request.urlopen('http://127.0.0.1:9222/json/list') as resp:
            targets = json.loads(resp.read())
            ws_url = targets[0]['webSocketDebuggerUrl']
            print('Connecting to page:', ws_url)
            
        async with websockets.connect(ws_url) as ws:
            # Enable Runtime, Page, Log, Network
            await ws.send(json.dumps({"id": 1, "method": "Runtime.enable"}))
            await ws.send(json.dumps({"id": 2, "method": "Page.enable"}))
            await ws.send(json.dumps({"id": 3, "method": "Log.enable"}))

            # Navigate to https://spec-media.vercel.app/
            print('\n=== NAVIGATING TO LIVE VERCEL SITE ===')
            await ws.send(json.dumps({"id": 4, "method": "Page.navigate", "params": {"url": "https://spec-media.vercel.app/"}}))
            
            # Collect messages for 5 seconds
            t0 = time.time()
            while time.time() - t0 < 6:
                try:
                    msg = await asyncio.wait_for(ws.recv(), timeout=1.0)
                    data = json.loads(msg)
                    method = data.get("method")
                    if method == "Runtime.consoleAPICalled":
                        args = [str(a.get("value", a.get("description"))) for a in data["params"].get("args", [])]
                        print("[CONSOLE]", data["params"]["type"], " ".join(args))
                    elif method == "Runtime.exceptionThrown":
                        print("[EXCEPTION]", data["params"]["exceptionDetails"])
                    elif method == "Log.entryAdded":
                        print("[LOG]", data["params"]["entry"])
                except asyncio.TimeoutError:
                    pass

            # Now RELOAD the page
            print('\n=== NOW RELOADING THE PAGE ===')
            await ws.send(json.dumps({"id": 10, "method": "Page.reload"}))

            t0 = time.time()
            while time.time() - t0 < 6:
                try:
                    msg = await asyncio.wait_for(ws.recv(), timeout=1.0)
                    data = json.loads(msg)
                    method = data.get("method")
                    if method == "Runtime.consoleAPICalled":
                        args = [str(a.get("value", a.get("description"))) for a in data["params"].get("args", [])]
                        print("[CONSOLE RELOAD]", data["params"]["type"], " ".join(args))
                    elif method == "Runtime.exceptionThrown":
                        print("[EXCEPTION RELOAD]", data["params"]["exceptionDetails"])
                    elif method == "Log.entryAdded":
                        print("[LOG RELOAD]", data["params"]["entry"])
                except asyncio.TimeoutError:
                    pass

            # Evaluate DOM state
            await ws.send(json.dumps({
                "id": 20,
                "method": "Runtime.evaluate",
                "params": {
                    "expression": "JSON.stringify({loading: document.getElementById('__bundler_loading')?.textContent, err: document.getElementById('__bundler_err')?.textContent, title: document.title, bodyChildCount: document.body.children.length, firstTag: document.body.firstElementChild?.tagName, thumbnail: !!document.getElementById('__bundler_thumbnail')})"
                }
            }))
            resp = await ws.recv()
            print('\n=== DOM STATE AFTER RELOAD ===')
            print(resp)

    finally:
        proc.terminate()

asyncio.run(run())
