import http from 'k6/http';
import { check, sleep } from 'k6';

const urls = [
    "http://3.11.85.207/api/v2/init",
    "http://3.11.85.207/api/v2/get_national_data?date=2024-05",
    "http://3.11.85.207/api/v2/get_ground_truth_subnational",
    "http://3.11.85.207/api/v2/get_ground_truth_national",

]

export const options = {
    //vus: 5, // number of virtual users
    //duration: '30s', // duration of the test
    // stages: [
    //     { duration: '20s', target: 50 }, // ramp up to 50 users over 20 seconds
    //     { duration: '30s', target: 50 }, // hold at 50 users for 30 seconds
    //     { duration: '10s', target: 0 },  // ramp down to 0 users over 10 seconds
    // ],
    stages: [
        { duration: '5s', target: 5 }, // ramp up to 5 users over 5 seconds
        { duration: '10s', target: 5 }, // hold at 10 users for 5 seconds
        { duration: '5s', target: 0 },  // ramp down to 0 users over 5 seconds
    ],
    thresholds: {
      http_req_duration: ['p(95)<20000'], // 95% of requests must complete below 20 seconds
      http_req_failed: ['rate<0.05'], // less than 1% of requests should fail
      http_reqs: ['rate>2'],            // at least 2 requests per second
      iteration_duration: ['p(95)<10000'], // 95% of iterations should complete within 6 seconds
    },
  };

export default function () {
    urls.forEach(url => {
        const res = http.get(url);
        check(res, {
            'is status 200': (r) => r.status === 200,
        });
        sleep(1);
    });
}