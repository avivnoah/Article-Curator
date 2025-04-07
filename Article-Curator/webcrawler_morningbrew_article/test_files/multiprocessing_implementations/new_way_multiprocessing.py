import time
import concurrent.futures



def do_something(seconds):
    print(f"sleeping {seconds} seconds")
    time.sleep(seconds)
    return f'done sleeping...{seconds}'
def main():
    start = time.perf_counter()

    #joins processess automatically, and is more 'meta'
    with concurrent.futures.ProcessPoolExecutor() as executor:
        secs = [5,4,3,2,1]

        #results = [executor.submit(do_something, sec) for sec in secs]
        results = executor.map(do_something, secs)
        for result in results:
            print(result)

        for f in concurrent.futures.as_completed(results):
            print(f.result())

    finish = time.perf_counter()
    print(f'finished in {round(finish - start, 2)} seconds')

if __name__ == "__main__":
    main()

