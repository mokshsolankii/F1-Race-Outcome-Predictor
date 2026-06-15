try:
    import playwright
    print("playwright installed")
except ImportError:
    print("playwright NOT installed")

try:
    import selenium
    print("selenium installed")
except ImportError:
    print("selenium NOT installed")

try:
    import pyppeteer
    print("pyppeteer installed")
except ImportError:
    print("pyppeteer NOT installed")
