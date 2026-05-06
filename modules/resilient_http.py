import random
import time

import requests


TRANSIENT_STATUS = {408, 409, 425, 429, 500, 502, 503, 504}


class TransientNetworkError(RuntimeError):
    pass


def request_with_retry(
    method,
    url,
    *,
    attempts=4,
    timeout=60,
    backoff=2.0,
    jitter=0.6,
    retry_statuses=None,
    **kwargs,
):
    retry_statuses = retry_statuses or TRANSIENT_STATUS
    last_error = None
    for attempt in range(1, attempts + 1):
        try:
            response = requests.request(method, url, timeout=timeout, **kwargs)
            if response.status_code not in retry_statuses:
                return response
            last_error = TransientNetworkError(
                f"HTTP {response.status_code}: {response.text[:300]}"
            )
            retry_after = response.headers.get("Retry-After")
            if retry_after:
                try:
                    delay = float(retry_after)
                except ValueError:
                    delay = backoff * attempt
            else:
                delay = backoff * attempt
        except (
            requests.Timeout,
            requests.ConnectionError,
            requests.exceptions.ChunkedEncodingError,
        ) as exc:
            last_error = exc
            delay = backoff * attempt
        if attempt >= attempts:
            break
        time.sleep(delay + random.uniform(0, jitter))
    raise TransientNetworkError(str(last_error))
