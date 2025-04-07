import multiprocessing
import time



def do_something(seconds):
    print(f"sleeping {seconds} seconds")
    time.sleep(seconds)
    print('done sleeping')
def main():
    start = time.perf_counter()
    processes_list = []

    #_ = throw away variable, we're not using it
    for _ in range(10):
        # We can't use join in the loop because  it'll run join on the process before looping through and creating and starting the next process in the loop
        p = multiprocessing.Process(target=do_something, args = [1.5])
        p.start()
        processes_list.append(p)

    # The process will finish before continuing running the script
    for process in processes_list:
        process.join()

    finish = time.perf_counter()
    print(f'finished in {round(finish - start, 2)} seconds')

if __name__ == "__main__":
    main()

