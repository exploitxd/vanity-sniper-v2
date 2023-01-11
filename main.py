import aiohttp, asyncio, os, sys, time

os.system("cls" if os.name == "nt" else "clear")

token = "authorization | user token only"
hook = "https://canary.discord.com/api/webhooks/guild_id/webhook_token"
guild = "serer_id"
list = ["vanity1", "vanity2]
delay = 0

async def notify(session, url, jsonxd):
    async with session.post(url, json=jsonxd) as response:
        return response.status

async def claim(session, url, jsonxd):
    # headers = {"Authorization": token, "X-Audit-Log-Reason": "slapped by exploit"}
    async with session.patch(url, json=jsonxd) as response:
        return response.status

async def fetch(session, url):
    async with session.get(url) as response:
        return response.status, response.text, response.json()

async def main():
    os.system("cls" if os.name == "nt" else "clear")
    async with aiohttp.ClientSession(headers={"Authorization": token, "X-Audit-Log-Reason": "slapped by exploit"}, connector=None) as session:
        async with session.get("https://canary.discord.com/api/v9/users/@me") as response:
          if response.status in (200, 201, 204):
            user = await response.json()
            id = user["id"]
            username = user["username"]
            print("Logged in as {} | {}".format(username, id))
          elif response.status == 429:
            print("[-] Connection failed to discord websocket, this ip is rate limited")
            sys.exit()
          else:
            await notify(session, hook, {"content": "@everyone failed to connect to discord websocket."})
            print("Bad Auth")
            sys.exit()
        await notify(session, hook, {"content": "connected; %s" % str(list)})
        for x in range(100000):
            for vanity in list:
                idk, text, jsonxd = await fetch(session, 'https://canary.discord.com/api/v9/invites/%s' % vanity)
                if idk == 404:
                    idk2 = await claim(session, 'https://canary.discord.com/api/v9/guilds/%s/vanity-url' % (guild), {"code": vanity})
                    if idk2 in (200, 201, 204):
                        await notify(session, hook, {"content": "@everyone claimed %s" % vanity})
                        sys.exit()
                    else:
                        await notify(session, hook, {"content": "@everyone failed to claim %s | status: %s" % (vanity, idk2)})
                        sys.exit()
                elif idk == 200:
                    print("[+] Attempt: %s | Vanity: %s" % (x, vanity))
                    await asyncio.sleep(delay)
                    continue
                elif idk == 429:
                    #print()
                    await notify(session, hook, {"content": "got rate limited; sleeping..."})
                    print("[-] Rate Limited")
                    if 'retry_after' in text:
                      time.sleep(int(jsonxd['retry_after']))
                    else:
                      sys.exit()                 
                else:
                    print("[-] Unknown Error")
                    sys.exit()


loop = asyncio.get_event_loop()
loop.run_until_complete(main()) 
