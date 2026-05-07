# Gemini API Test Report

- Timestamp: 2026-05-07T15:45:27.551633-04:00
- Key loaded by config: True
- Model list status: 200 / ok=True
- Final status: KEY_VALID_BUT_NO_PREPAY_CREDITS

## Generate Tests

- gemini-flash-latest: status=429 ok=False elapsed=0.63s
  - error: RESOURCE_EXHAUSTED | Your prepayment credits are depleted. Please go to AI Studio at https://ai.studio/projects to manage your project and billing. Learn more at https://ai.google.dev/gemini-api/docs/billing#prepay. 
- gemini-flash-lite-latest: status=429 ok=False elapsed=0.65s
  - error: RESOURCE_EXHAUSTED | Your prepayment credits are depleted. Please go to AI Studio at https://ai.studio/projects to manage your project and billing. Learn more at https://ai.google.dev/gemini-api/docs/billing#prepay. 
- gemini-2.0-flash-lite: status=429 ok=False elapsed=0.6s
  - error: RESOURCE_EXHAUSTED | Your prepayment credits are depleted. Please go to AI Studio at https://ai.studio/projects to manage your project and billing. Learn more at https://ai.google.dev/gemini-api/docs/billing#prepay. 
- gemini-2.0-flash: status=429 ok=False elapsed=0.62s
  - error: RESOURCE_EXHAUSTED | Your prepayment credits are depleted. Please go to AI Studio at https://ai.studio/projects to manage your project and billing. Learn more at https://ai.google.dev/gemini-api/docs/billing#prepay. 
- gemini-2.5-flash: status=429 ok=False elapsed=0.58s
  - error: RESOURCE_EXHAUSTED | Your prepayment credits are depleted. Please go to AI Studio at https://ai.studio/projects to manage your project and billing. Learn more at https://ai.google.dev/gemini-api/docs/billing#prepay. 

## Operator Meaning

- If status is GENERATE_OK, the Grey Memory Bridge can send real tasks.
- If status is KEY_VALID_BUT_NO_PREPAY_CREDITS, the key is configured but Google billing/prepay must be fixed before generation works.
- The probe intentionally stops at tiny requests and does not retry aggressively.
