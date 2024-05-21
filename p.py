import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
import time

# Function to send a single request and check its content
def fetch_url(url, expected_content):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # Raise an error for bad status codes
        content_check=False
        for i in range(2,5):
            if str(i) in response.text:
                content_check = i
        return (url, response.status_code, content_check)
    except requests.RequestException as e:
        return (url, None, False, str(e))

# Function to perform stress test
def stress_test(url, expected_content, num_requests):
    results = []
    start_time = time.time()
    with ThreadPoolExecutor(max_workers=num_requests) as executor:
        # Launch multiple requests concurrently
        futures = [executor.submit(fetch_url, url, expected_content) for _ in range(num_requests)]
        for future in as_completed(futures):
            result = future.result()
            results.append(result)
    end_time = time.time()
    duration = end_time - start_time
    return results, duration

# Main function to execute the stress test
def main():
    url = 'http://127.0.0.1:5002/'
    expected_content = 'Welcome to XAMPP for Linux 8.2.0'
    num_requests = 10000

    results, duration = stress_test(url, expected_content, num_requests)

    success_count = sum(1 for r in results if r[1] == 200 and r[2])
    failure_count = len(results) - success_count

    print(f'Total requests: {num_requests}')
    print(f'Successful requests: {success_count}')
    print(f'Failed requests: {failure_count}')
    print(f'Time taken: {duration:.2f} seconds')
    resdist={2:0,3:0,4:0}
    # Print details of each request
    for result in results:
        print(f'URL: {result[0]}, Status Code: {result[1]}, Content Check: {result[2]}')
        resdist[result[2]]+=1
    print(resdist)
if __name__ == '__main__':
    main()

