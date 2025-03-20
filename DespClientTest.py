from CommonClient import CommonContext
from CommonClient import server_loop
import asyncio


async def main():
    ctx = CommonContext()
    ctx.auth = "desp"
    ctx.server_task = asyncio.create_task(server_loop(ctx), name="server loop")
    ctx.run_cli()

    await ctx.exit_event.wait()
    await ctx.shutdown()


asyncio.run(main())
