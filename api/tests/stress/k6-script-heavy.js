import http from 'k6/http';
import { check, sleep } from 'k6';

export const options = {
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
        http_req_duration: ['p(95)<2000'], // 95% of requests must complete below 1 second
        http_req_failed: ['rate<0.01'], // less than 1% of requests should fail
        http_reqs: ['rate>0.5'],            // at least 10 requests per second
        iteration_duration: ['p(95)<5000'], // 95% of iterations should complete within 2 seconds
      },
};


export default function () {
    const url = "http://3.11.85.207/api/v2/get_subnational_data?date=2024-05"
    const res = http.get(url);
    check(res, {
        'is status 200': (r) => r.status === 200,
    });
    sleep(1);
}

