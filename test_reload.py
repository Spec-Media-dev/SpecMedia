import subprocess, time, json, urllib.request, asyncio, base64
import websockets

async def test_reload(url):
    print(f"\n==========================================")
    print(f"TESTING RELOAD ON: {url}")
    print(f"==========================================")
    
    with urllib.request.urlopen('http://127.0.0.1:9222/json/list') as resp:
        targets = json.loads(resp.read())
        ws_url = targets[0]['webSocketDebuggerUrl']
        
    async with websockets.connect(ws_url, max_size=50*1024*1024) as ws:
        await ws.send(json.dumps({"id": 1, "method": "Runtime.enable"}))
        await ws.send(json.dumps({"id": 2, "method": "Page.enable"}))
        await ws.send(json.dumps({"id": 3, "method": "Log.enable"}))
        
        # 1. Initial navigation
        print("1. Initial navigation...")
        await ws.send(json.dumps({"id": 4, "method": "Page.navigate", "params": {"url": url}}))
        
        # Wait 4s for initial load and unpacking
        await asyncio.sleep(4)
        
        # 2. Now trigger RELOAD
        print("2. Triggering RELOAD via Page.reload()...")
        await ws.send(json.dumps({"id": 5, "method": "Page.reload", "params": {"ignoreCache": False}}))
        
        # Check messages for 6 seconds after reload
        t0 = time.time()
        while time.time() - t0 < 6:
            try:
                msg = await asyncio.wait_for(ws.recv(), timeout=0.5)
                data = json.loads(msg)
                method = data.get("method")
                if method == "Page.loadEventFired":
                    print("[AFTER RELOAD] Page.loadEventFired!")
                elif method == "Runtime.consoleAPICalled":
                    args = [str(a.get("value", a.get("description"))) for a in data["params"].get("args", [])]
                    print("[AFTER RELOAD CONSOLE]", data["params"]["type"], " ".join(args))
                elif method == "Runtime.exceptionThrown":
                    print("[AFTER RELOAD EXCEPTION]", data["params"]["exceptionDetails"])
                elif method == "Log.entryAdded":
                    print("[AFTER RELOAD LOG]", data["params"]["entry"])
            except asyncio.TimeoutError:
                pass
                
        # Capture screenshot after reload
        await ws.send(json.dumps({"id": 10, "method": "Page.captureScreenshot", "params": {"format": "png"}}))
        resp = await ws.recv()
        data = json.loads(resp)
        if "result" in data and "data" in data["result"]:
            img_data = base64.b64decode(data["result"]["data"])
            with open("screenshot_after_reload.png", "wb") as f:
                f.write(img_data)
            print(f"Saved screenshot_after_reload.png ({len(img_data)} bytes)")
            
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
        print("[DOM EVAL AFTER RELOAD]", data.get("result", {}).get("result", {}).get("value"))

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
        await test_reload("https://spec-media.vercel.app/")
    finally:
        proc.terminate()

asyncio.run(main())
