import subprocess, time, json, urllib.request, asyncio, base64
import websockets

async def test_url(url, label):
    print(f"\n==========================================")
    print(f"TESTING {label}: {url}")
    print(f"==========================================")
    
    with urllib.request.urlopen('http://127.0.0.1:9222/json/list') as resp:
        targets = json.loads(resp.read())
        ws_url = targets[0]['webSocketDebuggerUrl']
        
    async with websockets.connect(ws_url, max_size=50*1024*1024) as ws:
        await ws.send(json.dumps({"id": 1, "method": "Runtime.enable"}))
        await ws.send(json.dumps({"id": 2, "method": "Page.enable"}))
        await ws.send(json.dumps({"id": 3, "method": "Log.enable"}))
        
        # Navigate
        await ws.send(json.dumps({"id": 4, "method": "Page.navigate", "params": {"url": url}}))
        
        loaded = False
        t0 = time.time()
        while time.time() - t0 < 8:
            try:
                msg = await asyncio.wait_for(ws.recv(), timeout=0.5)
                data = json.loads(msg)
                method = data.get("method")
                if method == "Page.loadEventFired":
                    print(f"[{label}] Page.loadEventFired!")
                    loaded = True
                elif method == "Runtime.consoleAPICalled":
                    args = [str(a.get("value", a.get("description"))) for a in data["params"].get("args", [])]
                    print(f"[{label} CONSOLE]", data["params"]["type"], " ".join(args))
                elif method == "Runtime.exceptionThrown":
                    print(f"[{label} EXCEPTION]", data["params"]["exceptionDetails"])
                elif method == "Log.entryAdded":
                    print(f"[{label} LOG]", data["params"]["entry"])
            except asyncio.TimeoutError:
                pass
                
        # Capture screenshot
        await ws.send(json.dumps({"id": 10, "method": "Page.captureScreenshot", "params": {"format": "png"}}))
        resp = await ws.recv()
        data = json.loads(resp)
        if "result" in data and "data" in data["result"]:
            img_data = base64.b64decode(data["result"]["data"])
            filename = f"screenshot_{label}.png"
            with open(filename, "wb") as f:
                f.write(img_data)
            print(f"Saved screenshot: {filename} ({len(img_data)} bytes)")
            
        # Check DOM status
        await ws.send(json.dumps({
            "id": 11,
            "method": "Runtime.evaluate",
            "params": {
                "expression": "({ loading: document.getElementById('__bundler_loading')?.textContent, err: document.getElementById('__bundler_err')?.textContent, thumbnail: !!document.getElementById('__bundler_thumbnail'), title: document.title, readyState: document.readyState })",
                "returnByValue": True
            }
        }))
        resp = await ws.recv()
        data = json.loads(resp)
        print(f"[{label} DOM EVAL]", data.get("result", {}).get("result", {}).get("value"))

async def main():
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
        await test_url("http://127.0.0.1:8000/", "django_local")
        await test_url("https://spec-media.vercel.app/", "vercel_live")
        await test_url(r"file:///c:/Users/acer/Desktop/specmedia/index.html", "local_file")
    finally:
        proc.terminate()

asyncio.run(main())
