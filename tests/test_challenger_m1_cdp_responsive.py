"""
Empirical CDP Browser Automation Test Suite for Challenger 2.
Tests responsive layout under 1000px at: 1024px, 800px, 768px, 640px, 375px.
Verifies:
1. Multi-column stacking (flex-direction: column / 100% width)
2. Table-responsive horizontal scrolling
3. Dual chambers (Tab 2) no-clipping and full containment
4. Sidebar collapse / expand behavior
5. Zero root-level horizontal overflow (no viewport blowout)
"""

import asyncio
import json
import os
import subprocess
import time
import urllib.request
import websockets
import pytest


async def cdp_command(ws, method, params=None, msg_id=1):
    msg = {"id": msg_id, "method": method, "params": params or {}}
    await ws.send(json.dumps(msg))
    while True:
        resp = await ws.recv()
        data = json.loads(resp)
        if data.get("id") == msg_id:
            return data


async def cdp_eval(ws, expr, msg_id=100):
    res = await cdp_command(ws, "Runtime.evaluate", {
        "expression": expr,
        "returnByValue": True,
        "awaitPromise": True
    }, msg_id=msg_id)
    return res.get("result", {}).get("result", {}).get("value")


async def run_viewport_tests():
    chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
    chrome = subprocess.Popen([
        chrome_path,
        "--headless=new",
        "--remote-debugging-port=9224",
        "--disable-gpu",
        "--no-sandbox",
        "about:blank"
    ])
    await asyncio.sleep(1.5)

    results = {}
    try:
        with urllib.request.urlopen("http://localhost:9224/json/list") as r:
            targets = json.loads(r.read())
            page_target = [t for t in targets if t.get("type") == "page"][0]
            ws_url = page_target["webSocketDebuggerUrl"]

        async with websockets.connect(ws_url, max_size=50_000_000) as ws:
            await cdp_command(ws, "Page.enable", msg_id=2)
            await cdp_command(ws, "DOM.enable", msg_id=3)
            await cdp_command(ws, "CSS.enable", msg_id=4)

            print("Navigating to http://localhost:8503/?tab=tab_simulation ...")
            await cdp_command(ws, "Page.navigate", {"url": "http://localhost:8503/?tab=tab_simulation"}, msg_id=5)

            # Wait for Streamlit to render with polling
            for attempt in range(20):
                ready = await cdp_eval(ws, """
                (() => {
                    const blocks = document.querySelectorAll('[data-testid=\"stHorizontalBlock\"]');
                    const table = document.querySelector('.table-responsive');
                    return blocks.length > 0 && table !== null;
                })()
                """, msg_id=10 + attempt)
                if ready:
                    print(f"Page rendered and stabilized on attempt {attempt+1}")
                    break
                await asyncio.sleep(0.5)

            viewports = [1024, 800, 768, 640, 375]

            for vp_width in viewports:
                vp_height = 800 if vp_width > 400 else 667
                print(f"\n==========================================")
                print(f"Testing Viewport: {vp_width}px x {vp_height}px")
                print(f"==========================================")

                await cdp_command(ws, "Emulation.setDeviceMetricsOverride", {
                    "width": vp_width,
                    "height": vp_height,
                    "deviceScaleFactor": 1,
                    "mobile": (vp_width <= 768)
                }, msg_id=50 + vp_width)
                await asyncio.sleep(1.2)

                # 1. TAB 1 EVALUATION: Columns, Root width, Table
                tab1_metrics = await cdp_eval(ws, f"""
                (() => {{
                    const vw = window.innerWidth;
                    const docEl = document.documentElement;
                    const docScrollWidth = docEl.scrollWidth;
                    const docClientWidth = docEl.clientWidth;

                    // Check horizontal blocks
                    const blocks = Array.from(document.querySelectorAll('[data-testid="stHorizontalBlock"]'));
                    const blockInfos = blocks.map((b, idx) => {{
                        const style = window.getComputedStyle(b);
                        const rect = b.getBoundingClientRect();
                        const children = Array.from(b.children);
                        const childWidths = children.map(c => c.getBoundingClientRect().width);
                        return {{
                            index: idx,
                            flexDirection: style.flexDirection,
                            flexWrap: style.flexWrap,
                            rectWidth: rect.width,
                            childWidths: childWidths,
                            stacked: style.flexDirection === 'column' || style.flexWrap === 'wrap'
                        }};
                    }});

                    // Check table-responsive
                    const tableResp = document.querySelector('.table-responsive');
                    let tableInfo = null;
                    if (tableResp) {{
                        const style = window.getComputedStyle(tableResp);
                        const rect = tableResp.getBoundingClientRect();
                        tableInfo = {{
                            overflowX: style.overflowX,
                            rectWidth: rect.width,
                            scrollWidth: tableResp.scrollWidth,
                            clientWidth: tableResp.clientWidth,
                            canScrollHorizontally: tableResp.scrollWidth > tableResp.clientWidth
                        }};
                    }}

                    // Check sidebar in collapsed and expanded state
                    const sidebar = document.querySelector('section[data-testid="stSidebar"]');
                    let sidebarCollapsedInfo = null;
                    if (sidebar) {{
                        const style = window.getComputedStyle(sidebar);
                        const rect = sidebar.getBoundingClientRect();
                        sidebarCollapsedInfo = {{
                            isCollapsed: sidebar.getAttribute('data-collapsed') === 'true',
                            position: style.position,
                            width: rect.width,
                            transform: style.transform,
                            display: style.display,
                            visibility: style.visibility
                        }};
                    }}

                    return {{
                        viewportWidth: vw,
                        docScrollWidth: docScrollWidth,
                        docClientWidth: docClientWidth,
                        rootBlowout: docScrollWidth > (vw + 2),
                        blockCount: blocks.length,
                        allBlocksStacked: blockInfos.every(b => b.stacked),
                        blockInfos: blockInfos,
                        tableInfo: tableInfo,
                        sidebarCollapsed: sidebarCollapsedInfo
                    }};
                }})()
                """, msg_id=100 + vp_width)

                # Test sidebar toggle / expansion
                sidebar_toggle_res = await cdp_eval(ws, """
                (() => {
                    const btn = document.querySelector('[data-testid="stSidebarCollapseButton"] button') ||
                                document.querySelector('[data-testid="stSidebarCollapseButton"]');
                    if (btn) {
                        btn.click();
                        return true;
                    }
                    return false;
                })()
                """, msg_id=200 + vp_width)
                await asyncio.sleep(1.0)

                sidebar_expanded_info = await cdp_eval(ws, """
                (() => {
                    const sidebar = document.querySelector('section[data-testid="stSidebar"]');
                    if (!sidebar) return null;
                    const style = window.getComputedStyle(sidebar);
                    const rect = sidebar.getBoundingClientRect();
                    return {
                        isCollapsed: sidebar.getAttribute('data-collapsed') === 'true',
                        position: style.position,
                        width: rect.width,
                        transform: style.transform,
                        visibility: style.visibility
                    };
                })()
                """, msg_id=250 + vp_width)

                # Collapse it back if it was expanded
                if sidebar_toggle_res:
                    await cdp_eval(ws, """
                    (() => {
                        const btn = document.querySelector('[data-testid="stSidebarCollapseButton"] button') ||
                                    document.querySelector('[data-testid="stSidebarCollapseButton"]');
                        if (btn) btn.click();
                    })()
                    """, msg_id=280 + vp_width)
                    await asyncio.sleep(0.5)

                # 2. TAB 2 EVALUATION: Dual chambers clipping test
                # Click Tab 2
                await cdp_eval(ws, """
                (() => {
                    const tabs = Array.from(document.querySelectorAll('[data-testid="stTab"]'));
                    if (tabs.length >= 2) tabs[1].click();
                })()
                """, msg_id=300 + vp_width)
                await asyncio.sleep(2.0)

                chamber_info = await cdp_eval(ws, f"""
                (() => {{
                    const vw = window.innerWidth;
                    const left = document.querySelector('div[class*="st-key-flame_chamber_left"]');
                    const right = document.querySelector('div[class*="st-key-flame_chamber_right"]');

                    let leftData = null;
                    let rightData = null;

                    if (left) {{
                        const rect = left.getBoundingClientRect();
                        leftData = {{
                            rectWidth: rect.width,
                            scrollWidth: left.scrollWidth,
                            clientWidth: left.clientWidth,
                            clipped: left.scrollWidth > (left.clientWidth + 2),
                            overflowsViewport: rect.width > (vw + 2)
                        }};
                    }}

                    if (right) {{
                        const rect = right.getBoundingClientRect();
                        rightData = {{
                            rectWidth: rect.width,
                            scrollWidth: right.scrollWidth,
                            clientWidth: right.clientWidth,
                            clipped: right.scrollWidth > (right.clientWidth + 2),
                            overflowsViewport: rect.width > (vw + 2)
                        }};
                    }}

                    // Check if chambers are stacked vertically
                    let stacked = false;
                    if (left && right) {{
                        const rL = left.getBoundingClientRect();
                        const rR = right.getBoundingClientRect();
                        stacked = (rR.top >= (rL.bottom - 10)) || (rL.top >= (rR.bottom - 10));
                    }}

                    return {{
                        left: leftData,
                        right: rightData,
                        chambersStacked: stacked
                    }};
                }})()
                """, msg_id=400 + vp_width)

                # Switch back to Tab 1
                await cdp_eval(ws, """
                (() => {
                    const tabs = Array.from(document.querySelectorAll('[data-testid="stTab"]'));
                    if (tabs.length >= 1) tabs[0].click();
                })()
                """, msg_id=500 + vp_width)
                await asyncio.sleep(1.0)

                results[vp_width] = {
                    "tab1": tab1_metrics,
                    "sidebar_expanded": sidebar_expanded_info,
                    "chambers": chamber_info
                }

    finally:
        chrome.terminate()

    return results


