# QA Instructions: Wrap AI Credits & Retire Tokens for Carbon Offset

## Objective:
To validate the end-to-end process of wrapping AI service credits into GPTX tokens, and then retiring those tokens to purchase carbon offsets, ensuring correct API responses and database updates.

## Prerequisites:
*   The GPTX API server is running (e.g., `make dev`).
*   A `.env` file is configured with `PROJECT_ROOT` and any necessary API keys (though for this test, mock data will be used).
*   A test user Ethereum address (e.g., `0x1234567890123456789012345678901234567890`).

## Test Data:
*   **User Address:** `0xTestUserAddress123456789012345678901234567890` (You can use any valid Ethereum address format)
*   **AI Provider:** `openai` (as seen in `src/gptx/core/database.py` and `src/gptx/routers/tokens.py`)
*   **Credit Amount to Wrap:** `100.0`
*   **Proof:** `mock_proof_of_ownership_123` (This is a simplified mock for POC)
*   **Tokens to Retire:** `50.0`

---

### Step-by-Step QA Instructions:

#### Phase 1: Initial State Verification

1.  **Check Initial Token Balance:**
    *   **Action:** Send a `GET` request to `/api/tokens/balance/{user_address}`.
    *   **Endpoint:** `GET http://localhost:8000/api/tokens/balance/0xTestUserAddress123456789012345678901234567890`
    *   **Expected Result:**
        *   HTTP Status: `200 OK`
        *   Response Body: `{"user_address": "0xTestUserAddress123456789012345678901234567890", "total_balance": 0.0, "wrapped_credits": []}` (or existing balance if user has tokens).
        *   **QA Check:** Confirm `total_balance` is `0.0` and `wrapped_credits` is empty (assuming a fresh database or new user).

2.  **Check Initial Carbon Offset History:**
    *   **Action:** Send a `GET` request to `/api/carbon/history/{user_address}`.
    *   **Endpoint:** `GET http://localhost:8000/api/carbon/history/0xTestUserAddress123456789012345678901234567890`
    *   **Expected Result:**
        *   HTTP Status: `200 OK`
        *   Response Body: `[]` (empty list).
        *   **QA Check:** Confirm the history is empty.

#### Phase 2: Wrap AI Service Credits

3.  **Wrap Credits into GPTX Tokens:**
    *   **Action:** Send a `POST` request to `/api/tokens/wrap`.
    *   **Endpoint:** `POST http://localhost:8000/api/tokens/wrap`
    *   **Request Body (JSON):**
        ```json
        {
            "provider": "openai",
            "credit_amount": 100.0,
            "proof": "mock_proof_of_ownership_123"
        }
        ```
    *   **Expected Result:**
        *   HTTP Status: `200 OK`
        *   Response Body (example, `transaction_hash` will vary):
            ```json
            {
                "transaction_hash": "0x...",
                "tokens_issued": 100.0,
                "message": "Successfully wrapped 100.0 openai credits into 100.0 GPTX tokens"
            }
            ```
        *   **QA Check:**
            *   Confirm `tokens_issued` matches `credit_amount` (assuming 1:1 conversion for `openai`).
            *   Verify `message` indicates success.
            *   Note the `transaction_hash`.

4.  **Verify Updated Token Balance:**
    *   **Action:** Send a `GET` request to `/api/tokens/balance/{user_address}` again.
    *   **Endpoint:** `GET http://localhost:8000/api/tokens/balance/0xTestUserAddress123456789012345678901234567890`
    *   **Expected Result:**
        *   HTTP Status: `200 OK`
        *   Response Body: `{"user_address": "0xTestUserAddress123456789012345678901234567890", "total_balance": 100.0, "wrapped_credits": [...]}`.
        *   **QA Check:** Confirm `total_balance` is `100.0` and `wrapped_credits` contains an entry for the wrapped credits.

#### Phase 3: Retire Tokens for Carbon Offset

5.  **Retire Tokens for Offset:**
    *   **Action:** Send a `POST` request to `/api/carbon/retire`.
    *   **Endpoint:** `POST http://localhost:8000/api/carbon/retire`
    *   **Request Body (JSON):**
        ```json
        {
            "token_amount": 50.0,
            "reason": "Carbon offset for AI workload"
        }
        ```
    *   **Expected Result:**
        *   HTTP Status: `200 OK`
        *   Response Body (example, `transaction_hash` and `certificate_id` will vary):
            ```json
            {
                "transaction_hash": "0x...",
                "tokens_retired": 50.0,
                "carbon_credits_purchased": 0.05, // 50 * 0.001 (from carbon.py)
                "offset_provider": "GreenCarbon Solutions",
                "certificate_id": "GCS-...",
                "message": "Successfully retired 50.0 GPTX tokens and purchased 0.05 tons CO2 offset"
            }
            ```
        *   **QA Check:**
            *   Confirm `tokens_retired` matches the requested amount.
            *   Verify `carbon_credits_purchased` is calculated correctly (e.g., `token_amount * 0.001`).
            *   Note the `transaction_hash` and `certificate_id`.

6.  **Verify Updated Token Balance (After Retirement):**
    *   **Action:** Send a `GET` request to `/api/tokens/balance/{user_address}` again.
    *   **Endpoint:** `GET http://localhost:8000/api/tokens/balance/0xTestUserAddress123456789012345678901234567890`
    *   **Expected Result:**
        *   HTTP Status: `200 OK`
        *   Response Body: `{"user_address": "0xTestUserAddress123456789012345678901234567890", "total_balance": 50.0, "wrapped_credits": [...]}`.
        *   **QA Check:** Confirm `total_balance` has decreased by the retired amount (`100.0 - 50.0 = 50.0`).

7.  **Verify Carbon Offset History:**
    *   **Action:** Send a `GET` request to `/api/carbon/history/{user_address}` again.
    *   **Endpoint:** `GET http://localhost:8000/api/carbon/history/0xTestUserAddress123456789012345678901234567890`
    *   **Expected Result:**
        *   HTTP Status: `200 OK`
        *   Response Body (should contain at least one entry):
            ```json
            [
                {
                    "id": 1,
                    "user_address": "0xTestUserAddress123456789012345678901234567890",
                    "tokens_retired": 50.0,
                    "carbon_credits_purchased": 0.05,
                    "offset_provider": "GreenCarbon Solutions",
                    "certificate_id": "GCS-...",
                    "created_at": "YYYY-MM-DDTHH:MM:SS.ssssss+00:00"
                }
            ]
            ```
        *   **QA Check:**
            *   Confirm a new entry exists with the correct `tokens_retired` and `carbon_credits_purchased`.
            *   Verify `offset_provider` and `certificate_id` are present.
