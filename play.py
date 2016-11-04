from rx import Observable, Observer


hello = Observable.just('Hallo world')
name = Observable.just('Hallo Mat!')
ao = Observable.just('Hallo everyone.')


async def run():
    # asyncio observable interaction
    result = await name.to_list().single()
    print(result)

    # non-asyncio subscription async interaction
    obs = hello.to_list().single()
    obs.subscribe(print)

    # Blocking iterable observable (works synchronously).
    result = [
        r for r in ao.to_blocking()
    ]

    print(result)

if __name__ == '__main__':
    import asyncio

    loop = asyncio.get_event_loop()
    loop.run_until_complete(run())
    loop.close()