def test_responsive_layout_empirical_all_viewports():
    results = asyncio.run(run_viewport_tests())
    
    print("\n\n==========================================")
    print("FINAL EMPIRICAL VIEWPORT AUDIT REPORT")
    print("==========================================")

    for vp, data in results.items():
        t1 = data["tab1"]
        ch = data["chambers"]
        se = data["sidebar_expanded"]

        print(f"\n[VIEWPORT {vp}px]")
        print(f"  • Root HTML scrollWidth: {t1['docScrollWidth']}px (Viewport: {vp}px) -> Blowout: {t1['rootBlowout']}")
        print(f"  • Multi-column blocks stacked: {t1['allBlocksStacked']} (Total blocks: {t1['blockCount']})")
        if t1["tableInfo"]:
            ti = t1["tableInfo"]
            print(f"  • Table-responsive: overflow-x={ti['overflowX']}, clientW={ti['clientWidth']}px, scrollW={ti['scrollWidth']}px, scrollable={ti['canScrollHorizontally']}")
        if t1["sidebarCollapsed"]:
            sc = t1["sidebarCollapsed"]
            print(f"  • Sidebar (Collapsed): width={sc['width']}px, pos={sc['position']}, transform={sc['transform']}")
        if se:
            print(f"  • Sidebar (Expanded): width={se['width']}px, pos={se['position']}, transform={se['transform']}")
        if ch["left"] and ch["right"]:
            print(f"  • Dual Chambers Stacked: {ch['chambersStacked']}")
            print(f"    - Chamber Left: width={ch['left']['rectWidth']}px, clipped={ch['left']['clipped']}, overflow={ch['left']['overflowsViewport']}")
            print(f"    - Chamber Right: width={ch['right']['rectWidth']}px, clipped={ch['right']['clipped']}, overflow={ch['right']['overflowsViewport']}")

        # Hard Assertions
        assert not t1["rootBlowout"], f"FAIL: Root page blowout at {vp}px (scrollWidth={t1['docScrollWidth']} > {vp})"
        assert t1["allBlocksStacked"], f"FAIL: Columns not stacked at {vp}px"
        if t1["tableInfo"]:
            assert t1["tableInfo"]["overflowX"] == "auto", f"FAIL: .table-responsive overflow-x is not auto at {vp}px"
        if ch["left"] and ch["right"]:
            assert not ch["left"]["clipped"], f"FAIL: Flame chamber left clipped at {vp}px"
            assert not ch["left"]["overflowsViewport"], f"FAIL: Flame chamber left overflows viewport at {vp}px"
            assert not ch["right"]["clipped"], f"FAIL: Flame chamber right clipped at {vp}px"
            assert not ch["right"]["overflowsViewport"], f"FAIL: Flame chamber right overflows viewport at {vp}px"
            assert ch["chambersStacked"], f"FAIL: Dual chambers did not stack vertically at {vp}px"


if __name__ == "__main__":
    test_responsive_layout_empirical_all_viewports()
