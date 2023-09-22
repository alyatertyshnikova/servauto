import http from 'k6/http';
import { check, sleep } from 'k6';

export let options = {
    stages: [
        // Ramp-up from 1 to 30 VUs in 30s
        { duration: "30s", target: 30 },

        // Stay on 30 VUs for 60s
        { duration: "60s", target: 30 },

        // Ramp-down from 30 to 0 VUs in 10s
        { duration: "10s", target: 0 }
    ]
};

export default function () {
  const url = 'http://server:8000';

  // Send a GET request to your server
  const response = http.get(url);

  // Check that the response status code is 200
  check(response, {
    'Status is 200': (r) => r.status === 404,
  });

  console.log(response.body);

  // You can add more checks here to verify the response content if needed
  // For example, you can check for specific JSON properties in the response

  // Sleep for a short duration (e.g., 1 second) before making the next request
  sleep(1);
}
